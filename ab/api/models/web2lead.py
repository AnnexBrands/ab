"""Web2Lead models for the ABC API."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class Web2LeadGetParams(RequestModel):
    """Query parameters for GET /Web2Lead/get — 29 params, all optional strings."""

    access_key: Optional[str] = Field(None, alias="AccessKey", description="API access key")
    first_name: Optional[str] = Field(None, alias="FirstName", description="Lead first name")
    last_name: Optional[str] = Field(None, alias="LastName", description="Lead last name")
    address1: Optional[str] = Field(None, alias="Address1", description="Street address line 1")
    address2: Optional[str] = Field(None, alias="Address2", description="Street address line 2")
    city: Optional[str] = Field(None, alias="City", description="City")
    state_province: Optional[str] = Field(None, alias="StateProvince", description="State or province")
    zip_postal_code: Optional[str] = Field(None, alias="ZipPostalCode", description="ZIP or postal code")
    referrer_page: Optional[str] = Field(None, alias="ReferrerPage", description="Referring page URL")
    entry_url: Optional[str] = Field(None, alias="EntryUrl", description="Entry URL")
    submission_page: Optional[str] = Field(None, alias="SubmissionPage", description="Form submission page")
    how_heard: Optional[str] = Field(None, alias="HowHeard", description="How the lead heard about us")
    email: Optional[str] = Field(None, alias="Email", description="Lead email address")
    phone: Optional[str] = Field(None, alias="Phone", description="Lead phone number")
    ship_date: Optional[str] = Field(None, alias="ShipDate", description="Requested ship date")
    ship_from: Optional[str] = Field(None, alias="ShipFrom", description="Ship from location")
    ship_to: Optional[str] = Field(None, alias="ShipTo", description="Ship to location")
    business_lead: Optional[str] = Field(None, alias="BusinessLead", description="Business lead flag")
    referred_by: Optional[str] = Field(None, alias="ReferredBy", description="Referral source")
    referred_name: Optional[str] = Field(None, alias="ReferredName", description="Referrer name")
    customer_comments: Optional[str] = Field(None, alias="CustomerComments", description="Customer comments")
    ip_address: Optional[str] = Field(None, alias="IPAddress", description="Client IP address")
    search_term: Optional[str] = Field(None, alias="SearchTerm", description="Search term used")
    franchisee_id: Optional[str] = Field(None, alias="FranchiseeId", description="Franchisee UUID")
    company_name: Optional[str] = Field(None, alias="CompanyName", description="Company name")
    paid: Optional[str] = Field(None, alias="Paid", description="Paid status")
    commodity: Optional[str] = Field(None, alias="Commodity", description="Commodity type")
    industry: Optional[str] = Field(None, alias="Industry", description="Industry")
    full_name: Optional[str] = Field(None, alias="FullName", description="Lead full name")


class Web2LeadGETResult(ResponseModel):
    """Inner result object from GET /Web2Lead/get."""

    nc_import_failed: Optional[bool] = Field(None, alias="NC_Import_Failed", description="Whether import failed")
    nc_import_error_message: Optional[str] = Field(None, alias="NC_Import_ErrorMessage", description="Error message")
    nc_job_id: Optional[str] = Field(None, alias="NC_JobId", description="Created job ID")
    nc_contact_id: Optional[str] = Field(None, alias="NC_ContactId", description="Created contact ID")


class Web2LeadResponse(ResponseModel):
    """Response from GET /Web2Lead/get.

    Live API wraps the result under ``SubmitNewLeadGETResult``.
    """

    result: Optional[Web2LeadGETResult] = Field(
        None, alias="SubmitNewLeadGETResult", description="Lead submission result"
    )


class Web2LeadRequest(RequestModel):
    """Body for POST /Web2Lead/post."""

    name: Optional[str] = Field(None, description="Lead name")
    email: Optional[str] = Field(None, description="Lead email")
    phone: Optional[str] = Field(None, description="Lead phone")
    company: Optional[str] = Field(None, description="Lead company")
    message: Optional[str] = Field(None, description="Lead message/inquiry")
