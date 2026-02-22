"""Example: Company operations (8 methods)."""

from examples._runner import ExampleRunner
from tests.constants import LIVE_COMPANY_UUID

runner = ExampleRunner("Companies", env="staging")

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "get_by_id",
    lambda api: api.companies.get_by_id(LIVE_COMPANY_UUID),
    response_model="CompanySimple",
    fixture_file="CompanySimple.json",
)

runner.add(
    "get_fulldetails",
    lambda api: api.companies.get_fulldetails(LIVE_COMPANY_UUID),
    response_model="CompanyDetails",
    fixture_file="CompanyDetails.json",
)

runner.add(
    "available_by_current_user",
    lambda api: api.companies.available_by_current_user(),
    response_model="List[SearchCompanyResponse]",
    fixture_file="SearchCompanyResponse.json",
)

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get_details",
    lambda api: api.companies.get_details(
        # TODO: capture fixture — needs company UUID with populated details
        LIVE_COMPANY_UUID,
    ),
    response_model="CompanyDetails",
)

runner.add(
    "update_fulldetails",
    lambda api: api.companies.update_fulldetails(
        LIVE_COMPANY_UUID,
        # TODO: capture fixture — needs valid CompanyDetails kwargs
    ),
    request_model="CompanyDetails",
    response_model="CompanyDetails",
)

runner.add(
    "create",
    lambda api: api.companies.create(
        # TODO: capture fixture — needs valid CompanyDetails kwargs for new company
    ),
    request_model="CompanyDetails",
    response_model="str",
)

runner.add(
    "search",
    lambda api: api.companies.search(
        # TODO: capture fixture — needs valid CompanySearchRequest kwargs
        search_text="test",
        page=1,
        page_size=25,
    ),
    request_model="CompanySearchRequest",
    response_model="List[SearchCompanyResponse]",
)

runner.add(
    "list",
    lambda api: api.companies.list(
        # TODO: capture fixture — needs valid ListRequest kwargs
    ),
    request_model="ListRequest",
    response_model="List[CompanySimple]",
)

if __name__ == "__main__":
    runner.run()
