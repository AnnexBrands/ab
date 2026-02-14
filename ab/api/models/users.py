"""User models for the ACPortal API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel
from ab.api.models.mixins import IdentifiedModel


class User(ResponseModel, IdentifiedModel):
    """User record — POST /users/list."""

    username: Optional[str] = Field(None, description="Login username")
    email: Optional[str] = Field(None, description="Email address")
    roles: Optional[List[dict]] = Field(None, description="Assigned roles")
    company: Optional[dict] = Field(None, description="Associated company")


class UserRole(ResponseModel):
    """Role definition — GET /users/roles.

    The live API returns roles as plain strings (e.g. ``"CorporateAccounting"``),
    not ``{id, name}`` objects as swagger implies.  When the fixture is a
    string, construct with ``name=value``.
    """

    id: Optional[str] = Field(None, description="Role ID")
    name: Optional[str] = Field(None, description="Role name")


class UserCreateRequest(RequestModel):
    """Body for POST /users/user."""

    username: Optional[str] = Field(None, description="Username")
    email: Optional[str] = Field(None, description="Email")
    roles: Optional[List[str]] = Field(None, description="Role IDs")


class UserUpdateRequest(RequestModel):
    """Body for PUT /users/user."""

    id: Optional[str] = Field(None, description="User ID")
    username: Optional[str] = Field(None, description="Updated username")
    email: Optional[str] = Field(None, description="Updated email")
    roles: Optional[List[str]] = Field(None, description="Updated role IDs")
