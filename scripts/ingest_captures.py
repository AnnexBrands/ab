#!/usr/bin/env python
"""Ingest an operator's captures.json into fixtures + examples (feature 037).

For each validated capture:
  1. write tests/fixtures/<Model>.json (canonical model_dump),
  2. write tests/fixtures/requests/<ReqModel>.json when a request body was pasted,
  3. generate a canonical example for the endpoint if it has none yet,
  4. mark the endpoint passing(source=paste) in tests/example_run_results.json.

Malformed pastes are reported and skipped — never written (Constitution II).

Usage::

    python scripts/ingest_captures.py captures.json
    python scripts/ingest_captures.py captures.json --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from ab.progress.captures import load_captures, validate_all  # noqa: E402
from ab.progress.example_gen import CallSpec, call_expr_for, module_path_for, render_module  # noqa: E402
from ab.progress.example_index import build_example_index  # noqa: E402

FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
REQUESTS_DIR = FIXTURES_DIR / "requests"
RESULTS_JSON = REPO_ROOT / "tests" / "example_run_results.json"


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _method_param_names(endpoint_key: str) -> list[str]:
    """Positional parameter names for the endpoint's method (for the example call)."""
    from ab.cli.discovery import discover_endpoints_from_class

    group, method = endpoint_key[len("api.") :].rsplit(".", 1)
    reg = discover_endpoints_from_class()
    info = reg.get(group)
    if not info:
        return []
    for m in info.methods:
        if m.name == method:
            return [p.name for p in m.positional_params]
    return []


def _load_results() -> dict[str, dict]:
    if RESULTS_JSON.is_file():
        try:
            return json.loads(RESULTS_JSON.read_text(encoding="utf-8")).get("results", {})
        except (OSError, ValueError):
            return {}
    return {}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("captures", help="path to captures.json")
    ap.add_argument("--dry-run", action="store_true", help="validate + report, write nothing")
    ap.add_argument("--date", help="ISO date to stamp results (default: today)")
    args = ap.parse_args(argv)

    try:
        captures = load_captures(Path(args.captures))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}")
        return 2

    validated = validate_all(captures)
    index = build_example_index()

    if args.date:
        today = args.date
    else:
        from datetime import date

        today = date.today().isoformat()

    results = _load_results()
    written = examples_made = rejected = 0

    for vc in validated:
        if not vc.ok:
            rejected += 1
            print(f"  [reject] {vc.endpoint}: {vc.error}")
            continue

        print(f"  [ok    ] {vc.endpoint} -> {vc.fixture_name}")
        if not args.dry_run:
            _write_json(FIXTURES_DIR / vc.fixture_name, vc.response_json)
            written += 1
            if vc.request_json is not None and vc.request_model:
                _write_json(REQUESTS_DIR / f"{vc.request_model}.json", vc.request_json)

            # Generate an example only if the endpoint has no canonical one yet.
            existing = index.get(vc.endpoint)
            if existing is None or not existing.is_canonical:
                group, method = vc.endpoint[len("api.") :].rsplit(".", 1)
                module_rel = module_path_for(group)
                module_path = REPO_ROOT / module_rel
                # examples/<top>/ as a package shadows examples/<top>.py — writing the
                # file would be dead code that `import examples.<top>` never reaches.
                pkg_dir = REPO_ROOT / "examples" / group.split(".")[0]
                if module_path.exists():
                    print(f"           (example module {module_rel} exists; add the call manually)")
                elif pkg_dir.is_dir():
                    top = group.split(".")[0]
                    print(f"           (examples/{top}/ is a package; add {vc.endpoint} to a module there manually)")
                else:
                    call_expr, consts = call_expr_for(group, method, _method_param_names(vc.endpoint))
                    spec = CallSpec(
                        group=group,
                        method=method,
                        call_expr=call_expr,
                        save_name=vc.fixture_name,
                        constants=consts,
                        comment="generated from captures.json paste",
                    )
                    module_path.parent.mkdir(parents=True, exist_ok=True)
                    module_path.write_text(render_module(group, [spec]), encoding="utf-8")
                    examples_made += 1
                    print(f"           generated {module_rel}")

            results[vc.endpoint] = {
                "status": "passing",
                "checked": today,
                "source": "paste",
                "fixture": vc.fixture_name,
                "detail": None,
            }

    if not args.dry_run and results:
        ordered = {k: results[k] for k in sorted(results)}
        _write_json(RESULTS_JSON, {"schema": 1, "results": ordered})

    print(
        f"\nsummary: {written} fixtures written, {examples_made} examples generated, "
        f"{rejected} rejected"
        + (" (dry run — nothing written)" if args.dry_run else "")
    )
    return 1 if rejected else 0


if __name__ == "__main__":
    raise SystemExit(main())
