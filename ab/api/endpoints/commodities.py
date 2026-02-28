"""Commodities API endpoints (5 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ab.api.models.commodities import Commodity

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

    def update(
        self,
        commodity_id: str,
        *,
        description: str | None = None,
        freight_class: str | None = None,
        nmfc_code: str | None = None,
    ) -> Commodity:
        """PUT /commodity/{id}.

        Args:
            commodity_id: Commodity identifier.
            description: Commodity description.
            freight_class: Freight class.
            nmfc_code: NMFC code.

        Request model: :class:`CommodityUpdateRequest`
        """
        body = dict(description=description, freight_class=freight_class, nmfc_code=nmfc_code)
        return self._request(_UPDATE.bind(id=commodity_id), json=body)

    def create(
        self,
        *,
        description: str | None = None,
        freight_class: str | None = None,
        nmfc_code: str | None = None,
        weight_min: float | None = None,
        weight_max: float | None = None,
    ) -> Commodity:
        """POST /commodity.

        Args:
            description: Commodity description.
            freight_class: Freight class.
            nmfc_code: NMFC code.
            weight_min: Minimum weight.
            weight_max: Maximum weight.

        Request model: :class:`CommodityCreateRequest`
        """
        body = dict(description=description, freight_class=freight_class,
                     nmfc_code=nmfc_code, weight_min=weight_min, weight_max=weight_max)
        return self._request(_CREATE, json=body)

    def search(
        self,
        *,
        search_text: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> list[Commodity]:
        """POST /commodity/search.

        Args:
            search_text: Search query.
            page: Page number.
            page_size: Results per page.

        Request model: :class:`CommoditySearchRequest`
        """
        body = dict(search_text=search_text, page=page, page_size=page_size)
        return self._request(_SEARCH, json=body)

    def suggestions(self, *, search_text: str | None = None) -> list[Commodity]:
        """POST /commodity/suggestions.

        Args:
            search_text: Search query for suggestions.

        Request model: :class:`CommoditySuggestionRequest`
        """
        body = dict(search_text=search_text)
        return self._request(_SUGGESTIONS, json=body)
