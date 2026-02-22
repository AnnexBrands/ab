"""Example: Commodity and commodity map operations (10 methods).

Covers CRUD and search for both commodities and commodity maps.
"""

from examples._runner import ExampleRunner

runner = ExampleRunner("Commodities", env="staging")

TEST_COMMODITY_ID = "PLACEHOLDER"
TEST_MAP_ID = "PLACEHOLDER"

# ═══════════════════════════════════════════════════════════════════════
# Commodities
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "commodity_search",
    lambda api, data=None: api.commodities.search(**(data or {})),
    request_model="CommoditySearchRequest",
    request_fixture_file="CommoditySearchRequest.json",
    response_model="List[Commodity]",
    fixture_file="Commodity.json",
)

runner.add(
    "commodity_suggestions",
    lambda api, data=None: api.commodities.suggestions(**(data or {})),
    request_model="CommoditySuggestionRequest",
    request_fixture_file="CommoditySuggestionRequest.json",
    response_model="List[Commodity]",
)

runner.add(
    "commodity_get",
    lambda api: api.commodities.get(TEST_COMMODITY_ID),
    response_model="Commodity",
)

runner.add(
    "commodity_create",
    lambda api, data=None: api.commodities.create(**(data or {})),
    request_model="CommodityCreateRequest",
    request_fixture_file="CommodityCreateRequest.json",
    response_model="Commodity",
)

runner.add(
    "commodity_update",
    lambda api, data=None: api.commodities.update(TEST_COMMODITY_ID, **(data or {})),
    request_model="CommodityUpdateRequest",
    request_fixture_file="CommodityUpdateRequest.json",
    response_model="Commodity",
)

# ═══════════════════════════════════════════════════════════════════════
# Commodity Maps
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "commodity_map_search",
    lambda api, data=None: api.commodity_maps.search(**(data or {})),
    request_model="CommodityMapSearchRequest",
    request_fixture_file="CommodityMapSearchRequest.json",
    response_model="List[CommodityMap]",
    fixture_file="CommodityMap.json",
)

runner.add(
    "commodity_map_get",
    lambda api: api.commodity_maps.get(TEST_MAP_ID),
    response_model="CommodityMap",
)

runner.add(
    "commodity_map_create",
    lambda api, data=None: api.commodity_maps.create(**(data or {})),
    request_model="CommodityMapCreateRequest",
    request_fixture_file="CommodityMapCreateRequest.json",
    response_model="CommodityMap",
)

runner.add(
    "commodity_map_update",
    lambda api, data=None: api.commodity_maps.update(TEST_MAP_ID, **(data or {})),
    request_model="CommodityMapUpdateRequest",
    request_fixture_file="CommodityMapUpdateRequest.json",
    response_model="CommodityMap",
)

runner.add(
    "commodity_map_delete",
    lambda api: api.commodity_maps.delete(TEST_MAP_ID),
    response_model="ServiceBaseResponse",
)

if __name__ == "__main__":
    runner.run()
