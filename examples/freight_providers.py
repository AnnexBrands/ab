"""Example: Freight provider operations (4 methods).

Covers list, save, rate quote, and add freight items.
"""

from examples._runner import ExampleRunner
from tests.constants import LIVE_JOB_DISPLAY_ID

runner = ExampleRunner("Freight Providers", env="staging")

# ═══════════════════════════════════════════════════════════════════════
# Freight Providers
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "list_freight_providers",
    lambda api: api.jobs.list_freight_providers(LIVE_JOB_DISPLAY_ID),
    response_model="List[PricedFreightProvider]",
    fixture_file="PricedFreightProvider.json",
)

runner.add(
    "save_freight_providers",
    lambda api, data=None: api.jobs.save_freight_providers(LIVE_JOB_DISPLAY_ID, **(data or {})),
    request_model="ShipmentPlanProvider",
    request_fixture_file="ShipmentPlanProvider.json",
)

runner.add(
    "get_freight_provider_rate_quote",
    lambda api: api.jobs.get_freight_provider_rate_quote(LIVE_JOB_DISPLAY_ID, 0),
)

runner.add(
    "add_freight_items",
    lambda api: api.jobs.add_freight_items(LIVE_JOB_DISPLAY_ID, items=[]),
)

if __name__ == "__main__":
    runner.run()
