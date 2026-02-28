"""Shipments API endpoints — ACPortal.

Covers job-scoped shipment operations (rate quotes, booking, accessorials)
and global shipment endpoints (shipment lookup, accessorial catalog, documents).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

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
from ab.api.route import Route

# Job-scoped shipment routes
_GET_RATE_QUOTES = Route(
    "GET", "/job/{jobDisplayId}/shipment/ratequotes",
    params_model="RateQuotesParams", response_model="List[RateQuote]",
)
_POST_RATE_QUOTES = Route(
    "POST", "/job/{jobDisplayId}/shipment/ratequotes",
    request_model="ShipmentRateQuoteRequest", response_model="List[RateQuote]",
)
_BOOK = Route(
    "POST", "/job/{jobDisplayId}/shipment/book",
    request_model="ShipmentBookRequest", response_model="ServiceBaseResponse",
)
_DELETE_SHIPMENT = Route("DELETE", "/job/{jobDisplayId}/shipment", response_model="ServiceBaseResponse")
_GET_ACCESSORIALS = Route(
    "GET", "/job/{jobDisplayId}/shipment/accessorials", response_model="List[Accessorial]",
)
_ADD_ACCESSORIAL = Route(
    "POST", "/job/{jobDisplayId}/shipment/accessorial",
    request_model="AccessorialAddRequest", response_model="ServiceBaseResponse",
)
_REMOVE_ACCESSORIAL = Route(
    "DELETE", "/job/{jobDisplayId}/shipment/accessorial/{addOnId}",
    response_model="ServiceBaseResponse",
)
_GET_ORIGIN_DEST = Route(
    "GET", "/job/{jobDisplayId}/shipment/origindestination",
    response_model="ShipmentOriginDestination",
)
_GET_EXPORT_DATA = Route("GET", "/job/{jobDisplayId}/shipment/exportdata", response_model="ShipmentExportData")
_POST_EXPORT_DATA = Route(
    "POST", "/job/{jobDisplayId}/shipment/exportdata",
    request_model="ShipmentExportRequest", response_model="ServiceBaseResponse",
)
_GET_RATES_STATE = Route("GET", "/job/{jobDisplayId}/shipment/ratesstate", response_model="RatesState")

# Global shipment routes
_GET_SHIPMENT = Route("GET", "/shipment", params_model="ShipmentParams", response_model="ShipmentInfo")
_GET_GLOBAL_ACCESSORIALS = Route("GET", "/shipment/accessorials", response_model="List[GlobalAccessorial]")
_GET_SHIPMENT_DOCUMENT = Route(
    "GET", "/shipment/document/{docId}",
    params_model="ShipmentDocumentParams", response_model="bytes",
)


class ShipmentsEndpoint(BaseEndpoint):
    """Shipment operations (ACPortal API)."""

    # ---- Job-scoped shipment methods ----------------------------------

    def get_rate_quotes(self, job_display_id: int) -> list[RateQuote]:
        """GET /job/{jobDisplayId}/shipment/ratequotes (ACPortal)"""
        return self._request(_GET_RATE_QUOTES.bind(jobDisplayId=job_display_id))

    def request_rate_quotes(self, job_display_id: int, *, data: ShipmentRateQuoteRequest | dict) -> list[RateQuote]:
        """POST /job/{jobDisplayId}/shipment/ratequotes.

        Args:
            job_display_id: Job display ID.
            data: Rate quote request payload.
                Accepts a :class:`ShipmentRateQuoteRequest` instance or a dict.

        Request model: :class:`ShipmentRateQuoteRequest`
        """
        return self._request(_POST_RATE_QUOTES.bind(jobDisplayId=job_display_id), json=data)

    def book(self, job_display_id: int, *, data: ShipmentBookRequest | dict) -> ServiceBaseResponse:
        """POST /job/{jobDisplayId}/shipment/book.

        Args:
            job_display_id: Job display ID.
            data: Shipment booking payload.
                Accepts a :class:`ShipmentBookRequest` instance or a dict.

        Request model: :class:`ShipmentBookRequest`
        """
        return self._request(_BOOK.bind(jobDisplayId=job_display_id), json=data)

    def delete_shipment(self, job_display_id: int) -> ServiceBaseResponse:
        """DELETE /job/{jobDisplayId}/shipment (ACPortal)"""
        return self._request(_DELETE_SHIPMENT.bind(jobDisplayId=job_display_id))

    def get_accessorials(self, job_display_id: int) -> list[Accessorial]:
        """GET /job/{jobDisplayId}/shipment/accessorials (ACPortal)"""
        return self._request(_GET_ACCESSORIALS.bind(jobDisplayId=job_display_id))

    def add_accessorial(self, job_display_id: int, *, data: AccessorialAddRequest | dict) -> ServiceBaseResponse:
        """POST /job/{jobDisplayId}/shipment/accessorial.

        Args:
            job_display_id: Job display ID.
            data: Accessorial add payload.
                Accepts an :class:`AccessorialAddRequest` instance or a dict.

        Request model: :class:`AccessorialAddRequest`
        """
        return self._request(_ADD_ACCESSORIAL.bind(jobDisplayId=job_display_id), json=data)

    def remove_accessorial(self, job_display_id: int, add_on_id: str) -> ServiceBaseResponse:
        """DELETE /job/{jobDisplayId}/shipment/accessorial/{addOnId} (ACPortal)"""
        return self._request(
            _REMOVE_ACCESSORIAL.bind(jobDisplayId=job_display_id, addOnId=add_on_id),
        )

    def get_origin_destination(self, job_display_id: int) -> ShipmentOriginDestination:
        """GET /job/{jobDisplayId}/shipment/origindestination (ACPortal)"""
        return self._request(_GET_ORIGIN_DEST.bind(jobDisplayId=job_display_id))

    def get_export_data(self, job_display_id: int) -> ShipmentExportData:
        """GET /job/{jobDisplayId}/shipment/exportdata (ACPortal)"""
        return self._request(_GET_EXPORT_DATA.bind(jobDisplayId=job_display_id))

    def post_export_data(self, job_display_id: int, *, data: ShipmentExportRequest | dict) -> ServiceBaseResponse:
        """POST /job/{jobDisplayId}/shipment/exportdata.

        Args:
            job_display_id: Job display ID.
            data: Export data payload.
                Accepts a :class:`ShipmentExportRequest` instance or a dict.

        Request model: :class:`ShipmentExportRequest`
        """
        return self._request(_POST_EXPORT_DATA.bind(jobDisplayId=job_display_id), json=data)

    def get_rates_state(self, job_display_id: int) -> RatesState:
        """GET /job/{jobDisplayId}/shipment/ratesstate (ACPortal)"""
        return self._request(_GET_RATES_STATE.bind(jobDisplayId=job_display_id))

    # ---- Global shipment methods --------------------------------------

    def get_shipment(
        self,
        *,
        franchisee_id: str | None = None,
        provider_id: str | None = None,
        pro_number: str | None = None,
    ) -> ShipmentInfo:
        """GET /shipment (ACPortal)"""
        return self._request(
            _GET_SHIPMENT,
            params=dict(franchisee_id=franchisee_id, provider_id=provider_id, pro_number=pro_number),
        )

    def get_global_accessorials(self) -> list[GlobalAccessorial]:
        """GET /shipment/accessorials (ACPortal)"""
        return self._request(_GET_GLOBAL_ACCESSORIALS)

    def get_shipment_document(self, doc_id: str) -> Any:
        """GET /shipment/document/{docId} (ACPortal)"""
        return self._request(_GET_SHIPMENT_DOCUMENT.bind(docId=doc_id))

    # ---- Backwards Compatibility Aliases --------------------------------

    def delete(self, job_display_id: int) -> ServiceBaseResponse:
        """Alias for :meth:`delete_shipment`."""
        return self.delete_shipment(job_display_id)

    def get_origin_dest(self, job_display_id: int) -> ShipmentOriginDestination:
        """Alias for :meth:`get_origin_destination`."""
        return self.get_origin_destination(job_display_id)
