"""Form models for ACPortal API."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import ResponseModel


class FormsShipmentPlan(ResponseModel):
    """Shipment plan for BOL selection — GET /job/{jobDisplayId}/form/shipments.

    This is the only JSON-returning form endpoint.  All other form endpoints
    return raw bytes (PDF/HTML).
    """

    shipment_plan_id: Optional[str] = Field(None, alias="shipmentPlanId", description="Plan identifier")
    provider_option_index: Optional[int] = Field(None, alias="providerOptionIndex", description="Provider index")
    carrier_name: Optional[str] = Field(None, alias="carrierName", description="Carrier")
    service_type: Optional[str] = Field(None, alias="serviceType", description="Service level")
