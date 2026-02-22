"""Shipment models for ACPortal API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel
from ab.api.models.mixins import IdentifiedModel


class ShipmentParams(RequestModel):
    """Query parameters for GET /shipment."""

    franchisee_id: Optional[str] = Field(None, alias="franchiseeId", description="Franchisee UUID")
    provider_id: Optional[str] = Field(None, alias="providerId", description="Provider UUID")
    pro_number: Optional[str] = Field(None, alias="proNumber", description="PRO/tracking number")


# ---- Response models --------------------------------------------------


class RateQuote(ResponseModel):
    """Rate quote — GET /job/{jobDisplayId}/shipment/ratequotes."""

    carrier_name: Optional[str] = Field(None, alias="carrierName", description="Carrier company name")
    service_type: Optional[str] = Field(None, alias="serviceType", description="Service level")
    total_charge: Optional[float] = Field(None, alias="totalCharge", description="Total quoted price")
    transit_days: Optional[int] = Field(None, alias="transitDays", description="Estimated transit time")
    accessorial_charges: Optional[List[dict]] = Field(
        None, alias="accessorialCharges", description="Itemized extras",
    )
    provider_option_index: Optional[int] = Field(
        None, alias="providerOptionIndex", description="Index for booking selection",
    )
    errors: Optional[list] = Field(None, description="Rate quote errors")
    rates: Optional[list] = Field(None, description="Available rates")
    rates_key: Optional[str] = Field(None, alias="ratesKey", description="Rates cache key")
    request_snapshot: Optional[dict] = Field(None, alias="requestSnapshot", description="Original request snapshot")


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
    from_zip: Optional[str] = Field(None, alias="fromZip", description="Origin ZIP code")
    to_zip: Optional[str] = Field(None, alias="toZip", description="Destination ZIP code")
    item_weight: Optional[float] = Field(None, alias="itemWeight", description="Total item weight")
    services: Optional[list] = Field(None, description="Available services")
    parcel_items: Optional[list] = Field(None, alias="parcelItems", description="Parcel items")
    parcel_services: Optional[list] = Field(None, alias="parcelServices", description="Parcel services")
    ship_out_date: Optional[str] = Field(None, alias="shipOutDate", description="Ship out date")


class ShipmentWeight(ResponseModel):
    """Weight details for a shipment."""

    pounds: Optional[float] = Field(None, description="Weight in pounds")
    original_weight: Optional[float] = Field(None, alias="originalWeight", description="Original weight value")
    original_weight_measure_unit: Optional[str] = Field(
        None, alias="originalWeightMeasureUnit", description="Original weight unit"
    )


class ShipmentInfo(ResponseModel):
    """Shipment info — GET /shipment."""

    shipment_id: Optional[str] = Field(None, alias="shipmentId", description="Shipment identifier")
    status: Optional[str] = Field(None, description="Current status")
    carrier: Optional[str] = Field(None, description="Carrier name")
    pro_number: Optional[str] = Field(None, alias="proNumber", description="PRO tracking number")
    used_api: Optional[int] = Field(None, alias="usedAPI", description="API used for shipment")
    history_provider_name: Optional[str] = Field(
        None, alias="historyProviderName", description="Tracking history provider"
    )
    history_statuses: Optional[list] = Field(None, alias="historyStatuses", description="Tracking status history")
    weight: Optional[ShipmentWeight] = Field(None, description="Shipment weight details")
    job_weight: Optional[float] = Field(None, alias="jobWeight", description="Job total weight")
    successfully: Optional[bool] = Field(None, description="Whether shipment was successful")
    error_message: Optional[str] = Field(None, alias="errorMessage", description="Error message if failed")
    multiple_shipments: Optional[bool] = Field(None, alias="multipleShipments", description="Multiple shipments flag")
    packages: Optional[list] = Field(None, description="Package details")
    estimated_delivery: Optional[str] = Field(None, alias="estimatedDelivery", description="Estimated delivery date")


class RadioButtonOption(ResponseModel):
    """Radio button option within an accessorial option."""

    description: Optional[str] = Field(None, description="Option description")
    code: Optional[str] = Field(None, description="Option code")


class AccessorialOption(ResponseModel):
    """Option within a global accessorial."""

    key: Optional[str] = Field(None, description="Option key")
    type: Optional[int] = Field(None, description="Option type")
    radio_button_options: Optional[List[RadioButtonOption]] = Field(
        None, alias="radioButtonOptions", description="Radio button choices"
    )


class GlobalAccessorial(ResponseModel):
    """Global accessorial — GET /shipment/accessorials."""

    id: Optional[str] = Field(None, description="Accessorial ID")
    name: Optional[str] = Field(None, description="Name")
    category: Optional[str] = Field(None, description="Category grouping")
    description: Optional[str] = Field(None, description="Accessorial description")
    price: Optional[str] = Field(None, description="Price or price range")
    options: Optional[List[AccessorialOption]] = Field(None, description="Accessorial options")
    unique_id: Optional[str] = Field(None, alias="uniqueId", description="Unique identifier")
    source_apis: Optional[List[int]] = Field(None, alias="sourceAPIs", description="Source API identifiers")


# ---- Request models ---------------------------------------------------


class ShipmentBookRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/shipment/book."""

    provider_option_index: Optional[int] = Field(
        None, alias="providerOptionIndex", description="Selected rate quote index",
    )
    ship_date: Optional[str] = Field(None, alias="shipDate", description="Requested ship date")


class AccessorialAddRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/shipment/accessorial."""

    add_on_id: str = Field(..., alias="addOnId", description="Accessorial ID to add")
