"""DEPRECATED: ``api.payments`` is being phased out.

All payment operations now live at
:class:`~ab.api.endpoints.jobs.payment.JobPaymentEndpoint`, reached as
``api.jobs.payment``. This module is retained only as a thin deprecation
shim: every method emits a :class:`DeprecationWarning` and forwards the
call. Method names are unchanged.
"""

from __future__ import annotations

import warnings
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
from ab.api.endpoints.jobs.payment import JobPaymentEndpoint


def _deprecated(method: str) -> None:
    warnings.warn(
        f"api.payments.{method}() is deprecated; use api.jobs.payment.{method}() instead.",
        DeprecationWarning,
        stacklevel=3,
    )


class PaymentsEndpoint(BaseEndpoint):
    """Deprecated shim — every method forwards to ``api.jobs.payment``."""

    def __init__(self, client) -> None:
        super().__init__(client)
        self._payment = JobPaymentEndpoint(client)

    def get(self, job_display_id: int) -> PaymentInfo:
        _deprecated("get")
        return self._payment.get(job_display_id)

    def get_create(self, job_display_id: int) -> PaymentInfo:
        _deprecated("get_create")
        return self._payment.get_create(job_display_id)

    def get_sources(self, job_display_id: int) -> list[PaymentSource]:
        _deprecated("get_sources")
        return self._payment.get_sources(job_display_id)

    def pay_by_source(self, job_display_id: int, *, data: PayBySourceRequest | dict) -> ServiceBaseResponse:
        _deprecated("pay_by_source")
        return self._payment.pay_by_source(job_display_id, data=data)

    def create_ach_session(self, job_display_id: int, *, data: ACHSessionRequest | dict) -> ACHSessionResponse:
        _deprecated("create_ach_session")
        return self._payment.create_ach_session(job_display_id, data=data)

    def ach_credit_transfer(
        self, job_display_id: int, *, data: ACHCreditTransferRequest | dict,
    ) -> ServiceBaseResponse:
        _deprecated("ach_credit_transfer")
        return self._payment.ach_credit_transfer(job_display_id, data=data)

    def attach_customer_bank(
        self, job_display_id: int, *, data: AttachBankRequest | dict,
    ) -> ServiceBaseResponse:
        _deprecated("attach_customer_bank")
        return self._payment.attach_customer_bank(job_display_id, data=data)

    def verify_ach_source(self, job_display_id: int, *, data: VerifyACHRequest | dict) -> ServiceBaseResponse:
        _deprecated("verify_ach_source")
        return self._payment.verify_ach_source(job_display_id, data=data)

    def cancel_ach_verification(self, job_display_id: int) -> ServiceBaseResponse:
        _deprecated("cancel_ach_verification")
        return self._payment.cancel_ach_verification(job_display_id)

    def set_bank_source(self, job_display_id: int, *, data: BankSourceRequest | dict) -> ServiceBaseResponse:
        _deprecated("set_bank_source")
        return self._payment.set_bank_source(job_display_id, data=data)
