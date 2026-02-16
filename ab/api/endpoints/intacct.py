"""Intacct API endpoints (5 routes).

Covers JobIntacct endpoints under /api/jobintacct/.
"""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET_JOB_INTACCT = Route("GET", "/jobintacct/{jobDisplayId}", response_model="JobIntacctData")
_POST_JOB_INTACCT = Route("POST", "/jobintacct/{jobDisplayId}", request_model="JobIntacctRequest", response_model="JobIntacctData")
_POST_DRAFT = Route("POST", "/jobintacct/{jobDisplayId}/draft", request_model="JobIntacctDraftRequest", response_model="JobIntacctData")
_POST_APPLY_REBATE = Route("POST", "/jobintacct/{jobDisplayId}/applyRebate", request_model="ApplyRebateRequest")
_DELETE_FRANCHISEE = Route("DELETE", "/jobintacct/{jobDisplayId}/{franchiseeId}")


class IntacctEndpoint(BaseEndpoint):
    """Intacct accounting integration (ACPortal API)."""

    def get(self, job_display_id: int) -> Any:
        """GET /jobintacct/{jobDisplayId}"""
        return self._request(_GET_JOB_INTACCT.bind(jobDisplayId=job_display_id))

    def post(self, job_display_id: int, **kwargs: Any) -> Any:
        """POST /jobintacct/{jobDisplayId}"""
        return self._request(_POST_JOB_INTACCT.bind(jobDisplayId=job_display_id), json=kwargs)

    def draft(self, job_display_id: int, **kwargs: Any) -> Any:
        """POST /jobintacct/{jobDisplayId}/draft"""
        return self._request(_POST_DRAFT.bind(jobDisplayId=job_display_id), json=kwargs)

    def apply_rebate(self, job_display_id: int, **kwargs: Any) -> Any:
        """POST /jobintacct/{jobDisplayId}/applyRebate"""
        return self._request(_POST_APPLY_REBATE.bind(jobDisplayId=job_display_id), json=kwargs)

    def delete_franchisee(self, job_display_id: int, franchisee_id: str) -> Any:
        """DELETE /jobintacct/{jobDisplayId}/{franchiseeId}"""
        return self._request(_DELETE_FRANCHISEE.bind(jobDisplayId=job_display_id, franchiseeId=franchisee_id))
