"""Lookup models for the ACPortal API."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class LookupItemsParams(RequestModel):
    """Query parameters for GET /lookup/items."""

    job_display_id: Optional[int] = Field(None, alias="jobDisplayId", description="Job display ID for item lookup")
    job_item_id: Optional[str] = Field(None, alias="jobItemId", description="Job item UUID filter")


class LookupDocumentTypesParams(RequestModel):
    """Query parameters for GET /lookup/documentTypes."""

    document_source: Optional[str] = Field(None, alias="documentSource", description="Document source filter")


class LookupDensityClassMapParams(RequestModel):
    """Query parameters for GET /lookup/densityClassMap."""

    carrier_api: Optional[str] = Field(None, alias="carrierApi", description="Carrier API identifier")


class ContactTypeEntity(ResponseModel):
    """Contact type — GET /lookup/contactTypes."""

    id: Optional[int] = Field(None, description="Contact type ID")
    name: Optional[str] = Field(None, description="Contact type name")
    description: Optional[str] = Field(None, description="Description")
    value: Optional[str] = Field(None, description="Contact type value")


class CountryCodeDto(ResponseModel):
    """Country code — GET /lookup/countries."""

    code: Optional[str] = Field(None, description="ISO country code")
    name: Optional[str] = Field(None, description="Country name")
    id: Optional[str] = Field(None, description="Country UUID")
    iata_code: Optional[str] = Field(None, alias="iataCode", description="IATA country code")


class JobStatus(ResponseModel):
    """Job status entry — GET /lookup/jobStatuses."""

    id: Optional[int] = Field(None, description="Status ID")
    name: Optional[str] = Field(None, description="Status name")
    description: Optional[str] = Field(None, description="Description")
    key: Optional[str] = Field(None, description="Status key")
    value: Optional[str] = Field(None, description="Status value")


class LookupItem(ResponseModel):
    """Generic lookup item — GET /lookup/items."""

    id: Optional[str] = Field(None, description="Item UUID")
    name: Optional[str] = Field(None, description="Item name")


# ---- Extended lookup models (008) -----------------------------------------


class LookupValue(ResponseModel):
    """Generic lookup value — GET /lookup/{masterConstantKey}.

    Source: MasterData.cs — controller returns id/key/name/value.
    """

    id: Optional[str] = Field(None, description="Value ID (Guid)")
    key: Optional[str] = Field(None, description="Master data key")
    name: Optional[str] = Field(None, description="Display name")
    value: Optional[str] = Field(None, description="Value (Guid)")


class AccessKey(ResponseModel):
    """Access key record — GET /lookup/accessKeys.

    Source: APIAccessKey.cs — accessKey/friendlyName fields.
    """

    access_key: Optional[str] = Field(None, alias="accessKey", description="Access key string")
    friendly_name: Optional[str] = Field(None, alias="friendlyName", description="Friendly display name")


class AccessKeySetup(ResponseModel):
    """Access key setup details — GET /lookup/accessKey/{accessKey}.

    Source: APIAccessKeySetup.cs — includes parent AccessKey fields.
    """

    access_key: Optional[str] = Field(None, alias="accessKey", description="Access key string")
    friendly_name: Optional[str] = Field(None, alias="friendlyName", description="Friendly display name")
    user_id: Optional[str] = Field(None, alias="userId", description="User ID (Guid)")
    user_identifier: Optional[int] = Field(None, alias="userIdentifier", description="User identifier (int)")
    referred_by_id: Optional[str] = Field(None, alias="referredById", description="Referred by ID (Guid)")
    referred_by: Optional[str] = Field(None, alias="referredBy", description="Referred by name")
    use_agent_search: Optional[bool] = Field(None, alias="useAgentSearch", description="Use agent search")
    allow_job_info_update: Optional[bool] = Field(None, alias="allowJobInfoUpdate", description="Allow job info update")
    allow_job_info_update_without_booking_key: Optional[bool] = Field(
        None, alias="allowJobInfoUpdateWithoutBookingKey", description="Allow update without booking key",
    )
    ip_protections: Optional[list] = Field(None, alias="ipProtections", description="IP protection rules")
    parcel_transportation_multiplier: Optional[float] = Field(
        None, alias="parcelTransportationMultiplier", description="Parcel transportation multiplier",
    )
    parcel_accessorial_multiplier: Optional[float] = Field(
        None, alias="parcelAccessorialMultiplier", description="Parcel accessorial multiplier",
    )
    items_combine_max_inches: Optional[int] = Field(
        None, alias="itemsCombineMaxInches", description="Max combine inches",
    )
    use_pack_labor_calculation: Optional[bool] = Field(
        None, alias="usePackLaborCalculation", description="Use pack labor calculation",
    )
    use_base_pickup_fee_calculation: Optional[bool] = Field(
        None, alias="useBasePickupFeeCalculation", description="Use base pickup fee calculation",
    )
    force_agent_pickup: Optional[bool] = Field(None, alias="forceAgentPickup", description="Force agent pickup")


class DocumentTypeBySource(ResponseModel):
    """Document type by source — GET /lookup/documentTypes.

    Source: DocumentTypeBySource.cs — name/value/documentSource fields.
    """

    name: Optional[str] = Field(None, description="Document type name")
    value: Optional[int] = Field(None, description="Document type value")
    document_source: Optional[int] = Field(None, alias="documentSource", description="Document source")


class PPCCampaign(ResponseModel):
    """PPC campaign — GET /lookup/PPCCampaigns.

    Source: PPCCampaign.cs — id/name fields.
    """

    id: Optional[int] = Field(None, description="Campaign ID")
    name: Optional[str] = Field(None, description="Campaign name")


class CommonInsuranceSlab(ResponseModel):
    """Common insurance slab — GET /lookup/comonInsurance.

    Source: Live API — insurance slab entity with rate/deductible fields.
    """

    id: Optional[str] = Field(None, description="Slab ID (Guid)")
    key: Optional[str] = Field(None, description="Slab key")
    name: Optional[str] = Field(None, description="Slab name")
    value: Optional[str] = Field(None, description="Slab value (Guid)")
    insurance_slab_id: Optional[str] = Field(None, alias="insuranceSlabID", description="Insurance slab ID (Guid)")
    transp_type_id: Optional[str] = Field(None, alias="transpTypeID", description="Transport type ID (Guid)")
    deductible_amount: Optional[float] = Field(None, alias="deductibleAmount", description="Deductible amount")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Whether active")
    rate: Optional[float] = Field(None, description="Insurance rate")
    revision: Optional[int] = Field(None, description="Revision number")
    insurance_type: Optional[str] = Field(None, alias="insuranceType", description="Insurance type")


class ParcelPackageType(ResponseModel):
    """Parcel package type — GET /lookup/parcelPackageTypes.

    Source: Live API response — full package type entity.
    """

    id: Optional[int] = Field(None, description="Package type ID")
    name: Optional[str] = Field(None, description="Package type name")
    code: Optional[str] = Field(None, description="Package type code")
    description: Optional[str] = Field(None, description="Description")
    carrier_api: Optional[int] = Field(None, alias="carrierAPI", description="Carrier API identifier")
    carrier_code: Optional[str] = Field(None, alias="carrierCode", description="Carrier code")
    weight_limit: Optional[float] = Field(None, alias="weightLimit", description="Weight limit")
    length_limit: Optional[float] = Field(None, alias="lengthLimit", description="Length limit")
    width_limit: Optional[float] = Field(None, alias="widthLimit", description="Width limit")
    height_limit: Optional[float] = Field(None, alias="heightLimit", description="Height limit")
    priority: Optional[int] = Field(None, description="Priority")
    weight: Optional[float] = Field(None, description="Default weight")
    length: Optional[float] = Field(None, description="Default length")
    width: Optional[float] = Field(None, description="Default width")
    height: Optional[float] = Field(None, description="Default height")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Whether active")
    cost: Optional[float] = Field(None, description="Cost")
    sell: Optional[float] = Field(None, description="Sell price")


class DensityClassEntry(ResponseModel):
    """Density-to-class mapping — GET /lookup/densityClassMap.

    Source: Live API — GuidSequentialRangeValue shape.
    """

    range_end: Optional[float] = Field(None, alias="rangeEnd", description="Range end value")
    value: Optional[str] = Field(None, description="Value (Guid)")
