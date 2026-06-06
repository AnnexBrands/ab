#!/usr/bin/env python
"""Run read-only examples against staging and verify output matches fixtures.

Feature 037 live harness (Constitution II capture loop; contracts/example-contract.md §3).

For every routed **GET** endpoint that has a canonical example, the harness runs the
example MODULE once in a subprocess with ``AB_EXAMPLE_CAPTURE_DIR`` pointed at a temp
dir (so ``examples._capture.save`` writes there, never to ``tests/fixtures/``), then
diffs each produced ``<Model>.json`` against the committed fixture using the shared
comparison policy. Results are written to ``tests/example_run_results.json``.

Mutating endpoints (POST/PUT/PATCH/DELETE) are **never** run here — they are surfaced
in the report's paste-capture section instead.

Usage::

    python scripts/run_examples.py                 # run all read-only, verify, write results
    python scripts/run_examples.py --group jobs.timeline
    python scripts/run_examples.py --capture       # re-capture fixtures from live (refresh)
    python scripts/run_examples.py --list          # dry run: show what would run (no network)
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from ab.progress.example_gen import strip_list_wrapper  # noqa: E402
from ab.progress.example_index import build_example_index  # noqa: E402
from ab.progress.example_verify import compare  # noqa: E402

FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
RESULTS_JSON = REPO_ROOT / "tests" / "example_run_results.json"


def _endpoint_meta() -> dict[str, tuple[str, str]]:
    """Map endpoint key -> (http_method, response_model) from live routes."""
    from ab.cli.discovery import discover_endpoints_from_class

    out: dict[str, tuple[str, str]] = {}
    for name, info in discover_endpoints_from_class().items():
        for m in info.methods:
            if m.route is not None:
                out[f"api.{name}.{m.name}"] = (m.route.method, m.route.response_model or "")
    return out


def _module_for(example_path: str) -> str:
    """'examples/jobs/payment.py' -> 'examples.jobs.payment'."""
    return example_path[:-3].replace("/", ".")


def _plan(group_filter: str | None) -> dict[str, list[tuple[str, str]]]:
    """Build {module: [(endpoint_key, fixture_name), ...]} for read-only endpoints."""
    index = build_example_index()
    meta = _endpoint_meta()
    plan: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for key, ex in index.items():
        if not ex.is_canonical or not ex.example_path:
            continue
        http_method, response_model = meta.get(key, ("", ""))
        if http_method.upper() != "GET":
            continue  # mutations never auto-run
        if group_filter and not ex.group.startswith(group_filter):
            continue
        model = strip_list_wrapper(response_model)
        if not model:
            continue
        plan[_module_for(ex.example_path)].append((key, f"{model}.json"))
    return plan


def _run_module(module: str, capture_dir: Path | None) -> tuple[bool, str]:
    """Run ``python -m <module>``; return (ok, combined_output)."""
    env = dict(os.environ)
    if capture_dir is not None:
        env["AB_EXAMPLE_CAPTURE_DIR"] = str(capture_dir)
    proc = subprocess.run(
        [sys.executable, "-m", module],
        cwd=str(REPO_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
    )
    return proc.returncode == 0, (proc.stdout + proc.stderr)


def _write_results(results: dict[str, dict], today: str) -> None:
    ordered = {k: results[k] for k in sorted(results)}
    RESULTS_JSON.write_text(
        json.dumps({"schema": 1, "results": ordered}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"\nwrote {RESULTS_JSON.relative_to(REPO_ROOT)} ({len(ordered)} endpoints)")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--group", help="only run endpoints whose group starts with this")
    ap.add_argument("--capture", action="store_true", help="re-capture fixtures from live (refresh)")
    ap.add_argument("--list", action="store_true", dest="list_only", help="dry run; print plan, no network")
    ap.add_argument("--date", help="ISO date to stamp results (default: today)")
    args = ap.parse_args(argv)

    plan = _plan(args.group)
    total_eps = sum(len(v) for v in plan.values())
    print(f"{len(plan)} example modules, {total_eps} read-only endpoints to verify")

    if args.list_only:
        for module in sorted(plan):
            print(f"\n  python -m {module}")
            for key, fixture in plan[module]:
                print(f"      {key:<45} -> {fixture}")
        return 0

    if args.date:
        today = args.date
    else:
        from datetime import date

        today = date.today().isoformat()

    results: dict[str, dict] = {}
    passing = failing = errored = 0

    for module in sorted(plan):
        if args.capture:
            ok, output = _run_module(module, capture_dir=None)  # writes real fixtures
            status_line = "captured" if ok else "ERROR"
            print(f"  [{status_line}] python -m {module}")
            if not ok:
                print("    " + output.strip().replace("\n", "\n    ")[:500])
            continue

        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            ok, output = _run_module(module, capture_dir=tmp_dir)
            if not ok:
                errored += 1
                print(f"  [ERROR ] {module}: example raised")
                print("    " + output.strip().replace("\n", "\n    ")[:500])
                continue
            for key, fixture in plan[module]:
                produced_path = tmp_dir / fixture
                committed_path = FIXTURES_DIR / fixture
                if not produced_path.is_file() or not committed_path.is_file():
                    continue  # nothing produced/committed -> stays derived awaiting_data
                produced = json.loads(produced_path.read_text(encoding="utf-8"))
                expected = json.loads(committed_path.read_text(encoding="utf-8"))
                matches, detail = compare(produced, expected)
                results[key] = {
                    "status": "passing" if matches else "failing",
                    "checked": today,
                    "source": "live",
                    "fixture": fixture,
                    "detail": detail,
                }
                if matches:
                    passing += 1
                    print(f"  [pass  ] {key}")
                else:
                    failing += 1
                    print(f"  [FAIL  ] {key}  ({fixture})")

    if not args.capture:
        _write_results(results, today)
        print(f"\nsummary: {passing} passing, {failing} failing, {errored} module errors")
        return 1 if (failing or errored) else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
