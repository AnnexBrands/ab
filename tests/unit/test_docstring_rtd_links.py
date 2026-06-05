"""help() -> RTD: every jobs route-backed method carries a derived Docs footer.

This is the *verify* half of the "footers written into source" contract for
the help()->RTD discoverability goal. The expected footer is recomputed from
each method's :class:`~ab.api.route.Route` via :mod:`ab.api.rtd` and asserted
present (and correct) in the live docstring. A drifted RTD URL, a renamed
request/response model, or a hand-edit that drops the footer turns the build
red — so ``help(api.jobs.transfer)`` always links to the right page.
"""

from __future__ import annotations

import inspect

import pytest

from ab.api import rtd
from ab.cli.discovery import discover_endpoints_from_class


def _jobs_routed():
    eps = discover_endpoints_from_class()
    out = []
    for group, info in eps.items():
        if rtd.endpoint_top_group(group) != "jobs":
            continue
        for m in info.methods:
            if m.route is None:
                continue
            out.append((group, m.name, getattr(info.endpoint_class, m.name), m.route))
    return out


JOBS_ROUTED = _jobs_routed()


def test_jobs_routed_methods_were_discovered():
    """Guard against discovery silently returning nothing (which would make the
    parametrized test below vacuously pass)."""
    assert len(JOBS_ROUTED) >= 70  # ~78 today across JobsEndpoint + subgroups


@pytest.mark.parametrize(
    "group,name,func,route",
    JOBS_ROUTED,
    ids=[f"{g}.{n}" for g, n, _f, _r in JOBS_ROUTED],
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
    for group, name, _func, route in JOBS_ROUTED:
        for line in rtd.docstring_footer_lines(
            group,
            name,
            request_model=route.request_model,
            params_model=route.params_model,
            response_model=route.response_model,
        ):
            # 8 = a method-body docstring's indentation.
            assert len(line) + 8 <= 120, f"{group}.{name}: footer line too long: {line!r}"
