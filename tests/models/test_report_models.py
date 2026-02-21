"""Fixture validation tests for Report models."""

from ab.api.models.reports import (
    InsuranceReport,
    ReferredByReport,
    RevenueCustomer,
    SalesForecastReport,
    SalesForecastSummary,
    Web2LeadReport,
)
from tests.conftest import require_fixture


class TestReportModels:
    def test_insurance_report(self):
        data = require_fixture("InsuranceReport", "POST", "/reports/insurance")
        InsuranceReport.model_validate(data)

    def test_sales_forecast_report(self):
        data = require_fixture("SalesForecastReport", "POST", "/reports/sales")
        SalesForecastReport.model_validate(data)

    def test_sales_forecast_summary(self):
        data = require_fixture("SalesForecastSummary", "POST", "/reports/sales/summary")
        SalesForecastSummary.model_validate(data)

    def test_revenue_customer(self):
        data = require_fixture("RevenueCustomer", "POST", "/reports/topRevenueCustomers")
        RevenueCustomer.model_validate(data)

    def test_referred_by_report(self):
        data = require_fixture("ReferredByReport", "POST", "/reports/referredBy")
        ReferredByReport.model_validate(data)

    def test_web2lead_report(self):
        data = require_fixture("Web2LeadReport", "POST", "/reports/web2Lead")
        Web2LeadReport.model_validate(data)
