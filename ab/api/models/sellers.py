"""Seller models for the Catalog API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class SellerDto(ResponseModel):
    """Seller summary — returned by create/update."""

    id: Optional[int] = Field(None, description="Seller ID")
    name: Optional[str] = Field(None, description="Seller name")
    display_id: Optional[str] = Field(None, alias="displayId", description="Display identifier")


class SellerExpandedDto(ResponseModel):
    """Seller with catalog associations — returned by GET /Seller/{id}."""

    id: Optional[int] = Field(None, description="Seller ID")
    name: Optional[str] = Field(None, description="Seller name")
    display_id: Optional[str] = Field(None, alias="displayId", description="Display identifier")
    catalogs: Optional[List[dict]] = Field(None, description="Associated catalogs")
    customer_display_id: Optional[int] = Field(None, alias="customerDisplayId", description="Customer display ID")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Whether seller is active")


class AddSellerRequest(RequestModel):
    """Body for POST /Seller."""

    name: str = Field(..., description="Seller name")
    display_id: Optional[str] = Field(None, alias="displayId", description="Display identifier")


class UpdateSellerRequest(RequestModel):
    """Body for PUT /Seller/{id}."""

    name: Optional[str] = Field(None, description="Updated name")
    display_id: Optional[str] = Field(None, alias="displayId", description="Updated display ID")
