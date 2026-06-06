"""Partners API endpoints (3 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.partners import Partner, PartnerSearchRequest

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_LIST = Route("GET", "/partner", params_model="PartnerListParams", response_model="List[Partner]")
_GET = Route("GET", "/partner/{id}", response_model="Partner")
_SEARCH = Route("POST", "/partner/search", request_model="PartnerSearchRequest", response_model="List[Partner]")


class PartnersEndpoint(BaseEndpoint):
    """Partner operations (ACPortal API)."""

    def list(self) -> list[Partner]:
        """GET /partner

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/partners/list.html
        Query params: PartnerListParams
        Response model: List[Partner]
        """
        return self._request(_LIST)

    def get(self, partner_id: str) -> Partner:
        """GET /partner/{id}

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/partners/get.html
        Response model: Partner
        """
        return self._request(_GET.bind(id=partner_id))

    def search(self, *, data: PartnerSearchRequest | dict) -> list[Partner]:
        """POST /partner/search.

        Args:
            data: Partner search payload.
                Accepts a :class:`PartnerSearchRequest` instance or a dict.

        Request model: :class:`PartnerSearchRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/partners/search.html
        Request model: PartnerSearchRequest
        Response model: List[Partner]
        """
        return self._request(_SEARCH, json=data)
