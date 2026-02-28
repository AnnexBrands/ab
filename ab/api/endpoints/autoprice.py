"""AutoPrice API endpoints (2 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ab.api.models.autoprice import QuoteRequestModel, QuickQuoteResponse, QuoteRequestResponse

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_QUICK_QUOTE = Route(
    "POST", "/autoprice/quickquote",
    request_model="QuoteRequestModel", response_model="QuickQuoteResponse", api_surface="abc",
)
_QUOTE_REQUEST = Route(
    "POST", "/autoprice/v2/quoterequest",
    request_model="QuoteRequestModel", response_model="QuoteRequestResponse", api_surface="abc",
)


class AutoPriceEndpoint(BaseEndpoint):
    """Quoting/pricing (ABC API)."""

    def quick_quote(self, *, data: QuoteRequestModel | dict) -> QuickQuoteResponse:
        """POST /autoprice/quickquote.

        Args:
            data: Quote request with job_info, contact_info, service_info,
                and items. Accepts a :class:`QuoteRequestModel` instance
                or a dict.

        Request model: :class:`QuoteRequestModel`
        """
        return self._request(_QUICK_QUOTE, json=data)

    def quote_request(self, *, data: QuoteRequestModel | dict) -> QuoteRequestResponse:
        """POST /autoprice/v2/quoterequest.

        Args:
            data: Quote request with job_info, contact_info, service_info,
                and items. Accepts a :class:`QuoteRequestModel` instance
                or a dict.

        Request model: :class:`QuoteRequestModel`
        """
        return self._request(_QUOTE_REQUEST, json=data)
