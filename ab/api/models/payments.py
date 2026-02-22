"""Payment models for ACPortal API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class PaymentParams(RequestModel):
    """Query parameters for GET /job/{jobDisplayId}/payment."""

    job_sub_key: Optional[str] = Field(None, alias="jobSubKey")


class PaymentInfo(ResponseModel):
    """Payment state for a job — GET /job/{jobDisplayId}/payment."""

    total_amount: Optional[float] = Field(None, alias="totalAmount", description="Job total")
    balance_due: Optional[float] = Field(None, alias="balanceDue", description="Remaining balance")
    payment_status: Optional[str] = Field(None, alias="paymentStatus", description="Current status")
    payments: Optional[List[dict]] = Field(None, description="Payment history")


class PaymentSource(ResponseModel):
    """Stored payment method — GET /job/{jobDisplayId}/payment/sources."""

    source_id: Optional[str] = Field(None, alias="sourceId", description="Payment source ID")
    type: Optional[str] = Field(None, description="card or bank_account")
    last_four: Optional[str] = Field(None, alias="lastFour", description="Last 4 digits")
    brand: Optional[str] = Field(None, description="Card brand (Visa, etc.)")
    is_default: Optional[bool] = Field(None, alias="isDefault", description="Default source flag")


class ACHSessionResponse(ResponseModel):
    """ACH payment session — POST /job/{jobDisplayId}/payment/ACHPaymentSession."""

    session_id: Optional[str] = Field(None, alias="sessionId", description="ACH session identifier")
    client_secret: Optional[str] = Field(None, alias="clientSecret", description="Stripe client secret")


class PayBySourceRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/payment/bysource."""

    source_id: str = Field(..., alias="sourceId", description="Payment source to charge")
    amount: Optional[float] = Field(None, description="Amount (or full balance)")


class ACHSessionRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/payment/ACHPaymentSession."""

    return_url: Optional[str] = Field(None, alias="returnUrl", description="Redirect after session")


class ACHCreditTransferRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/payment/ACHCreditTransfer."""

    amount: float = Field(..., description="Transfer amount")


class AttachBankRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/payment/attachCustomerBank."""

    token: str = Field(..., description="Bank account token")


class VerifyACHRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/payment/verifyJobACHSource."""

    amounts: List[int] = Field(..., description="Micro-deposit verification amounts")


class BankSourceRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/payment/banksource."""

    source_id: str = Field(..., alias="sourceId", description="Bank source ID")
