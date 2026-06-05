"""Job-scoped status operations — swagger tag ``JobStatus`` (1 route).

Exposed as ``api.jobs.status``. Old name (``set_quote_status``) remains
on :class:`~ab.api.endpoints.jobs.JobsEndpoint` as a deprecation shim.

Method renames:

* :meth:`set_quote`  (was ``set_quote_status``)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.shared import ServiceBaseResponse

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_SET_QUOTE = Route("POST", "/job/{jobDisplayId}/status/quote", response_model="ServiceBaseResponse")


class JobStatusEndpoint(BaseEndpoint):
    """Job-scoped status operations (ACPortal API)."""

    def set_quote(self, job_display_id: int) -> ServiceBaseResponse:
        """``POST /job/{jobDisplayId}/status/quote``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/status.set_quote.html
        Response model: ServiceBaseResponse
        """
        return self._request(_SET_QUOTE.bind(jobDisplayId=job_display_id))
