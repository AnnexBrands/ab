"""Notification models for the ACPortal API.

Covers /api/notifications endpoint.
"""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import ResponseModel


class Notification(ResponseModel):
    """Notification — GET /notifications."""

    id: Optional[str] = Field(None, description="Notification ID")
    message: Optional[str] = Field(None, description="Notification message")
    is_read: Optional[bool] = Field(None, alias="isRead", description="Whether notification has been read")
    created_date: Optional[str] = Field(None, alias="createdDate", description="Creation date")
