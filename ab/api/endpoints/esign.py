"""E-Sign API endpoints (2 routes).

Covers JobSign endpoints under /api/e-sign/.
"""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET_RESULT = Route("GET", "/e-sign/result", response_model="ESignResult")
_GET_ESIGN = Route("GET", "/e-sign/{jobDisplayId}/{bookingKey}", response_model="ESignData")


class ESignEndpoint(BaseEndpoint):
    """E-sign / DocuSign integration (ACPortal API)."""

    def get_result(self, **params: Any) -> Any:
        """GET /e-sign/result — query params: envelope, event."""
        return self._request(_GET_RESULT, params=params)

    def get_esign(self, job_display_id: int, booking_key: str) -> Any:
        """GET /e-sign/{jobDisplayId}/{bookingKey}"""
        return self._request(_GET_ESIGN.bind(jobDisplayId=job_display_id, bookingKey=booking_key))
