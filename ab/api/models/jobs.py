"""Job models for ACPortal and ABC APIs."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel
from ab.api.models.mixins import FullAuditModel, IdentifiedModel


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


# ---- Timeline / Status models -----------------------------------------


class TimelineTask(ResponseModel, IdentifiedModel):
    """Timeline task — GET /job/{jobDisplayId}/timeline."""

    id: Optional[str] = Field(None, description="Timeline task ID")
    task_code: Optional[str] = Field(None, alias="taskCode", description="Task type code")
    status: Optional[int] = Field(None, description="Status code")
    status_name: Optional[str] = Field(None, alias="statusName", description="Human-readable status")
    agent_contact_id: Optional[str] = Field(None, alias="agentContactId", description="Assigned agent")
    scheduled_date: Optional[str] = Field(None, alias="scheduledDate", description="When task is scheduled")
    completed_date: Optional[str] = Field(None, alias="completedDate", description="When task was completed")
    comments: Optional[str] = Field(None, description="Task notes")
    is_completed: Optional[bool] = Field(None, alias="isCompleted", description="Completion flag")
    sort_order: Optional[int] = Field(None, alias="sortOrder", description="Display order")


class TimelineAgent(ResponseModel):
    """Timeline agent — GET /job/{jobDisplayId}/timeline/{taskCode}/agent."""

    contact_id: Optional[str] = Field(None, alias="contactId", description="Agent contact ID")
    name: Optional[str] = Field(None, description="Agent name")
    company_name: Optional[str] = Field(None, alias="companyName", description="Agent's company")


class TimelineTaskCreateRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/timeline."""

    task_code: str = Field(..., alias="taskCode", description="Task type code")
    scheduled_date: Optional[str] = Field(None, alias="scheduledDate", description="Scheduled date")
    comments: Optional[str] = Field(None, description="Notes")
    agent_contact_id: Optional[str] = Field(None, alias="agentContactId", description="Assigned agent")


class TimelineTaskUpdateRequest(RequestModel):
    """Body for PATCH /job/{jobDisplayId}/timeline/{timelineTaskId}."""

    status: Optional[int] = Field(None, description="New status code")
    scheduled_date: Optional[str] = Field(None, alias="scheduledDate", description="Updated schedule")
    completed_date: Optional[str] = Field(None, alias="completedDate", description="Completion date")
    comments: Optional[str] = Field(None, description="Updated notes")


class IncrementStatusRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/timeline/incrementjobstatus."""

    create_email: Optional[bool] = Field(None, alias="createEmail", description="Send status notification email")


# ---- Tracking models --------------------------------------------------


class TrackingInfo(ResponseModel):
    """Tracking info — GET /job/{jobDisplayId}/tracking."""

    status: Optional[str] = Field(None, description="Current tracking status")
    location: Optional[str] = Field(None, description="Current location")
    estimated_delivery: Optional[str] = Field(None, alias="estimatedDelivery", description="ETA")
    events: Optional[List[dict]] = Field(None, description="Tracking event history")
    carrier_name: Optional[str] = Field(None, alias="carrierName", description="Carrier")
    pro_number: Optional[str] = Field(None, alias="proNumber", description="PRO number")


class TrackingInfoV3(ResponseModel):
    """Tracking info v3 — GET /v3/job/{jobDisplayId}/tracking/{historyAmount}."""

    tracking_details: Optional[List[dict]] = Field(None, alias="trackingDetails", description="Detailed tracking entries")
    carrier_info: Optional[List[dict]] = Field(None, alias="carrierInfo", description="Carrier metadata")
    shipment_status: Optional[str] = Field(None, alias="shipmentStatus", description="Overall status")


# ---- Notes models -----------------------------------------------------


class JobNote(ResponseModel, IdentifiedModel):
    """Job note — GET /job/{jobDisplayId}/note."""

    id: Optional[str] = Field(None, description="Note ID")
    comment: Optional[str] = Field(None, description="Note content")
    is_important: Optional[bool] = Field(None, alias="isImportant", description="Flagged as important")
    is_completed: Optional[bool] = Field(None, alias="isCompleted", description="Completion status")
    author: Optional[str] = Field(None, description="Author name")
    modify_date: Optional[str] = Field(None, alias="modifiyDate", description="Last modified (API typo preserved)")
    task_code: Optional[str] = Field(None, alias="taskCode", description="Associated timeline task")


class JobNoteCreateRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/note."""

    comments: str = Field(..., description="Note content (max 8000 chars)")
    task_code: str = Field(..., alias="taskCode", description="Associated timeline task code")
    is_important: Optional[bool] = Field(None, alias="isImportant", description="Flag as important")
    send_notification: Optional[bool] = Field(None, alias="sendNotification", description="Notify assigned users")
    due_date: Optional[str] = Field(None, alias="dueDate", description="Due date")


class JobNoteUpdateRequest(RequestModel):
    """Body for PUT /job/{jobDisplayId}/note/{id}."""

    comments: Optional[str] = Field(None, description="Updated content")
    is_important: Optional[bool] = Field(None, alias="isImportant", description="Updated flag")
    is_completed: Optional[bool] = Field(None, alias="isCompleted", description="Mark complete")


# ---- Parcels & Items models -------------------------------------------


class ParcelItem(ResponseModel):
    """Parcel item — GET /job/{jobDisplayId}/parcelitems."""

    parcel_item_id: Optional[str] = Field(None, alias="parcelItemId", description="Parcel item ID")
    description: Optional[str] = Field(None, description="Item description")
    length: Optional[float] = Field(None, description="Length (inches)")
    width: Optional[float] = Field(None, description="Width (inches)")
    height: Optional[float] = Field(None, description="Height (inches)")
    weight: Optional[float] = Field(None, description="Weight (lbs)")
    quantity: Optional[int] = Field(None, description="Number of pieces")
    packaging_type: Optional[str] = Field(None, alias="packagingType", description="Package type")


class ParcelItemWithMaterials(ResponseModel):
    """Parcel item with materials — GET /job/{jobDisplayId}/parcel-items-with-materials."""

    parcel_item_id: Optional[str] = Field(None, alias="parcelItemId", description="Parcel item ID")
    description: Optional[str] = Field(None, description="Item description")
    materials: Optional[List[dict]] = Field(None, description="Associated materials")
    dimensions: Optional[dict] = Field(None, description="Packed dimensions")


class PackagingContainer(ResponseModel):
    """Packaging container — GET /job/{jobDisplayId}/packagingcontainers."""

    container_id: Optional[str] = Field(None, alias="containerId", description="Container ID")
    name: Optional[str] = Field(None, description="Container name")
    dimensions: Optional[dict] = Field(None, description="Container dimensions")


class ParcelItemCreateRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/parcelitems."""

    description: str = Field(..., description="Item description")
    length: Optional[float] = Field(None, description="Length")
    width: Optional[float] = Field(None, description="Width")
    height: Optional[float] = Field(None, description="Height")
    weight: Optional[float] = Field(None, description="Weight")
    quantity: Optional[int] = Field(None, description="Quantity")


class ItemNotesRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/item/notes."""

    notes: str = Field(..., description="Item notes content")


class ItemUpdateRequest(RequestModel):
    """Body for PUT /job/{jobDisplayId}/item/{itemId}."""

    description: Optional[str] = Field(None, description="Updated description")
    quantity: Optional[int] = Field(None, description="Updated quantity")
    weight: Optional[float] = Field(None, description="Updated weight")
