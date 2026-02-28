"""Web2Lead API endpoints (2 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ab.api.models.web2lead import Web2LeadGetParams, Web2LeadResponse

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET = Route(
    "GET", "/Web2Lead/get",
    params_model="Web2LeadGetParams", response_model="Web2LeadResponse", api_surface="abc",
)
_POST = Route(
    "POST", "/Web2Lead/post",
    request_model="Web2LeadRequest", response_model="Web2LeadResponse", api_surface="abc",
)


class Web2LeadEndpoint(BaseEndpoint):
    """Web-to-lead capture (ABC API)."""

    def get(self, *, params: Web2LeadGetParams | dict) -> Web2LeadResponse:
        """GET /Web2Lead/get.

        Args:
            params: Lead query parameters (29 optional string fields).
                Accepts a :class:`Web2LeadGetParams` instance or a dict
                with snake_case or PascalCase keys.

        Params model: :class:`Web2LeadGetParams`
        """
        return self._request(_GET, params=params)

    def post(
        self,
        *,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        company: str | None = None,
        message: str | None = None,
    ) -> Web2LeadResponse:
        """POST /Web2Lead/post.

        Args:
            name: Lead name.
            email: Lead email.
            phone: Lead phone.
            company: Lead company.
            message: Lead message/inquiry.

        Request model: :class:`Web2LeadRequest`
        """
        body = dict(name=name, email=email, phone=phone, company=company, message=message)
        return self._request(_POST, json=body)
