"""Example: Lots operations (Catalog API).

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (examples/_lots.py) to the plain-script form.

See also: https://ab-sdk.readthedocs.io/en/latest/api/lots.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_LOT_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /Lot/{id}
    print(f"\n# api.lots.get({TEST_LOT_ID!r})")
    result = api.lots.get(TEST_LOT_ID)
    print(format_result(result))
    save("LotDto.json", result)

    # POST /Lot/get-overrides — read-only lookup, safe to run unguarded.
    print("\n# api.lots.get_overrides([...])")
    result = api.lots.get_overrides([])
    print(format_result(result))
    save("LotOverrideDto.json", result)

    # POST /Lot — creates a lot (mutates staging).
    if mutations_enabled():
        print("\n# api.lots.create(data=AddLotRequest(...))")
        result = api.lots.create(data=load_request("AddLotRequest.json"))
        print(format_result(result))
        save("LotDto.json", result)
    else:
        print("\n# api.lots.create skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # PUT /Lot/{id} — updates a lot (mutates staging).
    if mutations_enabled():
        print(f"\n# api.lots.update({TEST_LOT_ID!r}, data=UpdateLotRequest(...))")
        result = api.lots.update(TEST_LOT_ID, data=load_request("UpdateLotRequest.json"))
        print(format_result(result))
        save("LotDto.json", result)
    else:
        print("\n# api.lots.update skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # DELETE /Lot/{id} — deletes a lot (mutates staging); no response model.
    if mutations_enabled():
        print(f"\n# api.lots.delete({TEST_LOT_ID!r})")
        result = api.lots.delete(TEST_LOT_ID)
        print(format_result(result))
    else:
        print("\n# api.lots.delete skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")


if __name__ == "__main__":
    main()
