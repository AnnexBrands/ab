"""ABC Test API endpoints (3 routes).

Covers diagnostic Test endpoints under /api/Test/ on the ABC API surface.
"""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET_CONTACT = Route("GET", "/Test/contact", api_surface="abc")
_GET_RECENT_ESTIMATES = Route("GET", "/Test/recentestimates", api_surface="abc")
_GET_RENDERED_TEMPLATE = Route("GET", "/Test/renderedtemplate", api_surface="abc")


class ABCTestEndpoint(BaseEndpoint):
    """Diagnostic test endpoints (ABC API).

    Used for integration testing and SDK verification.
    """

    def get_contact(self, **params: Any) -> Any:
        """GET /Test/contact"""
        return self._request(_GET_CONTACT, params=params or None)

    def get_recent_estimates(self, **params: Any) -> Any:
        """GET /Test/recentestimates"""
        return self._request(_GET_RECENT_ESTIMATES, params=params or None)

    def get_rendered_template(self, **params: Any) -> Any:
        """GET /Test/renderedtemplate"""
        return self._request(_GET_RENDERED_TEMPLATE, params=params or None)
