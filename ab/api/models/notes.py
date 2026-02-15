"""Global note models for the ACPortal API."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class GlobalNote(ResponseModel):
    """Global note record — GET /note."""

    id: Optional[str] = Field(None, description="Note ID")
    comment: Optional[str] = Field(None, description="Note content")
    author: Optional[str] = Field(None, description="Author name")
    modify_date: Optional[str] = Field(None, alias="modifyDate", description="Last modified date")
    category: Optional[str] = Field(None, description="Note category")
    is_important: Optional[bool] = Field(None, alias="isImportant", description="Flagged as important")
    is_completed: Optional[bool] = Field(None, alias="isCompleted", description="Completion status")
    job_id: Optional[str] = Field(None, alias="jobId", description="Associated job ID")
    contact_id: Optional[str] = Field(None, alias="contactId", description="Associated contact ID")
    company_id: Optional[str] = Field(None, alias="companyId", description="Associated company ID")


class GlobalNoteCreateRequest(RequestModel):
    """Body for POST /note."""

    comment: str = Field(..., description="Note content")
    category: Optional[str] = Field(None, description="Note category")
    job_id: Optional[str] = Field(None, alias="jobId", description="Associated job ID")
    contact_id: Optional[str] = Field(None, alias="contactId", description="Associated contact ID")
    company_id: Optional[str] = Field(None, alias="companyId", description="Associated company ID")


class GlobalNoteUpdateRequest(RequestModel):
    """Body for PUT /note/{id}."""

    comment: Optional[str] = Field(None, description="Updated content")
    is_important: Optional[bool] = Field(None, alias="isImportant", description="Updated importance flag")
    is_completed: Optional[bool] = Field(None, alias="isCompleted", description="Mark complete")


class SuggestedUser(ResponseModel):
    """User suggestion for mentions — GET /note/suggestUsers."""

    contact_id: Optional[str] = Field(None, alias="contactId", description="Contact ID")
    name: Optional[str] = Field(None, description="User name")
    email: Optional[str] = Field(None, description="User email")
