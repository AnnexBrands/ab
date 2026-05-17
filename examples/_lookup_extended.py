"""Example: Extended lookup operations (12 methods).

Covers generic get_by_key, named convenience methods (access keys, PPC
campaigns, parcel package types, document types, insurance, density class,
refer categories), and cache reset.
"""

from examples._runner import ExampleRunner

runner = ExampleRunner("Extended Lookup", env="staging")

# ═══════════════════════════════════════════════════════════════════════
# Generic Lookup
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "get_by_key",
    lambda api: api.lookup.get_by_key("contactTypes"),
    response_model="List[LookupValue]",
    fixture_file="LookupValue.json",
)

runner.add(
    "get_by_key_and_id",
    lambda api: api.lookup.get_by_key_and_id("contactTypes", "1"),
    response_model="LookupValue",
    fixture_file="LookupValue.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Named Convenience Methods
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "get_access_keys",
    lambda api: api.lookup.get_access_keys(),
    response_model="List[AccessKey]",
    fixture_file="AccessKey.json",
)

runner.add(
    "get_access_key",
    lambda api: api.lookup.get_access_key("someKey"),
    response_model="AccessKey",
    fixture_file="AccessKey.json",
)

runner.add(
    "get_ppc_campaigns",
    lambda api: api.lookup.get_ppc_campaigns(),
    response_model="List[LookupValue]",
    fixture_file="LookupValue.json",
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
    response_model="List[LookupValue]",
    fixture_file="LookupValue.json",
)

runner.add(
    "get_common_insurance",
    lambda api: api.lookup.get_common_insurance(),
    response_model="List[LookupValue]",
    fixture_file="LookupValue.json",
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

runner.add(
    "reset_cache",
    lambda api: api.lookup.reset_cache(),
)

if __name__ == "__main__":
    runner.run()
