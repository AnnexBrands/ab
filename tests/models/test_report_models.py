"""Fixture validation tests for Report models."""

from ab.api.models.reports import (
    InsuranceReport,
    ReferredByReport,
    RevenueCustomer,
    SalesForecastReport,
    SalesForecastSummary,
    Web2LeadReport,
)
from tests.conftest import assert_no_extra_fields, require_fixture


class TestReportModels:
    def test_insurance_report(self):
        data = require_fixture("InsuranceReport", "POST", "/reports/insurance")
        model = InsuranceReport.model_validate(data)
        assert isinstance(model, InsuranceReport)
        assert_no_extra_fields(model)

    def test_sales_forecast_report(self):
        data = require_fixture("SalesForecastReport", "POST", "/reports/sales")
        model = SalesForecastReport.model_validate(data)
        assert isinstance(model, SalesForecastReport)
        assert_no_extra_fields(model)

    def test_sales_forecast_summary(self):
        data = require_fixture("SalesForecastSummary", "POST", "/reports/sales/summary")
        model = SalesForecastSummary.model_validate(data)
        assert isinstance(model, SalesForecastSummary)
        assert_no_extra_fields(model)

    def test_revenue_customer(self):
        data = require_fixture("RevenueCustomer", "POST", "/reports/topRevenueCustomers")
        model = RevenueCustomer.model_validate(data)
        assert isinstance(model, RevenueCustomer)
        assert_no_extra_fields(model)

    def test_referred_by_report(self):
        data = require_fixture("ReferredByReport", "POST", "/reports/referredBy")
        model = ReferredByReport.model_validate(data)
        assert isinstance(model, ReferredByReport)
        assert_no_extra_fields(model)

    def test_web2lead_report(self):
        data = require_fixture("Web2LeadReport", "POST", "/reports/web2Lead")
        model = Web2LeadReport.model_validate(data)
        assert isinstance(model, Web2LeadReport)
        assert_no_extra_fields(model)
