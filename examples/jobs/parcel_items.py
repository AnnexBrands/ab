"""Example: api.jobs.parcel_items — list / create / delete job parcel items.

Live SDK example — real call, real printed pydantic response. Authored for
feature 037 (endpoint previously had no example).

Parcel items are the packed pieces on a job. This script:

1. Lists existing parcel items on ``TEST_JOB_DISPLAY_ID`` (read-only).
2. Lists the same items with their material breakdown (read-only).
3. Creates a new parcel item (guarded — mutates staging).
4. Deletes a parcel item (guarded). The ``parcelItemId`` path param is
   discovered from the ``list()`` result; falls back to a placeholder the
   operator must supply for a live run.

See also: https://ab-sdk.readthedocs.io/en/latest/api/jobs.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_JOB_DISPLAY_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /job/{jobDisplayId}/parcelitems (read-only)
    print(f"\n# api.jobs.parcel_items.list({TEST_JOB_DISPLAY_ID})")
    items = api.jobs.parcel_items.list(TEST_JOB_DISPLAY_ID)
    print(format_result(items))
    save("ParcelItem.json", items)

    # GET /job/{jobDisplayId}/parcel-items-with-materials (read-only)
    print(f"\n# api.jobs.parcel_items.list_with_materials({TEST_JOB_DISPLAY_ID})")
    with_materials = api.jobs.parcel_items.list_with_materials(TEST_JOB_DISPLAY_ID)
    print(format_result(with_materials))
    save("ParcelItemWithMaterials.json", with_materials)

    # POST /job/{jobDisplayId}/parcelitems — state-changing, guarded.
    if mutations_enabled():
        print(f"\n# api.jobs.parcel_items.create({TEST_JOB_DISPLAY_ID}, data=...)")
        created = api.jobs.parcel_items.create(
            TEST_JOB_DISPLAY_ID,
            data=load_request("ParcelItemCreateRequest.json"),
        )
        print(format_result(created))
        save("ParcelItem.json", [created])
    else:
        print(
            "# api.jobs.parcel_items.create skipped — set AB_RUN_MUTATIONS=1 to run "
            "(mutates staging)",
        )

    # DELETE /job/{jobDisplayId}/parcelitems/{parcelItemId} — guarded.
    if mutations_enabled():
        # Discover a parcel-item id from the list above; fall back to a
        # placeholder the operator must replace with a real id for a live run.
        if items and items[0].id is not None:
            parcel_item_id = str(items[0].id)
        else:
            parcel_item_id = "PARCEL_ITEM_ID"  # supply a real id for a live run
        print(
            f"\n# api.jobs.parcel_items.delete({TEST_JOB_DISPLAY_ID}, {parcel_item_id!r})",
        )
        res = api.jobs.parcel_items.delete(TEST_JOB_DISPLAY_ID, parcel_item_id)
        print(format_result(res))
        save("ServiceBaseResponse.json", res)
    else:
        print(
            "# api.jobs.parcel_items.delete skipped — set AB_RUN_MUTATIONS=1 to run "
            "(mutates staging)",
        )


if __name__ == "__main__":
    main()
