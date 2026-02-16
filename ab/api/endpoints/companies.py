"""Companies API endpoints (31 routes)."""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route
from ab.cache import CodeResolver

_GET = Route("GET", "/companies/{id}", response_model="CompanySimple")
_GET_DETAILS = Route("GET", "/companies/{companyId}/details", response_model="CompanyDetails")
_GET_FULLDETAILS = Route("GET", "/companies/{companyId}/fulldetails", response_model="CompanyDetails")
_UPDATE_FULLDETAILS = Route("PUT", "/companies/{companyId}/fulldetails", request_model="CompanyDetails", response_model="CompanyDetails")
_CREATE = Route("POST", "/companies/fulldetails", request_model="CompanyDetails", response_model="str")
_SEARCH = Route("POST", "/companies/search/v2", request_model="CompanySearchRequest", response_model="List[SearchCompanyResponse]")
_LIST = Route("POST", "/companies/list", request_model="ListRequest", response_model="List[CompanySimple]")
_AVAILABLE = Route("GET", "/companies/availableByCurrentUser", response_model="List[CompanySimple]")

# Brands (008)
_GET_BRANDS = Route("GET", "/companies/brands", response_model="List[CompanyBrand]")
_GET_BRANDS_TREE = Route("GET", "/companies/brandstree", response_model="List[BrandTree]")

# Geo Settings (008)
_GET_GEO_AREA_COMPANIES = Route("GET", "/companies/geoAreaCompanies")
_GET_GEO_SETTINGS = Route("GET", "/companies/{companyId}/geosettings", response_model="GeoSettings")
_SAVE_GEO_SETTINGS = Route("POST", "/companies/{companyId}/geosettings", request_model="GeoSettingsSaveRequest")
_GET_GLOBAL_GEO_SETTINGS = Route("GET", "/companies/geosettings", response_model="GeoSettings")

# Carrier Accounts (008)
_SEARCH_CARRIER_ACCOUNTS = Route("GET", "/companies/search/carrier-accounts")
_SUGGEST_CARRIERS = Route("GET", "/companies/suggest-carriers")
_GET_CARRIER_ACCOUNTS = Route("GET", "/companies/{companyId}/carrierAcounts", response_model="List[CarrierAccount]")
_SAVE_CARRIER_ACCOUNTS = Route(
    "POST", "/companies/{companyId}/carrierAcounts",
    request_model="CarrierAccountSaveRequest",
)

# Packaging (008)
_GET_PACKAGING_SETTINGS = Route("GET", "/companies/{companyId}/packagingsettings", response_model="PackagingSettings")
_SAVE_PACKAGING_SETTINGS = Route("POST", "/companies/{companyId}/packagingsettings")
_GET_PACKAGING_LABOR = Route("GET", "/companies/{companyId}/packaginglabor", response_model="PackagingLabor")
_SAVE_PACKAGING_LABOR = Route("POST", "/companies/{companyId}/packaginglabor")
_GET_INHERITED_PACKAGING_TARIFFS = Route(
    "GET", "/companies/{companyId}/inheritedPackagingTariffs",
    response_model="List[PackagingTariff]",
)
_GET_INHERITED_PACKAGING_LABOR = Route(
    "GET", "/companies/{companyId}/inheritedpackaginglabor",
    response_model="PackagingLabor",
)


# Extended companies routes (009)
_POST_FILTERED_CUSTOMERS = Route("POST", "/companies/filteredCustomers")
_GET_INFO_FROM_KEY = Route("GET", "/companies/infoFromKey")
_GET_SEARCH_COMPANIES = Route("GET", "/companies/search")
_POST_SIMPLE_LIST = Route("POST", "/companies/simplelist")
_GET_CAPABILITIES = Route("GET", "/companies/{companyId}/capabilities")
_POST_CAPABILITIES = Route("POST", "/companies/{companyId}/capabilities")
_GET_FRANCHISEE_ADDRESSES = Route("GET", "/companies/{companyId}/franchiseeAddresses")


class CompaniesEndpoint(BaseEndpoint):
    """Operations on companies (ACPortal API)."""

    def __init__(self, client: Any, resolver: CodeResolver) -> None:
        super().__init__(client)
        self._resolver = resolver

    def _resolve(self, code_or_id: str) -> str:
        return self._resolver.resolve(code_or_id)

    def get_by_id(self, company_id: str) -> Any:
        """GET /companies/{id}"""
        return self._request(_GET.bind(id=self._resolve(company_id)))

    def get_details(self, company_id: str) -> Any:
        """GET /companies/{companyId}/details"""
        return self._request(_GET_DETAILS.bind(companyId=self._resolve(company_id)))

    def get_fulldetails(self, company_id: str) -> Any:
        """GET /companies/{companyId}/fulldetails"""
        return self._request(_GET_FULLDETAILS.bind(companyId=self._resolve(company_id)))

    def update_fulldetails(self, company_id: str, **kwargs: Any) -> Any:
        """PUT /companies/{companyId}/fulldetails"""
        return self._request(_UPDATE_FULLDETAILS.bind(companyId=self._resolve(company_id)), json=kwargs)

    def create(self, **kwargs: Any) -> Any:
        """POST /companies/fulldetails — returns new company ID string."""
        return self._request(_CREATE, json=kwargs)

    def search(self, **kwargs: Any) -> Any:
        """POST /companies/search/v2"""
        return self._request(_SEARCH, json=kwargs)

    def list(self, **kwargs: Any) -> Any:
        """POST /companies/list"""
        return self._request(_LIST, json=kwargs)

    def available_by_current_user(self) -> Any:
        """GET /companies/availableByCurrentUser"""
        return self._request(_AVAILABLE)

    # ---- Brands (008) -----------------------------------------------------

    def get_brands(self) -> Any:
        """GET /companies/brands"""
        return self._request(_GET_BRANDS)

    def get_brands_tree(self) -> Any:
        """GET /companies/brandstree"""
        return self._request(_GET_BRANDS_TREE)

    # ---- Geo Settings (008) -----------------------------------------------

    def get_geo_area_companies(self, **params: Any) -> Any:
        """GET /companies/geoAreaCompanies"""
        return self._request(_GET_GEO_AREA_COMPANIES, params=params or None)

    def get_geo_settings(self, company_id: str) -> Any:
        """GET /companies/{companyId}/geosettings"""
        return self._request(_GET_GEO_SETTINGS.bind(companyId=self._resolve(company_id)))

    def save_geo_settings(self, company_id: str, **kwargs: Any) -> Any:
        """POST /companies/{companyId}/geosettings"""
        return self._request(_SAVE_GEO_SETTINGS.bind(companyId=self._resolve(company_id)), json=kwargs)

    def get_global_geo_settings(self) -> Any:
        """GET /companies/geosettings"""
        return self._request(_GET_GLOBAL_GEO_SETTINGS)

    # ---- Carrier Accounts (008) -------------------------------------------

    def search_carrier_accounts(self, **params: Any) -> Any:
        """GET /companies/search/carrier-accounts"""
        return self._request(_SEARCH_CARRIER_ACCOUNTS, params=params or None)

    def suggest_carriers(self, **params: Any) -> Any:
        """GET /companies/suggest-carriers"""
        return self._request(_SUGGEST_CARRIERS, params=params or None)

    def get_carrier_accounts(self, company_id: str) -> Any:
        """GET /companies/{companyId}/carrierAcounts"""
        return self._request(_GET_CARRIER_ACCOUNTS.bind(companyId=self._resolve(company_id)))

    def save_carrier_accounts(self, company_id: str, **kwargs: Any) -> Any:
        """POST /companies/{companyId}/carrierAcounts"""
        return self._request(_SAVE_CARRIER_ACCOUNTS.bind(companyId=self._resolve(company_id)), json=kwargs)

    # ---- Packaging (008) --------------------------------------------------

    def get_packaging_settings(self, company_id: str) -> Any:
        """GET /companies/{companyId}/packagingsettings"""
        return self._request(_GET_PACKAGING_SETTINGS.bind(companyId=self._resolve(company_id)))

    def save_packaging_settings(self, company_id: str, **kwargs: Any) -> Any:
        """POST /companies/{companyId}/packagingsettings"""
        return self._request(_SAVE_PACKAGING_SETTINGS.bind(companyId=self._resolve(company_id)), json=kwargs)

    def get_packaging_labor(self, company_id: str) -> Any:
        """GET /companies/{companyId}/packaginglabor"""
        return self._request(_GET_PACKAGING_LABOR.bind(companyId=self._resolve(company_id)))

    def save_packaging_labor(self, company_id: str, **kwargs: Any) -> Any:
        """POST /companies/{companyId}/packaginglabor"""
        return self._request(_SAVE_PACKAGING_LABOR.bind(companyId=self._resolve(company_id)), json=kwargs)

    def get_inherited_packaging_tariffs(self, company_id: str) -> Any:
        """GET /companies/{companyId}/inheritedPackagingTariffs"""
        return self._request(_GET_INHERITED_PACKAGING_TARIFFS.bind(companyId=self._resolve(company_id)))

    def get_inherited_packaging_labor(self, company_id: str) -> Any:
        """GET /companies/{companyId}/inheritedpackaginglabor"""
        return self._request(_GET_INHERITED_PACKAGING_LABOR.bind(companyId=self._resolve(company_id)))

    # ---- Extended (009) -----------------------------------------------------

    def filtered_customers(self, **kwargs: Any) -> Any:
        """POST /companies/filteredCustomers"""
        return self._request(_POST_FILTERED_CUSTOMERS, json=kwargs)

    def info_from_key(self, **params: Any) -> Any:
        """GET /companies/infoFromKey"""
        return self._request(_GET_INFO_FROM_KEY, params=params)

    def search_companies(self, **params: Any) -> Any:
        """GET /companies/search"""
        return self._request(_GET_SEARCH_COMPANIES, params=params)

    def simple_list(self, **kwargs: Any) -> Any:
        """POST /companies/simplelist"""
        return self._request(_POST_SIMPLE_LIST, json=kwargs)

    def get_capabilities(self, company_id: str) -> Any:
        """GET /companies/{companyId}/capabilities"""
        return self._request(_GET_CAPABILITIES.bind(companyId=self._resolve(company_id)))

    def save_capabilities(self, company_id: str, **kwargs: Any) -> Any:
        """POST /companies/{companyId}/capabilities"""
        return self._request(_POST_CAPABILITIES.bind(companyId=self._resolve(company_id)), json=kwargs)

    def get_franchisee_addresses(self, company_id: str) -> Any:
        """GET /companies/{companyId}/franchiseeAddresses"""
        return self._request(_GET_FRANCHISEE_ADDRESSES.bind(companyId=self._resolve(company_id)))
