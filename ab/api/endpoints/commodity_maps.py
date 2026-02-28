"""Commodity Maps API endpoints (5 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ab.api.models.commodities import CommodityMap
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
        """GET /commodity-map/{id}"""
        return self._request(_GET.bind(id=map_id))

    def update(
        self,
        map_id: str,
        *,
        custom_name: str | None = None,
        commodity_id: str | None = None,
    ) -> CommodityMap:
        """PUT /commodity-map/{id}.

        Args:
            map_id: Commodity map identifier.
            custom_name: Custom commodity name.
            commodity_id: Linked commodity ID.

        Request model: :class:`CommodityMapUpdateRequest`
        """
        body = dict(custom_name=custom_name, commodity_id=commodity_id)
        return self._request(_UPDATE.bind(id=map_id), json=body)

    def delete(self, map_id: str) -> ServiceBaseResponse:
        """DELETE /commodity-map/{id}"""
        return self._request(_DELETE.bind(id=map_id))

    def create(
        self,
        *,
        custom_name: str | None = None,
        commodity_id: str | None = None,
    ) -> CommodityMap:
        """POST /commodity-map.

        Args:
            custom_name: Custom commodity name.
            commodity_id: Linked commodity ID.

        Request model: :class:`CommodityMapCreateRequest`
        """
        body = dict(custom_name=custom_name, commodity_id=commodity_id)
        return self._request(_CREATE, json=body)

    def search(
        self,
        *,
        search_text: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> list[CommodityMap]:
        """POST /commodity-map/search.

        Args:
            search_text: Search query.
            page: Page number.
            page_size: Results per page.

        Request model: :class:`CommodityMapSearchRequest`
        """
        body = dict(search_text=search_text, page=page, page_size=page_size)
        return self._request(_SEARCH, json=body)
