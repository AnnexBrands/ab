"""Users API endpoints (4 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ab.api.models.shared import ListRequest
    from ab.api.models.users import User

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_LIST = Route("POST", "/users/list", request_model="ListRequest", response_model="List[User]")
_ROLES = Route("GET", "/users/roles", response_model="List[str]")
_CREATE = Route("POST", "/users/user", request_model="UserCreateRequest")
_UPDATE = Route("PUT", "/users/user", request_model="UserUpdateRequest")


class UsersEndpoint(BaseEndpoint):
    """User management (ACPortal API)."""

    def list(self, *, data: ListRequest | dict) -> list[User]:
        """POST /users/list.

        Args:
            data: List filter with pagination, sorting, and filters.
                Accepts a :class:`ListRequest` instance or a dict.

        Request model: :class:`ListRequest`
        """
        return self._request(_LIST, json=data)

    def get_roles(self) -> list[str]:
        """GET /users/roles"""
        return self._request(_ROLES)

    def create(
        self,
        *,
        username: str | None = None,
        email: str | None = None,
        roles: list[str] | None = None,
    ) -> Any:
        """POST /users/user.

        Args:
            username: Username.
            email: Email.
            roles: Role IDs.

        Request model: :class:`UserCreateRequest`
        """
        body = dict(username=username, email=email, roles=roles)
        return self._request(_CREATE, json=body)

    def update(
        self,
        *,
        id: str | None = None,
        username: str | None = None,
        email: str | None = None,
        roles: list[str] | None = None,
    ) -> Any:
        """PUT /users/user.

        Args:
            id: User ID.
            username: Updated username.
            email: Updated email.
            roles: Updated role IDs.

        Request model: :class:`UserUpdateRequest`
        """
        body = dict(id=id, username=username, email=email, roles=roles)
        return self._request(_UPDATE, json=body)
