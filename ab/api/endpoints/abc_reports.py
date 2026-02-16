"""ABC Reports API endpoints (2 routes).

Covers Report and LogBuffer endpoints on the ABC API surface.
"""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET_WEB_REVENUE = Route("GET", "/report/webrevenue", api_surface="abc")
_POST_FLUSH = Route("POST", "/logbuffer/flush", api_surface="abc")


class ABCReportsEndpoint(BaseEndpoint):
    """Reports and log buffer (ABC API)."""

    def get_web_revenue(self, **params: Any) -> Any:
        """GET /report/webrevenue — query params: accessKey, startDate, endDate."""
        return self._request(_GET_WEB_REVENUE, params=params)

    def flush_log_buffer(self, **kwargs: Any) -> Any:
        """POST /logbuffer/flush"""
        return self._request(_POST_FLUSH, json=kwargs or None)
