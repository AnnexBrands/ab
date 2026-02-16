"""Values API endpoint (1 route).

Covers /api/Values — health check / test endpoint.
"""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET_VALUES = Route("GET", "/Values", response_model="List[str]")


class ValuesEndpoint(BaseEndpoint):
    """Values / health check (ACPortal API)."""

    def get_all(self) -> Any:
        """GET /Values"""
        return self._request(_GET_VALUES)
