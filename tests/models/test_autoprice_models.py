"""Fixture validation tests for AutoPrice models (T065)."""

import pytest

from tests.conftest import load_fixture

from ab.api.models.autoprice import QuickQuoteResponse, QuoteRequestResponse


class TestAutoPriceModels:
    @pytest.mark.mock
    def test_quick_quote_response(self):
        data = load_fixture("QuickQuoteResponse")
        model = QuickQuoteResponse.model_validate(data)

    @pytest.mark.mock
    def test_quote_request_response(self):
        data = load_fixture("QuoteRequestResponse")
        model = QuoteRequestResponse.model_validate(data)
