"""Job-scoped RFQ operations — swagger tag ``JobRfq`` (2 routes).

Exposed as ``api.jobs.rfq``. Old names on
:class:`~ab.api.endpoints.jobs.JobsEndpoint` (``list_rfqs``,
``get_rfq_status``) remain as deprecation shims.

The standalone :class:`~ab.api.endpoints.rfq.RFQEndpoint` (``api.rfq``)
keeps its 7 ``/rfq/*`` lifecycle methods (get / accept / decline / …);
only the two job-scoped ``/job/{jobDisplayId}/rfq/*`` routes live here.

Method renames (drop redundant ``_rfq(s)`` suffix):

* :meth:`list`         (was ``list_rfqs``)
* :meth:`status`       (was ``get_rfq_status``)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.rfq import QuoteRequestDisplayInfo

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_LIST = Route(
    "GET", "/job/{jobDisplayId}/rfq",
    params_model="JobRfqListParams", response_model="List[QuoteRequestDisplayInfo]",
)
_STATUS = Route(
    "GET",
    "/job/{jobDisplayId}/rfq/statusof/{rfqServiceType}/forcompany/{companyId}",
    response_model="int",
)


class JobRfqEndpoint(BaseEndpoint):
    """Job-scoped RFQ operations (ACPortal API)."""

    def list(self, job_display_id: int) -> list[QuoteRequestDisplayInfo]:
        """``GET /job/{jobDisplayId}/rfq``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/rfq.list.html
        Query params: JobRfqListParams
        Response model: List[QuoteRequestDisplayInfo]
        """
        return self._request(_LIST.bind(jobDisplayId=job_display_id))

    def status(self, job_display_id: int, rfq_service_type: str, company_id: str) -> int:
        """``GET /job/{jobDisplayId}/rfq/statusof/{rfqServiceType}/forcompany/{companyId}``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/rfq.status.html
        """
        return self._request(
            _STATUS.bind(
                jobDisplayId=job_display_id,
                rfqServiceType=rfq_service_type,
                companyId=company_id,
            )
        )
