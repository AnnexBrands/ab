"""Example: Commodity and commodity map operations (10 methods).

Covers CRUD and search for both commodities and commodity maps.
"""

from examples._runner import ExampleRunner

runner = ExampleRunner("Commodities", env="staging")

LIVE_COMMODITY_ID = "PLACEHOLDER"
LIVE_MAP_ID = "PLACEHOLDER"

# ═══════════════════════════════════════════════════════════════════════
# Commodities
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "commodity_search",
    lambda api: api.commodities.search(searchText="furniture"),
    request_model="CommoditySearchRequest",
    response_model="List[Commodity]",
    fixture_file="Commodity.json",
)

runner.add(
    "commodity_suggestions",
    lambda api: api.commodities.suggestions(searchText="chair"),
    request_model="CommoditySuggestionRequest",
    response_model="List[Commodity]",
)

runner.add(
    "commodity_get",
    lambda api: api.commodities.get(LIVE_COMMODITY_ID),
    response_model="Commodity",
)

runner.add(
    "commodity_create",
    lambda api: api.commodities.create(
        description="Test Commodity",
        freightClass="70",
        nmfcCode="12345",
    ),
    request_model="CommodityCreateRequest",
    response_model="Commodity",
)

runner.add(
    "commodity_update",
    lambda api: api.commodities.update(
        LIVE_COMMODITY_ID,
        description="Updated Commodity",
    ),
    request_model="CommodityUpdateRequest",
    response_model="Commodity",
)

# ═══════════════════════════════════════════════════════════════════════
# Commodity Maps
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "commodity_map_search",
    lambda api: api.commodity_maps.search(searchText="test"),
    request_model="CommodityMapSearchRequest",
    response_model="List[CommodityMap]",
    fixture_file="CommodityMap.json",
)

runner.add(
    "commodity_map_get",
    lambda api: api.commodity_maps.get(LIVE_MAP_ID),
    response_model="CommodityMap",
)

runner.add(
    "commodity_map_create",
    lambda api: api.commodity_maps.create(
        customName="Test Map",
        commodityId=LIVE_COMMODITY_ID,
    ),
    request_model="CommodityMapCreateRequest",
    response_model="CommodityMap",
)

runner.add(
    "commodity_map_update",
    lambda api: api.commodity_maps.update(
        LIVE_MAP_ID,
        customName="Updated Map",
    ),
    request_model="CommodityMapUpdateRequest",
    response_model="CommodityMap",
)

runner.add(
    "commodity_map_delete",
    lambda api: api.commodity_maps.delete(LIVE_MAP_ID),
    response_model="ServiceBaseResponse",
)

if __name__ == "__main__":
    runner.run()
