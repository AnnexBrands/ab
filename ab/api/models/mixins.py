"""Reusable mixin base classes for common ABConnect model fields."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Union

from pydantic import Field

from ab.api.models.base import ABConnectBaseModel, RequestModel


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


# --- Request mixins ---


class PaginatedRequestMixin(RequestModel):
    """Reusable pagination fields for request models."""

    page: Optional[int] = Field(None, description="Page number (1-based)")
    page_size: Optional[int] = Field(None, alias="pageSize", description="Items per page")


class SortableRequestMixin(RequestModel):
    """Reusable sort fields for request models."""

    sort_by: Optional[str] = Field(None, alias="sortBy", description="Field name to sort by")
    sort_dir: Optional[bool] = Field(None, alias="sortDir", description="Sort direction (true=ascending)")


class SearchableRequestMixin(RequestModel):
    """Reusable search text field for request models."""

    search_text: Optional[str] = Field(None, alias="searchText", description="Free-text search query")


class DateRangeRequestMixin(RequestModel):
    """Reusable date range fields for request models."""

    start_date: Optional[str] = Field(None, alias="startDate", description="Range start date (ISO 8601)")
    end_date: Optional[str] = Field(None, alias="endDate", description="Range end date (ISO 8601)")
