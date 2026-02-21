"""Catalog API endpoints (6 routes)."""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

# Routes — Catalog API surface
_CREATE = Route(
    "POST", "/Catalog",
    request_model="AddCatalogRequest", response_model="CatalogWithSellersDto", api_surface="catalog",
)
_LIST = Route("GET", "/Catalog", response_model="PaginatedList[CatalogExpandedDto]", api_surface="catalog")
_GET = Route("GET", "/Catalog/{id}", response_model="CatalogExpandedDto", api_surface="catalog")
_UPDATE = Route(
    "PUT", "/Catalog/{id}",
    request_model="UpdateCatalogRequest", response_model="CatalogWithSellersDto", api_surface="catalog",
)
_DELETE = Route("DELETE", "/Catalog/{id}", api_surface="catalog")
_BULK_INSERT = Route("POST", "/Bulk/insert", request_model="BulkInsertRequest", api_surface="catalog")


class CatalogEndpoint(BaseEndpoint):
    """Operations on catalogs (Catalog API)."""

    def create(self, data: dict | Any) -> Any:
        """POST /Catalog — create a new catalog."""
        return self._request(_CREATE, json=data)

    def list(self, *, page: int = 1, page_size: int = 25) -> Any:
        """GET /Catalog — paginated list of catalogs."""
        return self._paginated_request(
            _LIST, "CatalogExpandedDto",
            params={"pageNumber": page, "pageSize": page_size},
        )

    def get(self, catalog_id: int) -> Any:
        """GET /Catalog/{id}"""
        return self._request(_GET.bind(id=catalog_id))

    def update(self, catalog_id: int, data: dict | Any) -> Any:
        """PUT /Catalog/{id}"""
        return self._request(_UPDATE.bind(id=catalog_id), json=data)

    def delete(self, catalog_id: int) -> None:
        """DELETE /Catalog/{id}"""
        self._request(_DELETE.bind(id=catalog_id))

    def bulk_insert(self, data: dict | Any) -> Any:
        """POST /Bulk/insert"""
        return self._request(_BULK_INSERT, json=data)
