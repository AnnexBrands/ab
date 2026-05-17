"""Dashboard models for the ACPortal API."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class DashboardParams(RequestModel):
    """Query parameters for GET /dashboard."""

    view_id: Optional[int] = Field(None, alias="viewId", description="Grid view ID")
    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID filter")


class DashboardCompanyParams(RequestModel):
    """Query parameters for GET /dashboard/gridviews (company filter)."""

    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID filter")


class DashboardCompanyRequest(RequestModel):
    """Body for POST /dashboard/{inbound,inhouse,outbound,...} endpoints."""

    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID filter")


class DashboardItem(ResponseModel):
    """Row in the dashboard data grid — element of `DashboardSummary.data`."""

    location: Optional[str] = Field(None, description="Location code")
    job_display_id: Optional[int] = Field(None, alias="jobDisplayID", description="Job display ID")
    pickup: Optional[str] = Field(None, description="Pickup company name")
    customer: Optional[str] = Field(None, description="Customer name")
    packer: Optional[str] = Field(None, description="Packer name")
    priority: Optional[int] = Field(None, description="Priority")
    next: Optional[str] = Field(None, description="Next step label")
    pause: Optional[int] = Field(None, description="Pause flag")
    labels: Optional[str] = Field(None, description="Labels")
    ops_form: Optional[str] = Field(None, alias="opsForm", description="Ops form")
    step: Optional[int] = Field(None, description="Workflow step")
    ship_by: Optional[datetime] = Field(None, alias="shipBy", description="Ship-by date-time")
    expedite: Optional[str] = Field(None, description="Expedite flag")
    note: Optional[str] = Field(None, description="Note")
    carrier: Optional[str] = Field(None, description="Carrier name")
    labor: Optional[float] = Field(None, description="Estimated labor hours")
    actual: Optional[float] = Field(None, description="Actual labor hours")
    item_count: Optional[int] = Field(None, alias="item_Count", description="Item count")

    def cli_format(self) -> str:
        """One-line pretty row used by the CLI and examples (vs. JSON)."""
        ship = self.ship_by.strftime("%Y-%m-%d %H:%M") if self.ship_by else "—"
        job = "—" if self.job_display_id is None else str(self.job_display_id)
        step = "—" if self.step is None else str(self.step)
        return (
            f"job={job:<8} "
            f"loc={(self.location or '—'):<6} "
            f"customer={(self.customer or '—')[:30]:<30} "
            f"step={step:<3} "
            f"next={(self.next or '—')[:14]:<14} "
            f"ship_by={ship:<16} "
            f"carrier={(self.carrier or '—')[:18]}"
        )


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
    data: Optional[List[DashboardItem]] = Field(None, description="Grid view rows")

    def cli_format(self) -> str:
        """Pretty summary line + one line per row (vs. JSON).

        ``data`` is the active grid view's rows; counts are populated only
        when the API includes them. The header surfaces both so it's clear
        which fields were returned.
        """
        rows = self.data or []
        header = (
            f"inbound={self.inbound_count} "
            f"outbound={self.outbound_count} "
            f"in_house={self.in_house_count} "
            f"local_deliveries={self.local_deliveries_count} "
            f"recent_estimates={self.recent_estimates_count} "
            f"rows={len(rows)}"
        )
        if not rows:
            return header
        body = "\n".join(item.cli_format() for item in rows)
        return f"{header}\n{body}"


class GridViewState(ResponseModel):
    """Saved grid view state — GET/POST /dashboard/gridviewstate/{id}."""

    id: Optional[str] = Field(None, description="View state ID")
    columns: Optional[List[dict]] = Field(None, description="Column configurations")
    filters: Optional[List[dict]] = Field(None, description="Active filters")
    sort_order: Optional[List[dict]] = Field(None, alias="sortOrder", description="Sort configuration")


class GridViewInfo(ResponseModel):
    """Grid view metadata — GET /dashboard/gridviews.

    Shape matches the swagger ``GridViewDetails`` component. ``id`` is the
    forward reference consumed by :class:`DashboardParams.view_id` when
    calling GET ``/dashboard``.
    """

    id: Optional[int] = Field(None, description="View ID — feeds DashboardParams.view_id")
    name: Optional[str] = Field(None, description="View name")
    data_key: Optional[str] = Field(None, alias="dataKey", description="Data key")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Whether the view is active")
    stored_procedure: Optional[str] = Field(
        None, alias="storedProcedure", description="Backing stored procedure",
    )
    columns_specification: Optional[str] = Field(
        None, alias="columnsSpecification", description="Column specification (raw)",
    )
    sp_columns: Optional[List[dict]] = Field(
        None, alias="spColumns", description="Stored procedure column metadata",
    )

    def cli_format(self) -> str:
        """One-line pretty row used by the CLI and examples (vs. JSON)."""
        id_str = "—" if self.id is None else str(self.id)
        return (
            f"id={id_str:<5} "
            f"name={self.name!r:<30} "
            f"dataKey={self.data_key!r:<20} "
            f"active={self.is_active}"
        )
