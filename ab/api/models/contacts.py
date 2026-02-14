"""Contact models for the ACPortal API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel
from ab.api.models.mixins import FullAuditModel, IdentifiedModel


class ContactSimple(ResponseModel, IdentifiedModel):
    """Lightweight contact — GET /contacts/{id} and GET /contacts/user.

    The ``/contacts/user`` endpoint returns ``fullName``, ``companyId``,
    ``companyName`` instead of ``firstName``/``lastName`` — all fields
    are optional to accommodate both shapes.
    """

    first_name: Optional[str] = Field(None, alias="firstName", description="First name")
    last_name: Optional[str] = Field(None, alias="lastName", description="Last name")
    full_name: Optional[str] = Field(None, alias="fullName", description="Full display name (from /contacts/user)")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    company_id: Optional[str] = Field(None, alias="companyId", description="Associated company UUID")
    company_name: Optional[str] = Field(None, alias="companyName", description="Associated company name")


class ContactDetailedInfo(ResponseModel, FullAuditModel):
    """Full editable contact details — GET /contacts/{id}/editdetails."""

    first_name: Optional[str] = Field(None, alias="firstName", description="First name")
    last_name: Optional[str] = Field(None, alias="lastName", description="Last name")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    addresses: Optional[List[dict]] = Field(None, description="Contact addresses")
    phones: Optional[List[dict]] = Field(None, description="Phone numbers")
    emails: Optional[List[dict]] = Field(None, description="Email addresses")
    company_info: Optional[dict] = Field(None, alias="companyInfo", description="Associated company")


class ContactPrimaryDetails(ResponseModel):
    """Primary contact info — GET /contacts/{id}/primarydetails.

    The live API returns ``company`` as a nested dict (full company object)
    rather than a plain string as swagger implies.
    """

    id: Optional[int] = Field(None, description="Contact integer ID")
    full_name: Optional[str] = Field(None, alias="fullName", description="Full display name")
    email: Optional[str] = Field(None, description="Primary email")
    phone: Optional[str] = Field(None, description="Primary phone")
    company: Optional[dict] = Field(None, description="Associated company (full object)")
    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID")
    company_name: Optional[str] = Field(None, alias="companyName", description="Company name")


class SearchContactEntityResult(ResponseModel):
    """Single result from POST /contacts/v2/search.

    The live API returns integer IDs and nested detail fields rather than
    simple flat strings as swagger implies.
    """

    id: Optional[int] = Field(None, description="Contact integer ID")
    full_name: Optional[str] = Field(None, alias="fullName", description="Display name")
    email: Optional[str] = Field(None, description="Primary email")
    company_name: Optional[str] = Field(None, alias="companyName", description="Company name")
    contact_display_id: Optional[str] = Field(None, alias="contactDisplayId", description="Display ID")


class ContactEditRequest(RequestModel):
    """Body for PUT /contacts/{id}/editdetails and POST /contacts/editdetails."""

    first_name: Optional[str] = Field(None, alias="firstName", description="First name")
    last_name: Optional[str] = Field(None, alias="lastName", description="Last name")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    addresses: Optional[List[dict]] = Field(None, description="Contact addresses")


class ContactSearchRequest(RequestModel):
    """Body for POST /contacts/v2/search."""

    search_text: Optional[str] = Field(None, alias="searchText", description="Search query")
    page: int = Field(1, description="Page number")
    page_size: int = Field(25, alias="pageSize", description="Results per page")
