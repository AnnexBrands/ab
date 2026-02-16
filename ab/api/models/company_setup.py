"""Company setup models for the ACPortal API.

Covers Calendar, Stripe External Accounts, Document Templates,
Grid/Setup Settings, Container Thickness, and Planner endpoints
under /api/company/{companyId}/.
"""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


# ---- Calendar ---------------------------------------------------------------


class CalendarDay(ResponseModel):
    """Calendar day data — GET /company/{companyId}/calendar/{date}."""

    date: Optional[str] = Field(None, description="Calendar date")
    is_business_day: Optional[bool] = Field(None, alias="isBusinessDay", description="Whether this is a business day")
    events: Optional[List[dict]] = Field(None, description="Calendar events for the day")


class CalendarBaseInfo(ResponseModel):
    """Calendar base info — GET /company/{companyId}/calendar/{date}/baseinfo."""

    date: Optional[str] = Field(None, description="Calendar date")
    business_hours: Optional[dict] = Field(None, alias="businessHours", description="Business hours configuration")


class CalendarTimeInfo(ResponseModel):
    """Calendar time info — GET /company/{companyId}/calendar/{date}/startofday|endofday."""

    date: Optional[str] = Field(None, description="Calendar date")
    time: Optional[str] = Field(None, description="Time value (start or end of day)")


# ---- Stripe External Accounts ----------------------------------------------


class StripeConnectUrl(ResponseModel):
    """Stripe connect URL — GET /company/{companyId}/accounts/stripe/connecturl."""

    url: Optional[str] = Field(None, description="Stripe OAuth connect URL")


class StripeConnection(ResponseModel):
    """Stripe connection result — POST /company/{companyId}/accounts/stripe/completeconnection."""

    connected: Optional[bool] = Field(None, description="Whether the connection was successful")
    account_id: Optional[str] = Field(None, alias="accountId", description="Stripe account ID")


class StripeCompleteRequest(RequestModel):
    """Body for POST /company/{companyId}/accounts/stripe/completeconnection."""

    code: Optional[str] = Field(None, description="OAuth authorization code")
    state: Optional[str] = Field(None, description="OAuth state parameter")


# ---- Document Templates -----------------------------------------------------


class DocumentTemplate(ResponseModel):
    """Document template — GET/POST/PUT /company/{companyId}/document-templates."""

    id: Optional[str] = Field(None, description="Template ID")
    name: Optional[str] = Field(None, description="Template name")
    content: Optional[str] = Field(None, description="Template content")
    template_type: Optional[str] = Field(None, alias="templateType", description="Template type")
    company_id: Optional[str] = Field(None, alias="companyId", description="Company ID")


class DocumentTemplateRequest(RequestModel):
    """Body for POST/PUT /company/{companyId}/document-templates."""

    name: Optional[str] = Field(None, description="Template name")
    content: Optional[str] = Field(None, description="Template content")
    template_type: Optional[str] = Field(None, alias="templateType", description="Template type")


# ---- Grid/Setup Settings ----------------------------------------------------


class GridSettings(ResponseModel):
    """Grid settings — GET/POST /company/{companyId}/gridsettings."""

    company_id: Optional[str] = Field(None, alias="companyId", description="Company ID")
    settings: Optional[dict] = Field(None, description="Grid settings data")


class GridSettingsRequest(RequestModel):
    """Body for POST /company/{companyId}/gridsettings."""

    settings: Optional[dict] = Field(None, description="Grid settings data")


class CompanySetupData(ResponseModel):
    """Company setup data — GET /company/{companyId}/setupdata."""

    company_id: Optional[str] = Field(None, alias="companyId", description="Company ID")
    setup: Optional[dict] = Field(None, description="Setup configuration data")


# ---- Container Thickness ----------------------------------------------------


class ContainerThickness(ResponseModel):
    """Container thickness — GET/POST /company/{companyId}/containerthicknessinches."""

    id: Optional[str] = Field(None, description="Container thickness ID")
    thickness: Optional[float] = Field(None, description="Thickness in inches")
    description: Optional[str] = Field(None, description="Description")
    company_id: Optional[str] = Field(None, alias="companyId", description="Company ID")


class ContainerThicknessRequest(RequestModel):
    """Body for POST /company/{companyId}/containerthicknessinches."""

    thickness: Optional[float] = Field(None, description="Thickness in inches")
    description: Optional[str] = Field(None, description="Description")


# ---- Planner ----------------------------------------------------------------


class PlannerEntry(ResponseModel):
    """Planner entry — GET /company/{companyId}/planner."""

    id: Optional[str] = Field(None, description="Planner entry ID")
    date: Optional[str] = Field(None, description="Planned date")
    details: Optional[dict] = Field(None, description="Planner entry details")


# ---- Material ---------------------------------------------------------------


class Material(ResponseModel):
    """Material — GET/POST/PUT /company/{companyId}/material."""

    id: Optional[str] = Field(None, description="Material ID")
    name: Optional[str] = Field(None, description="Material name")
    description: Optional[str] = Field(None, description="Material description")
    company_id: Optional[str] = Field(None, alias="companyId", description="Company ID")


class MaterialRequest(RequestModel):
    """Body for POST/PUT /company/{companyId}/material."""

    name: Optional[str] = Field(None, description="Material name")
    description: Optional[str] = Field(None, description="Material description")


# ---- Truck ------------------------------------------------------------------


class Truck(ResponseModel):
    """Truck — GET/POST/PUT /company/{companyId}/truck."""

    id: Optional[str] = Field(None, description="Truck ID")
    name: Optional[str] = Field(None, description="Truck name")
    description: Optional[str] = Field(None, description="Truck description")
    company_id: Optional[str] = Field(None, alias="companyId", description="Company ID")


class TruckRequest(RequestModel):
    """Body for POST/PUT /company/{companyId}/truck."""

    name: Optional[str] = Field(None, description="Truck name")
    description: Optional[str] = Field(None, description="Truck description")
