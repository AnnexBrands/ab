"""Example: api.jobs.items — lenient parcel/freight item helpers.

The ``api.jobs.items`` helpers wrap the routed parcel-item and freight-item
endpoints with get-merge-write + loose-keyword ergonomics so that:

* a replace/update never makes the pydantic request model squawk — unknown
  keyword arguments are dropped instead of raising; and
* a freight update/delete preserves the other freight items (the freight
  endpoint is a full ``SaveAllFreightItemsRequest`` replace with no per-item
  routes), so the helper reads the current set, merges one item, and saves all.

This script shows the lifecycle the helpers exist for: read the current state,
create, read again (the GET shows the new item), replace, then delete. The
mutating calls are guarded — set ``AB_RUN_MUTATIONS=1`` to run them against
staging.

See also tests/helpers/test_item_helpers.py for the deterministic coverage of
create-then-delete, create-then-replace, and get-shows-expected-state.
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import mutations_enabled
from examples.constants import TEST_JOB_DISPLAY_ID


def main() -> None:
    api = ABConnectAPI(env="staging")
    job = TEST_JOB_DISPLAY_ID

    # --- Read current state (the GET shows us the expected state) -----------
    print(f"\n# api.jobs.items.list_parcel({job})")
    parcels = api.jobs.items.list_parcel(job)
    print(format_result(parcels))

    print(f"\n# api.jobs.items.list_freight({job})")
    freight = api.jobs.items.list_freight(job)
    print(format_result(freight))

    if not mutations_enabled():
        print(
            "\n# create / replace / delete skipped — set AB_RUN_MUTATIONS=1 to run "
            "(mutates staging)"
        )
        return

    # --- Parcel: create -> get (shows it) -> replace -> delete --------------
    print(f"\n# api.jobs.items.upsert_parcel({job}, description='SDK example crate', ...)")
    created = api.jobs.items.upsert_parcel(
        job,
        description="SDK example crate",
        length=24,
        width=18,
        height=12,
        weight=40,
        # an unknown key is dropped rather than raising — no squawk:
        not_a_real_field="ignored",
    )
    print(format_result(created))

    print(f"\n# api.jobs.items.list_parcel({job})  # GET shows the new item")
    print(format_result(api.jobs.items.list_parcel(job)))

    print(f"\n# api.jobs.items.replace_parcel({job}, {created.id!r}, description='...reinforced')")
    # Each parcel item needs dimensions (or a package-type id), so pass L/W/H too.
    replaced = api.jobs.items.replace_parcel(
        job, created.id, description="SDK example crate (reinforced)", length=26, width=20, height=14, weight=60
    )
    print(format_result(replaced))

    print(f"\n# api.jobs.items.delete_parcel({job}, {replaced.id!r})")
    print(format_result(api.jobs.items.delete_parcel(job, replaced.id)))

    # --- Freight: replace one item's weight, preserving the rest -----------
    # Freight saves replace the entire set, so the helper reads -> merges one
    # -> saves all. Only run when the job already has a freight item to edit.
    if freight:
        target = freight[0]
        print(
            f"\n# api.jobs.items.replace_freight({job}, {target.freight_item_id!r}, weight=...)"
            "  # other freight items preserved"
        )
        state = api.jobs.items.replace_freight(
            job, target.freight_item_id, weight=(target.item_weight or 100.0)
        )
        print(format_result(state))
    else:
        print("\n# freight replace skipped — job has no freight items to edit")


if __name__ == "__main__":
    main()
