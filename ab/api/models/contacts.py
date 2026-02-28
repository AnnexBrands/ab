"""Contact models for the ACPortal API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel
from ab.api.models.common import CompanyAddress
from ab.api.models.mixins import FullAuditModel, IdentifiedModel, PaginatedRequestMixin, SearchableRequestMixin


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

    # --- extended fields observed in live API responses ---
    addresses_list: Optional[List[dict]] = Field(None, alias="addressesList", description="Contact addresses list")
    assistant: Optional[str] = Field(None, description="Assistant name")
    birth_date: Optional[str] = Field(None, alias="birthDate", description="Birth date")
    bol_notes: Optional[str] = Field(None, alias="bolNotes", description="BOL notes")
    care_of: Optional[str] = Field(None, alias="careOf", description="Care-of / attention line")
    company: Optional[dict] = Field(None, description="Full company object")
    contact_display_id: Optional[str] = Field(None, alias="contactDisplayId", description="Display ID")
    contact_type_id: Optional[int] = Field(None, alias="contactTypeId", description="Contact type identifier")
    department: Optional[str] = Field(None, description="Department name")
    editable: Optional[bool] = Field(None, description="Whether the contact is editable")
    emails_list: Optional[List[dict]] = Field(None, alias="emailsList", description="Email addresses list")
    fax: Optional[str] = Field(None, description="Fax number")
    full_name_update_required: Optional[bool] = Field(
        None, alias="fullNameUpdateRequired", description="Whether full name needs update",
    )
    is_active: Optional[bool] = Field(None, alias="isActive", description="Whether the contact is active")
    is_business: Optional[bool] = Field(None, alias="isBusiness", description="Whether this is a business contact")
    is_empty: Optional[bool] = Field(None, alias="isEmpty", description="Whether the contact record is empty")
    is_payer: Optional[bool] = Field(None, alias="isPayer", description="Whether this contact is a payer")
    is_prefered: Optional[bool] = Field(None, alias="isPrefered", description="Whether this contact is preferred")
    is_primary: Optional[bool] = Field(None, alias="isPrimary", description="Whether this is the primary contact")
    is_private: Optional[bool] = Field(None, alias="isPrivate", description="Whether this contact is private")
    job_title: Optional[str] = Field(None, alias="jobTitle", description="Job title")
    job_title_id: Optional[int] = Field(None, alias="jobTitleId", description="Job title identifier")
    legacy_guid: Optional[str] = Field(None, alias="legacyGuid", description="Legacy system GUID")
    owner_franchisee_id: Optional[str] = Field(None, alias="ownerFranchiseeId", description="Owner franchisee UUID")
    phones_list: Optional[List[dict]] = Field(None, alias="phonesList", description="Phone numbers list")
    primary_email: Optional[str] = Field(None, alias="primaryEmail", description="Primary email address")
    primary_phone: Optional[str] = Field(None, alias="primaryPhone", description="Primary phone number")
    root_contact_id: Optional[int] = Field(None, alias="rootContactId", description="Root contact identifier")
    tax_id: Optional[str] = Field(None, alias="taxId", description="Tax ID")
    web_site: Optional[str] = Field(None, alias="webSite", description="Website URL")


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
    cell_phone: Optional[str] = Field(None, alias="cellPhone", description="Cell phone number")
    fax: Optional[str] = Field(None, description="Fax number")
    address: Optional[CompanyAddress] = Field(None, description="Contact address")


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


class ContactEditParams(RequestModel):
    """Query parameters for contact edit operations."""

    franchisee_id: Optional[str] = Field(None, alias="franchiseeId", description="Franchisee UUID filter")


class ContactHistoryParams(RequestModel):
    """Query parameters for contact history operations."""

    statuses: Optional[str] = Field(None, alias="statuses", description="Comma-separated status filters")


class ContactEditRequest(RequestModel):
    """Body for PUT /contacts/{id}/editdetails and POST /contacts/editdetails."""

    first_name: Optional[str] = Field(None, alias="firstName", description="First name")
    last_name: Optional[str] = Field(None, alias="lastName", description="Last name")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    addresses: Optional[List[dict]] = Field(None, description="Contact addresses")


class ContactSearchRequest(PaginatedRequestMixin, SearchableRequestMixin):
    """Body for POST /contacts/v2/search."""


# ---- Extended contact models (008) ----------------------------------------


class ContactHistory(ResponseModel):
    """Contact interaction history — POST /contacts/{contactId}/history."""

    events: Optional[List[dict]] = Field(None, description="History events")
    total_count: Optional[int] = Field(None, alias="totalCount", description="Total event count")


class ContactHistoryAggregated(ResponseModel):
    """Aggregated history — GET /contacts/{contactId}/history/aggregated."""

    summary: Optional[dict] = Field(None, description="Aggregated summary")
    by_type: Optional[List[dict]] = Field(None, alias="byType", description="Breakdown by type")


class ContactGraphData(ResponseModel):
    """Contact graph data — GET /contacts/{contactId}/history/graphdata."""

    data_points: Optional[List[dict]] = Field(None, alias="dataPoints", description="Graph data points")
    labels: Optional[List[str]] = Field(None, description="Graph labels")


class ContactMergePreview(ResponseModel):
    """Merge preview result — POST /contacts/{mergeToId}/merge/preview."""

    merge_to: Optional[dict] = Field(None, alias="mergeTo", description="Target contact")
    merge_from: Optional[dict] = Field(None, alias="mergeFrom", description="Source contact")
    conflicts: Optional[List[dict]] = Field(None, description="Merge conflicts")
