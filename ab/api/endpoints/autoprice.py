"""AutoPrice API endpoints (3 routes)."""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_QUICK_QUOTE = Route("POST", "/autoprice/quickquote", request_model="QuoteRequestModel", response_model="QuickQuoteResponse", api_surface="abc")
_QUOTE_REQUEST = Route("POST", "/autoprice/v2/quoterequest", request_model="QuoteRequestModel", response_model="QuoteRequestResponse", api_surface="abc")

# Extended route (009) — v1 quote request
_QUOTE_REQUEST_V1 = Route("POST", "/autoprice/quoterequest", request_model="QuoteRequestModel", response_model="QuoteRequestResponse", api_surface="abc")


class AutoPriceEndpoint(BaseEndpoint):
    """Quoting/pricing (ABC API)."""

    def quick_quote(self, data: dict | Any) -> Any:
        """POST /autoprice/quickquote"""
        return self._request(_QUICK_QUOTE, json=data)

    def quote_request(self, data: dict | Any) -> Any:
        """POST /autoprice/v2/quoterequest"""
        return self._request(_QUOTE_REQUEST, json=data)

    # ---- Extended (009) -----------------------------------------------------

    def quote_request_v1(self, data: dict | Any) -> Any:
        """POST /autoprice/quoterequest (v1)"""
        return self._request(_QUOTE_REQUEST_V1, json=data)
