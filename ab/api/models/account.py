"""Account models for the ACPortal API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import ResponseModel


class AccountProfile(ResponseModel):
    """Current user's account profile — GET /account/profile.

    Swagger declares no response schema for this endpoint, so the fields
    below model the commonly consumed subset; any additional fields the
    API returns are preserved as extras (``ResponseModel`` tolerates and
    warns on undeclared fields).
    """

    user_name: Optional[str] = Field(None, alias="userName", description="Login user name")
    email: Optional[str] = Field(None, description="Account email address")
    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID")
    contact_id: Optional[int] = Field(None, alias="contactId", description="Contact ID")
    roles: Optional[List[str]] = Field(None, description="Role names assigned to the user")
