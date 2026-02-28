"""Lookup models for the ACPortal API."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class LookupItemsParams(RequestModel):
    """Query parameters for GET /lookup/items."""

    job_display_id: Optional[int] = Field(None, alias="jobDisplayId", description="Job display ID for item lookup")
    job_item_id: Optional[int] = Field(None, alias="jobItemId", description="Job item ID filter")


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

    id: Optional[int] = Field(None, description="Item ID")
    name: Optional[str] = Field(None, description="Item name")
    value: Optional[str] = Field(None, description="Item value")


# ---- Extended lookup models (008) -----------------------------------------


class LookupValue(ResponseModel):
    """Generic lookup value — GET /lookup/{masterConstantKey}."""

    id: Optional[int] = Field(None, description="Value ID")
    name: Optional[str] = Field(None, description="Value name")
    description: Optional[str] = Field(None, description="Value description")
    value: Optional[str] = Field(None, description="Value")


class AccessKey(ResponseModel):
    """Access key record — GET /lookup/accessKeys."""

    key: Optional[str] = Field(None, description="Access key")
    description: Optional[str] = Field(None, description="Key description")


class ParcelPackageType(ResponseModel):
    """Parcel package type — GET /lookup/parcelPackageTypes."""

    id: Optional[int] = Field(None, description="Package type ID")
    name: Optional[str] = Field(None, description="Package type name")
    dimensions: Optional[dict] = Field(None, description="Default dimensions")


class DensityClassEntry(ResponseModel):
    """Density-to-class mapping — GET /lookup/densityClassMap."""

    density_min: Optional[float] = Field(None, alias="densityMin", description="Minimum density")
    density_max: Optional[float] = Field(None, alias="densityMax", description="Maximum density")
    freight_class: Optional[str] = Field(None, alias="freightClass", description="Freight class")
