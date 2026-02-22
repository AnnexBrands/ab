"""Address models for the ACPortal API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class AddressValidateParams(RequestModel):
    """Query parameters for GET /address/isvalid."""

    line1: str = Field(..., alias="Line1", description="Street address line 1")
    city: str = Field(..., alias="City", description="City name")
    state: str = Field(..., alias="State", description="State abbreviation")
    zip: str = Field(..., alias="Zip", description="ZIP/postal code")


class AddressPropertyTypeParams(RequestModel):
    """Query parameters for GET /address/propertytype."""

    address1: Optional[str] = Field(None, alias="Address1", description="Street address line 1")
    address2: Optional[str] = Field(None, alias="Address2", description="Street address line 2")
    city: Optional[str] = Field(None, alias="City", description="City name")
    state: Optional[str] = Field(None, alias="State", description="State abbreviation")
    zip_code: Optional[str] = Field(None, alias="ZipCode", description="ZIP/postal code")


class AddressIsValidResult(ResponseModel):
    """Result from GET /address/isvalid."""

    is_valid: Optional[bool] = Field(None, alias="isValid", description="Whether address is valid")
    validated_address: Optional[dict] = Field(
        None, alias="validatedAddress", description="Corrected/validated address"
    )
    suggestions: Optional[List[dict]] = Field(None, description="Alternative suggestions")
    dont_validate: Optional[bool] = Field(None, alias="dontValidate", description="Skip validation flag")
    country_id: Optional[str] = Field(None, alias="countryId", description="Country UUID")
    country_code: Optional[str] = Field(None, alias="countryCode", description="ISO country code")
    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")
    property_type: Optional[int] = Field(None, alias="propertyType", description="Property type classification")


class PropertyType(ResponseModel):
    """Result from GET /address/propertytype."""

    property_type: Optional[str] = Field(None, alias="propertyType", description="Property type classification")
    confidence: Optional[float] = Field(None, description="Confidence score")
