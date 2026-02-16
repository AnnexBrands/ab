"""Users API endpoints (5 routes)."""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_LIST = Route("POST", "/users/list", request_model="ListRequest", response_model="List[User]")
_ROLES = Route("GET", "/users/roles", response_model="List[UserRole]")
_CREATE = Route("POST", "/users/user", request_model="UserCreateRequest")
_UPDATE = Route("PUT", "/users/user", request_model="UserUpdateRequest")

# Extended users route (009)
_GET_POC_USERS = Route("GET", "/users/pocusers")


class UsersEndpoint(BaseEndpoint):
    """User management (ACPortal API)."""

    def list(self, data: dict | Any) -> Any:
        """POST /users/list"""
        return self._request(_LIST, json=data)

    def get_roles(self) -> Any:
        """GET /users/roles"""
        return self._request(_ROLES)

    def create(self, data: dict | Any) -> Any:
        """POST /users/user"""
        return self._request(_CREATE, json=data)

    def update(self, data: dict | Any) -> Any:
        """PUT /users/user"""
        return self._request(_UPDATE, json=data)

    # ---- Extended (009) -----------------------------------------------------

    def get_poc_users(self) -> Any:
        """GET /users/pocusers"""
        return self._request(_GET_POC_USERS)
