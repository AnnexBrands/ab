"""Example: Lookup operations (14 methods)."""

from examples._runner import ExampleRunner
from tests.constants import TEST_ITEM_ID, TEST_JOB_DISPLAY_ID, TEST_LOOKUP_KEY_SUB_MGMT

runner = ExampleRunner("Lookup", env="staging")

# ═══════════════════════════════════════════════════════════════════════
# Basic Lookups
# ═══════════════════════════════════════════════════════════════════════

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

runner.add(
    "get_items",
    lambda api: api.lookup.get_items(
        job_display_id=TEST_JOB_DISPLAY_ID,
        job_item_id=TEST_ITEM_ID,
    ),
    response_model="List[LookupItem]",
    fixture_file="LookupItem.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Extended Lookups
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "get_by_key",
    lambda api: api.lookup.get_by_key(TEST_LOOKUP_KEY_SUB_MGMT),
    response_model="List[LookupValue]",
    fixture_file="LookupValue.json",
)

runner.add(
    "get_access_keys",
    lambda api: api.lookup.get_access_keys(),
    response_model="List[AccessKey]",
    fixture_file="AccessKey.json",
)

runner.add(
    "get_access_key",
    lambda api: api.lookup.get_access_key("3CD4E92F-6ADD-4C2B-8F36-79C58E6437E5"),
    response_model="AccessKeySetup",
    fixture_file="AccessKeySetup.json",
)

runner.add(
    "get_ppc_campaigns",
    lambda api: api.lookup.get_ppc_campaigns(),
    response_model="List[PPCCampaign]",
    fixture_file="PPCCampaign.json",
)

runner.add(
    "get_parcel_package_types",
    lambda api: api.lookup.get_parcel_package_types(),
    response_model="List[ParcelPackageType]",
    fixture_file="ParcelPackageType.json",
)

runner.add(
    "get_document_types",
    lambda api: api.lookup.get_document_types(),
    response_model="List[DocumentTypeBySource]",
    fixture_file="DocumentTypeBySource.json",
)

runner.add(
    "get_common_insurance",
    lambda api: api.lookup.get_common_insurance(),
    response_model="List[CommonInsuranceSlab]",
    fixture_file="CommonInsuranceSlab.json",
)

runner.add(
    "get_density_class_map",
    lambda api: api.lookup.get_density_class_map(),
    response_model="List[DensityClassEntry]",
    fixture_file="DensityClassEntry.json",
)

runner.add(
    "get_refer_categories",
    lambda api: api.lookup.get_refer_categories(),
    response_model="List[LookupValue]",
    fixture_file="LookupValue.json",
)

runner.add(
    "get_refer_category_hierarchy",
    lambda api: api.lookup.get_refer_category_hierarchy(),
    response_model="List[LookupValue]",
    fixture_file="LookupValue.json",
)

if __name__ == "__main__":
    runner.run()
