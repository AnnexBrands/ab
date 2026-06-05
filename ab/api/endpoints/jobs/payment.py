"""Job-scoped payment operations — swagger tag ``JobPayment`` (10 routes).

Exposed as ``api.jobs.payment``. All routes were moved here from the
legacy ``api.payments`` endpoint group, which now exists as a thin
deprecation shim (:class:`~ab.api.endpoints.payments.PaymentsEndpoint`)
that forwards every call.

Method names are unchanged from the legacy ``api.payments.*`` surface.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.payments import (
        ACHCreditTransferRequest,
        ACHSessionRequest,
        ACHSessionResponse,
        AttachBankRequest,
        BankSourceRequest,
        PayBySourceRequest,
        PaymentInfo,
        PaymentSource,
        VerifyACHRequest,
    )
    from ab.api.models.shared import ServiceBaseResponse

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET = Route("GET", "/job/{jobDisplayId}/payment", params_model="PaymentParams", response_model="PaymentInfo")
_GET_CREATE = Route("GET", "/job/{jobDisplayId}/payment/create", response_model="PaymentInfo")
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


class JobPaymentEndpoint(BaseEndpoint):
    """Job-scoped payment operations (ACPortal API)."""

    def get(self, job_display_id: int) -> PaymentInfo:
        """``GET /job/{jobDisplayId}/payment``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/payment.get.html
        Query params: PaymentParams
        Response model: PaymentInfo
        """
        return self._request(_GET.bind(jobDisplayId=job_display_id))

    def get_create(self, job_display_id: int) -> PaymentInfo:
        """``GET /job/{jobDisplayId}/payment/create``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/payment.get_create.html
        Response model: PaymentInfo
        """
        return self._request(_GET_CREATE.bind(jobDisplayId=job_display_id))

    def get_sources(self, job_display_id: int) -> list[PaymentSource]:
        """``GET /job/{jobDisplayId}/payment/sources``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/payment.get_sources.html
        Response model: List[PaymentSource]
        """
        return self._request(_GET_SOURCES.bind(jobDisplayId=job_display_id))

    def pay_by_source(
        self,
        job_display_id: int,
        *,
        data: PayBySourceRequest | dict,
    ) -> ServiceBaseResponse:
        """``POST /job/{jobDisplayId}/payment/bysource``

        Request model: :class:`PayBySourceRequest`.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/payment.pay_by_source.html
        Request model: PayBySourceRequest
        Response model: ServiceBaseResponse
        """
        return self._request(_PAY_BY_SOURCE.bind(jobDisplayId=job_display_id), json=data)

    def create_ach_session(
        self,
        job_display_id: int,
        *,
        data: ACHSessionRequest | dict,
    ) -> ACHSessionResponse:
        """``POST /job/{jobDisplayId}/payment/ACHPaymentSession``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/payment.create_ach_session.html
        Request model: ACHSessionRequest
        Response model: ACHSessionResponse
        """
        return self._request(_ACH_SESSION.bind(jobDisplayId=job_display_id), json=data)

    def ach_credit_transfer(
        self,
        job_display_id: int,
        *,
        data: ACHCreditTransferRequest | dict,
    ) -> ServiceBaseResponse:
        """``POST /job/{jobDisplayId}/payment/ACHCreditTransfer``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/payment.ach_credit_transfer.html
        Request model: ACHCreditTransferRequest
        Response model: ServiceBaseResponse
        """
        return self._request(_ACH_CREDIT_TRANSFER.bind(jobDisplayId=job_display_id), json=data)

    def attach_customer_bank(
        self,
        job_display_id: int,
        *,
        data: AttachBankRequest | dict,
    ) -> ServiceBaseResponse:
        """``POST /job/{jobDisplayId}/payment/attachCustomerBank``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/payment.attach_customer_bank.html
        Request model: AttachBankRequest
        Response model: ServiceBaseResponse
        """
        return self._request(_ATTACH_BANK.bind(jobDisplayId=job_display_id), json=data)

    def verify_ach_source(
        self,
        job_display_id: int,
        *,
        data: VerifyACHRequest | dict,
    ) -> ServiceBaseResponse:
        """``POST /job/{jobDisplayId}/payment/verifyJobACHSource``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/payment.verify_ach_source.html
        Request model: VerifyACHRequest
        Response model: ServiceBaseResponse
        """
        return self._request(_VERIFY_ACH.bind(jobDisplayId=job_display_id), json=data)

    def cancel_ach_verification(self, job_display_id: int) -> ServiceBaseResponse:
        """``POST /job/{jobDisplayId}/payment/cancelJobACHVerification``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/payment.cancel_ach_verification.html
        Response model: ServiceBaseResponse
        """
        return self._request(_CANCEL_ACH.bind(jobDisplayId=job_display_id))

    def set_bank_source(
        self,
        job_display_id: int,
        *,
        data: BankSourceRequest | dict,
    ) -> ServiceBaseResponse:
        """``POST /job/{jobDisplayId}/payment/banksource``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/payment.set_bank_source.html
        Request model: BankSourceRequest
        Response model: ServiceBaseResponse
        """
        return self._request(_BANK_SOURCE.bind(jobDisplayId=job_display_id), json=data)
