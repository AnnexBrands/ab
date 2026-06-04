"""No-drift guard for the progress report.

The progress report (``html/progress.html``) is generated entirely from live
introspection — the route set, the on-disk fixtures, and the test constants —
rather than from hand-maintained markdown that silently rots. These tests pin
that contract: each one would have failed against the bugs that motivated the
rewrite, so a regression that reintroduces drift turns the build red.
"""

from __future__ import annotations

import sys
from pathlib import Path

from ab.progress.route_index import (
    build_endpoint_class_progress,
    build_groups_from_routes,
    derive_fixtures_from_routes,
    index_all_routes,
    normalize_path,
    routes_as_endpoint_dicts,
)
from ab.progress.scanner import parse_constants, scan_fixture_files

REPO_ROOT = Path(__file__).resolve().parent.parent
CONSTANTS_PY = REPO_ROOT / "tests" / "constants.py"
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"


def _route_keys() -> set[tuple[str, str]]:
    return set(index_all_routes())


def test_gate_feed_covers_every_live_route():
    """The gate-evaluation feed must mirror the live route set exactly.

    This is the core no-drift invariant: if the report's endpoint inventory
    ever stops being derived from live Routes (e.g. reverts to FIXTURES.md),
    the feed and the live routes diverge and this fails.
    """
    feed_keys = {
        (normalize_path(row["endpoint_path"]), row["method"])
        for row in routes_as_endpoint_dicts()
    }
    assert feed_keys == _route_keys()


def test_headline_groups_count_matches_live_routes():
    """The coverage-summary headline must total the real route count."""
    groups = build_groups_from_routes()
    assert sum(g.total for g in groups) == len(routes_as_endpoint_dicts())
    # Every counted endpoint exists in code, so all are "done".
    assert all(g.done == g.total for g in groups)


def test_constants_are_discovered():
    """``parse_constants`` must find the TEST_* constants.

    Regression guard for the re-export refactor of ``tests/constants.py``: the
    old regex scanner silently returned zero once the module became a
    ``from examples.constants import (...)`` re-export.
    """
    constants = parse_constants(CONSTANTS_PY)
    names = {c.name for c in constants}
    assert constants, "no TEST_* constants discovered — scanner is blind"
    assert "TEST_CONTACT_DID" in names


def test_example_scan_is_static_and_finds_underscore_runners():
    """The example scanner must see ``_``-prefixed runners without importing.

    Regression guard for two bugs at once: the old scanner skipped every
    underscore-prefixed example file, and it *imported* the rest — firing live
    API calls (TimelineTask dumps) during report generation.
    """
    before = {m for m in sys.modules if m.startswith("examples.")}
    from ab.progress.route_index import _scan_example_entries

    discovered = _scan_example_entries()
    after = {m for m in sys.modules if m.startswith("examples.")}

    # Static parsing must not import any example module as a side effect.
    assert before == after
    # Underscore-prefixed runners (e.g. examples/_contacts.py) are seen.
    assert "get_did" in discovered.get("contacts", set())


def test_derived_fixtures_reflect_disk_state():
    """Fixture capture status must be derived from files actually on disk."""
    fixture_files = scan_fixture_files(FIXTURES_DIR)
    fixtures = derive_fixtures_from_routes(fixture_files)
    captured = {f.model_name for f in fixtures if f.status == "captured"}
    # Every "captured" model must have a real fixture file backing it.
    assert captured <= fixture_files
    assert captured, "no captured fixtures derived — disk scan is blind"


def test_wrapped_models_strip_to_inner_fixture_name():
    """``List[X]``/``PaginatedList[X]`` must resolve to the inner fixture file.

    Regression guard: an earlier feed left ``PaginatedList[...]`` unstripped, so
    wrapped response models never matched their on-disk fixture and were
    mislabelled ``needs-request-data``.
    """
    fixture_files = scan_fixture_files(FIXTURES_DIR)
    fixtures = derive_fixtures_from_routes(fixture_files)
    # No wrapper brackets may leak into the name used for fixture matching.
    assert not any("[" in f.model_name for f in fixtures)
    # A wrapped response model whose inner fixture exists must be captured.
    if "CatalogExpandedDto" in fixture_files:
        statuses = {
            f.status for f in fixtures if f.model_name == "CatalogExpandedDto"
        }
        assert "captured" in statuses


def test_committed_report_is_current():
    """The committed html/progress.html must match a fresh render.

    This is the freshness gate (also run in CI via
    ``generate_progress.py --check``): a route/model/doc change that forgets to
    regenerate the report turns the build red. Compared modulo the generation
    timestamp via the same code path the CLI uses.
    """
    from ab.progress.report import OUTPUT, is_report_current

    assert is_report_current(OUTPUT), (
        "html/progress.html is stale — regenerate with "
        "`python scripts/generate_progress.py`"
    )


def test_docstring_signal_is_populated():
    """The report must carry a per-method docstring signal for the help() goal."""
    ecp = build_endpoint_class_progress()
    methods = [
        mp
        for e in ecp
        for mp in (*e.helpers, *(m for v in e.sub_groups.values() for m in v))
    ]
    assert methods, "no methods discovered"
    # At least some methods are documented (signal is wired, not hard-coded).
    assert any(mp.has_docstring for mp in methods)
