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
    login: Optional[str] = Field(None, description="Login name")
    full_name: Optional[str] = Field(None, alias="fullName", description="Full display name")
    contact_id: Optional[int] = Field(None, alias="contactId", description="Contact integer ID")
    contact_display_id: Optional[str] = Field(None, alias="contactDisplayId", description="Contact display ID")
    contact_company_name: Optional[str] = Field(None, alias="contactCompanyName", description="Contact company name")
    contact_company_id: Optional[str] = Field(None, alias="contactCompanyId", description="Contact company UUID")
    contact_company_display_id: Optional[str] = Field(
        None, alias="contactCompanyDisplayId", description="Contact company display ID"
    )
    email_confirmed: Optional[bool] = Field(None, alias="emailConfirmed", description="Email confirmed flag")
    contact_phone: Optional[str] = Field(None, alias="contactPhone", description="Contact phone number")
    contact_email: Optional[str] = Field(None, alias="contactEmail", description="Contact email address")
    password: Optional[str] = Field(None, description="Password (null in responses)")
    lockout_date_utc: Optional[str] = Field(None, alias="lockoutDateUtc", description="Lockout date")
    lockout_enabled: Optional[bool] = Field(None, alias="lockoutEnabled", description="Whether lockout is enabled")
    role: Optional[str] = Field(None, description="Primary role name")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Whether user is active")
    legacy_id: Optional[str] = Field(None, alias="legacyId", description="Legacy system identifier")
    additional_user_companies: Optional[List[str]] = Field(
        None, alias="additionalUserCompanies", description="Additional company UUIDs"
    )
    additional_user_companies_names: Optional[List[str]] = Field(
        None, alias="additionalUserCompaniesNames", description="Additional company names"
    )
    crm_contact_id: Optional[int] = Field(None, alias="crmContactId", description="CRM contact ID")


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
