"""Commodity Maps API endpoints (5 routes)."""

from __future__ import annotations

from typing import Any

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

    def get(self, map_id: str) -> Any:
        """GET /commodity-map/{id}"""
        return self._request(_GET.bind(id=map_id))

    def update(self, map_id: str, **kwargs: Any) -> Any:
        """PUT /commodity-map/{id}"""
        return self._request(_UPDATE.bind(id=map_id), json=kwargs)

    def delete(self, map_id: str) -> Any:
        """DELETE /commodity-map/{id}"""
        return self._request(_DELETE.bind(id=map_id))

    def create(self, **kwargs: Any) -> Any:
        """POST /commodity-map"""
        return self._request(_CREATE, json=kwargs)

    def search(self, **kwargs: Any) -> Any:
        """POST /commodity-map/search"""
        return self._request(_SEARCH, json=kwargs)
