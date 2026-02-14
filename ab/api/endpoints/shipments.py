"""Shipments API endpoints — ACPortal.

Covers job-scoped shipment operations (rate quotes, booking, accessorials)
and global shipment endpoints (shipment lookup, accessorial catalog, documents).
"""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

# Job-scoped shipment routes
_GET_RATE_QUOTES = Route("GET", "/job/{jobDisplayId}/shipment/ratequotes", response_model="List[RateQuote]")
_POST_RATE_QUOTES = Route("POST", "/job/{jobDisplayId}/shipment/ratequotes", response_model="List[RateQuote]")
_BOOK = Route("POST", "/job/{jobDisplayId}/shipment/book", request_model="ShipmentBookRequest", response_model="ServiceBaseResponse")
_DELETE_SHIPMENT = Route("DELETE", "/job/{jobDisplayId}/shipment", response_model="ServiceBaseResponse")
_GET_ACCESSORIALS = Route("GET", "/job/{jobDisplayId}/shipment/accessorials", response_model="List[Accessorial]")
_ADD_ACCESSORIAL = Route("POST", "/job/{jobDisplayId}/shipment/accessorial", request_model="AccessorialAddRequest", response_model="ServiceBaseResponse")
_REMOVE_ACCESSORIAL = Route("DELETE", "/job/{jobDisplayId}/shipment/accessorial/{addOnId}", response_model="ServiceBaseResponse")
_GET_ORIGIN_DEST = Route("GET", "/job/{jobDisplayId}/shipment/origindestination", response_model="ShipmentOriginDestination")
_GET_EXPORT_DATA = Route("GET", "/job/{jobDisplayId}/shipment/exportdata", response_model="ShipmentExportData")
_POST_EXPORT_DATA = Route("POST", "/job/{jobDisplayId}/shipment/exportdata", response_model="ServiceBaseResponse")
_GET_RATES_STATE = Route("GET", "/job/{jobDisplayId}/shipment/ratesstate", response_model="RatesState")

# Global shipment routes
_GET_SHIPMENT = Route("GET", "/shipment", response_model="ShipmentInfo")
_GET_GLOBAL_ACCESSORIALS = Route("GET", "/shipment/accessorials", response_model="List[GlobalAccessorial]")
_GET_SHIPMENT_DOCUMENT = Route("GET", "/shipment/document/{docId}", response_model="bytes")


class ShipmentsEndpoint(BaseEndpoint):
    """Shipment operations (ACPortal API)."""

    # ---- Job-scoped shipment methods ----------------------------------

    def get_rate_quotes(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/shipment/ratequotes (ACPortal)"""
        return self._request(_GET_RATE_QUOTES.bind(jobDisplayId=job_display_id))

    def request_rate_quotes(self, job_display_id: int, data: dict | None = None) -> Any:
        """POST /job/{jobDisplayId}/shipment/ratequotes (ACPortal)"""
        return self._request(_POST_RATE_QUOTES.bind(jobDisplayId=job_display_id), json=data)

    def book(self, job_display_id: int, data: dict | Any) -> Any:
        """POST /job/{jobDisplayId}/shipment/book (ACPortal)"""
        return self._request(_BOOK.bind(jobDisplayId=job_display_id), json=data)

    def delete_shipment(self, job_display_id: int) -> Any:
        """DELETE /job/{jobDisplayId}/shipment (ACPortal)"""
        return self._request(_DELETE_SHIPMENT.bind(jobDisplayId=job_display_id))

    def get_accessorials(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/shipment/accessorials (ACPortal)"""
        return self._request(_GET_ACCESSORIALS.bind(jobDisplayId=job_display_id))

    def add_accessorial(self, job_display_id: int, data: dict | Any) -> Any:
        """POST /job/{jobDisplayId}/shipment/accessorial (ACPortal)"""
        return self._request(_ADD_ACCESSORIAL.bind(jobDisplayId=job_display_id), json=data)

    def remove_accessorial(self, job_display_id: int, add_on_id: str) -> Any:
        """DELETE /job/{jobDisplayId}/shipment/accessorial/{addOnId} (ACPortal)"""
        return self._request(_REMOVE_ACCESSORIAL.bind(jobDisplayId=job_display_id, addOnId=add_on_id))

    def get_origin_destination(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/shipment/origindestination (ACPortal)"""
        return self._request(_GET_ORIGIN_DEST.bind(jobDisplayId=job_display_id))

    def get_export_data(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/shipment/exportdata (ACPortal)"""
        return self._request(_GET_EXPORT_DATA.bind(jobDisplayId=job_display_id))

    def post_export_data(self, job_display_id: int, data: dict | Any) -> Any:
        """POST /job/{jobDisplayId}/shipment/exportdata (ACPortal)"""
        return self._request(_POST_EXPORT_DATA.bind(jobDisplayId=job_display_id), json=data)

    def get_rates_state(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/shipment/ratesstate (ACPortal)"""
        return self._request(_GET_RATES_STATE.bind(jobDisplayId=job_display_id))

    # ---- Global shipment methods --------------------------------------

    def get_shipment(self, **params: Any) -> Any:
        """GET /shipment (ACPortal)"""
        return self._request(_GET_SHIPMENT, params=params)

    def get_global_accessorials(self) -> Any:
        """GET /shipment/accessorials (ACPortal)"""
        return self._request(_GET_GLOBAL_ACCESSORIALS)

    def get_shipment_document(self, doc_id: str) -> Any:
        """GET /shipment/document/{docId} (ACPortal)"""
        return self._request(_GET_SHIPMENT_DOCUMENT.bind(docId=doc_id))
