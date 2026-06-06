"""Shape + no-drift guards for the run-results artifact (feature 037, T019).

Non-live. The committed ``tests/example_run_results.json`` (written by the live
harness / ingest) must conform to the contract and keep the report deterministic.
When the artifact is absent, the report derives statuses and these shape checks
skip — the no-drift guarantee still holds.
"""

from __future__ import annotations

import json

import pytest

from ab.progress.report import RUN_RESULTS_JSON, is_report_current, load_run_results

_PERSISTED_STATUSES = {"passing", "failing", "binary"}
_SOURCES = {"live", "paste", "binary"}


def test_run_results_shape_when_present() -> None:
    if not RUN_RESULTS_JSON.is_file():
        pytest.skip("no run-results artifact yet (operator runs scripts/run_examples.py)")

    data = json.loads(RUN_RESULTS_JSON.read_text(encoding="utf-8"))
    assert data.get("schema") == 1
    results = data["results"]
    assert isinstance(results, dict)

    # Keys must be sorted (no-drift stability).
    assert list(results) == sorted(results), "results keys must be sorted"

    for key, entry in results.items():
        assert key.startswith("api."), key
        assert entry["status"] in _PERSISTED_STATUSES, (key, entry["status"])
        assert entry["source"] in _SOURCES, (key, entry["source"])
        assert isinstance(entry["checked"], str) and len(entry["checked"]) == 10


def test_loader_returns_dict() -> None:
    assert isinstance(load_run_results(), dict)


def test_report_is_current() -> None:
    """The committed report must match a fresh render (no-drift), artifact included."""
    assert is_report_current(), (
        "html/progress.html is stale — run `python scripts/generate_progress.py`"
    )
