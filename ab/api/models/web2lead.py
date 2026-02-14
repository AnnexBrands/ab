"""Web2Lead models for the ABC API."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class Web2LeadResponse(ResponseModel):
    """Response from Web2Lead endpoints."""

    success: Optional[bool] = Field(None, description="Whether the operation succeeded")
    lead_id: Optional[str] = Field(None, alias="leadId", description="Created lead ID")


class Web2LeadRequest(RequestModel):
    """Body for POST /Web2Lead/post."""

    name: Optional[str] = Field(None, description="Lead name")
    email: Optional[str] = Field(None, description="Lead email")
    phone: Optional[str] = Field(None, description="Lead phone")
    company: Optional[str] = Field(None, description="Lead company")
    message: Optional[str] = Field(None, description="Lead message/inquiry")
