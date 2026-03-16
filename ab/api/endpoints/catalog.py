"""Catalog API endpoints (6 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.catalog import AddCatalogRequest, BulkInsertRequest, CatalogExpandedDto, CatalogWithSellersDto, UpdateCatalogRequest
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

    def create(self, *, data: AddCatalogRequest | dict) -> CatalogWithSellersDto:
        """POST /Catalog.

        Args:
            data: Catalog creation payload.
                Accepts an :class:`AddCatalogRequest` instance or a dict.

        Request model: :class:`AddCatalogRequest`
        """
        return self._request(_CREATE, json=data)

    def list(
        self,
        *,
        id: int | None = None,
        customer_catalog_id: str | None = None,
        agent: str | None = None,
        title: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        is_completed: bool | None = None,
        seller_ids: list[int] | None = None,
        page_size: int = 25,
        page_number: int = 1,
    ) -> PaginatedList[CatalogExpandedDto]:
        """List catalogs with optional filters.

        Args:
            id: Filter by catalog ID.
            customer_catalog_id: Filter by customer-facing catalog ID.
            agent: Filter by assigned agent name.
            title: Filter by catalog title.
            start_date: Filter by start date (ISO 8601 date-time string).
            end_date: Filter by end date (ISO 8601 date-time string).
            is_completed: Filter by completion status.
            seller_ids: Filter by seller IDs.
            page_size: Number of items per page.
            page_number: Page number (1-based).

        Returns:
            PaginatedList[CatalogExpandedDto]: Paginated catalog results.
        """
        params = {
            "id": id,
            "customer_catalog_id": customer_catalog_id,
            "agent": agent,
            "title": title,
            "start_date": start_date,
            "end_date": end_date,
            "is_completed": is_completed,
            "seller_ids": seller_ids,
            "page_size": page_size,
            "page_number": page_number,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._paginated_request(_LIST, "CatalogExpandedDto", params=params)

    def get(self, catalog_id: int) -> CatalogExpandedDto:
        """Retrieve a single catalog by ID.

        Args:
            catalog_id: Catalog identifier.

        Returns:
            CatalogExpandedDto: Catalog details with seller/lot counts.
        """
        return self._request(_GET.bind(id=catalog_id))

    def update(self, catalog_id: int, *, data: UpdateCatalogRequest | dict) -> CatalogWithSellersDto:
        """PUT /Catalog/{id}.

        Args:
            catalog_id: Catalog identifier.
            data: Catalog update payload.
                Accepts an :class:`UpdateCatalogRequest` instance or a dict.

        Request model: :class:`UpdateCatalogRequest`
        """
        return self._request(_UPDATE.bind(id=catalog_id), json=data)

    def delete(self, catalog_id: int) -> None:
        """Delete a catalog.

        Args:
            catalog_id: Catalog identifier.
        """
        self._request(_DELETE.bind(id=catalog_id))

    def bulk_insert(self, *, data: BulkInsertRequest | dict) -> None:
        """POST /Bulk/insert.

        Args:
            data: Bulk insert payload with catalog_id and items.
                Accepts a :class:`BulkInsertRequest` instance or a dict.

        Request model: :class:`BulkInsertRequest`
        """
        return self._request(_BULK_INSERT, json=data)
