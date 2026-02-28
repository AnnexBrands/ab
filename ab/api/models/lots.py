"""Lot models for the Catalog API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class LotDataDto(ResponseModel):
    """Nested data payload within a lot."""

    qty: Optional[int] = Field(None, description="Quantity")
    length: Optional[float] = Field(None, alias="l", description="Length")
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
    catalogs: Optional[list] = Field(None, alias="catalogs", description="Associated catalogs")
    image_links: Optional[list] = Field(None, alias="imageLinks", description="Image links")
    initial_data: Optional[LotDataDto] = Field(None, alias="initialData", description="Initial lot data")
    overriden_data: Optional[List[LotDataDto]] = Field(
        None, alias="overridenData", description="Overridden lot data entries",
    )


class LotOverrideDto(ResponseModel):
    """Override data for a lot item."""

    customer_item_id: Optional[str] = Field(None, alias="customerItemId", description="Customer item ID")
    overrides: Optional[dict] = Field(None, description="Override key-value pairs")


class AddLotRequest(RequestModel):
    """Body for POST /Lot."""

    catalog_id: Optional[int] = Field(None, alias="catalogId", description="Parent catalog ID")
    lot_number: Optional[str] = Field(None, alias="lotNumber", description="Lot number")
    data: Optional[dict] = Field(None, description="Lot data payload")


class UpdateLotRequest(RequestModel):
    """Body for PUT /Lot/{id}."""

    lot_number: Optional[str] = Field(None, alias="lotNumber", description="Updated lot number")
    data: Optional[dict] = Field(None, description="Updated lot data")


class LotListParams(RequestModel):
    """Query parameters for GET /Lot."""

    id: Optional[int] = Field(None, alias="Id", description="Filter by lot ID")
    customer_item_id: Optional[str] = Field(None, alias="CustomerItemId", description="Filter by customer item ID")
    lot_number: Optional[str] = Field(None, alias="LotNumber", description="Filter by lot number")
    page_size: Optional[int] = Field(None, alias="PageSize", description="Number of items per page")
    page_number: Optional[int] = Field(None, alias="PageNumber", description="Page number")
