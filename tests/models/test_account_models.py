"""Fixture validation tests for Account models (009)."""

from tests.conftest import require_fixture

from ab.api.models.account import (
    AccountPaymentSource,
    AccountResponse,
    TokenVerification,
    UserProfile,
)


class TestAccountModels:
    def test_account_response(self):
        data = require_fixture("AccountResponse", "POST", "/account/register")
        AccountResponse.model_validate(data)

    def test_token_verification(self):
        data = require_fixture("TokenVerification", "GET", "/account/verifyresettoken")
        TokenVerification.model_validate(data)

    def test_user_profile(self):
        data = require_fixture("UserProfile", "GET", "/account/profile")
        UserProfile.model_validate(data)

    def test_payment_source(self):
        data = require_fixture("AccountPaymentSource", "PUT", "/account/paymentsource/{sourceId}")
        AccountPaymentSource.model_validate(data)
