"""Example: Companies operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (examples/_companies.py) to the plain-script form.

See also: https://ab-sdk.readthedocs.io/en/latest/api/companies.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_COMPANY_UUID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /companies/{id}
    print(f"\n# api.companies.get_by_id({TEST_COMPANY_UUID!r})")
    result = api.companies.get_by_id(TEST_COMPANY_UUID)
    print(format_result(result))
    save("CompanySimple.json", result)

    # GET /companies/{companyId}/details
    print(f"\n# api.companies.get_details({TEST_COMPANY_UUID!r})")
    result = api.companies.get_details(TEST_COMPANY_UUID)
    print(format_result(result))
    save("CompanyDetails.json", result)

    # GET /companies/{companyId}/fulldetails
    print(f"\n# api.companies.get_fulldetails({TEST_COMPANY_UUID!r})")
    result = api.companies.get_fulldetails(TEST_COMPANY_UUID)
    print(format_result(result))
    save("CompanyDetails_full.json", result)

    # GET /companies/availableByCurrentUser
    print("\n# api.companies.available_by_current_user()")
    result = api.companies.available_by_current_user()
    print(format_result(result))
    save("CompanySimple_available.json", result)

    # POST /companies/list — read-only listing, safe to run unguarded.
    print("\n# api.companies.list(data=ListRequest(...))")
    result = api.companies.list(data=load_request("ListRequest.json"))
    print(format_result(result))
    save("CompanySimple_list.json", result)

    # POST /companies/search/v2 — read-only search, safe to run unguarded.
    print("\n# api.companies.search(data=CompanySearchRequest(...))")
    result = api.companies.search(data=load_request("CompanySearchRequest.json"))
    print(format_result(result))
    save("SearchCompanyResponse.json", result)

    # POST /companies/fulldetails — creates a company (mutates staging).
    if mutations_enabled():
        print("\n# api.companies.create(data=CompanyDetails(...))")
        result = api.companies.create(data=load_request("CompanyDetails.json"))
        print(format_result(result))
    else:
        print("\n# api.companies.create skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # PUT /companies/{companyId}/fulldetails — updates a company (mutates staging).
    if mutations_enabled():
        print(f"\n# api.companies.update_fulldetails({TEST_COMPANY_UUID!r}, data=CompanyDetails(...))")
        result = api.companies.update_fulldetails(
            TEST_COMPANY_UUID, data=load_request("CompanyDetails.json")
        )
        print(format_result(result))
        save("CompanyDetails.json", result)
    else:
        print(
            "\n# api.companies.update_fulldetails skipped — "
            "set AB_RUN_MUTATIONS=1 to run (mutates staging)"
        )


if __name__ == "__main__":
    main()
