"""Partner models for the ACPortal API."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class Partner(ResponseModel):
    """Partner record — GET /partner/{id}."""

    id: Optional[str] = Field(None, description="Partner ID")
    name: Optional[str] = Field(None, description="Partner name")
    type: Optional[str] = Field(None, description="Partner type")
    contact_info: Optional[dict] = Field(None, alias="contactInfo", description="Contact information")


class PartnerSearchRequest(RequestModel):
    """Search filter for POST /partner/search."""

    search_text: Optional[str] = Field(None, alias="searchText", description="Search query")
    page: Optional[int] = Field(None, description="Page number")
    page_size: Optional[int] = Field(None, alias="pageSize", description="Results per page")
