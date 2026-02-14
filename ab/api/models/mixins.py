"""Reusable mixin base classes for common ABConnect model fields."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Union

from pydantic import Field

from ab.api.models.base import ABConnectBaseModel


class IdentifiedModel(ABConnectBaseModel):
    """Mixin for models with an ``id`` field."""

    id: Optional[Union[str, int]] = Field(None, description="Unique identifier")


class TimestampedModel(ABConnectBaseModel):
    """Mixin for models with created/modified audit timestamps."""

    created_date: Optional[datetime] = Field(None, alias="createdDate", description="Creation timestamp")
    modified_date: Optional[datetime] = Field(None, alias="modifiedDate", description="Last modification timestamp")
    created_by: Optional[str] = Field(None, alias="createdBy", description="Creator identifier")
    modified_by: Optional[str] = Field(None, alias="modifiedBy", description="Last modifier identifier")


class ActiveModel(ABConnectBaseModel):
    """Mixin for models with an ``is_active`` flag."""

    is_active: Optional[bool] = Field(None, alias="isActive", description="Whether the record is active")


class CompanyRelatedModel(ABConnectBaseModel):
    """Mixin for models associated with a company."""

    company_id: Optional[str] = Field(None, alias="companyId", description="Associated company ID")
    company_name: Optional[str] = Field(None, alias="companyName", description="Associated company name")


class JobRelatedModel(ABConnectBaseModel):
    """Mixin for models associated with a job."""

    job_id: Optional[str] = Field(None, alias="jobId", description="Associated job ID")


# --- Composite mixins ---


class FullAuditModel(IdentifiedModel, TimestampedModel, ActiveModel):
    """ID + timestamps + active status."""


class CompanyAuditModel(FullAuditModel, CompanyRelatedModel):
    """Full audit trail + company association."""


class JobAuditModel(FullAuditModel, JobRelatedModel):
    """Full audit trail + job association."""
