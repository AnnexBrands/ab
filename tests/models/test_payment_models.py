"""Fixture validation tests for Payment models."""

from tests.conftest import require_fixture

from ab.api.models.payments import ACHSessionResponse, PaymentInfo, PaymentSource


class TestPaymentModels:
    def test_payment_info(self):
        data = require_fixture("PaymentInfo", "GET", "/job/{id}/payment")
        model = PaymentInfo.model_validate(data)
        assert model.total_amount is not None
        assert model.payment_status is not None

    def test_payment_source(self):
        data = require_fixture("PaymentSource", "GET", "/job/{id}/payment/sources")
        model = PaymentSource.model_validate(data)
        assert model.source_id is not None
        assert model.type is not None

    def test_ach_session_response(self):
        data = require_fixture("ACHSessionResponse", "POST", "/job/{id}/payment/ACHPaymentSession")
        model = ACHSessionResponse.model_validate(data)
        assert model.session_id is not None
