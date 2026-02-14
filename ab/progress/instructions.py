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
    if item.blocker_type == "needs_request_data":
        return _instructions_needs_request_data(item)
    elif item.blocker_type == "constant_needed":
        return _instructions_constant_needed(item)
    elif item.blocker_type == "not_implemented":
        return _instructions_not_implemented(item)
    return []


def _instructions_needs_request_data(item: ActionItem) -> list[str]:
    """Instructions for endpoints that need correct request data."""
    ep = item.endpoint
    model = ep.response_model
    group_lower = ep.group_name.lower().replace(" ", "_").replace("—", "").strip("_")

    steps = []

    # Show what's missing if known from FIXTURES.md
    if item.fixture and item.fixture.blocker:
        steps.append(
            f"<strong>What's missing:</strong> {item.fixture.blocker}"
        )

    steps.append(
        f"Research ABConnectTools endpoint code "
        f"(<code>endpoints/{group_lower}.py</code>) and swagger "
        f"for required params/body"
    )
    steps.append(
        f"Fix the example in <code>examples/{group_lower}.py</code> "
        f"with correct request data"
    )
    steps.append(
        f"Run the example — save 200 response to "
        f"<code>tests/fixtures/{model}.json</code>"
    )
    steps.append(
        f"Run <code>pytest tests/ -k {_test_name(model)}</code> to verify "
        f"the fixture validates against the Pydantic model"
    )
    steps.append(
        "Update <code>FIXTURES.md</code>: move to Captured with today's date"
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

    # Then add request data steps
    steps.extend(_instructions_needs_request_data(item))
    return steps


def _instructions_not_implemented(item: ActionItem) -> list[str]:
    """Instructions for endpoints that need full DISCOVER workflow."""
    ep = item.endpoint
    model = ep.response_model
    group_lower = ep.group_name.lower().replace(" ", "_").replace("—", "").strip("_")

    steps = [
        f"<strong>Phase D:</strong> Research ABConnectTools "
        f"(<code>endpoints/{group_lower}.py</code>, "
        f"<code>examples/api/{group_lower}.py</code>) "
        f"and swagger for required params/body",
    ]

    if model and model != "—" and model != "ServiceBaseResponse":
        steps.append(
            f"<strong>Phase I:</strong> Create Pydantic model "
            f"<code>{model}</code> in "
            f"<code>ab/api/models/{group_lower}.py</code>"
        )

    steps.append(
        f"<strong>Phase S:</strong> Add endpoint method for "
        f"<code>{ep.method} {ep.path}</code> in "
        f"<code>ab/api/endpoints/{group_lower}.py</code>"
    )

    if ep.ref_status != "none":
        steps.append(
            f"ABConnectTools has a reference fixture ({ep.ref_status}) — "
            f"use for response shape guidance"
        )

    steps.append(
        f"<strong>Phase C:</strong> Write example with researched params, "
        f"run it, save 200 response to "
        f"<code>tests/fixtures/{model}.json</code>"
    )

    return steps


def _test_name(model: str) -> str:
    """Generate a pytest -k filter from a model name."""
    # Convert CamelCase to snake_case for test matching
    s = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", model)
    s = re.sub(r"(?<=[A-Z])([A-Z][a-z])", r"_\1", s)
    return s.lower()
