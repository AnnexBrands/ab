"""Catalog API endpoints (6 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ab.api.models.catalog import BulkInsertRequest, CatalogExpandedDto, CatalogWithSellersDto
    from ab.api.models.shared import PaginatedList

from ab.api.base import BaseEndpoint
from ab.api.route import Route

# Routes — Catalog API surface
_CREATE = Route(
    "POST", "/Catalog",
    request_model="AddCatalogRequest", response_model="CatalogWithSellersDto", api_surface="catalog",
)
_LIST = Route(
    "GET", "/Catalog",
    params_model="CatalogListParams", response_model="PaginatedList[CatalogExpandedDto]", api_surface="catalog",
)
_GET = Route("GET", "/Catalog/{id}", response_model="CatalogExpandedDto", api_surface="catalog")
_UPDATE = Route(
    "PUT", "/Catalog/{id}",
    request_model="UpdateCatalogRequest", response_model="CatalogWithSellersDto", api_surface="catalog",
)
_DELETE = Route("DELETE", "/Catalog/{id}", api_surface="catalog")
_BULK_INSERT = Route("POST", "/Bulk/insert", request_model="BulkInsertRequest", api_surface="catalog")


class CatalogEndpoint(BaseEndpoint):
    """Operations on catalogs (Catalog API)."""

    def create(
        self,
        *,
        title: str | None = None,
        agent_id: str | None = None,
        seller_ids: list[int] | None = None,
    ) -> CatalogWithSellersDto:
        """POST /Catalog.

        Args:
            title: Catalog title.
            agent_id: Assigned agent ID.
            seller_ids: Seller IDs to attach.

        Request model: :class:`AddCatalogRequest`
        """
        body = dict(title=title, agent_id=agent_id, seller_ids=seller_ids)
        return self._request(_CREATE, json=body)

    def list(self, *, page: int = 1, page_size: int = 25) -> PaginatedList[CatalogExpandedDto]:
        """GET /Catalog — paginated list of catalogs."""
        return self._paginated_request(
            _LIST, "CatalogExpandedDto",
            params={"pageNumber": page, "pageSize": page_size},
        )

    def get(self, catalog_id: int) -> CatalogExpandedDto:
        """GET /Catalog/{id}"""
        return self._request(_GET.bind(id=catalog_id))

    def update(
        self,
        catalog_id: int,
        *,
        title: str | None = None,
        agent_id: str | None = None,
        seller_ids: list[int] | None = None,
    ) -> CatalogWithSellersDto:
        """PUT /Catalog/{id}.

        Args:
            catalog_id: Catalog identifier.
            title: Updated title.
            agent_id: Updated agent ID.
            seller_ids: Updated seller IDs.

        Request model: :class:`UpdateCatalogRequest`
        """
        body = dict(title=title, agent_id=agent_id, seller_ids=seller_ids)
        return self._request(_UPDATE.bind(id=catalog_id), json=body)

    def delete(self, catalog_id: int) -> None:
        """DELETE /Catalog/{id}"""
        self._request(_DELETE.bind(id=catalog_id))

    def bulk_insert(self, *, data: BulkInsertRequest | dict) -> Any:
        """POST /Bulk/insert.

        Args:
            data: Bulk insert payload with catalog_id and items.
                Accepts a :class:`BulkInsertRequest` instance or a dict.

        Request model: :class:`BulkInsertRequest`
        """
        return self._request(_BULK_INSERT, json=data)
