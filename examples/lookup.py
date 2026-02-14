"""Example: Lookup operations (4 methods)."""

from examples._runner import ExampleRunner

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
        # TODO: capture fixture — returns 204, research needed
    ),
    response_model="List[LookupItem]",
    fixture_file="LookupItem.json",
)

if __name__ == "__main__":
    runner.run()
