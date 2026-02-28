"""Commodities API endpoints (5 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ab.api.models.commodities import (
        Commodity,
        CommodityCreateRequest,
        CommoditySearchRequest,
        CommoditySuggestionRequest,
        CommodityUpdateRequest,
    )

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

    def get(self, commodity_id: str) -> Commodity:
        """GET /commodity/{id}"""
        return self._request(_GET.bind(id=commodity_id))

    def update(self, commodity_id: str, *, data: CommodityUpdateRequest | dict) -> Commodity:
        """PUT /commodity/{id}.

        Args:
            commodity_id: Commodity identifier.
            data: Commodity update payload with description, freight_class, nmfc_code.
                Accepts a :class:`CommodityUpdateRequest` instance or a dict.

        Request model: :class:`CommodityUpdateRequest`
        """
        return self._request(_UPDATE.bind(id=commodity_id), json=data)

    def create(self, *, data: CommodityCreateRequest | dict) -> Commodity:
        """POST /commodity.

        Args:
            data: Commodity creation payload with description, freight_class,
                nmfc_code, weight_min, weight_max.
                Accepts a :class:`CommodityCreateRequest` instance or a dict.

        Request model: :class:`CommodityCreateRequest`
        """
        return self._request(_CREATE, json=data)

    def search(self, *, data: CommoditySearchRequest | dict) -> list[Commodity]:
        """POST /commodity/search.

        Args:
            data: Search payload with search_text, page, page_size.
                Accepts a :class:`CommoditySearchRequest` instance or a dict.

        Request model: :class:`CommoditySearchRequest`
        """
        return self._request(_SEARCH, json=data)

    def suggestions(self, *, data: CommoditySuggestionRequest | dict) -> list[Commodity]:
        """POST /commodity/suggestions.

        Args:
            data: Suggestion request payload with search_text.
                Accepts a :class:`CommoditySuggestionRequest` instance or a dict.

        Request model: :class:`CommoditySuggestionRequest`
        """
        return self._request(_SUGGESTIONS, json=data)
