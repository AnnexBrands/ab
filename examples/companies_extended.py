"""Example: Extended Companies operations.

Covers brands, geo settings, carrier accounts, and packaging settings.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (examples/_companies_extended.py) to the plain-script form.

See also: https://ab-sdk.readthedocs.io/en/latest/api/companies.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_COMPANY_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # ---- Brands -----------------------------------------------------------

    # GET /companies/brands
    print("\n# api.companies.get_brands()")
    result = api.companies.get_brands()
    print(format_result(result))
    save("CompanyBrand.json", result)

    # GET /companies/brandstree
    print("\n# api.companies.get_brands_tree()")
    result = api.companies.get_brands_tree()
    print(format_result(result))
    save("BrandTree.json", result)

    # ---- Carrier Accounts -------------------------------------------------

    # GET /companies/{companyId}/carrierAcounts
    print(f"\n# api.companies.get_carrier_accounts({TEST_COMPANY_ID!r})")
    result = api.companies.get_carrier_accounts(TEST_COMPANY_ID)
    print(format_result(result))
    save("CarrierAccount.json", result)

    # GET /companies/search/carrier-accounts — read-only search (no response model).
    print("\n# api.companies.search_carrier_accounts(current_company_id=..., query=...)")
    result = api.companies.search_carrier_accounts(
        current_company_id=TEST_COMPANY_ID, query="FedEx"
    )
    print(format_result(result))

    # GET /companies/suggest-carriers — read-only suggestions (no response model).
    print("\n# api.companies.suggest_carriers(tracking_number=...)")
    result = api.companies.suggest_carriers(tracking_number="1Z999AA10123456784")
    print(format_result(result))

    # ---- Geo Settings -----------------------------------------------------

    # GET /companies/geoAreaCompanies — read-only (no response model).
    print("\n# api.companies.get_geo_area_companies()")
    result = api.companies.get_geo_area_companies()
    print(format_result(result))

    # GET /companies/{companyId}/geosettings
    print(f"\n# api.companies.get_geo_settings({TEST_COMPANY_ID!r})")
    result = api.companies.get_geo_settings(TEST_COMPANY_ID)
    print(format_result(result))
    save("GeoSettings.json", result)

    # GET /companies/geosettings
    print("\n# api.companies.get_global_geo_settings()")
    result = api.companies.get_global_geo_settings()
    print(format_result(result))
    save("GeoSettings_global.json", result)

    # ---- Packaging --------------------------------------------------------

    # GET /companies/{companyId}/packagingsettings
    print(f"\n# api.companies.get_packaging_settings({TEST_COMPANY_ID!r})")
    result = api.companies.get_packaging_settings(TEST_COMPANY_ID)
    print(format_result(result))
    save("PackagingSettings.json", result)

    # GET /companies/{companyId}/packaginglabor
    print(f"\n# api.companies.get_packaging_labor({TEST_COMPANY_ID!r})")
    result = api.companies.get_packaging_labor(TEST_COMPANY_ID)
    print(format_result(result))
    save("PackagingLabor.json", result)

    # GET /companies/{companyId}/inheritedpackaginglabor
    print(f"\n# api.companies.get_inherited_packaging_labor({TEST_COMPANY_ID!r})")
    result = api.companies.get_inherited_packaging_labor(TEST_COMPANY_ID)
    print(format_result(result))
    save("PackagingLabor_inherited.json", result)

    # GET /companies/{companyId}/inheritedPackagingTariffs
    print(f"\n# api.companies.get_inherited_packaging_tariffs({TEST_COMPANY_ID!r})")
    result = api.companies.get_inherited_packaging_tariffs(TEST_COMPANY_ID)
    print(format_result(result))
    save("PackagingTariff.json", result)

    # ---- Mutating saves (guarded) -----------------------------------------

    # POST /companies/{companyId}/carrierAcounts — mutates staging.
    if mutations_enabled():
        print(f"\n# api.companies.save_carrier_accounts({TEST_COMPANY_ID!r}, data=CarrierAccountSaveRequest(...))")
        result = api.companies.save_carrier_accounts(
            TEST_COMPANY_ID, data=load_request("CarrierAccountSaveRequest.json")
        )
        print(format_result(result))
    else:
        print(
            "\n# api.companies.save_carrier_accounts skipped — "
            "set AB_RUN_MUTATIONS=1 to run (mutates staging)"
        )

    # POST /companies/{companyId}/geosettings — mutates staging.
    if mutations_enabled():
        print(f"\n# api.companies.save_geo_settings({TEST_COMPANY_ID!r}, data=GeoSettingsSaveRequest(...))")
        result = api.companies.save_geo_settings(
            TEST_COMPANY_ID, data=load_request("GeoSettingsSaveRequest.json")
        )
        print(format_result(result))
    else:
        print(
            "\n# api.companies.save_geo_settings skipped — "
            "set AB_RUN_MUTATIONS=1 to run (mutates staging)"
        )

    # POST /companies/{companyId}/packaginglabor — mutates staging.
    if mutations_enabled():
        print(f"\n# api.companies.save_packaging_labor({TEST_COMPANY_ID!r}, data=PackagingLaborSaveRequest(...))")
        result = api.companies.save_packaging_labor(
            TEST_COMPANY_ID, data=load_request("PackagingLaborSaveRequest.json")
        )
        print(format_result(result))
    else:
        print(
            "\n# api.companies.save_packaging_labor skipped — "
            "set AB_RUN_MUTATIONS=1 to run (mutates staging)"
        )

    # POST /companies/{companyId}/packagingsettings — mutates staging.
    if mutations_enabled():
        print(f"\n# api.companies.save_packaging_settings({TEST_COMPANY_ID!r}, data=PackagingSettingsSaveRequest(...))")
        result = api.companies.save_packaging_settings(
            TEST_COMPANY_ID, data=load_request("PackagingSettingsSaveRequest.json")
        )
        print(format_result(result))
    else:
        print(
            "\n# api.companies.save_packaging_settings skipped — "
            "set AB_RUN_MUTATIONS=1 to run (mutates staging)"
        )


if __name__ == "__main__":
    main()
