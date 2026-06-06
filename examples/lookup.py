"""Example: Lookup operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runners (``examples/_lookup.py`` and ``examples/_lookup_extended.py``)
to the plain-script form.

All lookup endpoints are read-only GETs that take explicit snake_case kwargs (or
no args), so the calls use real inline values rather than a request fixture.
See also: https://ab-sdk.readthedocs.io/en/latest/api/lookup.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import save
from examples.constants import TEST_ITEM_ID, TEST_JOB_DISPLAY_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /lookup/contactTypes
    print("\n# api.lookup.get_contact_types()")
    result = api.lookup.get_contact_types()
    print(format_result(result))
    save("ContactTypeEntity.json", result)

    # GET /lookup/countries
    print("\n# api.lookup.get_countries()")
    result = api.lookup.get_countries()
    print(format_result(result))
    save("CountryCodeDto.json", result)

    # GET /lookup/jobStatuses
    print("\n# api.lookup.get_job_statuses()")
    result = api.lookup.get_job_statuses()
    print(format_result(result))
    save("JobStatus.json", result)

    # GET /lookup/items
    print("\n# api.lookup.get_items(job_display_id=..., job_item_id=...)")
    result = api.lookup.get_items(
        job_display_id=TEST_JOB_DISPLAY_ID,
        job_item_id=TEST_ITEM_ID,
    )
    print(format_result(result))
    save("LookupItem.json", result)

    # GET /lookup/accessKeys
    print("\n# api.lookup.get_access_keys()")
    result = api.lookup.get_access_keys()
    print(format_result(result))
    save("AccessKey.json", result)

    # GET /lookup/accessKey/{accessKey}
    print("\n# api.lookup.get_access_key(access_key=...)")
    result = api.lookup.get_access_key(
        access_key="3CD4E92F-6ADD-4C2B-8F36-79C58E6437E5",
    )
    print(format_result(result))
    save("AccessKeySetup.json", result)

    # GET /lookup/PPCCampaigns
    print("\n# api.lookup.get_ppc_campaigns()")
    result = api.lookup.get_ppc_campaigns()
    print(format_result(result))
    save("PPCCampaign.json", result)

    # GET /lookup/parcelPackageTypes
    print("\n# api.lookup.get_parcel_package_types()")
    result = api.lookup.get_parcel_package_types()
    print(format_result(result))
    save("ParcelPackageType.json", result)

    # GET /lookup/documentTypes
    print("\n# api.lookup.get_document_types()")
    result = api.lookup.get_document_types()
    print(format_result(result))
    save("DocumentTypeBySource.json", result)

    # GET /lookup/comonInsurance
    print("\n# api.lookup.get_common_insurance()")
    result = api.lookup.get_common_insurance()
    print(format_result(result))
    save("CommonInsuranceSlab.json", result)

    # GET /lookup/densityClassMap
    print("\n# api.lookup.get_density_class_map()")
    result = api.lookup.get_density_class_map()
    print(format_result(result))
    save("DensityClassEntry.json", result)

    # GET /lookup/referCategoryHeirachy
    print("\n# api.lookup.get_refer_category_hierarchy()")
    result = api.lookup.get_refer_category_hierarchy()
    print(format_result(result))
    save("LookupValue.json", result)

    # GET /lookup/{masterConstantKey}/{valueId}
    print("\n# api.lookup.get_by_key_and_id(key=..., value_id=...)")
    result = api.lookup.get_by_key_and_id(key="contactTypes", value_id="1")
    print(format_result(result))
    save("LookupValue.json", result)

    # GET /lookup/resetMasterConstantCache — no response model; nothing to diff.
    print("\n# api.lookup.reset_cache()")
    result = api.lookup.reset_cache()
    print(format_result(result))
    print("  (reset_cache has no response model — fixture save skipped)")


if __name__ == "__main__":
    main()
