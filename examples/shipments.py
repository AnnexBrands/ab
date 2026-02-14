"""Example: Shipment operations (14 methods).

Covers rates, booking, accessorials, origin/destination, export data,
shipment info, global accessorials, and document retrieval.
"""

from examples._runner import ExampleRunner

LIVE_JOB_DISPLAY_ID = 2000000

runner = ExampleRunner("Shipments", env="staging")

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "get_rate_quotes",
    lambda api: api.shipments.get_rate_quotes(LIVE_JOB_DISPLAY_ID),
    response_model="List[RateQuote]",
    fixture_file="RateQuote.json",
)

runner.add(
    "get_accessorials",
    lambda api: api.shipments.get_accessorials(LIVE_JOB_DISPLAY_ID),
    response_model="List[Accessorial]",
    fixture_file="Accessorial.json",
)

runner.add(
    "get_origin_destination",
    lambda api: api.shipments.get_origin_destination(LIVE_JOB_DISPLAY_ID),
    response_model="ShipmentOriginDestination",
    fixture_file="ShipmentOriginDestination.json",
)

runner.add(
    "get_rates_state",
    lambda api: api.shipments.get_rates_state(LIVE_JOB_DISPLAY_ID),
    response_model="RatesState",
    fixture_file="RatesState.json",
)

runner.add(
    "get_shipment",
    lambda api: api.shipments.get_shipment(),
    response_model="ShipmentInfo",
    fixture_file="ShipmentInfo.json",
)

runner.add(
    "get_global_accessorials",
    lambda api: api.shipments.get_global_accessorials(),
    response_model="List[GlobalAccessorial]",
    fixture_file="GlobalAccessorial.json",
)

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "request_rate_quotes",
    lambda api: api.shipments.request_rate_quotes(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs rate-quote request params
    ),
    response_model="List[RateQuote]",
)

runner.add(
    "book",
    lambda api: api.shipments.book(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs ShipmentBookRequest body
        {},
    ),
    request_model="ShipmentBookRequest",
    response_model="ServiceBaseResponse",
)

runner.add(
    "delete_shipment",
    lambda api: api.shipments.delete_shipment(
        # TODO: capture fixture — needs job with active shipment
        LIVE_JOB_DISPLAY_ID,
    ),
    response_model="ServiceBaseResponse",
)

runner.add(
    "add_accessorial",
    lambda api: api.shipments.add_accessorial(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs AccessorialAddRequest body
        {},
    ),
    request_model="AccessorialAddRequest",
    response_model="ServiceBaseResponse",
)

runner.add(
    "remove_accessorial",
    lambda api: api.shipments.remove_accessorial(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid add_on_id
        "ADD_ON_ID",
    ),
    response_model="ServiceBaseResponse",
)

runner.add(
    "get_export_data",
    lambda api: api.shipments.get_export_data(
        # TODO: capture fixture — needs job with shipment export data
        LIVE_JOB_DISPLAY_ID,
    ),
    response_model="ShipmentExportData",
)

runner.add(
    "post_export_data",
    lambda api: api.shipments.post_export_data(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs export data body
        {},
    ),
    response_model="ServiceBaseResponse",
)

runner.add(
    "get_shipment_document",
    lambda api: api.shipments.get_shipment_document(
        # TODO: capture fixture — needs valid document ID
        "DOC_ID",
    ),
    response_model="bytes",
    # binary response — fixture save N/A
)

if __name__ == "__main__":
    runner.run()
