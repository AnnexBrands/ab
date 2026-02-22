"""Example: On-hold management operations (10 methods).

Covers the full on-hold lifecycle: list, create, get, update, comment,
update dates, resolve, delete, follow-up users.
"""

from examples._runner import ExampleRunner
from tests.constants import LIVE_CONTACT_ID, LIVE_JOB_DISPLAY_ID

runner = ExampleRunner("On-Hold", env="staging")

LIVE_ON_HOLD_ID = "PLACEHOLDER"

# ═══════════════════════════════════════════════════════════════════════
# On-Hold CRUD
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "list_on_hold",
    lambda api: api.jobs.list_on_hold(LIVE_JOB_DISPLAY_ID),
    response_model="List[ExtendedOnHoldInfo]",
    fixture_file="ExtendedOnHoldInfo.json",
)

runner.add(
    "create_on_hold",
    lambda api: api.jobs.create_on_hold(
        LIVE_JOB_DISPLAY_ID,
        reason="SDK Test",
        description="Testing on-hold creation",
    ),
    request_model="SaveOnHoldRequest",
    response_model="SaveOnHoldResponse",
    fixture_file="SaveOnHoldResponse.json",
)

runner.add(
    "get_on_hold",
    lambda api: api.jobs.get_on_hold(LIVE_JOB_DISPLAY_ID, LIVE_ON_HOLD_ID),
    response_model="OnHoldDetails",
    fixture_file="OnHoldDetails.json",
)

runner.add(
    "update_on_hold",
    lambda api: api.jobs.update_on_hold(
        LIVE_JOB_DISPLAY_ID,
        LIVE_ON_HOLD_ID,
        description="Updated description",
    ),
    request_model="SaveOnHoldRequest",
    response_model="SaveOnHoldResponse",
)

runner.add(
    "add_on_hold_comment",
    lambda api: api.jobs.add_on_hold_comment(
        LIVE_JOB_DISPLAY_ID,
        LIVE_ON_HOLD_ID,
        comment="Comment via SDK",
    ),
    response_model="OnHoldNoteDetails",
    fixture_file="OnHoldNoteDetails.json",
)

runner.add(
    "update_on_hold_dates",
    lambda api: api.jobs.update_on_hold_dates(
        LIVE_JOB_DISPLAY_ID,
        LIVE_ON_HOLD_ID,
        followUpDate="2026-03-01",
    ),
    request_model="SaveOnHoldDatesModel",
)

runner.add(
    "resolve_on_hold",
    lambda api: api.jobs.resolve_on_hold(LIVE_JOB_DISPLAY_ID, LIVE_ON_HOLD_ID),
    response_model="ResolveJobOnHoldResponse",
    fixture_file="ResolveJobOnHoldResponse.json",
)

runner.add(
    "delete_on_hold",
    lambda api: api.jobs.delete_on_hold(LIVE_JOB_DISPLAY_ID),
)

# ═══════════════════════════════════════════════════════════════════════
# Follow-Up Users
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "get_on_hold_followup_user",
    lambda api: api.jobs.get_on_hold_followup_user(LIVE_JOB_DISPLAY_ID, LIVE_CONTACT_ID),
    response_model="OnHoldUser",
    fixture_file="OnHoldUser.json",
)

runner.add(
    "list_on_hold_followup_users",
    lambda api: api.jobs.list_on_hold_followup_users(LIVE_JOB_DISPLAY_ID),
    response_model="List[OnHoldUser]",
)

if __name__ == "__main__":
    runner.run()
