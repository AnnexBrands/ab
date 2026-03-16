"""Sellers API endpoints (5 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.sellers import AddSellerRequest, SellerDto, SellerExpandedDto, UpdateSellerRequest
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

    def create(self, *, data: AddSellerRequest | dict) -> SellerDto:
        """POST /Seller.

        Args:
            data: Seller creation payload with name and display_id.
                Accepts an :class:`AddSellerRequest` instance or a dict.

        Request model: :class:`AddSellerRequest`
        """
        return self._request(_CREATE, json=data)

    def list(
        self,
        *,
        id: int | None = None,
        name: str | None = None,
        customer_display_id: int | None = None,
        is_active: bool | None = None,
        page_size: int = 25,
        page_number: int = 1,
    ) -> PaginatedList[SellerExpandedDto]:
        """List sellers with optional filters.

        Args:
            id: Filter by seller ID.
            name: Filter by seller name.
            customer_display_id: Filter by customer display ID.
            is_active: Filter by active status.
            page_size: Number of items per page.
            page_number: Page number (1-based).

        Returns:
            PaginatedList[SellerExpandedDto]: Paginated seller results.
        """
        params = {
            "id": id,
            "name": name,
            "customer_display_id": customer_display_id,
            "is_active": is_active,
            "page_size": page_size,
            "page_number": page_number,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._paginated_request(_LIST, "SellerExpandedDto", params=params)

    def get(self, seller_id: int) -> SellerExpandedDto:
        """Retrieve a single seller by ID.

        Args:
            seller_id: Seller identifier.

        Returns:
            SellerExpandedDto: Seller details with catalog associations.
        """
        return self._request(_GET.bind(id=seller_id))

    def update(self, seller_id: int, *, data: UpdateSellerRequest | dict) -> SellerDto:
        """PUT /Seller/{id}.

        Args:
            seller_id: Seller identifier.
            data: Seller update payload with name and display_id.
                Accepts an :class:`UpdateSellerRequest` instance or a dict.

        Request model: :class:`UpdateSellerRequest`
        """
        return self._request(_UPDATE.bind(id=seller_id), json=data)

    def delete(self, seller_id: int) -> None:
        """Delete a seller.

        Args:
            seller_id: Seller identifier.
        """
        self._request(_DELETE.bind(id=seller_id))
