"""Shipments API endpoints — ACPortal.

Three routes remain here (non-job-scoped); the 11 job-scoped routes
have moved to :class:`~ab.api.endpoints.jobs.shipment.JobShipmentEndpoint`
(``api.jobs.shipment``). Deprecation shims for the moved methods are
retained on this class.
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.shared import ServiceBaseResponse
    from ab.api.models.shipments import (
        Accessorial,
        AccessorialAddRequest,
        GlobalAccessorial,
        RateQuote,
        RatesState,
        ShipmentBookRequest,
        ShipmentExportData,
        ShipmentExportRequest,
        ShipmentInfo,
        ShipmentOriginDestination,
        ShipmentRateQuoteRequest,
    )

from ab.api.base import BaseEndpoint
from ab.api.endpoints.jobs.shipment import JobShipmentEndpoint
from ab.api.route import Route

# Non-job-scoped routes (kept here)
_GET_SHIPMENT = Route("GET", "/shipment", params_model="ShipmentParams", response_model="ShipmentInfo")
_GET_GLOBAL_ACCESSORIALS = Route("GET", "/shipment/accessorials", response_model="List[GlobalAccessorial]")
_GET_SHIPMENT_DOCUMENT = Route(
    "GET", "/shipment/document/{docId}",
    params_model="ShipmentDocumentParams", response_model="bytes",
)


def _deprecated(old: str, new: str) -> None:
    warnings.warn(
        f"api.shipments.{old}() is deprecated; use api.jobs.shipment.{new}() instead.",
        DeprecationWarning,
        stacklevel=3,
    )


class ShipmentsEndpoint(BaseEndpoint):
    """Non-job-scoped shipment operations (ACPortal API).

    The job-scoped methods live at ``api.jobs.shipment``; they remain
    here only as deprecation shims.
    """

    def __init__(self, client) -> None:
        super().__init__(client)
        self._shipment = JobShipmentEndpoint(client)

    # ---- Non-job-scoped routes (canonical home) -----------------------

    def get_shipment(
        self,
        *,
        franchisee_id: str | None = None,
        provider_id: str | None = None,
        pro_number: str | None = None,
    ) -> ShipmentInfo:
        """``GET /shipment``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/shipments/get_shipment.html
        Query params: ShipmentParams
        Response model: ShipmentInfo
        """
        return self._request(
            _GET_SHIPMENT,
            params=dict(franchisee_id=franchisee_id, provider_id=provider_id, pro_number=pro_number),
        )

    def get_global_accessorials(self) -> list[GlobalAccessorial]:
        """``GET /shipment/accessorials``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/shipments/get_global_accessorials.html
        Response model: List[GlobalAccessorial]
        """
        return self._request(_GET_GLOBAL_ACCESSORIALS)

    def get_shipment_document(self, doc_id: str) -> bytes:
        """``GET /shipment/document/{docId}``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/shipments/get_shipment_document.html
        Query params: ShipmentDocumentParams
        """
        return self._request(_GET_SHIPMENT_DOCUMENT.bind(docId=doc_id))

    # ---- Job-scoped (deprecated shims) --------------------------------

    def get_rate_quotes(self, job_display_id: int) -> list[RateQuote]:
        """Deprecated. Use ``api.jobs.shipment.get_rate_quotes(...)``."""
        _deprecated("get_rate_quotes", "get_rate_quotes")
        return self._shipment.get_rate_quotes(job_display_id)

    def request_rate_quotes(
        self, job_display_id: int, *, data: ShipmentRateQuoteRequest | dict,
    ) -> list[RateQuote]:
        """Deprecated. Use ``api.jobs.shipment.request_rate_quotes(...)``."""
        _deprecated("request_rate_quotes", "request_rate_quotes")
        return self._shipment.request_rate_quotes(job_display_id, data=data)

    def book(self, job_display_id: int, *, data: ShipmentBookRequest | dict) -> ServiceBaseResponse:
        """Deprecated. Use ``api.jobs.shipment.book(...)``."""
        _deprecated("book", "book")
        return self._shipment.book(job_display_id, data=data)

    def delete_shipment(self, job_display_id: int) -> ServiceBaseResponse:
        """Deprecated. Use ``api.jobs.shipment.delete(...)``."""
        _deprecated("delete_shipment", "delete")
        return self._shipment.delete(job_display_id)

    def get_accessorials(self, job_display_id: int) -> list[Accessorial]:
        """Deprecated. Use ``api.jobs.shipment.get_accessorials(...)``."""
        _deprecated("get_accessorials", "get_accessorials")
        return self._shipment.get_accessorials(job_display_id)

    def add_accessorial(
        self, job_display_id: int, *, data: AccessorialAddRequest | dict,
    ) -> ServiceBaseResponse:
        """Deprecated. Use ``api.jobs.shipment.add_accessorial(...)``."""
        _deprecated("add_accessorial", "add_accessorial")
        return self._shipment.add_accessorial(job_display_id, data=data)

    def remove_accessorial(self, job_display_id: int, add_on_id: str) -> ServiceBaseResponse:
        """Deprecated. Use ``api.jobs.shipment.remove_accessorial(...)``."""
        _deprecated("remove_accessorial", "remove_accessorial")
        return self._shipment.remove_accessorial(job_display_id, add_on_id)

    def get_origin_destination(self, job_display_id: int) -> ShipmentOriginDestination:
        """Deprecated. Use ``api.jobs.shipment.get_origin_destination(...)``."""
        _deprecated("get_origin_destination", "get_origin_destination")
        return self._shipment.get_origin_destination(job_display_id)

    def get_export_data(self, job_display_id: int) -> ShipmentExportData:
        """Deprecated. Use ``api.jobs.shipment.get_export_data(...)``."""
        _deprecated("get_export_data", "get_export_data")
        return self._shipment.get_export_data(job_display_id)

    def post_export_data(
        self, job_display_id: int, *, data: ShipmentExportRequest | dict,
    ) -> ServiceBaseResponse:
        """Deprecated. Use ``api.jobs.shipment.post_export_data(...)``."""
        _deprecated("post_export_data", "post_export_data")
        return self._shipment.post_export_data(job_display_id, data=data)

    def get_rates_state(self, job_display_id: int) -> RatesState:
        """Deprecated. Use ``api.jobs.shipment.get_rates_state(...)``."""
        _deprecated("get_rates_state", "get_rates_state")
        return self._shipment.get_rates_state(job_display_id)

    # ---- Pre-existing aliases (now also deprecated) -------------------

    def delete(self, job_display_id: int) -> ServiceBaseResponse:
        """Legacy alias of :meth:`delete_shipment`."""
        _deprecated("delete", "delete")
        return self._shipment.delete(job_display_id)

    def get_origin_dest(self, job_display_id: int) -> ShipmentOriginDestination:
        """Legacy alias of :meth:`get_origin_destination`."""
        _deprecated("get_origin_dest", "get_origin_destination")
        return self._shipment.get_origin_destination(job_display_id)
