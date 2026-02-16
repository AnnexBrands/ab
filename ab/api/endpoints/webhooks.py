"""Webhooks API endpoints (6 routes).

Covers Stripe and Twilio webhook handlers under /api/webhooks/.

Note: These are server-side callback receivers. Stripe/Twilio call these
endpoints on the ACPortal server. Calling them from the SDK is primarily
useful for testing scenarios.
"""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

# Stripe (3)
_STRIPE_HANDLE = Route("POST", "/webhooks/stripe/handle")
_STRIPE_CONNECT = Route("POST", "/webhooks/stripe/connect/handle")
_STRIPE_CHECKOUT = Route("POST", "/webhooks/stripe/checkout.session.completed")

# Twilio (3)
_TWILIO_BODY_SMS = Route("POST", "/webhooks/twilio/body-sms-inbound")
_TWILIO_FORM_SMS = Route("POST", "/webhooks/twilio/form-sms-inbound")
_TWILIO_STATUS = Route("POST", "/webhooks/twilio/smsStatusCallback")


class WebhooksEndpoint(BaseEndpoint):
    """Webhook handlers (ACPortal API).

    These are server-side callback receivers — Stripe and Twilio call
    these endpoints on the ACPortal server. SDK access is for testing only.
    """

    # ---- Stripe -------------------------------------------------------------

    def stripe_handle(self, **kwargs: Any) -> Any:
        """POST /webhooks/stripe/handle"""
        return self._request(_STRIPE_HANDLE, json=kwargs or None)

    def stripe_connect_handle(self, **kwargs: Any) -> Any:
        """POST /webhooks/stripe/connect/handle"""
        return self._request(_STRIPE_CONNECT, json=kwargs or None)

    def stripe_checkout_completed(self, **kwargs: Any) -> Any:
        """POST /webhooks/stripe/checkout.session.completed"""
        return self._request(_STRIPE_CHECKOUT, json=kwargs or None)

    # ---- Twilio -------------------------------------------------------------

    def twilio_body_sms_inbound(self, **kwargs: Any) -> Any:
        """POST /webhooks/twilio/body-sms-inbound"""
        return self._request(_TWILIO_BODY_SMS, json=kwargs or None)

    def twilio_form_sms_inbound(self, **kwargs: Any) -> Any:
        """POST /webhooks/twilio/form-sms-inbound"""
        return self._request(_TWILIO_FORM_SMS, json=kwargs or None)

    def twilio_sms_status_callback(self, **kwargs: Any) -> Any:
        """POST /webhooks/twilio/smsStatusCallback"""
        return self._request(_TWILIO_STATUS, json=kwargs or None)
