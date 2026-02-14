#!/usr/bin/env python3
"""Generate progress.html report for ABConnect SDK coverage.

Usage:
    python scripts/generate_progress.py

Output:
    progress.html in the repository root.
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
OUTPUT = REPO_ROOT / "progress.html"


def main() -> int:
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
    from ab.progress.models import classify_action_items
    from ab.progress.parsers import parse_api_surface, parse_fixtures
    from ab.progress.renderer import render_report
    from ab.progress.scanner import parse_constants, scan_fixture_files

    # Parse all data sources
    groups = parse_api_surface(API_SURFACE)
    fixtures = parse_fixtures(FIXTURES_MD)
    fixture_files = scan_fixture_files(FIXTURES_DIR)
    constants = parse_constants(CONSTANTS_PY)

    # Classify action items
    action_items = classify_action_items(groups, fixtures, fixture_files, constants)

    # Render and write
    html = render_report(groups, fixtures, constants, fixture_files, action_items)
    OUTPUT.write_text(html)

    # Print summary
    total = sum(g.total for g in groups)
    done = sum(g.done for g in groups)
    pending = sum(g.pending for g in groups)
    ns = sum(g.not_started for g in groups)
    tier1 = sum(1 for i in action_items if i.tier == 1)
    tier2 = sum(1 for i in action_items if i.tier == 2)

    print(f"Progress report written to {OUTPUT.relative_to(REPO_ROOT)}")
    print(f"  Endpoints: {total} total, {done} done, {pending} pending, {ns} not started")
    print(f"  Action items: {len(action_items)} ({tier1} tier 1, {tier2} tier 2)")
    print(f"  Fixtures on disk: {len(fixture_files)}")
    print(f"  Constants defined: {len(constants)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
