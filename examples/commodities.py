"""Example: Commodity operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (examples/_commodities.py) to the plain-script form.

See also: https://ab-sdk.readthedocs.io/en/latest/api/commodities.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save

# Commodity identifier (staging). No TEST_* constant exists for commodities yet;
# replace with a real id discovered via api.commodities.search(...).
TEST_COMMODITY_ID = "PLACEHOLDER"


def main() -> None:
    api = ABConnectAPI(env="staging")

    # POST /commodity/search — read-only.
    print("\n# api.commodities.search(data=CommoditySearchRequest(...))")
    result = api.commodities.search(data=load_request("CommoditySearchRequest.json"))
    print(format_result(result))
    save("Commodity.json", result)

    # POST /commodity/suggestions — read-only.
    print("\n# api.commodities.suggestions(data=CommoditySuggestionRequest(...))")
    result = api.commodities.suggestions(data=load_request("CommoditySuggestionRequest.json"))
    print(format_result(result))
    save("Commodity.json", result)

    # GET /commodity/{id}
    print(f"\n# api.commodities.get({TEST_COMMODITY_ID!r})")
    result = api.commodities.get(TEST_COMMODITY_ID)
    print(format_result(result))
    save("Commodity.json", result)

    # POST /commodity — creates a commodity (mutates staging).
    if mutations_enabled():
        print("\n# api.commodities.create(data=CommodityCreateRequest(...))")
        result = api.commodities.create(data=load_request("CommodityCreateRequest.json"))
        print(format_result(result))
        save("Commodity.json", result)
    else:
        print("\n# api.commodities.create skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # PUT /commodity/{id} — updates a commodity (mutates staging).
    if mutations_enabled():
        print(f"\n# api.commodities.update({TEST_COMMODITY_ID!r}, data=CommodityUpdateRequest(...))")
        result = api.commodities.update(
            TEST_COMMODITY_ID, data=load_request("CommodityUpdateRequest.json")
        )
        print(format_result(result))
        save("Commodity.json", result)
    else:
        print("\n# api.commodities.update skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")


if __name__ == "__main__":
    main()
