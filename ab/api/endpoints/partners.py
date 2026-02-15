"""Partners API endpoints (3 routes)."""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_LIST = Route("GET", "/partner", response_model="List[Partner]")
_GET = Route("GET", "/partner/{id}", response_model="Partner")
_SEARCH = Route("POST", "/partner/search", request_model="PartnerSearchRequest", response_model="List[Partner]")


class PartnersEndpoint(BaseEndpoint):
    """Partner operations (ACPortal API)."""

    def list(self) -> Any:
        """GET /partner"""
        return self._request(_LIST)

    def get(self, partner_id: str) -> Any:
        """GET /partner/{id}"""
        return self._request(_GET.bind(id=partner_id))

    def search(self, **kwargs: Any) -> Any:
        """POST /partner/search"""
        return self._request(_SEARCH, json=kwargs)
