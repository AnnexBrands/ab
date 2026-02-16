"""Notifications API endpoint (1 route).

Covers /api/notifications.
"""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET_NOTIFICATIONS = Route("GET", "/notifications", response_model="List[Notification]")


class NotificationsEndpoint(BaseEndpoint):
    """Notification retrieval (ACPortal API)."""

    def get_all(self) -> Any:
        """GET /notifications"""
        return self._request(_GET_NOTIFICATIONS)
