"""RFQ API endpoints (7 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.rfq import AcceptModel, QuoteRequestDisplayInfo

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET = Route("GET", "/rfq/{rfqId}", response_model="QuoteRequestDisplayInfo")
_GET_FOR_JOB = Route(
    "GET", "/rfq/forjob/{jobId}", params_model="RfqForJobParams", response_model="List[QuoteRequestDisplayInfo]"
)
_ACCEPT = Route("POST", "/rfq/{rfqId}/accept", request_model="AcceptModel")
_DECLINE = Route("POST", "/rfq/{rfqId}/decline")
_CANCEL = Route("POST", "/rfq/{rfqId}/cancel")
_ACCEPT_WINNER = Route("POST", "/rfq/{rfqId}/acceptwinner", params_model="RfqAcceptWinnerParams")
_ADD_COMMENT = Route("POST", "/rfq/{rfqId}/comment", request_model="AcceptModel")


class RFQEndpoint(BaseEndpoint):
    """RFQ lifecycle operations (ACPortal API)."""

    def get(self, rfq_id: str) -> QuoteRequestDisplayInfo:
        """GET /rfq/{rfqId}

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/rfq/get.html
        Response model: QuoteRequestDisplayInfo
        """
        return self._request(_GET.bind(rfqId=rfq_id))

    def get_for_job(self, job_id: str) -> list[QuoteRequestDisplayInfo]:
        """GET /rfq/forjob/{jobId}

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/rfq/get_for_job.html
        Query params: RfqForJobParams
        Response model: List[QuoteRequestDisplayInfo]
        """
        return self._request(_GET_FOR_JOB.bind(jobId=job_id))

    def accept(self, rfq_id: str, *, data: AcceptModel | dict) -> None:
        """POST /rfq/{rfqId}/accept.

        Args:
            rfq_id: RFQ identifier.
            data: Acceptance payload.
                Accepts an :class:`AcceptModel` instance or a dict.

        Request model: :class:`AcceptModel`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/rfq/accept.html
        Request model: AcceptModel
        """
        return self._request(_ACCEPT.bind(rfqId=rfq_id), json=data)

    def decline(self, rfq_id: str) -> None:
        """POST /rfq/{rfqId}/decline

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/rfq/decline.html
        """
        return self._request(_DECLINE.bind(rfqId=rfq_id))

    def cancel(self, rfq_id: str) -> None:
        """POST /rfq/{rfqId}/cancel

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/rfq/cancel.html
        """
        return self._request(_CANCEL.bind(rfqId=rfq_id))

    def accept_winner(self, rfq_id: str) -> None:
        """POST /rfq/{rfqId}/acceptwinner

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/rfq/accept_winner.html
        Query params: RfqAcceptWinnerParams
        """
        return self._request(_ACCEPT_WINNER.bind(rfqId=rfq_id))

    def add_comment(self, rfq_id: str, *, data: AcceptModel | dict) -> None:
        """POST /rfq/{rfqId}/comment.

        Args:
            rfq_id: RFQ identifier.
            data: Comment payload.
                Accepts an :class:`AcceptModel` instance or a dict.

        Request model: :class:`AcceptModel`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/rfq/add_comment.html
        Request model: AcceptModel
        """
        return self._request(_ADD_COMMENT.bind(rfqId=rfq_id), json=data)
