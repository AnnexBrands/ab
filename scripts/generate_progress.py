#!/usr/bin/env python3
"""Generate progress.html report for ABConnect SDK coverage.

Usage:
    python scripts/generate_progress.py             # HTML report only
    python scripts/generate_progress.py --fixtures   # Regenerate FIXTURES.md with gates

Output:
    progress.html in the repository root.
    FIXTURES.md (with --fixtures flag) regenerated with per-gate columns.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Resolve repo root (parent of scripts/)
REPO_ROOT = Path(__file__).resolve().parent.parent

# Prefer the in-repo ``ab`` over any pip-installed copy, so the report (and the
# --check freshness gate in CI, which runs after a non-editable ``pip install
# .``) is built from this checkout's routes, fixtures, and html/ directory.
sys.path.insert(0, str(REPO_ROOT))

# Introspected inputs (no hand-maintained markdown). FIXTURES_MD is only an
# output of ``--fixtures``, never a source for the HTML report.
FIXTURES_MD = REPO_ROOT / "FIXTURES.md"
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
CONSTANTS_PY = REPO_ROOT / "tests" / "constants.py"


def main() -> int:
    if "--fixtures" in sys.argv:
        return _generate_fixtures()

    if "--check" in sys.argv:
        return _check_html_report()

    return _generate_html_report()


def _check_html_report() -> int:
    """Freshness gate: fail if the committed report is stale vs live code.

    Compares the committed ``html/progress.html`` against a fresh render
    (ignoring the generation timestamp). Used by CI and the test suite so a
    route/model change that forgets to regenerate the report turns red.
    """
    from ab.progress.report import OUTPUT, is_report_current

    if is_report_current(OUTPUT):
        print(f"Progress report is current: {OUTPUT.relative_to(REPO_ROOT)}")
        return 0

    print(
        f"Progress report is STALE: {OUTPUT.relative_to(REPO_ROOT)}\n"
        "Regenerate it with: python scripts/generate_progress.py",
        file=sys.stderr,
    )
    return 1


def _generate_fixtures() -> int:
    """Regenerate FIXTURES.md with per-gate quality columns."""
    if not FIXTURES_MD.exists():
        print("Error: FIXTURES.md not found", file=sys.stderr)
        return 1

    from ab.progress.fixtures_generator import generate_fixtures_md

    _content, sync_report = generate_fixtures_md(FIXTURES_MD)
    print(f"FIXTURES.md regenerated with quality gate columns at {FIXTURES_MD.relative_to(REPO_ROOT)}")

    # Route sync summary
    print(
        f"  Route sync: {sync_report.matched} matched, "
        f"{len(sync_report.mismatches)} mismatches, "
        f"{len(sync_report.new_endpoints)} new endpoints added"
    )
    if sync_report.unmatched_rows:
        print(f"  Unmatched FIXTURES.md rows: {len(sync_report.unmatched_rows)}")
    for msg in sync_report.mismatches:
        print(f"    {msg}")
    for msg in sync_report.new_endpoints:
        print(f"    {msg}")
    for msg in sync_report.unmatched_rows:
        print(f"    {msg}")

    return 0


def _generate_html_report() -> int:
    """Generate progress.html report.

    The report is derived entirely from live introspection — the route set,
    the on-disk fixtures, and the test constants — so it cannot drift from the
    code the way a hand-maintained markdown inventory does. ``specs/
    api-surface.md`` and ``FIXTURES.md`` are no longer report *inputs*;
    ``FIXTURES.md`` is regenerated as an *output* via ``--fixtures``.
    """
    # Validate required inputs exist (introspected sources only)
    missing = []
    for path, label in [
        (FIXTURES_DIR, "tests/fixtures/"),
        (CONSTANTS_PY, "tests/constants.py"),
    ]:
        if not path.exists():
            missing.append(label)

    if missing:
        print(f"Error: Required files missing: {', '.join(missing)}", file=sys.stderr)
        print("Run from the repository root.", file=sys.stderr)
        return 1

    from ab.progress.report import OUTPUT, report_summary, write_report

    write_report(OUTPUT)
    s = report_summary()

    print(f"Progress report written to {OUTPUT.relative_to(REPO_ROOT)}")
    print(
        f"  Endpoints: {s['total']} total, {s['done']} done, "
        f"{s['pending']} pending, {s['not_started']} not started"
    )
    print(f"  Action items: {s['action_items']} ({s['tier1']} tier 1, {s['tier2']} tier 2)")
    print(f"  Fixtures on disk: {s['fixture_files']}")
    print(f"  Constants defined: {s['constants']}")
    if s["gate_total"]:
        print(f"  Quality gates: {s['gate_complete']}/{s['gate_total']} endpoints pass all gates")
        print(f"    G1 Model Fidelity:  {s['g1']}/{s['gate_total']}")
        print(f"    G2 Fixture Status:  {s['g2']}/{s['gate_total']}")
        print(f"    G3 Test Quality:    {s['g3']}/{s['gate_total']}")
        print(f"    G4 Doc Accuracy:    {s['g4']}/{s['gate_total']}")
        print(f"    G5 Param Routing:   {s['g5']}/{s['gate_total']}")
        print(f"    G6 Request Quality: {s['g6']}/{s['gate_total']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
