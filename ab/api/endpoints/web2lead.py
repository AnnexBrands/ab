"""Web2Lead API endpoints (2 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ab.api.models.web2lead import Web2LeadResponse

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET = Route("GET", "/Web2Lead/get", response_model="Web2LeadResponse", api_surface="abc")
_POST = Route(
    "POST", "/Web2Lead/post",
    request_model="Web2LeadRequest", response_model="Web2LeadResponse", api_surface="abc",
)


class Web2LeadEndpoint(BaseEndpoint):
    """Web-to-lead capture (ABC API)."""

    def get(self, **params: Any) -> Web2LeadResponse:
        """GET /Web2Lead/get"""
        return self._request(_GET, params=params)

    def post(self, data: dict | Any) -> Web2LeadResponse:
        """POST /Web2Lead/post"""
        return self._request(_POST, json=data)
