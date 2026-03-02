"""RFQ models for the ACPortal API."""

from __future__ import annotations

from typing import List, Optional

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
    request_id: Optional[int] = Field(None, alias="requestId", description="Request record ID")
    job_id: Optional[str] = Field(None, alias="jobId", description="Job UUID")
    company_id: Optional[str] = Field(None, alias="companyId", description="Provider company UUID")
    provider_company_id: Optional[str] = Field(None, alias="providerCompanyId", description="Provider company UUID (legacy)")
    provider_company_name: Optional[str] = Field(None, alias="providerCompanyName", description="Provider company name")
    company_name: Optional[str] = Field(None, alias="companyName", description="Company display name")
    company_code: Optional[str] = Field(None, alias="companyCode", description="Company code")
    contact_name: Optional[str] = Field(None, alias="contactName", description="Contact name")
    contact_phone: Optional[str] = Field(None, alias="contactPhone", description="Contact phone")
    contact_email: Optional[str] = Field(None, alias="contactEmail", description="Contact email")
    service_type: Optional[str] = Field(None, alias="serviceType", description="Service type")
    type: Optional[int] = Field(None, description="RFQ type code")
    status: Optional[int] = Field(None, description="RFQ status code")
    quoted_price: Optional[float] = Field(None, alias="quotedPrice", description="Quoted price")
    requested_amount: Optional[float] = Field(None, alias="requestedAmount", description="Requested amount")
    agent_amount: Optional[float] = Field(None, alias="agentAmount", description="Agent amount")
    final_amount: Optional[float] = Field(None, alias="finalAmount", description="Final accepted amount")
    transit_days: Optional[int] = Field(None, alias="transitDays", description="Transit days")
    is_winner: Optional[bool] = Field(None, alias="isWinner", description="Whether this quote won")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Whether RFQ is active")
    agent_responded: Optional[bool] = Field(None, alias="agentResponded", description="Whether agent responded")
    dont_use: Optional[bool] = Field(None, alias="dontUse", description="Do not use flag")
    negotiable_price: Optional[bool] = Field(None, alias="negotiablePrice", description="Whether price is negotiable")
    expedited: Optional[bool] = Field(None, alias="expedited", description="Expedited service flag")
    notify_bidder: Optional[bool] = Field(None, alias="notifyBidder", description="Notify bidder flag")
    api_send_status: Optional[int] = Field(None, alias="apiSendStatus", description="API send status code")
    commercial_capabilities: Optional[int] = Field(None, alias="commercialCapabilities", description="Commercial capabilities bitmask")
    address: Optional[dict] = Field(None, description="Address details")
    miles: Optional[float] = Field(None, description="Distance in miles")
    comments: Optional[List[dict]] = Field(None, description="RFQ comment entries")
    message: Optional[str] = Field(None, description="RFQ message")
    due_date: Optional[str] = Field(None, alias="dueDate", description="Due date")
    sent_utc: Optional[str] = Field(None, alias="sentUtc", description="When RFQ was sent (UTC)")
    sent_by: Optional[str] = Field(None, alias="sentBy", description="Who sent the RFQ")
    job_service_start: Optional[str] = Field(None, alias="jobServiceStart", description="Job service start date")
    job_service_end: Optional[str] = Field(None, alias="jobServiceEnd", description="Job service end date")
    agent_amount_job_state: Optional[str] = Field(None, alias="agentAmountJobState", description="Agent amount job state")


class QuoteRequestStatus(ResponseModel):
    """RFQ status for a service/company combo — GET /job/{id}/rfq/statusof/..."""

    status: Optional[str] = Field(None, description="RFQ status")
    rfq_id: Optional[str] = Field(None, alias="rfqId", description="RFQ ID")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Whether RFQ is active")


class AcceptModel(RequestModel):
    """Body for POST /rfq/{rfqId}/accept and POST /rfq/{rfqId}/comment."""

    notes: Optional[str] = Field(None, description="Acceptance notes or comment text")
