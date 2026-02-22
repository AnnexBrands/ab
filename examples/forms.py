"""Example: Forms generation (15 methods).

Most methods return binary PDF data. Only get_shipments returns JSON.
"""

from examples._runner import ExampleRunner
from tests.constants import TEST_JOB_DISPLAY_ID

runner = ExampleRunner("Forms", env="staging")

# ── JSON response ────────────────────────────────────────────────────

runner.add(
    "get_shipments",
    lambda api: api.forms.get_shipments(
        # TODO: capture fixture — needs job with shipment plans
        TEST_JOB_DISPLAY_ID,
    ),
    response_model="List[FormsShipmentPlan]",
    fixture_file="FormsShipmentPlan.json",
)

# ── Binary responses (PDFs) ─────────────────────────────────────────

runner.add(
    "get_invoice",
    lambda api: api.forms.get_invoice(TEST_JOB_DISPLAY_ID),
    response_model="bytes",
    # binary response — fixture save N/A
)

runner.add(
    "get_invoice_editable",
    lambda api: api.forms.get_invoice_editable(TEST_JOB_DISPLAY_ID),
    response_model="bytes",
    # binary response — fixture save N/A
)

runner.add(
    "get_bill_of_lading",
    lambda api: api.forms.get_bill_of_lading(TEST_JOB_DISPLAY_ID),
    response_model="bytes",
    # binary response — fixture save N/A
    # optional params: shipment_plan_id, provider_option_index
)

runner.add(
    "get_packing_slip",
    lambda api: api.forms.get_packing_slip(TEST_JOB_DISPLAY_ID),
    response_model="bytes",
    # binary response — fixture save N/A
)

runner.add(
    "get_customer_quote",
    lambda api: api.forms.get_customer_quote(TEST_JOB_DISPLAY_ID),
    response_model="bytes",
    # binary response — fixture save N/A
)

runner.add(
    "get_quick_sale",
    lambda api: api.forms.get_quick_sale(TEST_JOB_DISPLAY_ID),
    response_model="bytes",
    # binary response — fixture save N/A
)

runner.add(
    "get_operations",
    lambda api: api.forms.get_operations(TEST_JOB_DISPLAY_ID),
    response_model="bytes",
    # binary response — fixture save N/A
    # optional param: ops_type
)

runner.add(
    "get_address_label",
    lambda api: api.forms.get_address_label(TEST_JOB_DISPLAY_ID),
    response_model="bytes",
    # binary response — fixture save N/A
)

runner.add(
    "get_item_labels",
    lambda api: api.forms.get_item_labels(TEST_JOB_DISPLAY_ID),
    response_model="bytes",
    # binary response — fixture save N/A
)

runner.add(
    "get_packaging_labels",
    lambda api: api.forms.get_packaging_labels(TEST_JOB_DISPLAY_ID),
    response_model="bytes",
    # binary response — fixture save N/A
)

runner.add(
    "get_packaging_specification",
    lambda api: api.forms.get_packaging_specification(TEST_JOB_DISPLAY_ID),
    response_model="bytes",
    # binary response — fixture save N/A
)

runner.add(
    "get_credit_card_authorization",
    lambda api: api.forms.get_credit_card_authorization(TEST_JOB_DISPLAY_ID),
    response_model="bytes",
    # binary response — fixture save N/A
)

runner.add(
    "get_usar",
    lambda api: api.forms.get_usar(TEST_JOB_DISPLAY_ID),
    response_model="bytes",
    # binary response — fixture save N/A
)

runner.add(
    "get_usar_editable",
    lambda api: api.forms.get_usar_editable(TEST_JOB_DISPLAY_ID),
    response_model="bytes",
    # binary response — fixture save N/A
)

if __name__ == "__main__":
    runner.run()
