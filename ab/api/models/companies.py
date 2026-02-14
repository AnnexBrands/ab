"""Company models for the ACPortal API."""

from __future__ import annotations

from typing import Any, List, Optional, Union

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel
from ab.api.models.mixins import FullAuditModel


class CompanySimple(ResponseModel):
    """Lightweight company record — GET /companies/{id}."""

    id: Optional[str] = Field(None, description="Company UUID")
    name: Optional[str] = Field(None, description="Company name")
    code: Optional[str] = Field(None, description="Short company code")
    company_type: Optional[str] = Field(None, alias="companyType", description="Company type")


class CompanyDetails(ResponseModel):
    """Full company details — GET /companies/{id}/fulldetails.

    The live API nests most data under ``details`` and ``preferences``;
    ``capabilities`` is an integer bitmask (not a dict as swagger implies).
    """

    id: Optional[str] = Field(None, description="Company UUID")
    details: Optional[dict] = Field(None, description="Nested company detail fields")
    preferences: Optional[dict] = Field(None, description="Company preferences and logos")
    # swagger says dict; reality is an int bitmask
    capabilities: Optional[Union[int, dict]] = Field(None, description="Service capabilities (bitmask or dict)")
    settings: Optional[dict] = Field(None, description="Company settings")
    addresses: Optional[List[dict]] = Field(None, description="Associated addresses")
    contacts: Optional[List[dict]] = Field(None, description="Associated contacts")


class SearchCompanyResponse(ResponseModel):
    """Single result from POST /companies/search/v2."""

    id: Optional[str] = Field(None, description="Company UUID")
    name: Optional[str] = Field(None, description="Company name")
    code: Optional[str] = Field(None, description="Company code")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")


class CompanySearchRequest(RequestModel):
    """Body for POST /companies/search/v2."""

    search_text: Optional[str] = Field(None, alias="searchText", description="Search query")
    page: int = Field(1, description="Page number")
    page_size: int = Field(25, alias="pageSize", description="Results per page")
    filters: Optional[dict] = Field(None, description="Filter criteria")
