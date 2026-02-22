"""Form models for ACPortal API."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import ResponseModel


class FormsShipmentPlan(ResponseModel):
    """Shipment plan for BOL selection — GET /job/{jobDisplayId}/form/shipments.

    This is the only JSON-returning form endpoint.  All other form endpoints
    return raw PDF bytes.
    """

    shipment_plan_id: Optional[str] = Field(None, alias="shipmentPlanId", description="Plan identifier")
    provider_option_index: Optional[int] = Field(None, alias="providerOptionIndex", description="Provider index")
    carrier_name: Optional[str] = Field(None, alias="carrierName", description="Carrier")
    service_type: Optional[str] = Field(None, alias="serviceType", description="Service level")
    job_shipment_id: Optional[str] = Field(None, alias="jobShipmentID", description="Shipment UUID")
    job_id: Optional[str] = Field(None, alias="jobID", description="Job UUID")
    from_address_id: Optional[int] = Field(None, alias="fromAddressId", description="Origin address ID")
    to_address_id: Optional[int] = Field(None, alias="toAddressId", description="Destination address ID")
    provider_id: Optional[str] = Field(None, alias="providerID", description="Provider UUID")
    sequence_no: Optional[int] = Field(None, alias="sequenceNo", description="Sequence number")
    from_location_company_name: Optional[str] = Field(
        None, alias="fromLocationCompanyName", description="Origin company name"
    )
    to_location_company_name: Optional[str] = Field(
        None, alias="toLocationCompanyName", description="Destination company name"
    )
    transport_type: Optional[str] = Field(
        None, alias="transportType", description="Transport type (PickUp, Delivery, House)"
    )
    provider_company_name: Optional[str] = Field(
        None, alias="providerCompanyName", description="Provider company name"
    )
    option_index: Optional[int] = Field(None, alias="optionIndex", description="Option index")
