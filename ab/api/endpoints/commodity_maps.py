"""Commodity Maps API endpoints (5 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.commodities import (
        CommodityMap,
        CommodityMapCreateRequest,
        CommodityMapSearchRequest,
        CommodityMapUpdateRequest,
    )
    from ab.api.models.shared import ServiceBaseResponse

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET = Route("GET", "/commodity-map/{id}", response_model="CommodityMap")
_UPDATE = Route("PUT", "/commodity-map/{id}", request_model="CommodityMapUpdateRequest", response_model="CommodityMap")
_DELETE = Route("DELETE", "/commodity-map/{id}", response_model="ServiceBaseResponse")
_CREATE = Route("POST", "/commodity-map", request_model="CommodityMapCreateRequest", response_model="CommodityMap")
_SEARCH = Route(
    "POST", "/commodity-map/search",
    request_model="CommodityMapSearchRequest", response_model="List[CommodityMap]",
)


class CommodityMapsEndpoint(BaseEndpoint):
    """Commodity map operations (ACPortal API)."""

    def get(self, map_id: str) -> CommodityMap:
        """GET /commodity-map/{id}

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/commodity_maps/get.html
        Response model: CommodityMap
        """
        return self._request(_GET.bind(id=map_id))

    def update(self, map_id: str, *, data: CommodityMapUpdateRequest | dict) -> CommodityMap:
        """PUT /commodity-map/{id}.

        Args:
            map_id: Commodity map identifier.
            data: Commodity map update payload with custom_name, commodity_id.
                Accepts a :class:`CommodityMapUpdateRequest` instance or a dict.

        Request model: :class:`CommodityMapUpdateRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/commodity_maps/update.html
        Request model: CommodityMapUpdateRequest
        Response model: CommodityMap
        """
        return self._request(_UPDATE.bind(id=map_id), json=data)

    def delete(self, map_id: str) -> ServiceBaseResponse:
        """DELETE /commodity-map/{id}

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/commodity_maps/delete.html
        Response model: ServiceBaseResponse
        """
        return self._request(_DELETE.bind(id=map_id))

    def create(self, *, data: CommodityMapCreateRequest | dict) -> CommodityMap:
        """POST /commodity-map.

        Args:
            data: Commodity map creation payload with custom_name, commodity_id.
                Accepts a :class:`CommodityMapCreateRequest` instance or a dict.

        Request model: :class:`CommodityMapCreateRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/commodity_maps/create.html
        Request model: CommodityMapCreateRequest
        Response model: CommodityMap
        """
        return self._request(_CREATE, json=data)

    def search(self, *, data: CommodityMapSearchRequest | dict) -> list[CommodityMap]:
        """POST /commodity-map/search.

        Args:
            data: Search payload with search_text, page, page_size.
                Accepts a :class:`CommodityMapSearchRequest` instance or a dict.

        Request model: :class:`CommodityMapSearchRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/commodity_maps/search.html
        Request model: CommodityMapSearchRequest
        Response model: List[CommodityMap]
        """
        return self._request(_SEARCH, json=data)
