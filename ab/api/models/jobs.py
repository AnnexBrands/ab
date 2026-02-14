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
    """Single search hit — GET /job/search."""

    job_display_id: Optional[int] = Field(None, alias="jobDisplayId", description="Display ID")
    status: Optional[str] = Field(None, description="Job status")
    customer_name: Optional[str] = Field(None, alias="customerName", description="Customer name")
    agent: Optional[str] = Field(None, description="Assigned agent")


class JobPrice(ResponseModel):
    """Price info — GET /job/{jobDisplayId}/price."""

    # Fields TBD from fixture; using flexible dict-style for now
    job_display_id: Optional[int] = Field(None, alias="jobDisplayId")
    prices: Optional[List[dict]] = Field(None, description="Price breakdowns")
    total: Optional[float] = Field(None, description="Total price")


class CalendarItem(ResponseModel):
    """Calendar item — GET /job/{jobDisplayId}/calendaritems."""

    id: Optional[str] = Field(None, description="Calendar item ID")
    title: Optional[str] = Field(None, description="Item title")
    start: Optional[str] = Field(None, description="Start datetime")
    end: Optional[str] = Field(None, description="End datetime")


class JobUpdatePageConfig(ResponseModel):
    """Update page config — GET /job/{id}/updatePageConfig."""

    # Swagger-reliable; exact fields from fixture
    config: Optional[dict] = Field(None, description="Page configuration data")


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
