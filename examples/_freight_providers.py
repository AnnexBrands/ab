"""Example: Freight provider operations (4 methods).

Covers list, save, rate quote, and add freight items.
"""

from examples._runner import ExampleRunner
from tests.constants import TEST_JOB_DISPLAY_ID, TEST_JOB_DISPLAY_ID2

runner = ExampleRunner("Freight Providers", env="staging")

# ═══════════════════════════════════════════════════════════════════════
# Freight Providers
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "list_freight_providers",
    lambda api: api.jobs.list_freight_providers(TEST_JOB_DISPLAY_ID2),
    response_model="List[PricedFreightProvider]",
    fixture_file="PricedFreightProvider.json",
)

runner.add(
    "save_freight_providers",
    lambda api, data=None: api.jobs.save_freight_providers(TEST_JOB_DISPLAY_ID, data=data or {}),
    request_model="ShipmentPlanProvider",
    request_fixture_file="ShipmentPlanProvider.json",
)

runner.add(
    "get_freight_provider_rate_quote",
    lambda api: api.jobs.get_freight_provider_rate_quote(TEST_JOB_DISPLAY_ID, 0, data={}),
    request_model="RateQuoteRequest",
    request_fixture_file="RateQuoteRequest.json",
)

runner.add(
    "add_freight_items",
    lambda api: api.jobs.add_freight_items(TEST_JOB_DISPLAY_ID, data={}),
    request_model="FreightItemsRequest",
    request_fixture_file="FreightItemsRequest.json",
)

if __name__ == "__main__":
    runner.run()
