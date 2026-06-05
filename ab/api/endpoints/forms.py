"""DEPRECATED: ``api.forms`` is being phased out.

All form-generation methods now live at :class:`~ab.api.endpoints.jobs.form.JobFormEndpoint`,
reached as ``api.jobs.form``. This module is retained only as a thin
deprecation shim: every method here emits a :class:`DeprecationWarning`
and forwards the call to ``api.jobs.form`` (sometimes with a different
name -- the canonical class drops the ``get_`` prefix on PDF routes and
renames ``get_shipments`` to :meth:`shipments`).

Method name mapping (legacy ``api.forms.X`` -> canonical ``api.jobs.form.Y``):

==========================================  =================================
Legacy                                      Canonical
==========================================  =================================
``api.forms.get_invoice``                   ``api.jobs.form.invoice``
``api.forms.get_invoice_editable``          ``api.jobs.form.invoice_editable``
``api.forms.get_bill_of_lading``            ``api.jobs.form.bill_of_lading``
``api.forms.get_packing_slip``              ``api.jobs.form.packing_slip``
``api.forms.get_customer_quote``            ``api.jobs.form.customer_quote``
``api.forms.get_quick_sale``                ``api.jobs.form.quick_sale``
``api.forms.get_operations``                ``api.jobs.form.operations``
``api.forms.get_shipments``                 ``api.jobs.form.shipments``
``api.forms.get_address_label``             ``api.jobs.form.address_label``
``api.forms.get_item_labels``               ``api.jobs.form.item_labels``
``api.forms.get_packaging_labels``          ``api.jobs.form.packaging_labels``
``api.forms.get_packaging_specification``   ``api.jobs.form.packaging_specification``
``api.forms.get_credit_card_authorization`` ``api.jobs.form.credit_card_authorization``
``api.forms.get_usar``                      ``api.jobs.form.usar``
``api.forms.get_usar_editable``             ``api.jobs.form.usar_editable``
``api.forms.get_ops``                       ``api.jobs.form.ops``
``api.forms.get_bol``                       ``api.jobs.form.bol``
``api.forms.get_hbl``                       ``api.jobs.form.hbl``
``api.forms.get_pbl``                       ``api.jobs.form.pbl``
``api.forms.get_dbl``                       ``api.jobs.form.dbl``
==========================================  =================================
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ab.api.models.forms import FormsShipmentPlan

from ab.api.base import BaseEndpoint
from ab.api.endpoints.jobs.form import JobFormEndpoint


def _deprecated(old: str, new: str) -> None:
    warnings.warn(
        f"{old}() is deprecated; use {new}() instead.",
        DeprecationWarning,
        stacklevel=3,
    )


class FormsEndpoint(BaseEndpoint):
    """Deprecated shim — every method forwards to ``api.jobs.form``.

    The canonical home for these methods is
    :class:`ab.api.endpoints.jobs.form.JobFormEndpoint` (``api.jobs.form``).
    """

    def __init__(self, client) -> None:
        super().__init__(client)
        # The shim owns its own JobFormEndpoint so it can keep working
        # standalone (without an ABConnectAPI instance).
        self._form = JobFormEndpoint(client)

    # ------------------------------------------------------------------
    # PDF routes
    # ------------------------------------------------------------------

    def get_invoice(self, job_display_id: int, *, type: Optional[str] = None) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.invoice(...)``."""
        _deprecated("api.forms.get_invoice", "api.jobs.form.invoice")
        return self._form.invoice(job_display_id, type=type)

    def get_invoice_editable(self, job_display_id: int) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.invoice_editable(...)``."""
        _deprecated("api.forms.get_invoice_editable", "api.jobs.form.invoice_editable")
        return self._form.invoice_editable(job_display_id)

    def get_bill_of_lading(
        self,
        job_display_id: int,
        *,
        shipment_plan_id: Optional[str] = None,
        provider_option_index: Optional[int] = None,
    ) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.bill_of_lading(...)``."""
        _deprecated("api.forms.get_bill_of_lading", "api.jobs.form.bill_of_lading")
        return self._form.bill_of_lading(
            job_display_id,
            shipment_plan_id=shipment_plan_id,
            provider_option_index=provider_option_index,
        )

    def get_packing_slip(self, job_display_id: int) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.packing_slip(...)``."""
        _deprecated("api.forms.get_packing_slip", "api.jobs.form.packing_slip")
        return self._form.packing_slip(job_display_id)

    def get_customer_quote(self, job_display_id: int) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.customer_quote(...)``."""
        _deprecated("api.forms.get_customer_quote", "api.jobs.form.customer_quote")
        return self._form.customer_quote(job_display_id)

    def get_quick_sale(self, job_display_id: int) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.quick_sale(...)``."""
        _deprecated("api.forms.get_quick_sale", "api.jobs.form.quick_sale")
        return self._form.quick_sale(job_display_id)

    def get_operations(self, job_display_id: int, *, ops_type: Optional[str] = None) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.operations(...)``."""
        _deprecated("api.forms.get_operations", "api.jobs.form.operations")
        return self._form.operations(job_display_id, ops_type=ops_type)

    def get_shipments(self, job_display_id: int) -> list[FormsShipmentPlan]:
        """Deprecated. Use ``api.jobs.form.shipments(...)``."""
        _deprecated("api.forms.get_shipments", "api.jobs.form.shipments")
        return self._form.shipments(job_display_id)

    def get_address_label(self, job_display_id: int) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.address_label(...)``."""
        _deprecated("api.forms.get_address_label", "api.jobs.form.address_label")
        return self._form.address_label(job_display_id)

    def get_item_labels(self, job_display_id: int) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.item_labels(...)``."""
        _deprecated("api.forms.get_item_labels", "api.jobs.form.item_labels")
        return self._form.item_labels(job_display_id)

    def get_packaging_labels(
        self, job_display_id: int, *, shipment_plan_id: Optional[str] = None,
    ) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.packaging_labels(...)``."""
        _deprecated("api.forms.get_packaging_labels", "api.jobs.form.packaging_labels")
        return self._form.packaging_labels(job_display_id, shipment_plan_id=shipment_plan_id)

    def get_packaging_specification(self, job_display_id: int) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.packaging_specification(...)``."""
        _deprecated("api.forms.get_packaging_specification", "api.jobs.form.packaging_specification")
        return self._form.packaging_specification(job_display_id)

    def get_credit_card_authorization(self, job_display_id: int) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.credit_card_authorization(...)``."""
        _deprecated("api.forms.get_credit_card_authorization", "api.jobs.form.credit_card_authorization")
        return self._form.credit_card_authorization(job_display_id)

    def get_usar(self, job_display_id: int, *, type: Optional[str] = None) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.usar(...)``."""
        _deprecated("api.forms.get_usar", "api.jobs.form.usar")
        return self._form.usar(job_display_id, type=type)

    def get_usar_editable(self, job_display_id: int) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.usar_editable(...)``."""
        _deprecated("api.forms.get_usar_editable", "api.jobs.form.usar_editable")
        return self._form.usar_editable(job_display_id)

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def get_ops(self, job_display_id: int, *, ops_type: Optional[str] = None) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.ops(...)``."""
        _deprecated("api.forms.get_ops", "api.jobs.form.ops")
        return self._form.ops(job_display_id, ops_type=ops_type)

    def get_bol(self, job_display_id: int) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.bol(...)``."""
        _deprecated("api.forms.get_bol", "api.jobs.form.bol")
        return self._form.bol(job_display_id)

    def get_hbl(self, job_display_id: int) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.hbl(...)``."""
        _deprecated("api.forms.get_hbl", "api.jobs.form.hbl")
        return self._form.hbl(job_display_id)

    def get_pbl(self, job_display_id: int) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.pbl(...)``."""
        _deprecated("api.forms.get_pbl", "api.jobs.form.pbl")
        return self._form.pbl(job_display_id)

    def get_dbl(self, job_display_id: int) -> dict[str, bytes]:
        """Deprecated. Use ``api.jobs.form.dbl(...)``."""
        _deprecated("api.forms.get_dbl", "api.jobs.form.dbl")
        return self._form.dbl(job_display_id)
