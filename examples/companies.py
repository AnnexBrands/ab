"""Example: Company operations (8 methods)."""

from examples._runner import ExampleRunner
from tests.constants import TEST_COMPANY_UUID

runner = ExampleRunner("Companies", env="staging")

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "get_by_id",
    lambda api: api.companies.get_by_id(TEST_COMPANY_UUID),
    response_model="CompanySimple",
    fixture_file="CompanySimple.json",
)

runner.add(
    "get_fulldetails",
    lambda api: api.companies.get_fulldetails(TEST_COMPANY_UUID),
    response_model="CompanyDetails",
    fixture_file="CompanyDetails.json",
)

runner.add(
    "available_by_current_user",
    lambda api: api.companies.available_by_current_user(),
    response_model="List[SearchCompanyResponse]",
    fixture_file="SearchCompanyResponse.json",
)

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "get_details",
    lambda api: api.companies.get_details(TEST_COMPANY_UUID),
    response_model="CompanyDetails",
)

runner.add(
    "update_fulldetails",
    lambda api, data=None: api.companies.update_fulldetails(TEST_COMPANY_UUID, **(data or {})),
    request_model="CompanyDetails",
    request_fixture_file="CompanyDetails.json",
    response_model="CompanyDetails",
)

runner.add(
    "create",
    lambda api, data=None: api.companies.create(**(data or {})),
    request_model="CompanyDetails",
    request_fixture_file="CompanyDetails.json",
    response_model="str",
)

runner.add(
    "search",
    lambda api, data=None: api.companies.search(**(data or {})),
    request_model="CompanySearchRequest",
    request_fixture_file="CompanySearchRequest.json",
    response_model="List[SearchCompanyResponse]",
)

runner.add(
    "list",
    lambda api, data=None: api.companies.list(data or {}),
    request_model="ListRequest",
    request_fixture_file="ListRequest.json",
    response_model="List[CompanySimple]",
)

if __name__ == "__main__":
    runner.run()
