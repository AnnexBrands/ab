"""Example: Parcel item operations (5 methods, via api.jobs.*).

Parcel endpoints are accessed through the Jobs API namespace.
"""

from examples._runner import ExampleRunner

LIVE_JOB_DISPLAY_ID = 2000000

runner = ExampleRunner("Parcels", env="staging")

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get_parcel_items",
    lambda api: api.jobs.get_parcel_items(
        # TODO: capture fixture — needs job ID with parcel items
        LIVE_JOB_DISPLAY_ID,
    ),
    response_model="List[ParcelItem]",
)

runner.add(
    "create_parcel_item",
    lambda api: api.jobs.create_parcel_item(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs ParcelItemCreateRequest body
        {},
    ),
    request_model="ParcelItemCreateRequest",
    response_model="ParcelItem",
)

runner.add(
    "delete_parcel_item",
    lambda api: api.jobs.delete_parcel_item(
        LIVE_JOB_DISPLAY_ID,
        # destructive — no fixture
        "PARCEL_ITEM_ID",
    ),
)

runner.add(
    "get_parcel_items_with_materials",
    lambda api: api.jobs.get_parcel_items_with_materials(
        # TODO: capture fixture — needs job ID with parcel items
        LIVE_JOB_DISPLAY_ID,
    ),
    response_model="List[ParcelItemWithMaterials]",
)

runner.add(
    "get_packaging_containers",
    lambda api: api.jobs.get_packaging_containers(
        # TODO: capture fixture — needs job ID with packaging containers
        LIVE_JOB_DISPLAY_ID,
    ),
    response_model="List[PackagingContainer]",
)

if __name__ == "__main__":
    runner.run()
