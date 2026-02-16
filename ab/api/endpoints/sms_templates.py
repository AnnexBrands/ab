"""SMS Template API endpoints (5 routes).

Covers SmsTemplate endpoints under /api/SmsTemplate/.
"""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET_LIST = Route("GET", "/SmsTemplate/list", response_model="List[SmsTemplate]")
_GET_TOKENS = Route("GET", "/SmsTemplate/notificationTokens", response_model="NotificationTokens")
_POST_SAVE = Route("POST", "/SmsTemplate/save", request_model="SmsTemplateRequest", response_model="SmsTemplate")
_GET_TEMPLATE = Route("GET", "/SmsTemplate/{templateId}", response_model="SmsTemplate")
_DELETE_TEMPLATE = Route("DELETE", "/SmsTemplate/{templateId}")


class SmsTemplateEndpoint(BaseEndpoint):
    """SMS template management (ACPortal API)."""

    def list(self, **params: Any) -> Any:
        """GET /SmsTemplate/list — accepts companyId query param."""
        return self._request(_GET_LIST, params=params or None)

    def get_notification_tokens(self) -> Any:
        """GET /SmsTemplate/notificationTokens"""
        return self._request(_GET_TOKENS)

    def save(self, **kwargs: Any) -> Any:
        """POST /SmsTemplate/save"""
        return self._request(_POST_SAVE, json=kwargs)

    def get(self, template_id: str) -> Any:
        """GET /SmsTemplate/{templateId}"""
        return self._request(_GET_TEMPLATE.bind(templateId=template_id))

    def delete(self, template_id: str) -> Any:
        """DELETE /SmsTemplate/{templateId}"""
        return self._request(_DELETE_TEMPLATE.bind(templateId=template_id))
