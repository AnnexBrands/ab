"""Catalog API models."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class CatalogWithSellersDto(ResponseModel):
    """Full catalog with embedded sellers — returned by create/update."""

    id: Optional[int] = Field(None, description="Catalog ID")
    title: Optional[str] = Field(None, description="Catalog title")
    agent_id: Optional[str] = Field(None, alias="agentId", description="Assigned agent ID")
    sellers: Optional[List[dict]] = Field(None, description="Seller list")
    lots: Optional[List[dict]] = Field(None, description="Lot list")


class CatalogExpandedDto(ResponseModel):
    """Catalog summary with seller/lot counts — returned by GET /Catalog/{id}."""

    id: Optional[int] = Field(None, description="Catalog ID")
    customer_catalog_id: Optional[str] = Field(None, alias="customerCatalogId", description="Customer-facing catalog ID")
    agent: Optional[str] = Field(None, alias="agent", description="Assigned agent")
    title: Optional[str] = Field(None, description="Catalog title")
    start_date: Optional[str] = Field(None, alias="startDate", description="Catalog start date-time")
    end_date: Optional[str] = Field(None, alias="endDate", description="Catalog end date-time")
    is_completed: Optional[bool] = Field(None, alias="isCompleted", description="Whether the catalog is completed")
    sellers: Optional[List[dict]] = Field(None, description="Seller summaries")
    lots: Optional[list] = Field(None, alias="lots", description="Lot catalog information list")
    lot_count: Optional[int] = Field(None, alias="lotCount", description="Number of lots")
    status: Optional[str] = Field(None, description="Catalog status")


class AddCatalogRequest(RequestModel):
    """Body for POST /Catalog."""

    title: Optional[str] = Field(None, description="Catalog title")
    agent_id: Optional[str] = Field(None, alias="agentId", description="Assigned agent ID")
    seller_ids: Optional[List[int]] = Field(None, alias="sellerIds", description="Seller IDs to attach")


class UpdateCatalogRequest(RequestModel):
    """Body for PUT /Catalog/{id}."""

    title: Optional[str] = Field(None, description="Updated title")
    agent_id: Optional[str] = Field(None, alias="agentId", description="Updated agent ID")
    seller_ids: Optional[List[int]] = Field(None, alias="sellerIds", description="Updated seller IDs")


class CatalogListParams(RequestModel):
    """Query parameters for GET /Catalog."""

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


class BulkInsertRequest(RequestModel):
    """Body for POST /Bulk/insert."""

    catalog_id: Optional[int] = Field(None, alias="catalogId", description="Target catalog ID")
    items: Optional[List[dict]] = Field(None, description="Items to insert")
