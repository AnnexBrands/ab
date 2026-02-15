"""Commodity models for the ACPortal API."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class Commodity(ResponseModel):
    """Commodity record — GET /commodity/{id}."""

    id: Optional[str] = Field(None, description="Commodity ID")
    description: Optional[str] = Field(None, description="Commodity description")
    freight_class: Optional[str] = Field(None, alias="freightClass", description="Freight class")
    nmfc_code: Optional[str] = Field(None, alias="nmfcCode", description="NMFC code")
    weight_min: Optional[float] = Field(None, alias="weightMin", description="Minimum weight")
    weight_max: Optional[float] = Field(None, alias="weightMax", description="Maximum weight")


class CommodityCreateRequest(RequestModel):
    """Body for POST /commodity."""

    description: str = Field(..., description="Commodity description")
    freight_class: Optional[str] = Field(None, alias="freightClass", description="Freight class")
    nmfc_code: Optional[str] = Field(None, alias="nmfcCode", description="NMFC code")
    weight_min: Optional[float] = Field(None, alias="weightMin", description="Minimum weight")
    weight_max: Optional[float] = Field(None, alias="weightMax", description="Maximum weight")


class CommodityUpdateRequest(RequestModel):
    """Body for PUT /commodity/{id}."""

    description: Optional[str] = Field(None, description="Commodity description")
    freight_class: Optional[str] = Field(None, alias="freightClass", description="Freight class")
    nmfc_code: Optional[str] = Field(None, alias="nmfcCode", description="NMFC code")


class CommoditySearchRequest(RequestModel):
    """Search filter for POST /commodity/search."""

    search_text: Optional[str] = Field(None, alias="searchText", description="Search query")
    page: Optional[int] = Field(None, description="Page number")
    page_size: Optional[int] = Field(None, alias="pageSize", description="Results per page")


class CommoditySuggestionRequest(RequestModel):
    """Suggestion filter for POST /commodity/suggestions."""

    search_text: Optional[str] = Field(None, alias="searchText", description="Search query")


class CommodityMap(ResponseModel):
    """Commodity mapping record — GET /commodity-map/{id}."""

    id: Optional[str] = Field(None, description="Map ID")
    custom_name: Optional[str] = Field(None, alias="customName", description="Custom commodity name")
    commodity_id: Optional[str] = Field(None, alias="commodityId", description="Linked commodity ID")


class CommodityMapCreateRequest(RequestModel):
    """Body for POST /commodity-map."""

    custom_name: str = Field(..., alias="customName", description="Custom commodity name")
    commodity_id: Optional[str] = Field(None, alias="commodityId", description="Linked commodity ID")


class CommodityMapUpdateRequest(RequestModel):
    """Body for PUT /commodity-map/{id}."""

    custom_name: Optional[str] = Field(None, alias="customName", description="Custom commodity name")
    commodity_id: Optional[str] = Field(None, alias="commodityId", description="Linked commodity ID")


class CommodityMapSearchRequest(RequestModel):
    """Search filter for POST /commodity-map/search."""

    search_text: Optional[str] = Field(None, alias="searchText", description="Search query")
    page: Optional[int] = Field(None, description="Page number")
    page_size: Optional[int] = Field(None, alias="pageSize", description="Results per page")
