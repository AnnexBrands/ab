"""E-Sign models for the ACPortal API.

Covers JobSign endpoints under /api/e-sign/.
"""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import ResponseModel


class ESignResult(ResponseModel):
    """E-sign result — GET /e-sign/result."""

    status: Optional[str] = Field(None, description="E-sign status")
    envelope_id: Optional[str] = Field(None, alias="envelopeId", description="DocuSign envelope ID")
    event: Optional[str] = Field(None, description="E-sign event type")


class ESignData(ResponseModel):
    """E-sign data — GET /e-sign/{jobDisplayId}/{bookingKey}."""

    job_display_id: Optional[int] = Field(None, alias="jobDisplayId", description="Job display ID")
    booking_key: Optional[str] = Field(None, alias="bookingKey", description="Booking key")
    signing_url: Optional[str] = Field(None, alias="signingUrl", description="Signing URL")
    status: Optional[str] = Field(None, description="E-sign status")
