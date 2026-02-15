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
    """Single result from GET /companies/availableByCurrentUser.

    The live API returns ``companyName`` and ``name`` (both present),
    plus ``typeId`` and ``parentCompanyId``.
    """

    id: Optional[str] = Field(None, description="Company UUID")
    code: Optional[str] = Field(None, description="Company code")
    company_name: Optional[str] = Field(None, alias="companyName", description="Full company name")
    name: Optional[str] = Field(None, description="Company name")
    type_id: Optional[str] = Field(None, alias="typeId", description="Company type UUID")
    parent_company_id: Optional[str] = Field(None, alias="parentCompanyId", description="Parent company UUID")


class CompanySearchRequest(RequestModel):
    """Body for POST /companies/search/v2."""

    search_text: Optional[str] = Field(None, alias="searchText", description="Search query")
    page: int = Field(1, description="Page number")
    page_size: int = Field(25, alias="pageSize", description="Results per page")
    filters: Optional[dict] = Field(None, description="Filter criteria")


# ---- Extended company models (008) ----------------------------------------


class CompanyBrand(ResponseModel):
    """Brand record — GET /companies/brands."""

    id: Optional[str] = Field(None, description="Brand ID")
    name: Optional[str] = Field(None, description="Brand name")
    parent_id: Optional[str] = Field(None, alias="parentId", description="Parent brand ID")


class BrandTree(ResponseModel):
    """Hierarchical brand tree — GET /companies/brandstree."""

    id: Optional[str] = Field(None, description="Brand ID")
    name: Optional[str] = Field(None, description="Brand name")
    children: Optional[List[dict]] = Field(None, description="Child brands")


class GeoSettings(ResponseModel):
    """Geographic settings — GET /companies/{companyId}/geosettings."""

    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID")
    service_areas: Optional[List[dict]] = Field(None, alias="serviceAreas", description="Service area definitions")
    restrictions: Optional[List[dict]] = Field(None, description="Geographic restrictions")


class GeoSettingsSaveRequest(RequestModel):
    """Body for POST /companies/{companyId}/geosettings."""

    service_areas: Optional[List[dict]] = Field(None, alias="serviceAreas", description="Service area definitions")
    restrictions: Optional[List[dict]] = Field(None, description="Geographic restrictions")


class CarrierAccount(ResponseModel):
    """Carrier account — GET /companies/{companyId}/carrierAcounts."""

    id: Optional[str] = Field(None, description="Carrier account ID")
    carrier_name: Optional[str] = Field(None, alias="carrierName", description="Carrier name")
    account_number: Optional[str] = Field(None, alias="accountNumber", description="Account number")


class CarrierAccountSaveRequest(RequestModel):
    """Body for POST /companies/{companyId}/carrierAcounts."""

    carrier_name: Optional[str] = Field(None, alias="carrierName", description="Carrier name")
    account_number: Optional[str] = Field(None, alias="accountNumber", description="Account number")


class PackagingSettings(ResponseModel):
    """Packaging config — GET /companies/{companyId}/packagingsettings."""

    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID")
    settings: Optional[dict] = Field(None, description="Packaging settings data")


class PackagingLabor(ResponseModel):
    """Packaging labor config — GET /companies/{companyId}/packaginglabor."""

    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID")
    labor_rates: Optional[List[dict]] = Field(None, alias="laborRates", description="Labor rate entries")


class PackagingTariff(ResponseModel):
    """Inherited packaging tariff — GET /companies/{companyId}/inheritedPackagingTariffs."""

    tariff_id: Optional[str] = Field(None, alias="tariffId", description="Tariff ID")
    rates: Optional[List[dict]] = Field(None, description="Tariff rate entries")
