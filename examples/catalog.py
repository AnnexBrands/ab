"""Example: Catalog operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (examples/_catalog.py) to the plain-script form.

The single read-only call (``get``) runs by default. The state-changing calls
(create / update / bulk_insert / delete) mutate staging, so they are guarded:
set ``AB_RUN_MUTATIONS=1`` (or tick "confirm" in the progress app) to run them.

See also: https://ab-sdk.readthedocs.io/en/latest/api/catalog.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_CATALOG_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /Catalog/{id}
    print(f"\n# api.catalog.get({TEST_CATALOG_ID})")
    result = api.catalog.get(TEST_CATALOG_ID)
    print(format_result(result))
    save("CatalogExpandedDto.json", result)

    # The remaining calls write to staging — guarded behind AB_RUN_MUTATIONS=1.
    if not mutations_enabled():
        print("\n# (mutating catalog calls skipped — set AB_RUN_MUTATIONS=1 to run)")
        return

    # POST /Catalog
    print("\n# api.catalog.create(data=AddCatalogRequest(...))")
    created = api.catalog.create(data=load_request("AddCatalogRequest.json"))
    print(format_result(created))
    save("CatalogWithSellersDto.json", created)

    # PUT /Catalog/{id}
    print(f"\n# api.catalog.update({TEST_CATALOG_ID}, data=UpdateCatalogRequest(...))")
    updated = api.catalog.update(TEST_CATALOG_ID, data=load_request("UpdateCatalogRequest.json"))
    print(format_result(updated))
    save("CatalogWithSellersDto.json", updated)

    # POST /Bulk/insert — no response model to diff.
    print("\n# api.catalog.bulk_insert(data=BulkInsertRequest(...))")
    bulk_result = api.catalog.bulk_insert(data=load_request("BulkInsertRequest.json"))
    print(format_result(bulk_result))

    # DELETE /Catalog/{id} — no response model to diff.
    print(f"\n# api.catalog.delete({TEST_CATALOG_ID})")
    delete_result = api.catalog.delete(TEST_CATALOG_ID)
    print(format_result(delete_result))


if __name__ == "__main__":
    main()
