"""Example: Contact operations (7 methods)."""

from examples._runner import ExampleRunner

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
    lambda api: api.contacts.get_details("30760"),
    response_model="ContactDetailedInfo",
    fixture_file="ContactDetailedInfo.json",
)

runner.add(
    "get_primary_details",
    lambda api: api.contacts.get_primary_details("30760"),
    response_model="ContactPrimaryDetails",
    fixture_file="ContactPrimaryDetails.json",
)

runner.add(
    "search",
    lambda api: api.contacts.search({"searchText": "Justine"}),
    request_model="ContactSearchRequest",
    response_model="List[SearchContactEntityResult]",
    fixture_file="SearchContactEntityResult.json",
)

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get",
    lambda api: api.contacts.get(
        # TODO: capture fixture — needs valid contact ID (string)
        "30760",
    ),
    response_model="ContactSimple",
)

runner.add(
    "update_details",
    lambda api: api.contacts.update_details(
        "30760",
        # TODO: capture fixture — needs valid ContactEditRequest body
        {},
    ),
    request_model="ContactEditRequest",
)

runner.add(
    "create",
    lambda api: api.contacts.create(
        # TODO: capture fixture — needs valid ContactEditRequest body for new contact
        {},
    ),
    request_model="ContactEditRequest",
)

if __name__ == "__main__":
    runner.run()
