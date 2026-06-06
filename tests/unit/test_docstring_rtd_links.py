"""help() -> RTD: every route-backed method in TOP_GROUPS carries a Docs footer.

This is the *verify* half of the "footers written into source" contract for
the help()->RTD discoverability goal. The expected footer is recomputed from
each method's :class:`~ab.api.route.Route` via :mod:`ab.api.rtd` and asserted
present (and correct) in the live docstring. A drifted RTD URL, a renamed
request/response model, or a hand-edit that drops the footer turns the build
red — so ``help(api.jobs.transfer)`` always links to the right page.

The scope is every group in the generator's ``TOP_GROUPS`` (every route-backed
top-level group as of PR-6, no longer just ``jobs``). A companion test pins
``TOP_GROUPS`` to the full set of routed groups so a newly added endpoint group
cannot silently ship without help()->RTD docs.
"""

from __future__ import annotations

import importlib.util
import inspect
import sys
from pathlib import Path

import pytest

from ab.api import rtd
from ab.cli.discovery import discover_endpoints_from_class

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "generate_endpoint_docs.py"


def _load_generator():
    spec = importlib.util.spec_from_file_location("generate_endpoint_docs", _SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod  # so the module-level @dataclass can resolve itself
    spec.loader.exec_module(mod)
    return mod


TOP_GROUPS = list(_load_generator().TOP_GROUPS)


def _routed_top_groups():
    """Every top-level group that exposes at least one route-backed method."""
    eps = discover_endpoints_from_class()
    return {
        rtd.endpoint_top_group(group)
        for group, info in eps.items()
        if any(m.route is not None for m in info.methods)
    }


def _all_routed():
    eps = discover_endpoints_from_class()
    out = []
    for group, info in eps.items():
        if rtd.endpoint_top_group(group) not in TOP_GROUPS:
            continue
        for m in info.methods:
            if m.route is None:
                continue
            out.append((group, m.name, getattr(info.endpoint_class, m.name), m.route))
    return out


ROUTED = _all_routed()


def test_top_groups_cover_every_routed_group():
    """``TOP_GROUPS`` must list every group with a route-backed method.

    This is the rollout-completeness guard: if a new endpoint group is added (or
    an existing one gains its first route-backed method) without being added to
    ``TOP_GROUPS``, its methods would ship without help()->RTD footers and pages.
    """
    assert set(TOP_GROUPS) == _routed_top_groups()


def test_routed_methods_were_discovered():
    """Guard against discovery silently returning nothing (which would make the
    parametrized test below vacuously pass)."""
    assert len(ROUTED) >= 200  # ~208 today across every route-backed group


@pytest.mark.parametrize(
    "group,name,func,route",
    ROUTED,
    ids=[f"{g}.{n}" for g, n, _f, _r in ROUTED],
)
def test_method_docstring_has_rtd_footer(group, name, func, route):
    doc = inspect.getdoc(func) or ""
    marker = rtd.footer_marker()

    # The page-URL footer line appears exactly once...
    assert doc.count(marker) == 1, f"{group}.{name}: expected exactly one Docs footer"

    # ...and equals the URL derived from the Route, with the right model lines.
    expected = rtd.docstring_footer_lines(
        group,
        name,
        request_model=route.request_model,
        params_model=route.params_model,
        response_model=route.response_model,
        path=route.path,
    )
    for line in expected:
        assert line in doc, f"{group}.{name}: docstring missing footer line {line!r}"

    # The human prose is preserved above the footer (the footer augments, never
    # replaces, the docstring).
    assert doc.split(marker)[0].strip(), f"{group}.{name}: prose lost above footer"


def test_strip_footer_block_only_removes_the_trailing_generated_block():
    """Prose that merely mentions the RTD URL must not be truncated.

    Regression guard: an earlier implementation cut at the first marker match
    anywhere in the body, which would silently drop human prose that referenced
    the RTD base URL. The strip must target only the generator's trailing block.
    """
    marker = rtd.footer_marker()
    footer = "\n\n" + "\n".join(rtd.docstring_footer_lines("jobs", "transfer", request_model="TransferModel"))

    # Prose that references the RTD URL, then the real generated footer.
    prose = f"See {marker}api/jobs/old.html for history.\nMore prose."
    assert rtd.strip_footer_block(prose + footer) == prose
    # No generated footer present -> text is returned untouched (prose preserved).
    assert rtd.strip_footer_block(prose) == prose
    # Idempotent: stripping twice equals stripping once.
    once = rtd.strip_footer_block(prose + footer)
    assert rtd.strip_footer_block(once) == once


def test_footer_lines_stay_within_lint_line_length():
    """Footers must respect ruff's 120-col limit once indented in source."""
    for group, name, _func, route in ROUTED:
        for line in rtd.docstring_footer_lines(
            group,
            name,
            request_model=route.request_model,
            params_model=route.params_model,
            response_model=route.response_model,
            path=route.path,
        ):
            # 8 = a method-body docstring's indentation.
            assert len(line) + 8 <= 120, f"{group}.{name}: footer line too long: {line!r}"


def test_params_are_path_bound_detects_path_modelled_params():
    """A params_model whose every field is a path placeholder is path-bound.

    ``TrackingV3Params`` models ``historyAmount``, which jobs.tracking.v3 keys as
    a ``{historyAmount}`` path placeholder (and binds into the URL path), even
    though swagger declares it ``in: query``. The same model on a path *without*
    that placeholder is a query param. Resolution is defensive on bad input.
    """
    assert rtd.params_are_path_bound(
        "/v3/job/{jobDisplayId}/tracking/{historyAmount}", "TrackingV3Params"
    )
    assert not rtd.params_are_path_bound("/v3/job/{jobDisplayId}/tracking", "TrackingV3Params")
    assert not rtd.params_are_path_bound(None, "TrackingV3Params")
    assert not rtd.params_are_path_bound("/x/{y}", None)
    assert not rtd.params_are_path_bound("/x/{int}", "int")  # primitive, never a model


def test_footer_labels_path_vs_query_params_by_route_path():
    """The footer says 'Path params:' only when the path carries the placeholder."""
    path_bound = rtd.docstring_footer_lines(
        "jobs", "v3", params_model="TrackingV3Params",
        path="/v3/job/{jobDisplayId}/tracking/{historyAmount}",
    )
    assert "Path params: TrackingV3Params" in path_bound
    assert "Query params: TrackingV3Params" not in path_bound

    # No path signal -> falls back to the query-params label (back-compat default).
    no_path = rtd.docstring_footer_lines("jobs", "v3", params_model="TrackingV3Params")
    assert "Query params: TrackingV3Params" in no_path
