"""Intacct models for the ACPortal API.

Covers JobIntacct endpoints under /api/jobintacct/.
"""

from __future__ import annotations

from typing import Any, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class JobIntacctData(ResponseModel):
    """Intacct data for a job — GET/POST /jobintacct/{jobDisplayId}."""

    job_display_id: Optional[int] = Field(None, alias="jobDisplayId", description="Job display ID")
    intacct_id: Optional[str] = Field(None, alias="intacctId", description="Intacct record ID")
    status: Optional[str] = Field(None, description="Intacct sync status")
    data: Optional[dict] = Field(None, description="Intacct data payload")


class JobIntacctRequest(RequestModel):
    """Body for POST /jobintacct/{jobDisplayId}."""

    data: Optional[dict] = Field(None, description="Intacct data payload")


class JobIntacctDraftRequest(RequestModel):
    """Body for POST /jobintacct/{jobDisplayId}/draft."""

    data: Optional[dict] = Field(None, description="Draft Intacct data")


class ApplyRebateRequest(RequestModel):
    """Body for POST /jobintacct/{jobDisplayId}/applyRebate."""

    rebate_amount: Optional[float] = Field(None, alias="rebateAmount", description="Rebate amount")
