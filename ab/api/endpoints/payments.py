"""Payments API endpoints — ACPortal.

Covers payment info, payment sources, ACH operations, and pay-by-source.
"""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

# Payment routes
_GET_PAYMENT = Route("GET", "/job/{jobDisplayId}/payment", response_model="PaymentInfo")
_GET_PAYMENT_CREATE = Route("GET", "/job/{jobDisplayId}/payment/create", response_model="PaymentInfo")
_GET_SOURCES = Route("GET", "/job/{jobDisplayId}/payment/sources", response_model="List[PaymentSource]")
_PAY_BY_SOURCE = Route(
    "POST", "/job/{jobDisplayId}/payment/bysource",
    request_model="PayBySourceRequest", response_model="ServiceBaseResponse",
)
_ACH_SESSION = Route(
    "POST", "/job/{jobDisplayId}/payment/ACHPaymentSession",
    request_model="ACHSessionRequest", response_model="ACHSessionResponse",
)
_ACH_CREDIT_TRANSFER = Route(
    "POST", "/job/{jobDisplayId}/payment/ACHCreditTransfer",
    request_model="ACHCreditTransferRequest", response_model="ServiceBaseResponse",
)
_ATTACH_BANK = Route(
    "POST", "/job/{jobDisplayId}/payment/attachCustomerBank",
    request_model="AttachBankRequest", response_model="ServiceBaseResponse",
)
_VERIFY_ACH = Route(
    "POST", "/job/{jobDisplayId}/payment/verifyJobACHSource",
    request_model="VerifyACHRequest", response_model="ServiceBaseResponse",
)
_CANCEL_ACH = Route(
    "POST", "/job/{jobDisplayId}/payment/cancelJobACHVerification",
    response_model="ServiceBaseResponse",
)
_BANK_SOURCE = Route(
    "POST", "/job/{jobDisplayId}/payment/banksource",
    request_model="BankSourceRequest", response_model="ServiceBaseResponse",
)


class PaymentsEndpoint(BaseEndpoint):
    """Payment operations (ACPortal API)."""

    def get(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/payment (ACPortal)"""
        return self._request(_GET_PAYMENT.bind(jobDisplayId=job_display_id))

    def get_create(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/payment/create (ACPortal)"""
        return self._request(_GET_PAYMENT_CREATE.bind(jobDisplayId=job_display_id))

    def get_sources(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/payment/sources (ACPortal)"""
        return self._request(_GET_SOURCES.bind(jobDisplayId=job_display_id))

    def pay_by_source(self, job_display_id: int, data: dict | Any) -> Any:
        """POST /job/{jobDisplayId}/payment/bysource (ACPortal)"""
        return self._request(_PAY_BY_SOURCE.bind(jobDisplayId=job_display_id), json=data)

    def create_ach_session(self, job_display_id: int, data: dict | Any) -> Any:
        """POST /job/{jobDisplayId}/payment/ACHPaymentSession (ACPortal)"""
        return self._request(_ACH_SESSION.bind(jobDisplayId=job_display_id), json=data)

    def ach_credit_transfer(self, job_display_id: int, data: dict | Any) -> Any:
        """POST /job/{jobDisplayId}/payment/ACHCreditTransfer (ACPortal)"""
        return self._request(_ACH_CREDIT_TRANSFER.bind(jobDisplayId=job_display_id), json=data)

    def attach_customer_bank(self, job_display_id: int, data: dict | Any) -> Any:
        """POST /job/{jobDisplayId}/payment/attachCustomerBank (ACPortal)"""
        return self._request(_ATTACH_BANK.bind(jobDisplayId=job_display_id), json=data)

    def verify_ach_source(self, job_display_id: int, data: dict | Any) -> Any:
        """POST /job/{jobDisplayId}/payment/verifyJobACHSource (ACPortal)"""
        return self._request(_VERIFY_ACH.bind(jobDisplayId=job_display_id), json=data)

    def cancel_ach_verification(self, job_display_id: int) -> Any:
        """POST /job/{jobDisplayId}/payment/cancelJobACHVerification (ACPortal)"""
        return self._request(_CANCEL_ACH.bind(jobDisplayId=job_display_id))

    def set_bank_source(self, job_display_id: int, data: dict | Any) -> Any:
        """POST /job/{jobDisplayId}/payment/banksource (ACPortal)"""
        return self._request(_BANK_SOURCE.bind(jobDisplayId=job_display_id), json=data)
