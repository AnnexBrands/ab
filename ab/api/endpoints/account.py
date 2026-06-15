"""Account API endpoints — swagger tag ``Account`` (1 route)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ab.api.base import BaseEndpoint
from ab.api.route import Route

if TYPE_CHECKING:
    from ab.api.models.account import AccountProfile

_PROFILE = Route("GET", "/account/profile", response_model="AccountProfile")


class AccountEndpoint(BaseEndpoint):
    """Current-user account operations (ACPortal API)."""

    def get_profile(self) -> AccountProfile:
        """``GET /account/profile`` — the authenticated user's account profile.

        Returns the profile of whoever the client's token belongs to
        (user name, email, company, contact id, roles).

        Response model: AccountProfile

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/account/get_profile.html
        Response model: AccountProfile
        """
        return self._request(_PROFILE)
