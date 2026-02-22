"""Example: Shipment operations (14 methods).

Covers rates, booking, accessorials, origin/destination, export data,
shipment info, global accessorials, and document retrieval.
"""

from examples._runner import ExampleRunner
from tests.constants import LIVE_JOB_DISPLAY_ID

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

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "request_rate_quotes",
    lambda api: api.shipments.request_rate_quotes(LIVE_JOB_DISPLAY_ID, data={}),
    response_model="List[RateQuote]",
)

runner.add(
    "book",
    lambda api, data=None: api.shipments.book(LIVE_JOB_DISPLAY_ID, data or {}),
    request_model="ShipmentBookRequest",
    request_fixture_file="ShipmentBookRequest.json",
    response_model="ServiceBaseResponse",
)

runner.add(
    "delete_shipment",
    lambda api: api.shipments.delete_shipment(LIVE_JOB_DISPLAY_ID),
    response_model="ServiceBaseResponse",
)

runner.add(
    "add_accessorial",
    lambda api, data=None: api.shipments.add_accessorial(LIVE_JOB_DISPLAY_ID, data or {}),
    request_model="AccessorialAddRequest",
    request_fixture_file="AccessorialAddRequest.json",
    response_model="ServiceBaseResponse",
)

runner.add(
    "remove_accessorial",
    lambda api: api.shipments.remove_accessorial(LIVE_JOB_DISPLAY_ID, "ADD_ON_ID"),
    response_model="ServiceBaseResponse",
)

runner.add(
    "get_export_data",
    lambda api: api.shipments.get_export_data(LIVE_JOB_DISPLAY_ID),
    response_model="ShipmentExportData",
)

runner.add(
    "post_export_data",
    lambda api: api.shipments.post_export_data(LIVE_JOB_DISPLAY_ID, {}),
    response_model="ServiceBaseResponse",
)

runner.add(
    "get_shipment_document",
    lambda api: api.shipments.get_shipment_document("DOC_ID"),
    response_model="bytes",
)

if __name__ == "__main__":
    runner.run()
