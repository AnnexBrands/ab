"""Sellers API endpoints (5 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ab.api.models.sellers import SellerDto, SellerExpandedDto
    from ab.api.models.shared import PaginatedList

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_CREATE = Route("POST", "/Seller", request_model="AddSellerRequest", response_model="SellerDto", api_surface="catalog")
_LIST = Route(
    "GET", "/Seller",
    params_model="SellerListParams", response_model="PaginatedList[SellerExpandedDto]", api_surface="catalog",
)
_GET = Route("GET", "/Seller/{id}", response_model="SellerExpandedDto", api_surface="catalog")
_UPDATE = Route(
    "PUT", "/Seller/{id}",
    request_model="UpdateSellerRequest", response_model="SellerDto", api_surface="catalog",
)
_DELETE = Route("DELETE", "/Seller/{id}", api_surface="catalog")


class SellersEndpoint(BaseEndpoint):
    """Operations on sellers (Catalog API)."""

    def create(
        self,
        *,
        name: str | None = None,
        display_id: str | None = None,
    ) -> SellerDto:
        """POST /Seller.

        Args:
            name: Seller name.
            display_id: Display identifier.

        Request model: :class:`AddSellerRequest`
        """
        body = dict(name=name, display_id=display_id)
        return self._request(_CREATE, json=body)

    def list(self, *, page: int = 1, page_size: int = 25) -> PaginatedList[SellerExpandedDto]:
        """GET /Seller — paginated list."""
        return self._paginated_request(
            _LIST, "SellerExpandedDto",
            params={"pageNumber": page, "pageSize": page_size},
        )

    def get(self, seller_id: int) -> SellerExpandedDto:
        """GET /Seller/{id}"""
        return self._request(_GET.bind(id=seller_id))

    def update(
        self,
        seller_id: int,
        *,
        name: str | None = None,
        display_id: str | None = None,
    ) -> SellerDto:
        """PUT /Seller/{id}.

        Args:
            seller_id: Seller identifier.
            name: Updated name.
            display_id: Updated display ID.

        Request model: :class:`UpdateSellerRequest`
        """
        body = dict(name=name, display_id=display_id)
        return self._request(_UPDATE.bind(id=seller_id), json=body)

    def delete(self, seller_id: int) -> None:
        """DELETE /Seller/{id}"""
        self._request(_DELETE.bind(id=seller_id))
