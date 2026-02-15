"""Commodities API endpoints (5 routes)."""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET = Route("GET", "/commodity/{id}", response_model="Commodity")
_UPDATE = Route("PUT", "/commodity/{id}", request_model="CommodityUpdateRequest", response_model="Commodity")
_CREATE = Route("POST", "/commodity", request_model="CommodityCreateRequest", response_model="Commodity")
_SEARCH = Route("POST", "/commodity/search", request_model="CommoditySearchRequest", response_model="List[Commodity]")
_SUGGESTIONS = Route(
    "POST", "/commodity/suggestions",
    request_model="CommoditySuggestionRequest", response_model="List[Commodity]",
)


class CommoditiesEndpoint(BaseEndpoint):
    """Commodity operations (ACPortal API)."""

    def get(self, commodity_id: str) -> Any:
        """GET /commodity/{id}"""
        return self._request(_GET.bind(id=commodity_id))

    def update(self, commodity_id: str, **kwargs: Any) -> Any:
        """PUT /commodity/{id}"""
        return self._request(_UPDATE.bind(id=commodity_id), json=kwargs)

    def create(self, **kwargs: Any) -> Any:
        """POST /commodity"""
        return self._request(_CREATE, json=kwargs)

    def search(self, **kwargs: Any) -> Any:
        """POST /commodity/search"""
        return self._request(_SEARCH, json=kwargs)

    def suggestions(self, **kwargs: Any) -> Any:
        """POST /commodity/suggestions"""
        return self._request(_SUGGESTIONS, json=kwargs)
