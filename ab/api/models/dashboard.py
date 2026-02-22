"""Dashboard models for the ACPortal API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class DashboardParams(RequestModel):
    """Query parameters for GET /dashboard."""

    view_id: Optional[int] = Field(None, alias="viewId", description="Grid view ID")
    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID filter")


class DashboardSummary(ResponseModel):
    """Aggregated dashboard data — GET /dashboard."""

    inbound_count: Optional[int] = Field(None, alias="inboundCount", description="Inbound shipment count")
    outbound_count: Optional[int] = Field(None, alias="outboundCount", description="Outbound shipment count")
    in_house_count: Optional[int] = Field(None, alias="inHouseCount", description="In-house shipment count")
    local_deliveries_count: Optional[int] = Field(
        None, alias="localDeliveriesCount", description="Local delivery count",
    )
    recent_estimates_count: Optional[int] = Field(
        None, alias="recentEstimatesCount", description="Recent estimates count",
    )


class GridViewState(ResponseModel):
    """Saved grid view state — GET/POST /dashboard/gridviewstate/{id}."""

    id: Optional[str] = Field(None, description="View state ID")
    columns: Optional[List[dict]] = Field(None, description="Column configurations")
    filters: Optional[List[dict]] = Field(None, description="Active filters")
    sort_order: Optional[List[dict]] = Field(None, alias="sortOrder", description="Sort configuration")


class GridViewInfo(ResponseModel):
    """Grid view metadata — GET /dashboard/gridviews."""

    id: Optional[str] = Field(None, description="View ID")
    name: Optional[str] = Field(None, description="View name")
    is_default: Optional[bool] = Field(None, alias="isDefault", description="Whether this is the default view")
