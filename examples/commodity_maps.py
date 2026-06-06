"""Example: Commodity map operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (examples/_commodities.py) to the plain-script form.

See also: https://ab-sdk.readthedocs.io/en/latest/api/commodity_maps.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save

# Commodity map identifier (staging). No TEST_* constant exists for commodity
# maps yet; replace with a real id discovered via api.commodity_maps.search(...).
TEST_MAP_ID = "PLACEHOLDER"


def main() -> None:
    api = ABConnectAPI(env="staging")

    # POST /commodity-map/search — read-only.
    print("\n# api.commodity_maps.search(data=CommodityMapSearchRequest(...))")
    result = api.commodity_maps.search(data=load_request("CommodityMapSearchRequest.json"))
    print(format_result(result))
    save("CommodityMap.json", result)

    # GET /commodity-map/{id}
    print(f"\n# api.commodity_maps.get({TEST_MAP_ID!r})")
    result = api.commodity_maps.get(TEST_MAP_ID)
    print(format_result(result))
    save("CommodityMap.json", result)

    # POST /commodity-map — creates a commodity map (mutates staging).
    if mutations_enabled():
        print("\n# api.commodity_maps.create(data=CommodityMapCreateRequest(...))")
        result = api.commodity_maps.create(data=load_request("CommodityMapCreateRequest.json"))
        print(format_result(result))
        save("CommodityMap.json", result)
    else:
        print("\n# api.commodity_maps.create skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # PUT /commodity-map/{id} — updates a commodity map (mutates staging).
    if mutations_enabled():
        print(f"\n# api.commodity_maps.update({TEST_MAP_ID!r}, data=CommodityMapUpdateRequest(...))")
        result = api.commodity_maps.update(
            TEST_MAP_ID, data=load_request("CommodityMapUpdateRequest.json")
        )
        print(format_result(result))
        save("CommodityMap.json", result)
    else:
        print("\n# api.commodity_maps.update skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # DELETE /commodity-map/{id} — deletes a commodity map (mutates staging).
    if mutations_enabled():
        print(f"\n# api.commodity_maps.delete({TEST_MAP_ID!r})")
        result = api.commodity_maps.delete(TEST_MAP_ID)
        print(format_result(result))
        save("ServiceBaseResponse.json", result)
    else:
        print("\n# api.commodity_maps.delete skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")


if __name__ == "__main__":
    main()
