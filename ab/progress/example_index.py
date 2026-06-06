"""Precise endpoint -> canonical-example mapping.

Replaces the noisy ``route_index._scan_example_entries`` (which only globbed
top-level ``examples/*.py`` — missing ``examples/jobs/*.py`` entirely — and counted
method names without checking them against real routes, producing impossible
negative "missing" counts).

This module statically parses every example (``examples/**/*.py``) with :mod:`ast`
(no imports, no side effects), resolves each ``api.<group>[.<sub>].<method>(...)``
call chain to a registry key, and counts an endpoint *covered* only when:

1. ``api.<group>.<method>`` is a real routed endpoint (it exists in the live
   endpoint registry with a :class:`~ab.api.route.Route`), and
2. it is called by a **canonical** example — a plain-script file whose name does
   not begin with ``_`` (the underscore prefix marks the deprecated runner).

See ``specs/037-example-coverage/contracts/example-contract.md`` §4.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"

# Non-example files under examples/ that must never be treated as examples.
_SKIP_STEMS = {"__init__", "__main__", "_runner", "_capture", "constants"}


@dataclass(frozen=True)
class CanonicalExample:
    """How a single routed endpoint is demonstrated by the example set."""

    endpoint_key: str  # "api.<group>[.<sub>].<method>"
    group: str  # registry group name, e.g. "jobs.payment"
    method_name: str  # e.g. "list"
    example_path: str | None  # repo-relative path of the chosen example, or None
    is_canonical: bool  # True iff backed by a non-underscore plain script
    is_legacy_runner: bool  # True iff referenced ONLY by underscore-prefixed file(s)


# ----------------------------------------------------------------------
# Routed endpoint set (from live code)
# ----------------------------------------------------------------------


def routed_endpoint_keys() -> set[str]:
    """Every real routed endpoint as ``api.<group>.<method>`` (from live Routes)."""
    from ab.cli.discovery import discover_endpoints_from_class

    keys: set[str] = set()
    for name, info in discover_endpoints_from_class().items():
        for m in info.methods:
            if m.route is not None:
                keys.add(f"api.{name}.{m.name}")
    return keys


# ----------------------------------------------------------------------
# Example scan
# ----------------------------------------------------------------------


def _attr_chain(node: ast.Attribute) -> list[str]:
    """Flatten an attribute chain to ``[root, attr, attr, ...]`` (empty if not Name-rooted)."""
    parts: list[str] = []
    cur: ast.expr = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if isinstance(cur, ast.Name):
        parts.append(cur.id)
        parts.reverse()
        return parts
    return []


def _scan_calls(path: Path) -> set[tuple[str, str]]:
    """Return ``{(group, method)}`` for every ``api.<group>...<method>(...)`` call."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return set()

    found: set[tuple[str, str]] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        chain = _attr_chain(node.func)
        # api.<group>.<method> needs >= 3 segments rooted at "api".
        if len(chain) < 3 or chain[0] != "api":
            continue
        group = ".".join(chain[1:-1])
        method = chain[-1]
        found.add((group, method))
    return found


def _iter_example_files() -> list[Path]:
    """Every candidate example file under examples/ (recursive), skipping helpers."""
    if not EXAMPLES_DIR.exists():
        return []
    return [
        p
        for p in sorted(EXAMPLES_DIR.rglob("*.py"))
        if p.stem not in _SKIP_STEMS
    ]


def build_example_index() -> dict[str, CanonicalExample]:
    """Map every routed endpoint key -> :class:`CanonicalExample`.

    Endpoints with no example at all are omitted (treat absence as
    ``missing_example``); use :func:`uncovered_endpoints` for the gate.
    """
    routed = routed_endpoint_keys()

    # endpoint_key -> {"canonical": [paths], "legacy": [paths]}
    hits: dict[str, dict[str, list[str]]] = {}
    for path in _iter_example_files():
        is_canonical_file = not path.name.startswith("_")
        rel = str(path.relative_to(REPO_ROOT))
        for group, method in _scan_calls(path):
            key = f"api.{group}.{method}"
            if key not in routed:
                continue  # not a real routed endpoint — ignore (kills false positives)
            bucket = hits.setdefault(key, {"canonical": [], "legacy": []})
            bucket["canonical" if is_canonical_file else "legacy"].append(rel)

    index: dict[str, CanonicalExample] = {}
    for key, bucket in hits.items():
        group, method = key[len("api.") :].rsplit(".", 1)
        canonical_paths = sorted(bucket["canonical"])
        legacy_paths = sorted(bucket["legacy"])
        has_canonical = bool(canonical_paths)
        index[key] = CanonicalExample(
            endpoint_key=key,
            group=group,
            method_name=method,
            example_path=(canonical_paths or legacy_paths or [None])[0],
            is_canonical=has_canonical,
            is_legacy_runner=(not has_canonical) and bool(legacy_paths),
        )
    return index


def uncovered_endpoints() -> list[str]:
    """Routed endpoints with NO canonical example (gate fails on these)."""
    index = build_example_index()
    out = [
        key
        for key in routed_endpoint_keys()
        if key not in index or not index[key].is_canonical
    ]
    return sorted(out)


def legacy_only_endpoints() -> list[str]:
    """Routed endpoints backed ONLY by a deprecated underscore-prefixed example."""
    index = build_example_index()
    return sorted(k for k, v in index.items() if v.is_legacy_runner)
