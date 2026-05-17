"""Job-scoped tracking operations — swagger tag ``JobTracking`` (2 routes).

Exposed as ``api.jobs.tracking``. Old names on
:class:`~ab.api.endpoints.jobs.JobsEndpoint` remain as deprecation shims.

Method renames (``get_tracking`` collapsed):

* :meth:`get`     (was ``get_tracking``)        — ``GET /job/{id}/tracking``
* :meth:`v3`      (was ``get_tracking_v3``)     — ``GET /v3/job/{id}/tracking/{historyAmount}``

The ``v3`` route lives under ``/v3/`` (not ``/job/{id}/tracking/``)
because it's a separate versioned controller; both methods are tagged
``JobTracking`` in swagger.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.jobs import TrackingInfo, TrackingInfoV3

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET = Route("GET", "/job/{jobDisplayId}/tracking", response_model="TrackingInfo")
_GET_V3 = Route(
    "GET",
    "/v3/job/{jobDisplayId}/tracking/{historyAmount}",
    response_model="TrackingInfoV3",
    params_model="TrackingV3Params",
)


class JobTrackingEndpoint(BaseEndpoint):
    """Job-scoped tracking operations (ACPortal API)."""

    def get(self, job_display_id: int) -> TrackingInfo:
        """``GET /job/{jobDisplayId}/tracking``"""
        return self._request(_GET.bind(jobDisplayId=job_display_id))

    def v3(self, job_display_id: int, history_amount: int = 10) -> TrackingInfoV3:
        """``GET /v3/job/{jobDisplayId}/tracking/{historyAmount}``"""
        return self._request(
            _GET_V3.bind(jobDisplayId=job_display_id, historyAmount=history_amount),
        )
