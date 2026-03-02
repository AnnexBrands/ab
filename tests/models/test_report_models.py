"""Fixture validation tests for Report models."""

import pytest

from ab.api.models.reports import (
    InsuranceReport,
    ReferredByReport,
    RevenueCustomer,
    SalesForecastReport,
    SalesForecastSummary,
    Web2LeadReport,
)
from tests.conftest import assert_no_extra_fields, require_fixture


def _first_or_skip(data):
    """Return first element of a list fixture, or skip if empty."""
    if isinstance(data, list):
        if not data:
            pytest.skip("Fixture is an empty list — nothing to validate")
        return data[0]
    return data


class TestReportModels:
    def test_insurance_report(self):
        data = require_fixture("InsuranceReport", "POST", "/reports/insurance")
        item = _first_or_skip(data)
        model = InsuranceReport.model_validate(item)
        assert isinstance(model, InsuranceReport)
        assert_no_extra_fields(model)

    def test_sales_forecast_report(self):
        data = require_fixture("SalesForecastReport", "POST", "/reports/sales")
        item = _first_or_skip(data)
        model = SalesForecastReport.model_validate(item)
        assert isinstance(model, SalesForecastReport)
        assert_no_extra_fields(model)

    def test_sales_forecast_summary(self):
        data = require_fixture("SalesForecastSummary", "POST", "/reports/sales/summary")
        model = SalesForecastSummary.model_validate(data)
        assert isinstance(model, SalesForecastSummary)
        assert_no_extra_fields(model)

    def test_revenue_customer(self):
        data = require_fixture("RevenueCustomer", "POST", "/reports/topRevenueCustomers")
        item = _first_or_skip(data)
        model = RevenueCustomer.model_validate(item)
        assert isinstance(model, RevenueCustomer)
        assert_no_extra_fields(model)

    def test_referred_by_report(self):
        data = require_fixture("ReferredByReport", "POST", "/reports/referredBy")
        item = _first_or_skip(data)
        model = ReferredByReport.model_validate(item)
        assert isinstance(model, ReferredByReport)
        assert_no_extra_fields(model)

    def test_web2lead_report(self):
        data = require_fixture("Web2LeadReport", "POST", "/reports/web2Lead")
        item = _first_or_skip(data)
        model = Web2LeadReport.model_validate(item)
        assert isinstance(model, Web2LeadReport)
        assert_no_extra_fields(model)
