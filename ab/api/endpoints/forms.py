"""Forms API endpoints — ACPortal.

Covers 15 job form types: invoices, BOLs, packing slips, quotes, labels,
and more.  Most endpoints return ``{filename: bytes}``; the ``get_shipments``
method returns JSON (List[FormsShipmentPlan]).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ab.api.models.forms import FormsShipmentPlan

from ab.api.base import BaseEndpoint
from ab.api.route import Route

# Form routes — 14 return bytes, 1 returns JSON
_GET_INVOICE = Route("GET", "/job/{jobDisplayId}/form/invoice", params_model="FormTypeParams", response_model="bytes")
_GET_INVOICE_EDITABLE = Route("GET", "/job/{jobDisplayId}/form/invoice/editable", response_model="bytes")
_GET_BOL = Route(
    "GET", "/job/{jobDisplayId}/form/bill-of-lading", params_model="BillOfLadingParams", response_model="bytes"
)
_GET_PACKING_SLIP = Route("GET", "/job/{jobDisplayId}/form/packing-slip", response_model="bytes")
_GET_CUSTOMER_QUOTE = Route("GET", "/job/{jobDisplayId}/form/customer-quote", response_model="bytes")
_GET_QUICK_SALE = Route("GET", "/job/{jobDisplayId}/form/quick-sale", response_model="bytes")
_GET_OPERATIONS = Route(
    "GET", "/job/{jobDisplayId}/form/operations", params_model="OperationsFormParams", response_model="bytes"
)
_GET_SHIPMENTS = Route("GET", "/job/{jobDisplayId}/form/shipments", response_model="List[FormsShipmentPlan]")
_GET_ADDRESS_LABEL = Route("GET", "/job/{jobDisplayId}/form/address-label", response_model="bytes")
_GET_ITEM_LABELS = Route("GET", "/job/{jobDisplayId}/form/item-labels", response_model="bytes")
_GET_PACKAGING_LABELS = Route(
    "GET", "/job/{jobDisplayId}/form/packaging-labels", params_model="PackagingLabelsParams", response_model="bytes"
)
_GET_PACKAGING_SPEC = Route("GET", "/job/{jobDisplayId}/form/packaging-specification", response_model="bytes")
_GET_CC_AUTH = Route("GET", "/job/{jobDisplayId}/form/credit-card-authorization", response_model="bytes")
_GET_USAR = Route("GET", "/job/{jobDisplayId}/form/usar", params_model="FormTypeParams", response_model="bytes")
_GET_USAR_EDITABLE = Route("GET", "/job/{jobDisplayId}/form/usar/editable", response_model="bytes")


class FormsEndpoint(BaseEndpoint):
    """Form generation operations (ACPortal API).

    Most methods return ``{filename: bytes}`` (PDF content).  Use
    :meth:`get_shipments` to get JSON shipment plan data for BOL selection.
    """

    def _pdf(self, route: Route, job_display_id: int, name: str, **kw: Any) -> dict[str, bytes]:
        """Request a PDF form and return as ``{name_jobDisplayId.pdf: bytes}``."""
        data = self._request(route.bind(jobDisplayId=job_display_id), **kw)
        return {f"{name}_{job_display_id}.pdf": data}

    def get_invoice(self, job_display_id: int, *, type: Optional[str] = None) -> dict[str, bytes]:
        """GET /job/{jobDisplayId}/form/invoice (ACPortal)."""
        return self._pdf(_GET_INVOICE, job_display_id, "invoice", params=dict(type=type))

    def get_invoice_editable(self, job_display_id: int) -> dict[str, bytes]:
        """GET /job/{jobDisplayId}/form/invoice/editable (ACPortal)."""
        return self._pdf(_GET_INVOICE_EDITABLE, job_display_id, "invoice_editable")

    def get_bill_of_lading(
        self,
        job_display_id: int,
        *,
        shipment_plan_id: Optional[str] = None,
        provider_option_index: Optional[int] = None,
    ) -> dict[str, bytes]:
        """GET /job/{jobDisplayId}/form/bill-of-lading (ACPortal)."""
        return self._pdf(
            _GET_BOL, job_display_id, "bol",
            params=dict(shipment_plan_id=shipment_plan_id, provider_option_index=provider_option_index),
        )

    def get_packing_slip(self, job_display_id: int) -> dict[str, bytes]:
        """GET /job/{jobDisplayId}/form/packing-slip (ACPortal)."""
        return self._pdf(_GET_PACKING_SLIP, job_display_id, "packing_slip")

    def get_customer_quote(self, job_display_id: int) -> dict[str, bytes]:
        """GET /job/{jobDisplayId}/form/customer-quote (ACPortal)."""
        return self._pdf(_GET_CUSTOMER_QUOTE, job_display_id, "customer_quote")

    def get_quick_sale(self, job_display_id: int) -> dict[str, bytes]:
        """GET /job/{jobDisplayId}/form/quick-sale (ACPortal)."""
        return self._pdf(_GET_QUICK_SALE, job_display_id, "quick_sale")

    def get_operations(self, job_display_id: int, *, ops_type: Optional[str] = None) -> dict[str, bytes]:
        """GET /job/{jobDisplayId}/form/operations (ACPortal)."""
        return self._pdf(_GET_OPERATIONS, job_display_id, "operations", params=dict(ops_type=ops_type))

    def get_shipments(self, job_display_id: int) -> list[FormsShipmentPlan]:
        """GET /job/{jobDisplayId}/form/shipments (ACPortal) — returns List[FormsShipmentPlan]."""
        return self._request(_GET_SHIPMENTS.bind(jobDisplayId=job_display_id))

    def get_address_label(self, job_display_id: int) -> dict[str, bytes]:
        """GET /job/{jobDisplayId}/form/address-label (ACPortal)."""
        return self._pdf(_GET_ADDRESS_LABEL, job_display_id, "address_label")

    def get_item_labels(self, job_display_id: int) -> dict[str, bytes]:
        """GET /job/{jobDisplayId}/form/item-labels (ACPortal)."""
        return self._pdf(_GET_ITEM_LABELS, job_display_id, "item_labels")

    def get_packaging_labels(
        self,
        job_display_id: int,
        *,
        shipment_plan_id: Optional[str] = None,
    ) -> dict[str, bytes]:
        """GET /job/{jobDisplayId}/form/packaging-labels (ACPortal)."""
        return self._pdf(
            _GET_PACKAGING_LABELS, job_display_id, "packaging_labels",
            params=dict(shipment_plan_id=shipment_plan_id),
        )

    def get_packaging_specification(self, job_display_id: int) -> dict[str, bytes]:
        """GET /job/{jobDisplayId}/form/packaging-specification (ACPortal)."""
        return self._pdf(_GET_PACKAGING_SPEC, job_display_id, "packaging_spec")

    def get_credit_card_authorization(self, job_display_id: int) -> dict[str, bytes]:
        """GET /job/{jobDisplayId}/form/credit-card-authorization (ACPortal)."""
        return self._pdf(_GET_CC_AUTH, job_display_id, "cc_auth")

    def get_usar(self, job_display_id: int, *, type: Optional[str] = None) -> dict[str, bytes]:
        """GET /job/{jobDisplayId}/form/usar (ACPortal)."""
        return self._pdf(_GET_USAR, job_display_id, "usar", params=dict(type=type))

    def get_usar_editable(self, job_display_id: int) -> dict[str, bytes]:
        """GET /job/{jobDisplayId}/form/usar/editable (ACPortal)."""
        return self._pdf(_GET_USAR_EDITABLE, job_display_id, "usar_editable")

    # ---- Backwards Compatibility Aliases --------------------------------

    def _find_plan(self, job_display_id: int, *transport_types: str) -> FormsShipmentPlan:
        """Find a shipment plan by transport type preference order."""
        plans = self.get_shipments(job_display_id)
        for tt in transport_types:
            for plan in plans:
                if plan.transport_type == tt:
                    return plan
        raise ValueError(f"No shipment plan with transportType in {transport_types}")

    def get_ops(self, job_display_id: int, *, ops_type: Optional[str] = None) -> dict[str, bytes]:
        """Alias for :meth:`get_operations`."""
        return self._pdf(_GET_OPERATIONS, job_display_id, "ops", params=dict(ops_type=ops_type))

    def get_bol(self, job_display_id: int) -> dict[str, bytes]:
        """Get BOL for the freight leg (tries LTL, falls back to Delivery)."""
        plan = self._find_plan(job_display_id, "LTL", "Delivery")
        return self._pdf(
            _GET_BOL, job_display_id, "bol",
            params=dict(shipment_plan_id=plan.job_shipment_id),
        )

    def get_hbl(self, job_display_id: int) -> dict[str, bytes]:
        """Get House Bill of Lading."""
        plan = self._find_plan(job_display_id, "House")
        return self._pdf(
            _GET_BOL, job_display_id, "hbl",
            params=dict(shipment_plan_id=plan.job_shipment_id),
        )

    def get_pbl(self, job_display_id: int) -> dict[str, bytes]:
        """Get PickUp Bill of Lading."""
        plan = self._find_plan(job_display_id, "PickUp")
        return self._pdf(
            _GET_BOL, job_display_id, "pbl",
            params=dict(shipment_plan_id=plan.job_shipment_id),
        )

    def get_dbl(self, job_display_id: int) -> dict[str, bytes]:
        """Get Delivery Bill of Lading (only valid when an LTL leg exists)."""
        plans = self.get_shipments(job_display_id)
        if not any(p.transport_type == "LTL" for p in plans):
            raise ValueError("No LTL shipment plan exists — Delivery BOL not applicable")
        delivery = next((p for p in plans if p.transport_type == "Delivery"), None)
        if delivery is None:
            raise ValueError("No Delivery shipment plan found")
        return self._pdf(
            _GET_BOL, job_display_id, "dbl",
            params=dict(shipment_plan_id=delivery.job_shipment_id),
        )
