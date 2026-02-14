"""Address models for the ACPortal API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import ResponseModel


class AddressIsValidResult(ResponseModel):
    """Result from GET /address/isvalid."""

    is_valid: Optional[bool] = Field(None, alias="isValid", description="Whether address is valid")
    validated_address: Optional[dict] = Field(
        None, alias="validatedAddress", description="Corrected/validated address"
    )
    suggestions: Optional[List[dict]] = Field(None, description="Alternative suggestions")


class PropertyType(ResponseModel):
    """Result from GET /address/propertytype."""

    property_type: Optional[str] = Field(None, alias="propertyType", description="Property type classification")
    confidence: Optional[float] = Field(None, description="Confidence score")
