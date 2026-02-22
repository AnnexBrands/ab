"""Shared sub-models reused across multiple response models."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import ResponseModel


class Coordinates(ResponseModel):
    """GPS coordinates — nested in address objects."""

    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")


class CompanyAddress(ResponseModel):
    """Full address object — used by CompanyDetails.address and ContactPrimaryDetails.address."""

    id: Optional[int] = Field(None, description="Address integer ID")
    is_valid: Optional[bool] = Field(None, alias="isValid", description="Whether address is validated")
    dont_validate: Optional[bool] = Field(None, alias="dontValidate", description="Skip validation flag")
    property_type: Optional[int] = Field(None, alias="propertyType", description="Property type classification")
    address1_value: Optional[str] = Field(None, alias="address1Value", description="Primary address line (raw)")
    address2_value: Optional[str] = Field(None, alias="address2Value", description="Secondary address line (raw)")
    country_name: Optional[str] = Field(None, alias="countryName", description="Country name")
    country_code: Optional[str] = Field(None, alias="countryCode", description="ISO country code")
    country_id: Optional[str] = Field(None, alias="countryId", description="Country UUID")
    country_skip_zip_code_verification: Optional[bool] = Field(
        None, alias="countrySkipZipCodeVerification", description="Skip ZIP code verification"
    )
    zip_code_resolving_failed: Optional[bool] = Field(
        None, alias="zipCodeResolvingFailed", description="ZIP code resolution failed"
    )
    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")
    full_city_line: Optional[str] = Field(None, alias="fullCityLine", description="Formatted city/state/zip line")
    coordinates: Optional[Coordinates] = Field(None, description="GPS coordinates object")
    address1: Optional[str] = Field(None, description="Primary address line")
    address2: Optional[str] = Field(None, description="Secondary address line")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State/province code")
    zip_code: Optional[str] = Field(None, alias="zipCode", description="ZIP/postal code")
