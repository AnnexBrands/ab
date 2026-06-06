"""Lots API endpoints (6 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

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
            data: Lot creation payload with ``customer_item_id``,
                ``image_links``, ``initial_data`` (a :class:`LotDataDto`
                with the measurements), ``catalogs`` (list of
                :class:`LotCatalogDto`), and ``overriden_data``.
                Accepts an :class:`AddLotRequest` instance or a dict.

        Request model: :class:`AddLotRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lots/create.html
        Request model: AddLotRequest
        Response model: LotDto
        """
        return self._request(_CREATE, json=data)

    def list(
        self,
        *,
        id: int | None = None,
        customer_item_id: str | None = None,
        lot_number: str | None = None,
        page_size: int = 25,
        page_number: int = 1,
    ) -> PaginatedList[LotDto]:
        """List lots with optional filters.

        Args:
            id: Filter by lot ID.
            customer_item_id: Filter by customer item ID.
            lot_number: Filter by lot number.
            page_size: Number of items per page.
            page_number: Page number (1-based).

        Returns:
            PaginatedList[LotDto]: Paginated lot results.
        """
        params = {
            "id": id,
            "customer_item_id": customer_item_id,
            "lot_number": lot_number,
            "page_size": page_size,
            "page_number": page_number,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._paginated_request(_LIST, "LotDto", params=params)

    def get(self, lot_id: int) -> LotDto:
        """Retrieve a single lot by ID.

        Args:
            lot_id: Lot identifier.

        Returns:
            LotDto: Lot details.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lots/get.html
        Response model: LotDto
        """
        return self._request(_GET.bind(id=lot_id))

    def update(self, lot_id: int, *, data: UpdateLotRequest | dict) -> LotDto:
        """PUT /Lot/{id}.

        Args:
            lot_id: Lot identifier.
            data: Lot update payload with ``customer_item_id``,
                ``image_links``, ``overriden_data``, and ``catalogs``.
                (``initial_data`` is create-only — it cannot be updated
                via PUT.) Accepts an :class:`UpdateLotRequest` instance
                or a dict.

        Request model: :class:`UpdateLotRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lots/update.html
        Request model: UpdateLotRequest
        Response model: LotDto
        """
        return self._request(_UPDATE.bind(id=lot_id), json=data)

    def delete(self, lot_id: int) -> None:
        """Delete a lot.

        Args:
            lot_id: Lot identifier.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lots/delete.html
        """
        self._request(_DELETE.bind(id=lot_id))

    def get_overrides(self, customer_item_ids: List[str]) -> list[LotOverrideDto]:
        """Retrieve lot overrides for the given customer item IDs.

        Args:
            customer_item_ids: List of customer item ID strings.

        Returns:
            list[LotOverrideDto]: Override data for matched lots.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lots/get_overrides.html
        Response model: List[LotOverrideDto]
        """
        return self._request(_GET_OVERRIDES, json=customer_item_ids)
