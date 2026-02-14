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
    title: Optional[str] = Field(None, description="Catalog title")
    sellers: Optional[List[dict]] = Field(None, description="Seller summaries")
    lot_count: Optional[int] = Field(None, alias="lotCount", description="Number of lots")
    status: Optional[str] = Field(None, description="Catalog status")


class AddCatalogRequest(RequestModel):
    """Body for POST /Catalog."""

    title: str = Field(..., description="Catalog title")
    agent_id: Optional[str] = Field(None, alias="agentId", description="Assigned agent ID")
    seller_ids: Optional[List[int]] = Field(None, alias="sellerIds", description="Seller IDs to attach")


class UpdateCatalogRequest(RequestModel):
    """Body for PUT /Catalog/{id}."""

    title: Optional[str] = Field(None, description="Updated title")
    agent_id: Optional[str] = Field(None, alias="agentId", description="Updated agent ID")
    seller_ids: Optional[List[int]] = Field(None, alias="sellerIds", description="Updated seller IDs")


class BulkInsertRequest(RequestModel):
    """Body for POST /Bulk/insert."""

    catalog_id: int = Field(..., alias="catalogId", description="Target catalog ID")
    items: List[dict] = Field(default_factory=list, description="Items to insert")
