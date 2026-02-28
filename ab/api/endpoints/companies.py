"""Companies API endpoints (24 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route
from ab.cache import CodeResolver

if TYPE_CHECKING:
    from ab.api.models.companies import (
        BrandTree,
        CarrierAccount,
        CarrierAccountSaveRequest,
        CompanyBrand,
        CompanyDetails,
        CompanySearchRequest,
        CompanySimple,
        GeoSettings,
        GeoSettingsParams,
        GeoSettingsSaveRequest,
        InheritFromParams,
        PackagingLabor,
        PackagingLaborSaveRequest,
        PackagingSettings,
        PackagingSettingsSaveRequest,
        PackagingTariff,
        SearchCompanyResponse,
    )
    from ab.api.models.shared import ListRequest

_GET = Route("GET", "/companies/{id}", response_model="CompanySimple")
_GET_DETAILS = Route("GET", "/companies/{companyId}/details", response_model="CompanyDetails")
_GET_FULLDETAILS = Route("GET", "/companies/{companyId}/fulldetails", response_model="CompanyDetails")
_UPDATE_FULLDETAILS = Route(
    "PUT", "/companies/{companyId}/fulldetails",
    request_model="CompanyDetails", response_model="CompanyDetails",
)
_CREATE = Route("POST", "/companies/fulldetails", request_model="CompanyDetails", response_model="str")
_SEARCH = Route(
    "POST", "/companies/search/v2",
    request_model="CompanySearchRequest", response_model="List[SearchCompanyResponse]",
)
_LIST = Route("POST", "/companies/list", request_model="ListRequest", response_model="List[CompanySimple]")
_AVAILABLE = Route("GET", "/companies/availableByCurrentUser", response_model="List[CompanySimple]")

# Brands (008)
_GET_BRANDS = Route("GET", "/companies/brands", response_model="List[CompanyBrand]")
_GET_BRANDS_TREE = Route("GET", "/companies/brandstree", response_model="List[BrandTree]")

# Geo Settings (008)
_GET_GEO_AREA_COMPANIES = Route("GET", "/companies/geoAreaCompanies")
_GET_GEO_SETTINGS = Route("GET", "/companies/{companyId}/geosettings", response_model="GeoSettings")
_SAVE_GEO_SETTINGS = Route("POST", "/companies/{companyId}/geosettings", request_model="GeoSettingsSaveRequest")
_GET_GLOBAL_GEO_SETTINGS = Route(
    "GET", "/companies/geosettings",
    response_model="GeoSettings", params_model="GeoSettingsParams",
)

# Carrier Accounts (008)
_SEARCH_CARRIER_ACCOUNTS = Route(
    "GET", "/companies/search/carrier-accounts", params_model="CarrierAccountSearchParams",
)
_SUGGEST_CARRIERS = Route("GET", "/companies/suggest-carriers", params_model="SuggestCarriersParams")
_GET_CARRIER_ACCOUNTS = Route("GET", "/companies/{companyId}/carrierAcounts", response_model="List[CarrierAccount]")
_SAVE_CARRIER_ACCOUNTS = Route(
    "POST", "/companies/{companyId}/carrierAcounts",
    request_model="CarrierAccountSaveRequest",
)

# Packaging (008)
_GET_PACKAGING_SETTINGS = Route("GET", "/companies/{companyId}/packagingsettings", response_model="PackagingSettings")
_SAVE_PACKAGING_SETTINGS = Route("POST", "/companies/{companyId}/packagingsettings", request_model="PackagingSettingsSaveRequest")
_GET_PACKAGING_LABOR = Route("GET", "/companies/{companyId}/packaginglabor", response_model="PackagingLabor")
_SAVE_PACKAGING_LABOR = Route("POST", "/companies/{companyId}/packaginglabor", request_model="PackagingLaborSaveRequest")
_GET_INHERITED_PACKAGING_TARIFFS = Route(
    "GET", "/companies/{companyId}/inheritedPackagingTariffs",
    response_model="List[PackagingTariff]", params_model="InheritFromParams",
)
_GET_INHERITED_PACKAGING_LABOR = Route(
    "GET", "/companies/{companyId}/inheritedpackaginglabor",
    response_model="PackagingLabor", params_model="InheritFromParams",
)


class CompaniesEndpoint(BaseEndpoint):
    """Operations on companies (ACPortal API)."""

    def __init__(self, client: Any, resolver: CodeResolver) -> None:
        super().__init__(client)
        self._resolver = resolver

    def _resolve(self, code_or_id: str) -> str:
        return self._resolver.resolve(code_or_id)

    def get_by_id(self, company_id: str) -> CompanySimple:
        """GET /companies/{id}"""
        return self._request(_GET.bind(id=self._resolve(company_id)))

    def get_details(self, company_id: str) -> CompanyDetails:
        """GET /companies/{companyId}/details"""
        return self._request(_GET_DETAILS.bind(companyId=self._resolve(company_id)))

    def get_fulldetails(self, company_id: str) -> CompanyDetails:
        """GET /companies/{companyId}/fulldetails"""
        return self._request(_GET_FULLDETAILS.bind(companyId=self._resolve(company_id)))

    def update_fulldetails(self, company_id: str, *, data: CompanyDetails | dict) -> CompanyDetails:
        """PUT /companies/{companyId}/fulldetails.

        Args:
            company_id: Company ID or code.
            data: Full company details payload.
                Accepts a :class:`CompanyDetails` instance or a dict.

        Request model: :class:`CompanyDetails`
        """
        return self._request(
            _UPDATE_FULLDETAILS.bind(companyId=self._resolve(company_id)), json=data,
        )

    def create(self, *, data: CompanyDetails | dict) -> str:
        """POST /companies/fulldetails.

        Args:
            data: Full company details payload.
                Accepts a :class:`CompanyDetails` instance or a dict.

        Request model: :class:`CompanyDetails`
        """
        return self._request(_CREATE, json=data)

    def search(self, *, data: CompanySearchRequest | dict) -> list[SearchCompanyResponse]:
        """POST /companies/search/v2.

        Args:
            data: Search filter with pagination, search text, and filters.
                Accepts a :class:`CompanySearchRequest` instance or a dict.

        Request model: :class:`CompanySearchRequest`
        """
        return self._request(_SEARCH, json=data)

    def list(self, *, data: ListRequest | dict) -> list[CompanySimple]:
        """POST /companies/list.

        Args:
            data: List filter with pagination, sorting, and filters.
                Accepts a :class:`ListRequest` instance or a dict.

        Request model: :class:`ListRequest`
        """
        return self._request(_LIST, json=data)

    def available_by_current_user(self) -> list[CompanySimple]:
        """GET /companies/availableByCurrentUser"""
        return self._request(_AVAILABLE)

    # ---- Brands (008) -----------------------------------------------------

    def get_brands(self) -> list[CompanyBrand]:
        """GET /companies/brands"""
        return self._request(_GET_BRANDS)

    def get_brands_tree(self) -> list[BrandTree]:
        """GET /companies/brandstree"""
        return self._request(_GET_BRANDS_TREE)

    # ---- Geo Settings (008) -----------------------------------------------

    def get_geo_area_companies(self, *, params: dict | None = None) -> Any:
        """GET /companies/geoAreaCompanies.

        Args:
            params: Optional query parameters as a dict.
        """
        return self._request(_GET_GEO_AREA_COMPANIES, params=params)

    def get_geo_settings(self, company_id: str) -> GeoSettings:
        """GET /companies/{companyId}/geosettings"""
        return self._request(_GET_GEO_SETTINGS.bind(companyId=self._resolve(company_id)))

    def save_geo_settings(
        self, company_id: str, *, data: GeoSettingsSaveRequest | dict,
    ) -> Any:
        """POST /companies/{companyId}/geosettings.

        Args:
            company_id: Company ID or code.
            data: Geo settings payload with service_areas and restrictions.
                Accepts a :class:`GeoSettingsSaveRequest` instance or a dict.

        Request model: :class:`GeoSettingsSaveRequest`
        """
        return self._request(
            _SAVE_GEO_SETTINGS.bind(companyId=self._resolve(company_id)), json=data,
        )

    def get_global_geo_settings(self) -> GeoSettings:
        """GET /companies/geosettings"""
        return self._request(_GET_GLOBAL_GEO_SETTINGS)

    # ---- Carrier Accounts (008) -------------------------------------------

    def search_carrier_accounts(
        self,
        *,
        current_company_id: str | None = None,
        query: str | None = None,
    ) -> Any:
        """GET /companies/search/carrier-accounts"""
        return self._request(
            _SEARCH_CARRIER_ACCOUNTS,
            params=dict(current_company_id=current_company_id, query=query),
        )

    def suggest_carriers(self, *, tracking_number: str) -> Any:
        """GET /companies/suggest-carriers"""
        return self._request(_SUGGEST_CARRIERS, params=dict(tracking_number=tracking_number))

    def get_carrier_accounts(self, company_id: str) -> list[CarrierAccount]:
        """GET /companies/{companyId}/carrierAcounts"""
        return self._request(_GET_CARRIER_ACCOUNTS.bind(companyId=self._resolve(company_id)))

    def save_carrier_accounts(self, company_id: str, *, data: CarrierAccountSaveRequest | dict) -> Any:
        """POST /companies/{companyId}/carrierAcounts.

        Args:
            company_id: Company ID or code.
            data: Carrier account payload.
                Accepts a :class:`CarrierAccountSaveRequest` instance or a dict.

        Request model: :class:`CarrierAccountSaveRequest`
        """
        return self._request(
            _SAVE_CARRIER_ACCOUNTS.bind(companyId=self._resolve(company_id)), json=data,
        )

    # ---- Packaging (008) --------------------------------------------------

    def get_packaging_settings(self, company_id: str) -> PackagingSettings:
        """GET /companies/{companyId}/packagingsettings"""
        return self._request(_GET_PACKAGING_SETTINGS.bind(companyId=self._resolve(company_id)))

    def save_packaging_settings(self, company_id: str, *, data: PackagingSettingsSaveRequest | dict) -> Any:
        """POST /companies/{companyId}/packagingsettings.

        Args:
            company_id: Company ID or code.
            data: Packaging settings payload.
                Accepts a :class:`PackagingSettingsSaveRequest` instance or a dict.

        Request model: :class:`PackagingSettingsSaveRequest`
        """
        return self._request(
            _SAVE_PACKAGING_SETTINGS.bind(companyId=self._resolve(company_id)), json=data,
        )

    def get_packaging_labor(self, company_id: str) -> PackagingLabor:
        """GET /companies/{companyId}/packaginglabor"""
        return self._request(_GET_PACKAGING_LABOR.bind(companyId=self._resolve(company_id)))

    def save_packaging_labor(self, company_id: str, *, data: PackagingLaborSaveRequest | dict) -> Any:
        """POST /companies/{companyId}/packaginglabor.

        Args:
            company_id: Company ID or code.
            data: Packaging labor rates payload.
                Accepts a :class:`PackagingLaborSaveRequest` instance or a dict.

        Request model: :class:`PackagingLaborSaveRequest`
        """
        return self._request(
            _SAVE_PACKAGING_LABOR.bind(companyId=self._resolve(company_id)), json=data,
        )

    def get_inherited_packaging_tariffs(self, company_id: str) -> list[PackagingTariff]:
        """GET /companies/{companyId}/inheritedPackagingTariffs"""
        return self._request(_GET_INHERITED_PACKAGING_TARIFFS.bind(companyId=self._resolve(company_id)))

    def get_inherited_packaging_labor(self, company_id: str) -> PackagingLabor:
        """GET /companies/{companyId}/inheritedpackaginglabor"""
        return self._request(_GET_INHERITED_PACKAGING_LABOR.bind(companyId=self._resolve(company_id)))

    # ---- Backwards Compatibility Aliases ------------------------------------

    def get(self, company_id: str) -> CompanyDetails:
        """Alias for :meth:`get_fulldetails`."""
        return self.get_fulldetails(company_id)

    def available(self) -> list[CompanySimple]:
        """Alias for :meth:`available_by_current_user`."""
        return self.available_by_current_user()
