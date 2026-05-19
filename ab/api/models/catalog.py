"""Catalog API models.

Field shapes ported against ``ab/api/schemas/catalog.json`` (swagger,
Tier 3) with ``ABConnectTools/ABConnect/api/models/catalog.py`` as
secondary reference (Tier 4). The prior placeholder implementation
had invented field names for ``AddCatalogRequest``,
``UpdateCatalogRequest``, and ``BulkInsertRequest`` that did not match
either source — see ``specs/036-lotsdb-migration-prep/gap-recommendations.md``.

``SellerDto`` is a TYPE_CHECKING-only import to break the
``catalog`` ↔ ``sellers`` circular reference; :func:`_rebuild_catalog_models`
at the bottom of the module does the runtime import and calls
``model_rebuild()`` on any class whose annotations need it.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel
from ab.api.models.lots import LotCatalogInformationDto, LotDataDto

if TYPE_CHECKING:
    from ab.api.models.sellers import SellerDto


class CatalogDto(ResponseModel):
    """Core catalog information — parent of :class:`CatalogWithSellersDto`
    and :class:`CatalogExpandedDto`."""

    id: int = Field(..., description="Catalog ID")
    customer_catalog_id: Optional[str] = Field(
        None, alias="customerCatalogId", description="Customer-facing catalog ID",
    )
    agent: Optional[str] = Field(None, description="Assigned agent code")
    title: Optional[str] = Field(None, description="Catalog title")
    start_date: datetime = Field(..., alias="startDate", description="Catalog start date-time")
    end_date: datetime = Field(..., alias="endDate", description="Catalog end date-time")
    is_completed: bool = Field(..., alias="isCompleted", description="Whether the catalog is completed")


class CatalogWithSellersDto(CatalogDto):
    """Catalog with embedded sellers — returned by ``POST /Catalog`` and
    ``PUT /Catalog/{id}``."""

    sellers: Optional[List["SellerDto"]] = Field(None, description="Attached sellers")


class CatalogExpandedDto(CatalogDto):
    """Catalog with sellers and lot summaries — returned by
    ``GET /Catalog/{id}``."""

    sellers: Optional[List["SellerDto"]] = Field(None, description="Attached sellers")
    lots: Optional[List[LotCatalogInformationDto]] = Field(
        None, description="Lot summaries belonging to the catalog",
    )


class AddCatalogRequest(RequestModel):
    """Body for ``POST /Catalog``.

    ``start_date`` and ``end_date`` are required per swagger (no
    ``nullable: true``). All other fields are optional.
    """

    customer_catalog_id: Optional[str] = Field(
        None, alias="customerCatalogId", description="Customer-facing catalog ID",
    )
    agent: Optional[str] = Field(None, description="Assigned agent code")
    title: Optional[str] = Field(None, description="Catalog title")
    start_date: datetime = Field(..., alias="startDate", description="Catalog start date-time")
    end_date: datetime = Field(..., alias="endDate", description="Catalog end date-time")
    seller_ids: Optional[List[int]] = Field(None, alias="sellerIds", description="Seller IDs to attach")


class UpdateCatalogRequest(AddCatalogRequest):
    """Body for ``PUT /Catalog/{id}``. Same shape as :class:`AddCatalogRequest`
    per swagger."""


class CatalogListParams(RequestModel):
    """Query parameters for ``GET /Catalog``."""

    id: Optional[int] = Field(None, alias="Id", description="Filter by catalog ID")
    customer_catalog_id: Optional[str] = Field(
        None, alias="CustomerCatalogId", description="Filter by customer catalog ID",
    )
    agent: Optional[str] = Field(None, alias="Agent", description="Filter by agent")
    title: Optional[str] = Field(None, alias="Title", description="Filter by title")
    start_date: Optional[str] = Field(None, alias="StartDate", description="Filter by start date (date-time)")
    end_date: Optional[str] = Field(None, alias="EndDate", description="Filter by end date (date-time)")
    is_completed: Optional[bool] = Field(None, alias="IsCompleted", description="Filter by completion status")
    seller_ids: Optional[List[int]] = Field(None, alias="SellerIds", description="Filter by seller IDs")
    page_size: Optional[int] = Field(None, alias="PageSize", description="Number of items per page")
    page_number: Optional[int] = Field(None, alias="PageNumber", description="Page number")


# =============================================================================
# Bulk request models
# =============================================================================


class BulkInsertSellerRequest(RequestModel):
    """Seller entry inside a bulk insert payload."""

    name: Optional[str] = Field(None, description="Seller name")
    customer_display_id: int = Field(..., alias="customerDisplayId", description="Customer display ID")
    is_active: bool = Field(..., alias="isActive", description="Whether the seller is active")


class BulkInsertLotRequest(RequestModel):
    """Lot entry inside a bulk insert payload."""

    customer_item_id: Optional[str] = Field(None, alias="customerItemId", description="Customer item ID")
    lot_number: Optional[str] = Field(None, alias="lotNumber", description="Lot number")
    image_links: Optional[List[str]] = Field(None, alias="imageLinks", description="Image URLs")
    initial_data: Optional[LotDataDto] = Field(None, alias="initialData", description="Initial lot measurements")
    overriden_data: Optional[List[LotDataDto]] = Field(
        None, alias="overridenData", description="Per-catalog override entries",
    )


class BulkInsertCatalogRequest(RequestModel):
    """Catalog entry inside a bulk insert payload. Nests lots and sellers."""

    customer_catalog_id: Optional[str] = Field(None, alias="customerCatalogId", description="Customer catalog ID")
    agent: Optional[str] = Field(None, description="Assigned agent code")
    title: Optional[str] = Field(None, description="Catalog title")
    start_date: datetime = Field(..., alias="startDate", description="Catalog start date-time")
    end_date: datetime = Field(..., alias="endDate", description="Catalog end date-time")
    lots: Optional[List[BulkInsertLotRequest]] = Field(None, description="Lots in this catalog")
    sellers: Optional[List[BulkInsertSellerRequest]] = Field(None, description="Sellers in this catalog")


class BulkInsertRequest(RequestModel):
    """Body for ``POST /Bulk/insert``.

    Per swagger, the top-level payload contains exactly one key —
    ``catalogs`` — a list of :class:`BulkInsertCatalogRequest`. Each
    nested catalog carries its own lots and sellers. This is a nested
    bulk shape, *not* a flat list of rows.
    """

    catalogs: Optional[List[BulkInsertCatalogRequest]] = Field(
        None, description="Catalogs to insert, each with nested lots and sellers",
    )


def _rebuild_catalog_models() -> None:
    """Resolve the TYPE_CHECKING forward reference to ``SellerDto``.

    Deferred because ``sellers.py`` imports :class:`CatalogDto` from
    this module — a real import of ``SellerDto`` at the top of this
    file would create a load-time cycle.
    """
    from ab.api.models.sellers import SellerDto  # noqa: F401

    CatalogWithSellersDto.model_rebuild()
    CatalogExpandedDto.model_rebuild()


_rebuild_catalog_models()
