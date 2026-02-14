"""AutoPrice models for the ABC API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class QuickQuotePriceBreakdown(ResponseModel):
    """Price breakdown within a quick quote result."""

    pickup: Optional[float] = Field(None, alias="Pickup")
    packaging: Optional[float] = Field(None, alias="Packaging")
    transportation: Optional[float] = Field(None, alias="Transportation")
    insurance: Optional[float] = Field(None, alias="Insurance")
    delivery: Optional[float] = Field(None, alias="Delivery")
    miscellaneous: Optional[float] = Field(None, alias="Miscellaneous")


class QuickQuoteResult(ResponseModel):
    """Inner result from POST /autoprice/quickquote."""

    quote_certified: Optional[bool] = Field(None, alias="QuoteCertified")
    total_amount: Optional[float] = Field(None, alias="TotalAmount")
    warnings: Optional[List[str]] = Field(None, alias="Warnings")
    price_breakdown: Optional[QuickQuotePriceBreakdown] = Field(None, alias="PriceBreakdown")
    request_errors: Optional[List[str]] = Field(None, alias="RequestErrors")


class QuickQuoteResponse(ResponseModel):
    """Response from POST /autoprice/quickquote.

    Live API wraps the result under ``SubmitQuickQuoteRequestPOSTResult``.
    """

    result: Optional[QuickQuoteResult] = Field(
        None, alias="SubmitQuickQuoteRequestPOSTResult", description="Quote result"
    )


class QuoteRequestResponse(ResponseModel):
    """Response from POST /autoprice/v2/quoterequest."""

    quote_id: Optional[str] = Field(None, alias="quoteId", description="Quote request ID")
    status: Optional[str] = Field(None, description="Request status")
    results: Optional[List[dict]] = Field(None, description="Quote results")


class QuoteRequestModel(RequestModel):
    """Body for POST /autoprice/quickquote and /autoprice/v2/quoterequest."""

    job_info: Optional[dict] = Field(None, alias="jobInfo", description="Job/shipment details")
    contact_info: Optional[dict] = Field(None, alias="contactInfo", description="Contact details")
    service_info: Optional[dict] = Field(None, alias="serviceInfo", description="Service requirements")
    items: Optional[List[dict]] = Field(None, description="Items to quote")
