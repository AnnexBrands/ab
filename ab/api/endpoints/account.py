"""Account API endpoints (10 routes).

Covers registration, confirmation, password management,
profile, and payment source under /api/account/.
"""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_POST_REGISTER = Route("POST", "/account/register", request_model="RegisterRequest", response_model="AccountResponse")
_POST_SEND_CONFIRMATION = Route("POST", "/account/sendConfirmation", request_model="SendConfirmationRequest")
_POST_CONFIRM = Route("POST", "/account/confirm", request_model="ConfirmRequest")
_POST_FORGOT = Route("POST", "/account/forgot", request_model="ForgotRequest")
_GET_VERIFY_RESET_TOKEN = Route("GET", "/account/verifyresettoken", response_model="TokenVerification")
_POST_RESET_PASSWORD = Route("POST", "/account/resetpassword", request_model="ResetPasswordRequest")
_POST_SET_PASSWORD = Route("POST", "/account/setpassword", request_model="SetPasswordRequest")
_GET_PROFILE = Route("GET", "/account/profile", response_model="UserProfile")
_PUT_PAYMENT_SOURCE = Route("PUT", "/account/paymentsource/{sourceId}", request_model="PaymentSourceRequest", response_model="AccountPaymentSource")
_DELETE_PAYMENT_SOURCE = Route("DELETE", "/account/paymentsource/{sourceId}")


class AccountEndpoint(BaseEndpoint):
    """Account operations (ACPortal API).

    Manages registration, email confirmation, password reset/set,
    user profile, and payment sources.
    """

    def register(self, **kwargs: Any) -> Any:
        """POST /account/register"""
        return self._request(_POST_REGISTER, json=kwargs)

    def send_confirmation(self, **kwargs: Any) -> Any:
        """POST /account/sendConfirmation"""
        return self._request(_POST_SEND_CONFIRMATION, json=kwargs)

    def confirm(self, **kwargs: Any) -> Any:
        """POST /account/confirm"""
        return self._request(_POST_CONFIRM, json=kwargs)

    def forgot(self, **kwargs: Any) -> Any:
        """POST /account/forgot"""
        return self._request(_POST_FORGOT, json=kwargs)

    def verify_reset_token(self, **params: Any) -> Any:
        """GET /account/verifyresettoken — query params: username, token."""
        return self._request(_GET_VERIFY_RESET_TOKEN, params=params)

    def reset_password(self, **kwargs: Any) -> Any:
        """POST /account/resetpassword"""
        return self._request(_POST_RESET_PASSWORD, json=kwargs)

    def set_password(self, **kwargs: Any) -> Any:
        """POST /account/setpassword"""
        return self._request(_POST_SET_PASSWORD, json=kwargs)

    def get_profile(self) -> Any:
        """GET /account/profile"""
        return self._request(_GET_PROFILE)

    def update_payment_source(self, source_id: str, **kwargs: Any) -> Any:
        """PUT /account/paymentsource/{sourceId}"""
        return self._request(_PUT_PAYMENT_SOURCE.bind(sourceId=source_id), json=kwargs)

    def delete_payment_source(self, source_id: str) -> Any:
        """DELETE /account/paymentsource/{sourceId}"""
        return self._request(_DELETE_PAYMENT_SOURCE.bind(sourceId=source_id))
