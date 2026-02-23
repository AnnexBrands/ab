"""Example: Parcel item operations (5 methods, via api.jobs.*).

Parcel endpoints are accessed through the Jobs API namespace.
"""

from examples._runner import ExampleRunner
from tests.constants import TEST_JOB_DISPLAY_ID

runner = ExampleRunner("Parcels", env="staging")

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "get_parcel_items",
    lambda api: api.jobs.get_parcel_items(TEST_JOB_DISPLAY_ID),
    response_model="List[ParcelItem]",
    fixture_file="ParcelItem.json",
)

runner.add(
    "create_parcel_item",
    lambda api, data=None: api.jobs.create_parcel_item(TEST_JOB_DISPLAY_ID, data or {}),
    request_model="ParcelItemCreateRequest",
    request_fixture_file="ParcelItemCreateRequest.json",
    response_model="ParcelItem",
    fixture_file="ParcelItem.json",
)

runner.add(
    "delete_parcel_item",
    lambda api: api.jobs.delete_parcel_item(TEST_JOB_DISPLAY_ID, "PARCEL_ITEM_ID"),
)

runner.add(
    "get_parcel_items_with_materials",
    lambda api: api.jobs.get_parcel_items_with_materials(TEST_JOB_DISPLAY_ID),
    response_model="List[ParcelItemWithMaterials]",
    fixture_file="ParcelItemWithMaterials.json",
)

runner.add(
    "get_packaging_containers",
    lambda api: api.jobs.get_packaging_containers(TEST_JOB_DISPLAY_ID),
    response_model="List[PackagingContainer]",
    fixture_file="PackagingContainer.json",
)

if __name__ == "__main__":
    runner.run()
