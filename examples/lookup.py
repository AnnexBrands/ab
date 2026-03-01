"""Example: Lookup operations (4 methods)."""

from examples._runner import ExampleRunner
from tests.constants import TEST_ITEM_ID, TEST_JOB_DISPLAY_ID

runner = ExampleRunner("Lookup", env="staging")

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "get_contact_types",
    lambda api: api.lookup.get_contact_types(),
    response_model="List[ContactTypeEntity]",
    fixture_file="ContactTypeEntity.json",
)

runner.add(
    "get_countries",
    lambda api: api.lookup.get_countries(),
    response_model="List[CountryCodeDto]",
    fixture_file="CountryCodeDto.json",
)

runner.add(
    "get_job_statuses",
    lambda api: api.lookup.get_job_statuses(),
    response_model="List[JobStatus]",
    fixture_file="JobStatus.json",
)

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get_items",
    lambda api: api.lookup.get_items(
        job_display_id=TEST_JOB_DISPLAY_ID,
        job_item_id=TEST_ITEM_ID,
    ),
    response_model="List[LookupItem]",
    fixture_file="LookupItem.json",
)

if __name__ == "__main__":
    runner.run()
