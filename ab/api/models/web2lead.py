"""Web2Lead models for the ABC API."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


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
