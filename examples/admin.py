"""Example: Admin operations (13 endpoints)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Admin", env="staging")

# ── Advanced Settings ────────────────────────────────────────────────

runner.add(
    "get_advanced_settings",
    lambda api: api.admin.get_advanced_settings(),
    response_model="List[AdvancedSetting]",
    fixture_file="AdvancedSetting.json",
)

# ── Carrier Error Messages ───────────────────────────────────────────

runner.add(
    "get_carrier_error_messages",
    lambda api: api.admin.get_carrier_error_messages(),
    response_model="List[CarrierErrorMessage]",
    fixture_file="CarrierErrorMessage.json",
)

# ── Global Settings ──────────────────────────────────────────────────

runner.add(
    "get_company_hierarchy",
    lambda api: api.admin.get_company_hierarchy(),
    response_model="CompanyHierarchy",
    fixture_file="CompanyHierarchy.json",
)

runner.add(
    "get_insurance_exceptions",
    lambda api: api.admin.get_insurance_exceptions(),
    response_model="List[InsuranceException]",
    fixture_file="InsuranceException.json",
)

runner.add(
    "save_intacct_settings",
    lambda api: api.admin.save_intacct_settings(
        # TODO: capture fixture — needs valid IntacctSettingsRequest kwargs
    ),
    request_model="IntacctSettingsRequest",
    response_model="IntacctSettings",
)

if __name__ == "__main__":
    runner.run()
