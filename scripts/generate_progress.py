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

# Required input files
API_SURFACE = REPO_ROOT / "specs" / "api-surface.md"
FIXTURES_MD = REPO_ROOT / "FIXTURES.md"
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
CONSTANTS_PY = REPO_ROOT / "tests" / "constants.py"
OUTPUT = REPO_ROOT / "html" / "progress.html"


def main() -> int:
    generate_fixtures = "--fixtures" in sys.argv

    if generate_fixtures:
        return _generate_fixtures()

    return _generate_html_report()


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
    """Generate progress.html report."""
    # Validate required files exist
    missing = []
    for path, label in [
        (API_SURFACE, "specs/api-surface.md"),
        (FIXTURES_MD, "FIXTURES.md"),
        (FIXTURES_DIR, "tests/fixtures/"),
        (CONSTANTS_PY, "tests/constants.py"),
    ]:
        if not path.exists():
            missing.append(label)

    if missing:
        print(f"Error: Required files missing: {', '.join(missing)}", file=sys.stderr)
        print("Run from the repository root.", file=sys.stderr)
        return 1

    # Import here to keep validation fast
    import logging

    from ab.progress.fixtures_generator import parse_existing_fixtures
    from ab.progress.gates import evaluate_all_gates
    from ab.progress.models import classify_action_items
    from ab.progress.parsers import parse_api_surface, parse_fixtures
    from ab.progress.renderer import render_report
    from ab.progress.route_index import build_endpoint_class_progress
    from ab.progress.scanner import parse_constants, scan_fixture_files

    # Parse all data sources
    groups = parse_api_surface(API_SURFACE)
    fixtures = parse_fixtures(FIXTURES_MD)
    fixture_files = scan_fixture_files(FIXTURES_DIR)
    constants = parse_constants(CONSTANTS_PY)

    # Evaluate quality gates for all endpoints in FIXTURES.md
    fixtures_data = parse_existing_fixtures(FIXTURES_MD)
    prev_level = logging.root.level
    logging.root.setLevel(logging.ERROR)
    try:
        gate_results = evaluate_all_gates(fixtures_data)
    finally:
        logging.root.setLevel(prev_level)

    # Build endpoint class progress (US3)
    endpoint_class_progress = build_endpoint_class_progress()

    # Classify action items
    action_items = classify_action_items(groups, fixtures, fixture_files, constants)

    # Render and write
    html = render_report(
        groups, fixtures, constants, fixture_files, action_items,
        gate_results=gate_results,
        endpoint_class_progress=endpoint_class_progress,
    )
    OUTPUT.write_text(html)

    # Print summary
    total = sum(g.total for g in groups)
    done = sum(g.done for g in groups)
    pending = sum(g.pending for g in groups)
    ns = sum(g.not_started for g in groups)
    tier1 = sum(1 for i in action_items if i.tier == 1)
    tier2 = sum(1 for i in action_items if i.tier == 2)

    # Gate summary
    gate_total = len(gate_results)
    gate_complete = sum(1 for s in gate_results if s.overall_status == "complete")
    g1_pass = sum(1 for s in gate_results if s.g1_model_fidelity and s.g1_model_fidelity.passed)
    g2_pass = sum(1 for s in gate_results if s.g2_fixture_status and s.g2_fixture_status.passed)
    g3_pass = sum(1 for s in gate_results if s.g3_test_quality and s.g3_test_quality.passed)
    g4_pass = sum(1 for s in gate_results if s.g4_doc_accuracy and s.g4_doc_accuracy.passed)
    g5_pass = sum(1 for s in gate_results if s.g5_param_routing and s.g5_param_routing.passed)
    g6_pass = sum(1 for s in gate_results if s.g6_request_quality and s.g6_request_quality.passed)

    print(f"Progress report written to {OUTPUT.relative_to(REPO_ROOT)}")
    print(f"  Endpoints: {total} total, {done} done, {pending} pending, {ns} not started")
    print(f"  Action items: {len(action_items)} ({tier1} tier 1, {tier2} tier 2)")
    print(f"  Fixtures on disk: {len(fixture_files)}")
    print(f"  Constants defined: {len(constants)}")
    if gate_total:
        print(f"  Quality gates: {gate_complete}/{gate_total} endpoints pass all gates")
        print(f"    G1 Model Fidelity:  {g1_pass}/{gate_total}")
        print(f"    G2 Fixture Status:  {g2_pass}/{gate_total}")
        print(f"    G3 Test Quality:    {g3_pass}/{gate_total}")
        print(f"    G4 Doc Accuracy:    {g4_pass}/{gate_total}")
        print(f"    G5 Param Routing:   {g5_pass}/{gate_total}")
        print(f"    G6 Request Quality: {g6_pass}/{gate_total}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
