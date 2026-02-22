"""Fixture validation tests for RFQ models."""

from ab.api.models.rfq import QuoteRequestDisplayInfo, QuoteRequestStatus
from tests.conftest import assert_no_extra_fields, require_fixture


class TestRFQModels:
    def test_quote_request_display_info(self):
        data = require_fixture("QuoteRequestDisplayInfo", "GET", "/rfq/{rfqId}")
        model = QuoteRequestDisplayInfo.model_validate(data)
        assert isinstance(model, QuoteRequestDisplayInfo)
        assert_no_extra_fields(model)

    def test_quote_request_status(self):
        data = require_fixture("QuoteRequestStatus", "GET", "/job/{id}/rfq/statusof/{type}/forcompany/{id}")
        model = QuoteRequestStatus.model_validate(data)
        assert isinstance(model, QuoteRequestStatus)
        assert_no_extra_fields(model)
