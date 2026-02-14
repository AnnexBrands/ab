"""Companies API endpoints (8 routes)."""

from __future__ import annotations

from typing import Any, List, Optional

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

    def update_fulldetails(self, company_id: str, data: dict | Any) -> Any:
        """PUT /companies/{companyId}/fulldetails"""
        return self._request(_UPDATE_FULLDETAILS.bind(companyId=self._resolve(company_id)), json=data)

    def create(self, data: dict | Any) -> Any:
        """POST /companies/fulldetails — returns new company ID string."""
        return self._request(_CREATE, json=data)

    def search(self, data: dict | Any) -> Any:
        """POST /companies/search/v2"""
        return self._request(_SEARCH, json=data)

    def list(self, data: dict | Any) -> Any:
        """POST /companies/list"""
        return self._request(_LIST, json=data)

    def available_by_current_user(self) -> Any:
        """GET /companies/availableByCurrentUser"""
        return self._request(_AVAILABLE)
