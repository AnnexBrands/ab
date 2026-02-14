"""Lookup models for the ACPortal API."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import ResponseModel


class ContactTypeEntity(ResponseModel):
    """Contact type — GET /lookup/contactTypes."""

    id: Optional[int] = Field(None, description="Contact type ID")
    name: Optional[str] = Field(None, description="Contact type name")
    description: Optional[str] = Field(None, description="Description")


class CountryCodeDto(ResponseModel):
    """Country code — GET /lookup/countries."""

    code: Optional[str] = Field(None, description="ISO country code")
    name: Optional[str] = Field(None, description="Country name")


class JobStatus(ResponseModel):
    """Job status entry — GET /lookup/jobStatuses."""

    id: Optional[int] = Field(None, description="Status ID")
    name: Optional[str] = Field(None, description="Status name")
    description: Optional[str] = Field(None, description="Description")


class LookupItem(ResponseModel):
    """Generic lookup item — GET /lookup/items."""

    id: Optional[int] = Field(None, description="Item ID")
    name: Optional[str] = Field(None, description="Item name")
    value: Optional[str] = Field(None, description="Item value")
