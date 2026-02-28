"""Users API endpoints (4 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ab.api.models.shared import ListRequest
    from ab.api.models.users import User, UserCreateRequest, UserUpdateRequest

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

    def create(self, *, data: UserCreateRequest | dict) -> Any:
        """POST /users/user.

        Args:
            data: User creation payload.
                Accepts a :class:`UserCreateRequest` instance or a dict.

        Request model: :class:`UserCreateRequest`
        """
        return self._request(_CREATE, json=data)

    def update(self, *, data: UserUpdateRequest | dict) -> Any:
        """PUT /users/user.

        Args:
            data: User update payload.
                Accepts a :class:`UserUpdateRequest` instance or a dict.

        Request model: :class:`UserUpdateRequest`
        """
        return self._request(_UPDATE, json=data)
