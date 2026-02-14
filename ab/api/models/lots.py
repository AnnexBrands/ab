"""Lot models for the Catalog API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class LotDataDto(ResponseModel):
    """Nested data payload within a lot."""

    qty: Optional[int] = Field(None, description="Quantity")
    l: Optional[float] = Field(None, description="Length")
    w: Optional[float] = Field(None, description="Width")
    h: Optional[float] = Field(None, description="Height")
    wgt: Optional[float] = Field(None, description="Weight")
    value: Optional[float] = Field(None, description="Declared value")
    description: Optional[str] = Field(None, description="Item description")


class LotDto(ResponseModel):
    """A single lot — returned by CRUD operations."""

    id: Optional[int] = Field(None, description="Lot ID")
    catalog_id: Optional[int] = Field(None, alias="catalogId", description="Parent catalog ID")
    lot_number: Optional[str] = Field(None, alias="lotNumber", description="Lot number")
    customer_item_id: Optional[str] = Field(None, alias="customerItemId", description="Customer item ID")
    data: Optional[LotDataDto] = Field(None, description="Lot data payload")


class LotOverrideDto(ResponseModel):
    """Override data for a lot item."""

    customer_item_id: Optional[str] = Field(None, alias="customerItemId", description="Customer item ID")
    overrides: Optional[dict] = Field(None, description="Override key-value pairs")


class AddLotRequest(RequestModel):
    """Body for POST /Lot."""

    catalog_id: int = Field(..., alias="catalogId", description="Parent catalog ID")
    lot_number: Optional[str] = Field(None, alias="lotNumber", description="Lot number")
    data: Optional[dict] = Field(None, description="Lot data payload")


class UpdateLotRequest(RequestModel):
    """Body for PUT /Lot/{id}."""

    lot_number: Optional[str] = Field(None, alias="lotNumber", description="Updated lot number")
    data: Optional[dict] = Field(None, description="Updated lot data")
