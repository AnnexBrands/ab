"""SMS Template models for the ACPortal API.

Covers SmsTemplate endpoints under /api/SmsTemplate/.
"""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class SmsTemplate(ResponseModel):
    """SMS template — GET/POST /SmsTemplate/."""

    id: Optional[str] = Field(None, description="Template ID")
    name: Optional[str] = Field(None, description="Template name")
    body: Optional[str] = Field(None, description="Template body text")
    company_id: Optional[str] = Field(None, alias="companyId", description="Company ID")


class NotificationTokens(ResponseModel):
    """Notification tokens — GET /SmsTemplate/notificationTokens."""

    tokens: Optional[List[str]] = Field(None, description="Available notification tokens")


class SmsTemplateRequest(RequestModel):
    """Body for POST /SmsTemplate/save."""

    name: Optional[str] = Field(None, description="Template name")
    body: Optional[str] = Field(None, description="Template body text")
    company_id: Optional[str] = Field(None, alias="companyId", description="Company ID")
