"""Coverage gate: every routed endpoint has a canonical example (feature 037).

Non-live. Sources the precise endpoint->example map from
``ab.progress.example_index`` (canonical = a non-underscore plain script that calls
the endpoint, resolving to a real Route).

The two ``STRICT_*`` flags below are the explicit hardening points:
- ``STRICT_COVERAGE`` is flipped to True (T013) once every routed endpoint has a
  canonical example; until then a remaining gap is reported as ``xfail`` so the
  in-progress feature does not turn the suite red.
- ``STRICT_NO_LEGACY`` is flipped to True (T031) once the deprecated-runner
  migration is complete.
"""

from __future__ import annotations

import pytest

from ab.progress.example_index import legacy_only_endpoints, uncovered_endpoints

# Hardening flags — flip to True as the feature's phases complete.
STRICT_COVERAGE = False  # T013: every routed endpoint has a canonical example
STRICT_NO_LEGACY = False  # T031: no endpoint backed ONLY by a deprecated runner


def test_every_routed_endpoint_has_canonical_example() -> None:
    """FR-002 / FR-008 / SC-001 / SC-005."""
    missing = uncovered_endpoints()
    if missing and not STRICT_COVERAGE:
        pytest.xfail(
            f"{len(missing)} routed endpoints still lack a canonical example "
            "(feature 037 in progress — see specs/037-example-coverage/coverage-gaps.md)"
        )
    assert not missing, "Routed endpoints lacking a canonical example:\n  " + "\n  ".join(missing)


def test_no_endpoint_backed_only_by_deprecated_runner() -> None:
    """FR-014 / SC-006 — every endpoint's canonical example is a plain script."""
    legacy = legacy_only_endpoints()
    if legacy and not STRICT_NO_LEGACY:
        pytest.xfail(
            f"{len(legacy)} routed endpoints are still backed only by a deprecated "
            "underscore-prefixed runner example (feature 037 migration in progress)"
        )
    assert not legacy, "Endpoints still backed only by the deprecated runner:\n  " + "\n  ".join(legacy)
