"""Sellers API endpoints (5 routes)."""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_CREATE = Route("POST", "/Seller", request_model="AddSellerRequest", response_model="SellerDto", api_surface="catalog")
_LIST = Route("GET", "/Seller", response_model="PaginatedList[SellerExpandedDto]", api_surface="catalog")
_GET = Route("GET", "/Seller/{id}", response_model="SellerExpandedDto", api_surface="catalog")
_UPDATE = Route("PUT", "/Seller/{id}", request_model="UpdateSellerRequest", response_model="SellerDto", api_surface="catalog")
_DELETE = Route("DELETE", "/Seller/{id}", api_surface="catalog")


class SellersEndpoint(BaseEndpoint):
    """Operations on sellers (Catalog API)."""

    def create(self, data: dict | Any) -> Any:
        """POST /Seller"""
        return self._request(_CREATE, json=data)

    def list(self, *, page: int = 1, page_size: int = 25) -> Any:
        """GET /Seller — paginated list."""
        return self._paginated_request(
            _LIST, "SellerExpandedDto",
            params={"pageNumber": page, "pageSize": page_size},
        )

    def get(self, seller_id: int) -> Any:
        """GET /Seller/{id}"""
        return self._request(_GET.bind(id=seller_id))

    def update(self, seller_id: int, data: dict | Any) -> Any:
        """PUT /Seller/{id}"""
        return self._request(_UPDATE.bind(id=seller_id), json=data)

    def delete(self, seller_id: int) -> None:
        """DELETE /Seller/{id}"""
        self._request(_DELETE.bind(id=seller_id))
