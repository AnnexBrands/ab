"""Fixture validation tests for AutoPrice models."""

import pytest

from ab.api.models.autoprice import QuickQuoteResponse, QuoteRequestResponse
from tests.conftest import assert_no_extra_fields, require_fixture


class TestAutoPriceModels:
    @pytest.mark.live
    def test_quick_quote_response(self):
        data = require_fixture("QuickQuoteResponse", "POST", "/AutoPrice/QuickQuote", required=True)
        model = QuickQuoteResponse.model_validate(data)
        assert isinstance(model, QuickQuoteResponse)
        assert_no_extra_fields(model)

    def test_quote_request_response(self):
        data = require_fixture("QuoteRequestResponse", "POST", "/AutoPrice/QuoteRequest")
        model = QuoteRequestResponse.model_validate(data)
        assert isinstance(model, QuoteRequestResponse)
        assert_no_extra_fields(model)
