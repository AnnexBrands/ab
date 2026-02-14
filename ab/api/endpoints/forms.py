"""Forms API endpoints — ACPortal.

Covers 15 job form types: invoices, BOLs, packing slips, quotes, labels,
and more.  Most endpoints return raw PDF bytes; the ``get_shipments``
method returns JSON (List[FormsShipmentPlan]).
"""

from __future__ import annotations

from typing import Any, Optional

from ab.api.base import BaseEndpoint
from ab.api.route import Route

# Form routes — 14 return bytes, 1 returns JSON
_GET_INVOICE = Route("GET", "/job/{jobDisplayId}/form/invoice", response_model="bytes")
_GET_INVOICE_EDITABLE = Route("GET", "/job/{jobDisplayId}/form/invoice/editable", response_model="bytes")
_GET_BOL = Route("GET", "/job/{jobDisplayId}/form/bill-of-lading", response_model="bytes")
_GET_PACKING_SLIP = Route("GET", "/job/{jobDisplayId}/form/packing-slip", response_model="bytes")
_GET_CUSTOMER_QUOTE = Route("GET", "/job/{jobDisplayId}/form/customer-quote", response_model="bytes")
_GET_QUICK_SALE = Route("GET", "/job/{jobDisplayId}/form/quick-sale", response_model="bytes")
_GET_OPERATIONS = Route("GET", "/job/{jobDisplayId}/form/operations", response_model="bytes")
_GET_SHIPMENTS = Route("GET", "/job/{jobDisplayId}/form/shipments", response_model="List[FormsShipmentPlan]")
_GET_ADDRESS_LABEL = Route("GET", "/job/{jobDisplayId}/form/address-label", response_model="bytes")
_GET_ITEM_LABELS = Route("GET", "/job/{jobDisplayId}/form/item-labels", response_model="bytes")
_GET_PACKAGING_LABELS = Route("GET", "/job/{jobDisplayId}/form/packaging-labels", response_model="bytes")
_GET_PACKAGING_SPEC = Route("GET", "/job/{jobDisplayId}/form/packaging-specification", response_model="bytes")
_GET_CC_AUTH = Route("GET", "/job/{jobDisplayId}/form/credit-card-authorization", response_model="bytes")
_GET_USAR = Route("GET", "/job/{jobDisplayId}/form/usar", response_model="bytes")
_GET_USAR_EDITABLE = Route("GET", "/job/{jobDisplayId}/form/usar/editable", response_model="bytes")


class FormsEndpoint(BaseEndpoint):
    """Form generation operations (ACPortal API).

    Most methods return raw ``bytes`` (PDF content).  Use
    :meth:`get_shipments` to get JSON shipment plan data for BOL selection.
    """

    def get_invoice(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/form/invoice (ACPortal) — returns bytes."""
        return self._request(_GET_INVOICE.bind(jobDisplayId=job_display_id))

    def get_invoice_editable(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/form/invoice/editable (ACPortal) — returns bytes."""
        return self._request(_GET_INVOICE_EDITABLE.bind(jobDisplayId=job_display_id))

    def get_bill_of_lading(
        self,
        job_display_id: int,
        *,
        shipment_plan_id: Optional[str] = None,
        provider_option_index: Optional[int] = None,
    ) -> Any:
        """GET /job/{jobDisplayId}/form/bill-of-lading (ACPortal) — returns bytes.

        Args:
            shipment_plan_id: Optional shipment plan to render.
            provider_option_index: Optional provider index.
        """
        params: dict[str, Any] = {}
        if shipment_plan_id is not None:
            params["shipmentPlanId"] = shipment_plan_id
        if provider_option_index is not None:
            params["providerOptionIndex"] = provider_option_index
        return self._request(_GET_BOL.bind(jobDisplayId=job_display_id), params=params or None)

    def get_packing_slip(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/form/packing-slip (ACPortal) — returns bytes."""
        return self._request(_GET_PACKING_SLIP.bind(jobDisplayId=job_display_id))

    def get_customer_quote(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/form/customer-quote (ACPortal) — returns bytes."""
        return self._request(_GET_CUSTOMER_QUOTE.bind(jobDisplayId=job_display_id))

    def get_quick_sale(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/form/quick-sale (ACPortal) — returns bytes."""
        return self._request(_GET_QUICK_SALE.bind(jobDisplayId=job_display_id))

    def get_operations(self, job_display_id: int, *, ops_type: Optional[str] = None) -> Any:
        """GET /job/{jobDisplayId}/form/operations (ACPortal) — returns bytes.

        Args:
            ops_type: Optional operations type filter.
        """
        params: dict[str, Any] = {}
        if ops_type is not None:
            params["opsType"] = ops_type
        return self._request(_GET_OPERATIONS.bind(jobDisplayId=job_display_id), params=params or None)

    def get_shipments(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/form/shipments (ACPortal) — returns List[FormsShipmentPlan]."""
        return self._request(_GET_SHIPMENTS.bind(jobDisplayId=job_display_id))

    def get_address_label(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/form/address-label (ACPortal) — returns bytes."""
        return self._request(_GET_ADDRESS_LABEL.bind(jobDisplayId=job_display_id))

    def get_item_labels(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/form/item-labels (ACPortal) — returns bytes."""
        return self._request(_GET_ITEM_LABELS.bind(jobDisplayId=job_display_id))

    def get_packaging_labels(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/form/packaging-labels (ACPortal) — returns bytes."""
        return self._request(_GET_PACKAGING_LABELS.bind(jobDisplayId=job_display_id))

    def get_packaging_specification(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/form/packaging-specification (ACPortal) — returns bytes."""
        return self._request(_GET_PACKAGING_SPEC.bind(jobDisplayId=job_display_id))

    def get_credit_card_authorization(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/form/credit-card-authorization (ACPortal) — returns bytes."""
        return self._request(_GET_CC_AUTH.bind(jobDisplayId=job_display_id))

    def get_usar(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/form/usar (ACPortal) — returns bytes."""
        return self._request(_GET_USAR.bind(jobDisplayId=job_display_id))

    def get_usar_editable(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/form/usar/editable (ACPortal) — returns bytes."""
        return self._request(_GET_USAR_EDITABLE.bind(jobDisplayId=job_display_id))
