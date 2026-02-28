"""RFQ models for the ACPortal API."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class RfqForJobParams(RequestModel):
    """Query parameters for GET /rfq/forjob/{jobId}."""

    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID filter")


class RfqAcceptWinnerParams(RequestModel):
    """Query parameters for POST /rfq/{rfqId}/acceptwinner."""

    final_amount: Optional[float] = Field(None, alias="finalAmount", description="Final accepted amount")


class QuoteRequestDisplayInfo(ResponseModel):
    """RFQ listing entry — GET /rfq/{rfqId} and GET /job/{jobDisplayId}/rfq."""

    rfq_id: Optional[str] = Field(None, alias="rfqId", description="RFQ ID")
    provider_company_id: Optional[str] = Field(None, alias="providerCompanyId", description="Provider company UUID")
    service_type: Optional[str] = Field(None, alias="serviceType", description="Service type")
    quoted_price: Optional[float] = Field(None, alias="quotedPrice", description="Quoted price")
    transit_days: Optional[int] = Field(None, alias="transitDays", description="Transit days")
    status: Optional[str] = Field(None, description="RFQ status")
    provider_company_name: Optional[str] = Field(None, alias="providerCompanyName", description="Provider company name")
    is_winner: Optional[bool] = Field(None, alias="isWinner", description="Whether this quote won")
    comments: Optional[str] = Field(None, description="Comments")


class QuoteRequestStatus(ResponseModel):
    """RFQ status for a service/company combo — GET /job/{id}/rfq/statusof/..."""

    status: Optional[str] = Field(None, description="RFQ status")
    rfq_id: Optional[str] = Field(None, alias="rfqId", description="RFQ ID")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Whether RFQ is active")


class AcceptModel(RequestModel):
    """Body for POST /rfq/{rfqId}/accept and POST /rfq/{rfqId}/comment."""

    notes: Optional[str] = Field(None, description="Acceptance notes or comment text")
