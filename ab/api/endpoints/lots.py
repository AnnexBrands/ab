"""Lots API endpoints (6 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from ab.api.models.lots import AddLotRequest, LotDto, LotOverrideDto, UpdateLotRequest
    from ab.api.models.shared import PaginatedList

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_CREATE = Route("POST", "/Lot", request_model="AddLotRequest", response_model="LotDto", api_surface="catalog")
_LIST = Route(
    "GET", "/Lot",
    params_model="LotListParams", response_model="PaginatedList[LotDto]", api_surface="catalog",
)
_GET = Route("GET", "/Lot/{id}", response_model="LotDto", api_surface="catalog")
_UPDATE = Route("PUT", "/Lot/{id}", request_model="UpdateLotRequest", response_model="LotDto", api_surface="catalog")
_DELETE = Route("DELETE", "/Lot/{id}", api_surface="catalog")
_GET_OVERRIDES = Route("POST", "/Lot/get-overrides", response_model="List[LotOverrideDto]", api_surface="catalog")


class LotsEndpoint(BaseEndpoint):
    """Operations on lots (Catalog API)."""

    def create(self, *, data: AddLotRequest | dict) -> LotDto:
        """POST /Lot.

        Args:
            data: Lot creation payload with catalog_id, lot_number, and data.
                Accepts an :class:`AddLotRequest` instance or a dict.

        Request model: :class:`AddLotRequest`
        """
        return self._request(_CREATE, json=data)

    def list(self, *, page: int = 1, page_size: int = 25) -> PaginatedList[LotDto]:
        """GET /Lot — paginated list."""
        return self._paginated_request(
            _LIST, "LotDto",
            params={"pageNumber": page, "pageSize": page_size},
        )

    def get(self, lot_id: int) -> LotDto:
        """GET /Lot/{id}"""
        return self._request(_GET.bind(id=lot_id))

    def update(self, lot_id: int, *, data: UpdateLotRequest | dict) -> LotDto:
        """PUT /Lot/{id}.

        Args:
            lot_id: Lot identifier.
            data: Lot update payload with lot_number and data.
                Accepts an :class:`UpdateLotRequest` instance or a dict.

        Request model: :class:`UpdateLotRequest`
        """
        return self._request(_UPDATE.bind(id=lot_id), json=data)

    def delete(self, lot_id: int) -> None:
        """DELETE /Lot/{id}"""
        self._request(_DELETE.bind(id=lot_id))

    def get_overrides(self, customer_item_ids: List[str]) -> list[LotOverrideDto]:
        """POST /Lot/get-overrides"""
        return self._request(_GET_OVERRIDES, json=customer_item_ids)
