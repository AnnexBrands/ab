"""Step-by-step instruction builder for action items."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.progress.models import ActionItem, Constant, Endpoint

# Map path parameters to known constants
_PARAM_CONSTANT_MAP: dict[str, str] = {
    "companyId": "LIVE_COMPANY_UUID",
    "id": "LIVE_JOB_DISPLAY_ID",
    "jobDisplayId": "LIVE_JOB_DISPLAY_ID",
    "contactId": "LIVE_CONTACT_ID",
    "sellerId": "LIVE_SELLER_ID",
    "catalogId": "LIVE_CATALOG_ID",
}

_PATH_PARAM_RE = re.compile(r"\{(\w+)\}")


def detect_required_constants(endpoint: Endpoint) -> list[str]:
    """Map path parameters to required test constants.

    Returns list of constant names needed for this endpoint.
    """
    params = _PATH_PARAM_RE.findall(endpoint.path)
    constants: list[str] = []
    seen: set[str] = set()

    for param in params:
        const = _PARAM_CONSTANT_MAP.get(param)
        if const and const not in seen:
            constants.append(const)
            seen.add(const)
        elif not const:
            # Unknown param — suggest a new constant name
            suggested = f"LIVE_{param.upper()}"
            if suggested not in seen:
                constants.append(suggested)
                seen.add(suggested)

    return constants


def build_instructions(item: ActionItem, constants: list[Constant]) -> list[str]:
    """Build step-by-step instructions based on blocker type."""
    if item.blocker_type == "capture":
        return _instructions_capture(item)
    elif item.blocker_type == "constant_needed":
        return _instructions_constant_needed(item)
    elif item.blocker_type == "env_blocked":
        return _instructions_env_blocked(item)
    elif item.blocker_type == "not_implemented":
        return _instructions_not_implemented(item)
    return []


def _instructions_capture(item: ActionItem) -> list[str]:
    """Instructions for endpoints that just need fixture capture."""
    model = item.endpoint.response_model
    steps = []

    if item.fixture and item.fixture.capture_instructions:
        steps.append(
            f"Call the endpoint: <code>{item.fixture.capture_instructions}</code>"
        )
    else:
        steps.append(
            f"Call <code>{item.endpoint.method} {item.endpoint.path}</code> "
            f"against staging API"
        )

    steps.append(
        f"Save the JSON response to <code>tests/fixtures/{model}.json</code>"
    )
    steps.append(
        f"Run <code>pytest tests/ -k {_test_name(model)}</code> to verify "
        f"the fixture validates against the Pydantic model"
    )
    steps.append(
        f"Update <code>FIXTURES.md</code>: move this entry from Pending to "
        f"Captured with today's date"
    )

    return steps


def _instructions_constant_needed(item: ActionItem) -> list[str]:
    """Instructions for endpoints needing new constants."""
    steps = []

    for const in item.missing_constants:
        param = const.replace("LIVE_", "").lower()
        steps.append(
            f"Find a valid <code>{param}</code> in the staging environment "
            f"(check the ABConnect portal or database)"
        )
        steps.append(
            f"Add <code>{const} = &lt;value&gt;</code> to "
            f"<code>tests/constants.py</code>"
        )

    # Then add capture steps
    steps.extend(_instructions_capture(item))
    return steps


def _instructions_env_blocked(item: ActionItem) -> list[str]:
    """Instructions for endpoints blocked by environment limitations."""
    blocker = item.fixture.blocker if item.fixture else "Unknown environment limitation"
    model = item.endpoint.response_model

    return [
        f"<strong>Blocked:</strong> {blocker}",
        "This fixture cannot be captured from the staging environment.",
        (
            "Options: (a) capture from production if you have access, "
            "(b) request test data setup in staging, "
            "or (c) defer until the environment limitation is resolved."
        ),
        (
            f"When resolved, save the response to "
            f"<code>tests/fixtures/{model}.json</code> and update "
            f"<code>FIXTURES.md</code>"
        ),
    ]


def _instructions_not_implemented(item: ActionItem) -> list[str]:
    """Instructions for endpoints that need full implementation."""
    ep = item.endpoint
    model = ep.response_model
    group_lower = ep.group_name.lower().replace(" ", "_").replace("—", "").strip("_")

    steps = [
        f"<strong>Implementation needed</strong> — this endpoint has no models "
        f"or code yet",
    ]

    if model and model != "—" and model != "ServiceBaseResponse":
        steps.append(
            f"Create Pydantic model <code>{model}</code> in "
            f"<code>ab/api/models/{group_lower}.py</code>"
        )

    steps.append(
        f"Add endpoint method for <code>{ep.method} {ep.path}</code> in "
        f"<code>ab/api/endpoints/{group_lower}.py</code>"
    )

    steps.append(
        f"Create skeleton test with <code>require_fixture(\"{model}\", "
        f"\"{ep.method}\", \"{ep.path}\")</code>"
    )

    if ep.ref_status != "none":
        steps.append(
            f"ABConnectTools has a reference fixture ({ep.ref_status}) — "
            f"use for response shape guidance"
        )

    steps.append(
        f"Capture fixture: save response to "
        f"<code>tests/fixtures/{model}.json</code>"
    )

    return steps


def _test_name(model: str) -> str:
    """Generate a pytest -k filter from a model name."""
    # Convert CamelCase to snake_case for test matching
    s = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", model)
    s = re.sub(r"(?<=[A-Z])([A-Z][a-z])", r"_\1", s)
    return s.lower()
