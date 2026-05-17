"""Job-scoped shipment operations — swagger tag ``JobShipment`` (11 routes).

Exposed as ``api.jobs.shipment``. The legacy ``api.shipments``
endpoint retains the 3 non-job-scoped routes (``GET /shipment``,
``GET /shipment/accessorials``, ``GET /shipment/document/{docId}``); the
11 job-scoped routes move here and ``api.shipments`` keeps deprecation
shims that forward to this class.

Method renames (drop redundant ``_shipment`` suffix; standardise ``get_``):

* :meth:`get_rate_quotes`         (unchanged)
* :meth:`request_rate_quotes`     (unchanged)
* :meth:`book`                    (unchanged)
* :meth:`delete`                  (was ``delete_shipment``)
* :meth:`get_accessorials`        (unchanged)
* :meth:`add_accessorial`         (unchanged)
* :meth:`remove_accessorial`      (unchanged)
* :meth:`get_origin_destination`  (unchanged)
* :meth:`get_export_data`         (unchanged)
* :meth:`post_export_data`        (unchanged)
* :meth:`get_rates_state`         (unchanged)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.shared import ServiceBaseResponse
    from ab.api.models.shipments import (
        Accessorial,
        AccessorialAddRequest,
        RateQuote,
        RatesState,
        ShipmentBookRequest,
        ShipmentExportData,
        ShipmentExportRequest,
        ShipmentOriginDestination,
        ShipmentRateQuoteRequest,
    )

from ab.api.base import BaseEndpoint
from ab.api.route import Route

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
_DELETE = Route("DELETE", "/job/{jobDisplayId}/shipment", response_model="ServiceBaseResponse")
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


class JobShipmentEndpoint(BaseEndpoint):
    """Job-scoped shipment operations (ACPortal API)."""

    def get_rate_quotes(self, job_display_id: int) -> list[RateQuote]:
        """``GET /job/{jobDisplayId}/shipment/ratequotes``"""
        return self._request(_GET_RATE_QUOTES.bind(jobDisplayId=job_display_id))

    def request_rate_quotes(self, job_display_id: int, *, data: ShipmentRateQuoteRequest | dict) -> list[RateQuote]:
        """``POST /job/{jobDisplayId}/shipment/ratequotes``

        Request model: :class:`ShipmentRateQuoteRequest`.
        """
        return self._request(_POST_RATE_QUOTES.bind(jobDisplayId=job_display_id), json=data)

    def book(self, job_display_id: int, *, data: ShipmentBookRequest | dict) -> ServiceBaseResponse:
        """``POST /job/{jobDisplayId}/shipment/book``

        Request model: :class:`ShipmentBookRequest`.
        """
        return self._request(_BOOK.bind(jobDisplayId=job_display_id), json=data)

    def delete(self, job_display_id: int) -> ServiceBaseResponse:
        """``DELETE /job/{jobDisplayId}/shipment``"""
        return self._request(_DELETE.bind(jobDisplayId=job_display_id))

    def get_accessorials(self, job_display_id: int) -> list[Accessorial]:
        """``GET /job/{jobDisplayId}/shipment/accessorials``"""
        return self._request(_GET_ACCESSORIALS.bind(jobDisplayId=job_display_id))

    def add_accessorial(self, job_display_id: int, *, data: AccessorialAddRequest | dict) -> ServiceBaseResponse:
        """``POST /job/{jobDisplayId}/shipment/accessorial``

        Request model: :class:`AccessorialAddRequest`.
        """
        return self._request(_ADD_ACCESSORIAL.bind(jobDisplayId=job_display_id), json=data)

    def remove_accessorial(self, job_display_id: int, add_on_id: str) -> ServiceBaseResponse:
        """``DELETE /job/{jobDisplayId}/shipment/accessorial/{addOnId}``"""
        return self._request(
            _REMOVE_ACCESSORIAL.bind(jobDisplayId=job_display_id, addOnId=add_on_id),
        )

    def get_origin_destination(self, job_display_id: int) -> ShipmentOriginDestination:
        """``GET /job/{jobDisplayId}/shipment/origindestination``"""
        return self._request(_GET_ORIGIN_DEST.bind(jobDisplayId=job_display_id))

    def get_export_data(self, job_display_id: int) -> ShipmentExportData:
        """``GET /job/{jobDisplayId}/shipment/exportdata``"""
        return self._request(_GET_EXPORT_DATA.bind(jobDisplayId=job_display_id))

    def post_export_data(self, job_display_id: int, *, data: ShipmentExportRequest | dict) -> ServiceBaseResponse:
        """``POST /job/{jobDisplayId}/shipment/exportdata``

        Request model: :class:`ShipmentExportRequest`.
        """
        return self._request(_POST_EXPORT_DATA.bind(jobDisplayId=job_display_id), json=data)

    def get_rates_state(self, job_display_id: int) -> RatesState:
        """``GET /job/{jobDisplayId}/shipment/ratesstate``"""
        return self._request(_GET_RATES_STATE.bind(jobDisplayId=job_display_id))
