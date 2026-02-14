"""Job models for ACPortal and ABC APIs."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel
from ab.api.models.mixins import FullAuditModel


class Job(ResponseModel, FullAuditModel):
    """Full job record — GET /job/{jobDisplayId}."""

    job_display_id: Optional[int] = Field(None, alias="jobDisplayId", description="Human-readable job ID")
    status: Optional[str] = Field(None, description="Job status")
    customer: Optional[dict] = Field(None, description="Customer details")
    pickup: Optional[dict] = Field(None, description="Pickup info")
    delivery: Optional[dict] = Field(None, description="Delivery info")
    items: Optional[List[dict]] = Field(None, description="Line items")


class JobSearchResult(ResponseModel):
    """Single search hit — GET /job/search and POST /job/searchByDetails.

    The live API returns ``jobDisplayID`` (capital *ID*) as a string,
    not the camelCase ``jobDisplayId`` that swagger shows.
    """

    job_display_id: Optional[str] = Field(None, alias="jobDisplayID", description="Display ID (string)")
    job_id: Optional[str] = Field(None, alias="jobID", description="Job UUID")
    customer_full_name: Optional[str] = Field(None, alias="customerFullName", description="Customer full name")
    customer_phone_number: Optional[str] = Field(None, alias="customerPhoneNumber", description="Customer phone")
    jobstatus: Optional[str] = Field(None, description="Job status text")
    company_name: Optional[str] = Field(None, alias="companyName", description="Company name")
    agent_code: Optional[str] = Field(None, alias="agentCode", description="Agent code")
    job_total_amount: Optional[float] = Field(None, alias="jobTotalAmount", description="Total amount")
    pu_address1: Optional[str] = Field(None, alias="puAddress1", description="Pickup address line 1")
    pu_city: Optional[str] = Field(None, alias="puCity", description="Pickup city")
    pu_state: Optional[str] = Field(None, alias="puState", description="Pickup state")
    del_city: Optional[str] = Field(None, alias="delCity", description="Delivery city")
    del_state: Optional[str] = Field(None, alias="delState", description="Delivery state")
    status_id: Optional[str] = Field(None, alias="statusID", description="Status UUID")


class JobPrice(ResponseModel):
    """Price info — GET /job/{jobDisplayId}/price."""

    job_display_id: Optional[int] = Field(None, alias="jobDisplayId")
    prices: Optional[List[dict]] = Field(None, description="Price breakdowns")
    total: Optional[float] = Field(None, description="Total price")
    total_sell_price: Optional[float] = Field(None, alias="totalSellPrice", description="Total sell price")


class CalendarItem(ResponseModel):
    """Calendar/line item — GET /job/{jobDisplayId}/calendaritems.

    Despite the name, the live API returns job line-item details
    (name, quantity, dimensions, value) rather than calendar events.
    """

    id: Optional[str] = Field(None, description="Item UUID")
    title: Optional[str] = Field(None, description="Item title")
    start: Optional[str] = Field(None, description="Start datetime")
    end: Optional[str] = Field(None, description="End datetime")
    name: Optional[str] = Field(None, description="Item name/description")
    quantity: Optional[int] = Field(None, description="Quantity")
    length: Optional[float] = Field(None, description="Length dimension")
    width: Optional[float] = Field(None, description="Width dimension")
    height: Optional[float] = Field(None, description="Height dimension")
    weight: Optional[float] = Field(None, description="Weight")
    value: Optional[float] = Field(None, description="Declared value")
    notes: Optional[str] = Field(None, description="Item notes")
    customer_item_id: Optional[str] = Field(None, alias="customerItemId", description="Customer item reference")


class JobUpdatePageConfig(ResponseModel):
    """Update page config — GET /job/{id}/updatePageConfig."""

    config: Optional[dict] = Field(None, description="Page configuration data")
    page_controls: Optional[int] = Field(None, alias="pageControls", description="Page control bitmask")
    workflow_controls: Optional[int] = Field(None, alias="workflowControls", description="Workflow control bitmask")


class JobCreateRequest(RequestModel):
    """Body for POST /job."""

    customer: Optional[dict] = Field(None, description="Customer details")
    pickup: Optional[dict] = Field(None, description="Pickup info")
    delivery: Optional[dict] = Field(None, description="Delivery info")
    items: Optional[List[dict]] = Field(None, description="Line items")
    services: Optional[List[dict]] = Field(None, description="Requested services")


class JobSaveRequest(RequestModel):
    """Body for PUT /job/save."""

    job_display_id: Optional[int] = Field(None, alias="jobDisplayId")
    # Additional fields from job data
    customer: Optional[dict] = Field(None)
    pickup: Optional[dict] = Field(None)
    delivery: Optional[dict] = Field(None)
    items: Optional[List[dict]] = Field(None)


class JobSearchRequest(RequestModel):
    """Body for POST /job/searchByDetails."""

    search_text: Optional[str] = Field(None, alias="searchText", description="Search query")
    page: int = Field(1, description="Page number")
    page_size: int = Field(25, alias="pageSize", description="Results per page")


class JobUpdateRequest(RequestModel):
    """Body for POST /job/update (ABC API surface)."""

    job_id: Optional[str] = Field(None, alias="jobId", description="Job UUID")
    # Fields defined by ABC API — details from fixture
    updates: Optional[dict] = Field(None, description="Update payload")
