"""Example: Freight provider operations (4 methods).

Covers list, save, rate quote, and add freight items.
"""

from examples._runner import ExampleRunner

runner = ExampleRunner("Freight Providers", env="staging")

LIVE_JOB_DISPLAY_ID = 2000000

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
    lambda api: api.jobs.save_freight_providers(
        LIVE_JOB_DISPLAY_ID,
        providerData={},
    ),
    request_model="ShipmentPlanProvider",
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
