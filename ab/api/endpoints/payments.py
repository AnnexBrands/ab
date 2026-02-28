"""Payments API endpoints — ACPortal.

Covers payment info, payment sources, ACH operations, and pay-by-source.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ab.api.models.payments import ACHSessionResponse, PaymentInfo, PaymentSource
    from ab.api.models.shared import ServiceBaseResponse

from ab.api.base import BaseEndpoint
from ab.api.route import Route

# Payment routes
_GET_PAYMENT = Route("GET", "/job/{jobDisplayId}/payment", params_model="PaymentParams", response_model="PaymentInfo")
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

    def get(self, job_display_id: int) -> PaymentInfo:
        """GET /job/{jobDisplayId}/payment (ACPortal)"""
        return self._request(_GET_PAYMENT.bind(jobDisplayId=job_display_id))

    def get_create(self, job_display_id: int) -> PaymentInfo:
        """GET /job/{jobDisplayId}/payment/create (ACPortal)"""
        return self._request(_GET_PAYMENT_CREATE.bind(jobDisplayId=job_display_id))

    def get_sources(self, job_display_id: int) -> list[PaymentSource]:
        """GET /job/{jobDisplayId}/payment/sources (ACPortal)"""
        return self._request(_GET_SOURCES.bind(jobDisplayId=job_display_id))

    def pay_by_source(
        self,
        job_display_id: int,
        *,
        source_id: str | None = None,
        amount: float | None = None,
    ) -> ServiceBaseResponse:
        """POST /job/{jobDisplayId}/payment/bysource.

        Args:
            job_display_id: Job display ID.
            source_id: Payment source to charge.
            amount: Amount (or full balance).

        Request model: :class:`PayBySourceRequest`
        """
        body = dict(source_id=source_id, amount=amount)
        return self._request(_PAY_BY_SOURCE.bind(jobDisplayId=job_display_id), json=body)

    def create_ach_session(
        self,
        job_display_id: int,
        *,
        return_url: str | None = None,
    ) -> ACHSessionResponse:
        """POST /job/{jobDisplayId}/payment/ACHPaymentSession.

        Args:
            job_display_id: Job display ID.
            return_url: Redirect after session.

        Request model: :class:`ACHSessionRequest`
        """
        body = dict(return_url=return_url)
        return self._request(_ACH_SESSION.bind(jobDisplayId=job_display_id), json=body)

    def ach_credit_transfer(
        self,
        job_display_id: int,
        *,
        amount: float | None = None,
    ) -> ServiceBaseResponse:
        """POST /job/{jobDisplayId}/payment/ACHCreditTransfer.

        Args:
            job_display_id: Job display ID.
            amount: Transfer amount.

        Request model: :class:`ACHCreditTransferRequest`
        """
        body = dict(amount=amount)
        return self._request(_ACH_CREDIT_TRANSFER.bind(jobDisplayId=job_display_id), json=body)

    def attach_customer_bank(
        self,
        job_display_id: int,
        *,
        token: str | None = None,
    ) -> ServiceBaseResponse:
        """POST /job/{jobDisplayId}/payment/attachCustomerBank.

        Args:
            job_display_id: Job display ID.
            token: Bank account token.

        Request model: :class:`AttachBankRequest`
        """
        body = dict(token=token)
        return self._request(_ATTACH_BANK.bind(jobDisplayId=job_display_id), json=body)

    def verify_ach_source(
        self,
        job_display_id: int,
        *,
        amounts: list[int] | None = None,
    ) -> ServiceBaseResponse:
        """POST /job/{jobDisplayId}/payment/verifyJobACHSource.

        Args:
            job_display_id: Job display ID.
            amounts: Micro-deposit verification amounts.

        Request model: :class:`VerifyACHRequest`
        """
        body = dict(amounts=amounts)
        return self._request(_VERIFY_ACH.bind(jobDisplayId=job_display_id), json=body)

    def cancel_ach_verification(self, job_display_id: int) -> ServiceBaseResponse:
        """POST /job/{jobDisplayId}/payment/cancelJobACHVerification (ACPortal)"""
        return self._request(_CANCEL_ACH.bind(jobDisplayId=job_display_id))

    def set_bank_source(
        self,
        job_display_id: int,
        *,
        source_id: str | None = None,
    ) -> ServiceBaseResponse:
        """POST /job/{jobDisplayId}/payment/banksource.

        Args:
            job_display_id: Job display ID.
            source_id: Bank source ID.

        Request model: :class:`BankSourceRequest`
        """
        body = dict(source_id=source_id)
        return self._request(_BANK_SOURCE.bind(jobDisplayId=job_display_id), json=body)
