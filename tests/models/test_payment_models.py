"""Fixture validation tests for Payment models."""

from ab.api.models.payments import ACHSessionResponse, PaymentInfo, PaymentSource
from tests.conftest import assert_no_extra_fields, require_fixture


class TestPaymentModels:
    def test_payment_info(self):
        data = require_fixture("PaymentInfo", "GET", "/job/{id}/payment")
        model = PaymentInfo.model_validate(data)
        assert isinstance(model, PaymentInfo)
        assert_no_extra_fields(model)

    def test_payment_source(self):
        data = require_fixture("PaymentSource", "GET", "/job/{id}/payment/sources")
        model = PaymentSource.model_validate(data)
        assert isinstance(model, PaymentSource)
        assert_no_extra_fields(model)

    def test_ach_session_response(self):
        data = require_fixture("ACHSessionResponse", "POST", "/job/{id}/payment/ACHPaymentSession")
        model = ACHSessionResponse.model_validate(data)
        assert isinstance(model, ACHSessionResponse)
        assert_no_extra_fields(model)
