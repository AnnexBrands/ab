"""Example: Contact operations (7 methods)."""

from examples._runner import ExampleRunner
from tests.constants import TEST_CONTACT_ID

runner = ExampleRunner("Contacts", env="staging")

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "get_current_user",
    lambda api: api.contacts.get_current_user(),
    response_model="ContactSimple",
    fixture_file="ContactSimple.json",
)

runner.add(
    "get_details",
    lambda api: api.contacts.get_details(str(TEST_CONTACT_ID)),
    response_model="ContactDetailedInfo",
    fixture_file="ContactDetailedInfo.json",
)

runner.add(
    "get_primary_details",
    lambda api: api.contacts.get_primary_details(str(TEST_CONTACT_ID)),
    response_model="ContactPrimaryDetails",
    fixture_file="ContactPrimaryDetails.json",
)

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "search",
    lambda api, data=None: api.contacts.search(data or {}),
    request_model="ContactSearchRequest",
    request_fixture_file="ContactSearchRequest.json",
    response_model="List[SearchContactEntityResult]",
    fixture_file="SearchContactEntityResult.json",
)

runner.add(
    "get",
    lambda api: api.contacts.get(str(TEST_CONTACT_ID)),
    response_model="ContactSimple",
)

runner.add(
    "update_details",
    lambda api, data=None: api.contacts.update_details(str(TEST_CONTACT_ID), data or {}),
    request_model="ContactEditRequest",
    request_fixture_file="ContactEditRequest.json",
)

runner.add(
    "create",
    lambda api, data=None: api.contacts.create(data or {}),
    request_model="ContactEditRequest",
    request_fixture_file="ContactEditRequest.json",
)

if __name__ == "__main__":
    runner.run()
