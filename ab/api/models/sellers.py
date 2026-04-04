"""Seller models for the Catalog API.

Field shapes ported against ``ab/api/schemas/catalog.json`` (swagger,
Tier 3) with ``ABConnectTools/ABConnect/api/models/catalog.py`` as
secondary reference. The prior placeholder had an invented
``display_id`` field; swagger defines ``SellerDto`` as
``{id, name, customerDisplayId, isActive}``. Captured
``SellerExpandedDto`` fixtures show the real API also returns an
always-null ``displayId`` key not declared in swagger — kept as an
optional field on the response models to absorb the drift without
failing ``assert_no_extra_fields``.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class SellerDto(ResponseModel):
    """Seller summary — returned by ``POST /Seller``, ``PUT /Seller/{id}``,
    and embedded in ``CatalogWithSellersDto.sellers``."""

    id: int = Field(..., description="Seller ID")
    name: Optional[str] = Field(None, description="Seller name")
    customer_display_id: Optional[int] = Field(
        None, alias="customerDisplayId", description="Customer-facing display ID",
    )
    is_active: Optional[bool] = Field(None, alias="isActive", description="Whether seller is active")
    # Not in swagger but returned as always-null by the real API.
    # Kept to absorb the drift without failing `assert_no_extra_fields`.
    display_id: Optional[str] = Field(
        None, alias="displayId",
        description="Deprecated display identifier — always null per captured responses",
    )


class SellerExpandedDto(SellerDto):
    """Seller with embedded catalog associations — returned by
    ``GET /Seller/{id}``."""

    # Typed as ``List[dict]`` rather than ``List[CatalogDto]`` to avoid a
    # circular import with ``catalog.py`` (which imports ``SellerDto`` from
    # this module). Tighten to ``CatalogDto`` if both models move into a
    # shared sub-module later.
    catalogs: Optional[List[dict]] = Field(None, description="Associated catalogs")


class AddSellerRequest(RequestModel):
    """Body for ``POST /Seller``."""

    name: Optional[str] = Field(None, description="Seller name")
    customer_display_id: int = Field(..., alias="customerDisplayId", description="Customer display ID")
    is_active: bool = Field(..., alias="isActive", description="Whether the seller is active")


class UpdateSellerRequest(AddSellerRequest):
    """Body for ``PUT /Seller/{id}``. Same shape as :class:`AddSellerRequest`."""


class SellerListParams(RequestModel):
    """Query parameters for ``GET /Seller``."""

    id: Optional[int] = Field(None, alias="Id", description="Filter by seller ID")
    name: Optional[str] = Field(None, alias="Name", description="Filter by seller name")
    customer_display_id: Optional[int] = Field(
        None, alias="CustomerDisplayId", description="Filter by customer display ID",
    )
    is_active: Optional[bool] = Field(None, alias="IsActive", description="Filter by active status")
    page_size: Optional[int] = Field(None, alias="PageSize", description="Number of items per page")
    page_number: Optional[int] = Field(None, alias="PageNumber", description="Page number")
