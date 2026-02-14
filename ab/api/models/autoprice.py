"""AutoPrice models for the ABC API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class QuickQuoteResponse(ResponseModel):
    """Response from POST /autoprice/quickquote."""

    quotes: Optional[List[dict]] = Field(None, description="Quote results")
    errors: Optional[List[dict]] = Field(None, description="Errors encountered")


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
