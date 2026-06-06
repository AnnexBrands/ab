"""Build the no-drift progress report from live introspection.

This is the single source of report-generation logic: ``scripts/
generate_progress.py`` (the CLI), the freshness gate (``--check`` / CI), and
the test guard all call into here, so write-path and check-path can never
drift apart. Every input is derived from live code — the route set, the
on-disk fixtures, and the test constants — never from hand-maintained
markdown.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT = REPO_ROOT / "html" / "progress.html"
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
CONSTANTS_PY = REPO_ROOT / "tests" / "constants.py"
RUN_RESULTS_JSON = REPO_ROOT / "tests" / "example_run_results.json"


def load_run_results() -> dict[str, dict]:
    """Load the committed run-results artifact (feature 037), or {} if absent.

    Returns ``{endpoint_key: {status, checked, source, fixture, detail}}`` — the
    last live/paste-verified status per endpoint, overlaid onto derived statuses by
    the report builder. Keeps report generation deterministic (no live calls).
    """
    import json

    if not RUN_RESULTS_JSON.is_file():
        return {}
    try:
        data = json.loads(RUN_RESULTS_JSON.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    results = data.get("results", {})
    return results if isinstance(results, dict) else {}

# The only volatile part of the rendered report is its generation timestamp;
# strip it so freshness comparisons are stable across runs.
_TIMESTAMP_RE = re.compile(r"<p class='subtitle'>Generated[^<]*</p>")


@dataclass
class _Gathered:
    groups: list[Any]
    fixtures: list[Any]
    constants: list[Any]
    fixture_files: set[str]
    gate_results: list[Any]
    endpoint_class_progress: list[Any]
    action_items: list[Any]


def _gather() -> _Gathered:
    """Collect every report input from live introspection."""
    from ab.progress.gates import evaluate_all_gates
    from ab.progress.models import classify_action_items
    from ab.progress.route_index import (
        build_endpoint_class_progress,
        build_groups_from_routes,
        derive_fixtures_from_routes,
        routes_as_endpoint_dicts,
    )
    from ab.progress.scanner import parse_constants, scan_fixture_files

    groups = build_groups_from_routes()
    fixture_files = scan_fixture_files(FIXTURES_DIR)
    constants = parse_constants(CONSTANTS_PY)
    fixtures = derive_fixtures_from_routes(fixture_files)

    prev_level = logging.root.level
    logging.root.setLevel(logging.ERROR)
    try:
        gate_results = evaluate_all_gates(routes_as_endpoint_dicts())
    finally:
        logging.root.setLevel(prev_level)

    endpoint_class_progress = build_endpoint_class_progress(run_results=load_run_results())
    action_items = classify_action_items(groups, fixtures, fixture_files, constants)

    return _Gathered(
        groups=groups,
        fixtures=fixtures,
        constants=constants,
        fixture_files=fixture_files,
        gate_results=gate_results,
        endpoint_class_progress=endpoint_class_progress,
        action_items=action_items,
    )


def build_report_html() -> str:
    """Render the full progress report HTML from live introspection."""
    from ab.progress.renderer import render_report

    g = _gather()
    return render_report(
        g.groups,
        g.fixtures,
        g.constants,
        g.fixture_files,
        g.action_items,
        gate_results=g.gate_results,
        endpoint_class_progress=g.endpoint_class_progress,
    )


def write_report(path: Path | None = None) -> Path:
    """Generate and write the report. Returns the path written."""
    path = path or OUTPUT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_report_html())
    return path


def report_summary() -> dict[str, int]:
    """Return headline counts for the CLI summary."""
    g = _gather()
    gr = g.gate_results

    def _passes(attr: str) -> int:
        return sum(1 for s in gr if getattr(s, attr) and getattr(s, attr).passed)

    return {
        "total": sum(grp.total for grp in g.groups),
        "done": sum(grp.done for grp in g.groups),
        "pending": sum(grp.pending for grp in g.groups),
        "not_started": sum(grp.not_started for grp in g.groups),
        "action_items": len(g.action_items),
        "tier1": sum(1 for i in g.action_items if i.tier == 1),
        "tier2": sum(1 for i in g.action_items if i.tier == 2),
        "fixture_files": len(g.fixture_files),
        "constants": len(g.constants),
        "gate_total": len(gr),
        "gate_complete": sum(1 for s in gr if s.overall_status == "complete"),
        "g1": _passes("g1_model_fidelity"),
        "g2": _passes("g2_fixture_status"),
        "g3": _passes("g3_test_quality"),
        "g4": _passes("g4_doc_accuracy"),
        "g5": _passes("g5_param_routing"),
        "g6": _passes("g6_request_quality"),
    }


def _canonical(html: str) -> str:
    """Strip the volatile generation timestamp for stable comparison."""
    return _TIMESTAMP_RE.sub("", html)


def is_report_current(path: Path | None = None) -> bool:
    """Return whether the committed report matches a fresh render.

    Compares modulo the generation timestamp, so it answers "is the report's
    *content* up to date with the live code" — the no-drift freshness gate.
    """
    path = path or OUTPUT
    if not path.exists():
        return False
    return _canonical(path.read_text()) == _canonical(build_report_html())
