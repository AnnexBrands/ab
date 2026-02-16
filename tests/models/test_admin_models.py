"""Fixture validation tests for Admin models (009)."""

from tests.conftest import require_fixture

from ab.api.models.admin import (
    AdvancedSetting,
    CarrierErrorMessage,
    CompanyHierarchy,
    InsuranceException,
    IntacctSettings,
)


class TestAdminModels:
    def test_advanced_setting(self):
        data = require_fixture("AdvancedSetting", "GET", "/admin/advancedsettings/all")
        AdvancedSetting.model_validate(data)

    def test_carrier_error_message(self):
        data = require_fixture("CarrierErrorMessage", "GET", "/admin/carriererrormessage/all")
        CarrierErrorMessage.model_validate(data)

    def test_company_hierarchy(self):
        data = require_fixture("CompanyHierarchy", "GET", "/admin/globalsettings/companyhierarchy")
        CompanyHierarchy.model_validate(data)

    def test_insurance_exception(self):
        data = require_fixture("InsuranceException", "POST", "/admin/globalsettings/getinsuranceexceptions")
        InsuranceException.model_validate(data)

    def test_intacct_settings(self):
        data = require_fixture("IntacctSettings", "POST", "/admin/globalsettings/intacct")
        IntacctSettings.model_validate(data)
