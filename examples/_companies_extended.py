"""Example: Extended company operations (16 methods).

Covers brands, geo settings, carrier accounts, and packaging settings.
"""

from examples._runner import ExampleRunner

runner = ExampleRunner("Extended Companies", env="staging")

TEST_COMPANY_ID = "PLACEHOLDER"

# ═══════════════════════════════════════════════════════════════════════
# Brands
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "get_brands",
    lambda api: api.companies.get_brands(),
    response_model="List[CompanyBrand]",
    fixture_file="CompanyBrand.json",
)

runner.add(
    "get_brands_tree",
    lambda api: api.companies.get_brands_tree(),
    response_model="List[BrandTree]",
    fixture_file="BrandTree.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Geo Settings
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "get_geo_area_companies",
    lambda api: api.companies.get_geo_area_companies(),
)

runner.add(
    "get_geo_settings",
    lambda api: api.companies.get_geo_settings(TEST_COMPANY_ID),
    response_model="GeoSettings",
    fixture_file="GeoSettings.json",
)

runner.add(
    "save_geo_settings",
    lambda api, data=None: api.companies.save_geo_settings(TEST_COMPANY_ID, data=data or {}),
    request_model="GeoSettingsSaveRequest",
    request_fixture_file="GeoSettingsSaveRequest.json",
)

runner.add(
    "get_global_geo_settings",
    lambda api: api.companies.get_global_geo_settings(),
    response_model="GeoSettings",
    fixture_file="GeoSettings.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Carrier Accounts
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "search_carrier_accounts",
    lambda api: api.companies.search_carrier_accounts(),
)

runner.add(
    "suggest_carriers",
    lambda api: api.companies.suggest_carriers(),
)

runner.add(
    "get_carrier_accounts",
    lambda api: api.companies.get_carrier_accounts(TEST_COMPANY_ID),
    response_model="List[CarrierAccount]",
    fixture_file="CarrierAccount.json",
)

runner.add(
    "save_carrier_accounts",
    lambda api, data=None: api.companies.save_carrier_accounts(TEST_COMPANY_ID, data=data or {}),
    request_model="CarrierAccountSaveRequest",
    request_fixture_file="CarrierAccountSaveRequest.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Packaging
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "get_packaging_settings",
    lambda api: api.companies.get_packaging_settings(TEST_COMPANY_ID),
    response_model="PackagingSettings",
    fixture_file="PackagingSettings.json",
)

runner.add(
    "save_packaging_settings",
    lambda api: api.companies.save_packaging_settings(TEST_COMPANY_ID, settings={}),
)

runner.add(
    "get_packaging_labor",
    lambda api: api.companies.get_packaging_labor(TEST_COMPANY_ID),
    response_model="PackagingLabor",
    fixture_file="PackagingLabor.json",
)

runner.add(
    "save_packaging_labor",
    lambda api: api.companies.save_packaging_labor(TEST_COMPANY_ID, laborRates=[]),
)

runner.add(
    "get_inherited_packaging_tariffs",
    lambda api: api.companies.get_inherited_packaging_tariffs(TEST_COMPANY_ID),
    response_model="List[PackagingTariff]",
    fixture_file="PackagingTariff.json",
)

runner.add(
    "get_inherited_packaging_labor",
    lambda api: api.companies.get_inherited_packaging_labor(TEST_COMPANY_ID),
    response_model="PackagingLabor",
    fixture_file="PackagingLabor.json",
)

if __name__ == "__main__":
    runner.run()
