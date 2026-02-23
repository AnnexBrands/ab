"""Example: On-hold management operations (10 methods).

Covers the full on-hold lifecycle: list, create, get, update, comment,
update dates, resolve, delete, follow-up users.
"""

from examples._runner import ExampleRunner
from tests.constants import TEST_CONTACT_ID, TEST_JOB_DISPLAY_ID

runner = ExampleRunner("On-Hold", env="staging")

TEST_ON_HOLD_ID = "PLACEHOLDER"

# ═══════════════════════════════════════════════════════════════════════
# On-Hold CRUD
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "list_on_hold",
    lambda api: api.jobs.list_on_hold(TEST_JOB_DISPLAY_ID),
    response_model="List[ExtendedOnHoldInfo]",
    fixture_file="ExtendedOnHoldInfo.json",
)

runner.add(
    "create_on_hold",
    lambda api, data=None: api.jobs.create_on_hold(TEST_JOB_DISPLAY_ID, **(data or {})),
    request_model="SaveOnHoldRequest",
    request_fixture_file="SaveOnHoldRequest.json",
    response_model="SaveOnHoldResponse",
    fixture_file="SaveOnHoldResponse.json",
)

runner.add(
    "get_on_hold",
    lambda api: api.jobs.get_on_hold(TEST_JOB_DISPLAY_ID, TEST_ON_HOLD_ID),
    response_model="OnHoldDetails",
    fixture_file="OnHoldDetails.json",
)

runner.add(
    "update_on_hold",
    lambda api, data=None: api.jobs.update_on_hold(TEST_JOB_DISPLAY_ID, TEST_ON_HOLD_ID, **(data or {})),
    request_model="SaveOnHoldRequest",
    request_fixture_file="SaveOnHoldRequest.json",
    response_model="SaveOnHoldResponse",
    fixture_file="SaveOnHoldResponse.json",
)

runner.add(
    "add_on_hold_comment",
    lambda api: api.jobs.add_on_hold_comment(TEST_JOB_DISPLAY_ID, TEST_ON_HOLD_ID, comment="Comment via SDK"),
    response_model="OnHoldNoteDetails",
    fixture_file="OnHoldNoteDetails.json",
)

runner.add(
    "update_on_hold_dates",
    lambda api, data=None: api.jobs.update_on_hold_dates(TEST_JOB_DISPLAY_ID, TEST_ON_HOLD_ID, **(data or {})),
    request_model="SaveOnHoldDatesModel",
    request_fixture_file="SaveOnHoldDatesModel.json",
)

runner.add(
    "resolve_on_hold",
    lambda api: api.jobs.resolve_on_hold(TEST_JOB_DISPLAY_ID, TEST_ON_HOLD_ID),
    response_model="ResolveJobOnHoldResponse",
    fixture_file="ResolveJobOnHoldResponse.json",
)

runner.add(
    "delete_on_hold",
    lambda api: api.jobs.delete_on_hold(TEST_JOB_DISPLAY_ID),
)

# ═══════════════════════════════════════════════════════════════════════
# Follow-Up Users
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "get_on_hold_followup_user",
    lambda api: api.jobs.get_on_hold_followup_user(TEST_JOB_DISPLAY_ID, TEST_CONTACT_ID),
    response_model="OnHoldUser",
    fixture_file="OnHoldUser.json",
)

runner.add(
    "list_on_hold_followup_users",
    lambda api: api.jobs.list_on_hold_followup_users(TEST_JOB_DISPLAY_ID),
    response_model="List[OnHoldUser]",
    fixture_file="OnHoldUser.json",
)

if __name__ == "__main__":
    runner.run()
