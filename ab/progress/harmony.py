"""Four-Way Harmony per endpoint, for the interactive capture/sign-off app (037).

Constitution III requires, for every endpoint, four mutually-consistent artifacts:
Implementation, Example, Fixture & Test, and Sphinx documentation. This module
computes that harmony for every routed endpoint from live code + on-disk signals,
enriched with swagger tags (for the left-nav "tags" tree) and real test coverage
from ``coverage.json`` (run ``coverage run -m pytest -m "not live"; coverage json``).

It is read-only and import-safe (no network); the interactive app
(``ab/progress/app.py``) joins it with the SQLite sign-off/capture state.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from ab.api.rtd import endpoint_page_slug, endpoint_top_group
from ab.progress.route_index import normalize_path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
DOCS_API_DIR = REPO_ROOT / "docs" / "api"
COVERAGE_JSON = REPO_ROOT / "coverage.json"
SCHEMAS_DIR = REPO_ROOT / "ab" / "api" / "schemas"


@dataclass
class EndpointHarmony:
    """Harmony signals for one routed endpoint."""

    endpoint_key: str
    group: str
    method_name: str
    http_method: str
    path: str
    api_surface: str
    response_model: str
    request_model: str | None
    tags: list[str] = field(default_factory=list)
    # Four-Way Harmony signals
    has_impl: bool = True
    has_example: bool = False
    has_fixture: bool = False
    has_test: bool = False
    has_sphinx: bool = False
    coverage_pct: float | None = None
    run_status: str = "missing_example"
    example_path: str | None = None
    doc_path: str | None = None

    @property
    def harmony_score(self) -> int:
        """Count of the four harmony pillars satisfied (impl/example/fixture+test/sphinx)."""
        return sum([self.has_impl, self.has_example, (self.has_fixture and self.has_test), self.has_sphinx])

    def to_dict(self) -> dict:
        d = asdict(self)
        d["harmony_score"] = self.harmony_score
        return d


# ----------------------------------------------------------------------
# Swagger tags
# ----------------------------------------------------------------------


def _swagger_tag_map() -> dict[tuple[str, str], list[str]]:
    """Build ``{(normalized_path, METHOD): [tags]}`` from the three swagger specs.

    Swagger paths carry a leading ``/api`` that Route paths lack; we strip it so
    keys line up with live Route paths. Cached (see ``tag_map``) — the specs don't
    change within a process and ``build_harmony`` runs on every report/app poll.
    """
    out: dict[tuple[str, str], list[str]] = {}
    for name in ("acportal", "catalog", "abc"):
        spec_path = SCHEMAS_DIR / f"{name}.json"
        if not spec_path.is_file():
            continue
        try:
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for raw_path, methods in spec.get("paths", {}).items():
            stripped = raw_path[4:] if raw_path.startswith("/api/") else raw_path
            for http_method, op in methods.items():
                if not isinstance(op, dict):
                    continue
                tags = op.get("tags") or []
                if tags:
                    out[(normalize_path(stripped), http_method.upper())] = list(tags)
    return out


_TAG_MAP: dict[tuple[str, str], list[str]] | None = None


def tag_map() -> dict[tuple[str, str], list[str]]:
    """Cached swagger tag map."""
    global _TAG_MAP
    if _TAG_MAP is None:
        _TAG_MAP = _swagger_tag_map()
    return _TAG_MAP


# ----------------------------------------------------------------------
# Coverage
# ----------------------------------------------------------------------


def _coverage_map() -> dict[str, float]:
    """Return ``{repo_relative_file: percent_covered}`` from coverage.json (or {})."""
    if not COVERAGE_JSON.is_file():
        return {}
    try:
        data = json.loads(COVERAGE_JSON.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    out: dict[str, float] = {}
    for fname, info in data.get("files", {}).items():
        rel = fname[len(str(REPO_ROOT)) + 1 :] if fname.startswith(str(REPO_ROOT)) else fname
        out[rel.replace("\\", "/")] = info.get("summary", {}).get("percent_covered")
    return out


def _module_to_relpath(module: str | None) -> str | None:
    if not module:
        return None
    return module.replace(".", "/") + ".py"


# ----------------------------------------------------------------------
# Harmony build
# ----------------------------------------------------------------------


def build_harmony() -> list[EndpointHarmony]:
    """Compute harmony for every routed endpoint, sorted by key."""
    from ab.cli.discovery import discover_endpoints_from_class
    from ab.progress.example_gen import strip_list_wrapper
    from ab.progress.example_index import build_example_index
    from ab.progress.models import derive_run_status
    from ab.progress.report import load_run_results
    from ab.progress.scanner import scan_fixture_files

    index = build_example_index()
    fixture_files = scan_fixture_files(FIXTURES_DIR)
    tags_by_key = tag_map()
    cov = _coverage_map()
    run_results = load_run_results()

    out: list[EndpointHarmony] = []
    for name, info in discover_endpoints_from_class().items():
        class_rel = _module_to_relpath(getattr(info.endpoint_class, "__module__", None))
        cov_pct = cov.get(class_rel) if class_rel else None
        for m in info.methods:
            if m.route is None:
                continue
            key = f"api.{name}.{m.name}"
            model = strip_list_wrapper(m.route.response_model or "")
            has_fixture = bool(model) and model in fixture_files
            ex = index.get(key)
            has_example = bool(ex and ex.is_canonical)

            # Sphinx: per-endpoint page docs/api/<top>/<slug>.md
            top = endpoint_top_group(name)
            slug = endpoint_page_slug(name, m.name)
            doc_rel = f"docs/api/{top}/{slug}.md"
            has_sphinx = (REPO_ROOT / doc_rel).is_file()

            # Test signal: endpoint source file is exercised by the suite.
            has_test = bool(cov_pct) and cov_pct > 0

            run_status = derive_run_status(
                http_method=m.route.method,
                has_canonical_example=has_example,
                response_model=m.route.response_model,
                fixture_exists=has_fixture,
            ).value
            entry = run_results.get(key)
            if entry:
                run_status = entry.get("status", run_status)

            out.append(
                EndpointHarmony(
                    endpoint_key=key,
                    group=name,
                    method_name=m.name,
                    http_method=m.route.method,
                    path=m.route.path,
                    api_surface=m.route.api_surface,
                    response_model=model,
                    request_model=m.route.request_model,
                    tags=tags_by_key.get((normalize_path(m.route.path), m.route.method.upper()), []),
                    has_example=has_example,
                    has_fixture=has_fixture,
                    has_test=has_test,
                    has_sphinx=has_sphinx,
                    coverage_pct=cov_pct,
                    run_status=run_status,
                    example_path=ex.example_path if ex else None,
                    doc_path=doc_rel if has_sphinx else None,
                )
            )
    out.sort(key=lambda h: h.endpoint_key)
    return out


def harmony_summary(rows: list[EndpointHarmony]) -> dict[str, int]:
    """Headline counts for the app dashboard."""
    return {
        "total": len(rows),
        "example": sum(1 for r in rows if r.has_example),
        "fixture": sum(1 for r in rows if r.has_fixture),
        "test": sum(1 for r in rows if r.has_test),
        "sphinx": sum(1 for r in rows if r.has_sphinx),
        "full_harmony": sum(1 for r in rows if r.harmony_score == 4),
    }
