"""Admin models for the ACPortal API.

Covers AdvancedSettings, CarrierErrorMessage, GlobalSettings,
and LogBuffer endpoints under /api/admin/.
"""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


# ---- Advanced Settings ------------------------------------------------------


class AdvancedSetting(ResponseModel):
    """Advanced setting — GET/POST /admin/advancedsettings."""

    id: Optional[str] = Field(None, description="Setting ID")
    key: Optional[str] = Field(None, description="Setting key")
    value: Optional[str] = Field(None, description="Setting value")
    description: Optional[str] = Field(None, description="Setting description")


class AdvancedSettingRequest(RequestModel):
    """Body for POST /admin/advancedsettings."""

    key: Optional[str] = Field(None, description="Setting key")
    value: Optional[str] = Field(None, description="Setting value")
    description: Optional[str] = Field(None, description="Setting description")


# ---- Carrier Error Messages -------------------------------------------------


class CarrierErrorMessage(ResponseModel):
    """Carrier error message — GET/POST /admin/carriererrormessage."""

    id: Optional[str] = Field(None, description="Error message ID")
    carrier: Optional[str] = Field(None, description="Carrier name")
    error_message: Optional[str] = Field(None, alias="errorMessage", description="Error message text")
    resolution: Optional[str] = Field(None, description="Resolution instructions")


class CarrierErrorMessageRequest(RequestModel):
    """Body for POST /admin/carriererrormessage."""

    carrier: Optional[str] = Field(None, description="Carrier name")
    error_message: Optional[str] = Field(None, alias="errorMessage", description="Error message text")
    resolution: Optional[str] = Field(None, description="Resolution instructions")


# ---- Global Settings --------------------------------------------------------


class CompanyHierarchy(ResponseModel):
    """Company hierarchy — GET /admin/globalsettings/companyhierarchy."""

    companies: Optional[List[dict]] = Field(None, description="Hierarchical company list")


class InsuranceException(ResponseModel):
    """Insurance exception — POST /admin/globalsettings/getinsuranceexceptions."""

    id: Optional[str] = Field(None, description="Exception ID")
    job_id: Optional[str] = Field(None, alias="jobId", description="Job ID")
    reason: Optional[str] = Field(None, description="Exception reason")
    status: Optional[str] = Field(None, description="Exception status")


class InsuranceExceptionFilter(RequestModel):
    """Body for POST /admin/globalsettings/getinsuranceexceptions."""

    status: Optional[str] = Field(None, description="Filter by status")
    company_id: Optional[str] = Field(None, alias="companyId", description="Filter by company")


class IntacctSettings(ResponseModel):
    """Intacct settings — POST /admin/globalsettings/intacct."""

    settings: Optional[dict] = Field(None, description="Intacct integration settings")


class IntacctSettingsRequest(RequestModel):
    """Body for POST /admin/globalsettings/intacct."""

    settings: Optional[dict] = Field(None, description="Intacct integration settings")


# ---- Log Buffer -------------------------------------------------------------


class LogFlushRequest(RequestModel):
    """Body for POST /admin/logbuffer/flush (optional body)."""

    log_type: Optional[str] = Field(None, alias="logType", description="Type of logs to flush")
