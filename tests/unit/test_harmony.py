"""Tests for the per-endpoint Four-Way Harmony build (feature 037, T043)."""

from __future__ import annotations

from ab.progress.example_index import routed_endpoint_keys
from ab.progress.harmony import build_harmony, harmony_summary


def test_every_routed_endpoint_has_a_harmony_row() -> None:
    rows = build_harmony()
    keys = {r.endpoint_key for r in rows}
    assert keys == routed_endpoint_keys()


def test_harmony_invariants() -> None:
    for r in build_harmony():
        assert r.has_impl is True  # routed => implemented
        assert isinstance(r.tags, list)
        assert 0 <= r.harmony_score <= 4
        assert r.run_status in {
            "passing", "failing", "not_verified", "awaiting_data",
            "awaiting_paste", "binary", "missing_example",
        }


def test_summary_counts_consistent() -> None:
    rows = build_harmony()
    s = harmony_summary(rows)
    assert s["total"] == len(rows)
    assert 0 <= s["example"] <= s["total"]
    assert 0 <= s["full_harmony"] <= s["total"]
