#!/usr/bin/env python3
"""Generate or update the gate regression baseline.

Calls evaluate_all_gates() and writes a JSON mapping of
``"{normalized_path} {METHOD}": ["G1", "G2", ...]`` for all
currently-passing gates per endpoint.

Usage:
    python scripts/update_gate_baseline.py
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASELINE_FILE = REPO_ROOT / "tests" / "gate_baseline.json"
sys.path.insert(0, str(REPO_ROOT))


def main() -> None:
    from ab.progress.fixtures_generator import parse_existing_fixtures
    from ab.progress.gates import evaluate_all_gates
    from ab.progress.route_index import normalize_path

    fixtures_data = parse_existing_fixtures()

    prev_level = logging.root.level
    logging.root.setLevel(logging.ERROR)
    try:
        results = evaluate_all_gates(fixtures_data)
    finally:
        logging.root.setLevel(prev_level)

    baseline: dict[str, list[str]] = {}
    for status in results:
        key = f"{normalize_path(status.endpoint_path)} {status.method}"
        passing: list[str] = []
        for gate_attr, gate_id in [
            ("g1_model_fidelity", "G1"),
            ("g2_fixture_status", "G2"),
            ("g3_test_quality", "G3"),
            ("g4_doc_accuracy", "G4"),
            ("g5_param_routing", "G5"),
            ("g6_request_quality", "G6"),
        ]:
            gate_result = getattr(status, gate_attr)
            if gate_result and gate_result.passed:
                passing.append(gate_id)
        if passing:
            baseline[key] = passing

    # Load previous baseline for diff
    old_baseline: dict[str, list[str]] = {}
    if BASELINE_FILE.exists():
        old_baseline = json.loads(BASELINE_FILE.read_text())

    # Write new baseline
    sorted_baseline = dict(sorted(baseline.items()))
    BASELINE_FILE.write_text(json.dumps(sorted_baseline, indent=2) + "\n")

    # Print diff summary
    new_passes = 0
    removed_passes = 0
    for key in sorted(set(list(baseline.keys()) + list(old_baseline.keys()))):
        old_gates = set(old_baseline.get(key, []))
        new_gates = set(baseline.get(key, []))
        added = new_gates - old_gates
        removed = old_gates - new_gates
        if added:
            new_passes += len(added)
            print(f"  + {key}: {', '.join(sorted(added))}")
        if removed:
            removed_passes += len(removed)
            print(f"  - {key}: {', '.join(sorted(removed))}")

    total_endpoints = len(baseline)
    total_gates = sum(len(v) for v in baseline.values())
    print(f"\nBaseline written to {BASELINE_FILE}")
    print(f"  {total_endpoints} endpoints, {total_gates} passing gates")
    if new_passes:
        print(f"  {new_passes} new passes")
    if removed_passes:
        print(f"  {removed_passes} removed passes")


if __name__ == "__main__":
    main()
