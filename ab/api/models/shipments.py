"""Shipment models for ACPortal API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel
from ab.api.models.mixins import IdentifiedModel


# ---- Response models --------------------------------------------------


class RateQuote(ResponseModel):
    """Rate quote — GET /job/{jobDisplayId}/shipment/ratequotes."""

    carrier_name: Optional[str] = Field(None, alias="carrierName", description="Carrier company name")
    service_type: Optional[str] = Field(None, alias="serviceType", description="Service level")
    total_charge: Optional[float] = Field(None, alias="totalCharge", description="Total quoted price")
    transit_days: Optional[int] = Field(None, alias="transitDays", description="Estimated transit time")
    accessorial_charges: Optional[List[dict]] = Field(None, alias="accessorialCharges", description="Itemized extras")
    provider_option_index: Optional[int] = Field(None, alias="providerOptionIndex", description="Index for booking selection")


class ShipmentOriginDestination(ResponseModel):
    """Origin/destination — GET /job/{jobDisplayId}/shipment/origindestination."""

    origin: Optional[dict] = Field(None, description="Origin address details")
    destination: Optional[dict] = Field(None, description="Destination address details")


class Accessorial(ResponseModel, IdentifiedModel):
    """Accessorial — GET /job/{jobDisplayId}/shipment/accessorials."""

    name: Optional[str] = Field(None, description="Accessorial name")
    description: Optional[str] = Field(None, description="Description")
    price: Optional[float] = Field(None, description="Additional cost")
    is_selected: Optional[bool] = Field(None, alias="isSelected", description="Whether currently applied")


class ShipmentExportData(ResponseModel):
    """Export data — GET /job/{jobDisplayId}/shipment/exportdata."""

    export_data: Optional[dict] = Field(None, alias="exportData", description="Shipment export payload")


class RatesState(ResponseModel):
    """Rates state — GET /job/{jobDisplayId}/shipment/ratesstate."""

    state: Optional[str] = Field(None, description="Current rates state")
    rates: Optional[List[dict]] = Field(None, description="Available rates")


class ShipmentInfo(ResponseModel):
    """Shipment info — GET /shipment."""

    shipment_id: Optional[str] = Field(None, alias="shipmentId", description="Shipment identifier")
    status: Optional[str] = Field(None, description="Current status")
    carrier: Optional[str] = Field(None, description="Carrier name")
    pro_number: Optional[str] = Field(None, alias="proNumber", description="PRO tracking number")


class GlobalAccessorial(ResponseModel):
    """Global accessorial — GET /shipment/accessorials."""

    id: Optional[str] = Field(None, description="Accessorial ID")
    name: Optional[str] = Field(None, description="Name")
    category: Optional[str] = Field(None, description="Category grouping")


# ---- Request models ---------------------------------------------------


class ShipmentBookRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/shipment/book."""

    provider_option_index: Optional[int] = Field(None, alias="providerOptionIndex", description="Selected rate quote index")
    ship_date: Optional[str] = Field(None, alias="shipDate", description="Requested ship date")


class AccessorialAddRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/shipment/accessorial."""

    add_on_id: str = Field(..., alias="addOnId", description="Accessorial ID to add")
