"""Example: Job operations (31 methods).

Covers the full JobsEndpoint surface area, grouped by domain:
Core CRUD, Pricing, Status, Timeline, Tracking, Notes, Parcels, Items.
"""

from examples._runner import ExampleRunner
from tests.constants import TEST_JOB_DISPLAY_ID

runner = ExampleRunner("Jobs", endpoint_attr="jobs", env="staging")

# ═══════════════════════════════════════════════════════════════════════
# Core CRUD
# ═══════════════════════════════════════════════════════════════════════

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "get",
    lambda api: api.jobs.get(TEST_JOB_DISPLAY_ID),
    # response_model and fixture_file auto-discovered from Route
)

runner.add(
    "search",
    lambda api: api.jobs.search(),
    response_model="List[JobSearchResult]",
    fixture_file="JobSearchResult.json",
)

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "search_by_details",
    lambda api, data=None: api.jobs.search_by_details(data=data or {}),
    request_model="JobSearchRequest",
    request_fixture_file="JobSearchRequest.json",
    response_model="List[JobSearchResult]",
    fixture_file="JobSearchResult.json",
)

runner.add(
    "create",
    lambda api, data=None: api.jobs.create(data=data or {}),
    request_model="JobCreateRequest",
    request_fixture_file="JobCreateRequest.json",
)

runner.add(
    "save",
    lambda api, data=None: api.jobs.save(data=data or {}),
    request_model="JobSaveRequest",
    request_fixture_file="JobSaveRequest.json",
)

runner.add(
    "update",
    lambda api, data=None: api.jobs.update(data=data or {}),
    request_model="JobUpdateRequest",
    request_fixture_file="JobUpdateRequest.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Pricing
# ═══════════════════════════════════════════════════════════════════════

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "get_price",
    lambda api: api.jobs.get_price(TEST_JOB_DISPLAY_ID),
    # response_model and fixture_file auto-discovered from Route
)

# ═══════════════════════════════════════════════════════════════════════
# Status
# ═══════════════════════════════════════════════════════════════════════

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "get_update_page_config",
    lambda api: api.jobs.get_update_page_config(TEST_JOB_DISPLAY_ID),
    # response_model and fixture_file auto-discovered from Route
)

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "increment_status",
    lambda api: api.jobs.increment_status(TEST_JOB_DISPLAY_ID),
    request_model="IncrementStatusRequest",
    response_model="ServiceBaseResponse",
    fixture_file="ServiceBaseResponse.json",
)

runner.add(
    "undo_increment_status",
    lambda api: api.jobs.undo_increment_status(TEST_JOB_DISPLAY_ID),
    request_model="IncrementStatusRequest",
    response_model="ServiceBaseResponse",
    fixture_file="ServiceBaseResponse.json",
)

runner.add(
    "set_quote_status",
    lambda api: api.jobs.set_quote_status(TEST_JOB_DISPLAY_ID),
    response_model="ServiceBaseResponse",
    fixture_file="ServiceBaseResponse.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Timeline
# ═══════════════════════════════════════════════════════════════════════

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "get_calendar_items",
    lambda api: api.jobs.get_calendar_items(TEST_JOB_DISPLAY_ID),
    response_model="List[CalendarItem]",
    fixture_file="CalendarItem.json",
)

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get_timeline",
    lambda api: api.jobs.get_timeline(TEST_JOB_DISPLAY_ID),
    response_model="List[TimelineTask]",
    fixture_file="TimelineTask.json",
)

runner.add(
    "create_timeline_task",
    lambda api, data=None: api.jobs.create_timeline_task(TEST_JOB_DISPLAY_ID, data=data or {}),
    request_model="TimelineTaskCreateRequest",
    request_fixture_file="TimelineTaskCreateRequest.json",
    response_model="TimelineTask",
    fixture_file="TimelineTask.json",
)

runner.add(
    "get_timeline_task",
    lambda api: api.jobs.get_timeline_task(TEST_JOB_DISPLAY_ID, "TASK_ID"),
    response_model="TimelineTask",
    fixture_file="TimelineTask.json",
)

runner.add(
    "update_timeline_task",
    lambda api, data=None: api.jobs.update_timeline_task(TEST_JOB_DISPLAY_ID, "TASK_ID", data=data or {}),
    request_model="TimelineTaskUpdateRequest",
    request_fixture_file="TimelineTaskUpdateRequest.json",
    response_model="TimelineTask",
    fixture_file="TimelineTask.json",
)

runner.add(
    "delete_timeline_task",
    lambda api: api.jobs.delete_timeline_task(TEST_JOB_DISPLAY_ID, "TASK_ID"),
    # destructive — no fixture
)

runner.add(
    "get_timeline_agent",
    lambda api: api.jobs.get_timeline_agent(TEST_JOB_DISPLAY_ID, "SCH"),
    response_model="TimelineAgent",
    fixture_file="TimelineAgent.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Tracking
# ═══════════════════════════════════════════════════════════════════════

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get_tracking",
    lambda api: api.jobs.get_tracking(TEST_JOB_DISPLAY_ID),
    response_model="TrackingInfo",
    fixture_file="TrackingInfo.json",
)

runner.add(
    "get_tracking_v3",
    lambda api: api.jobs.get_tracking_v3(TEST_JOB_DISPLAY_ID, history_amount=10),
    response_model="TrackingInfoV3",
    fixture_file="TrackingInfoV3.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Notes
# ═══════════════════════════════════════════════════════════════════════

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "get_notes",
    lambda api: api.jobs.get_notes(TEST_JOB_DISPLAY_ID),
    response_model="List[JobNote]",
    fixture_file="JobNote.json",
)

runner.add(
    "create_note",
    lambda api, data=None: api.jobs.create_note(TEST_JOB_DISPLAY_ID, data=data or {}),
    request_model="JobNoteCreateRequest",
    request_fixture_file="JobNoteCreateRequest.json",
    response_model="JobNote",
    fixture_file="JobNote.json",
)

runner.add(
    "get_note",
    lambda api: api.jobs.get_note(TEST_JOB_DISPLAY_ID, "NOTE_ID"),
    response_model="JobNote",
    fixture_file="JobNote.json",
)

runner.add(
    "update_note",
    lambda api, data=None: api.jobs.update_note(TEST_JOB_DISPLAY_ID, "NOTE_ID", data=data or {}),
    request_model="JobNoteUpdateRequest",
    request_fixture_file="JobNoteUpdateRequest.json",
    response_model="JobNote",
    fixture_file="JobNote.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Parcels
# ═══════════════════════════════════════════════════════════════════════

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "get_parcel_items",
    lambda api: api.jobs.get_parcel_items(TEST_JOB_DISPLAY_ID),
    response_model="List[ParcelItem]",
    fixture_file="ParcelItem.json",
)

runner.add(
    "create_parcel_item",
    lambda api, data=None: api.jobs.create_parcel_item(TEST_JOB_DISPLAY_ID, data=data or {}),
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

# ═══════════════════════════════════════════════════════════════════════
# Items
# ═══════════════════════════════════════════════════════════════════════

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "update_item",
    lambda api, data=None: api.jobs.update_item(TEST_JOB_DISPLAY_ID, "ITEM_ID", data=data or {}),
    request_model="ItemUpdateRequest",
    request_fixture_file="ItemUpdateRequest.json",
    response_model="ServiceBaseResponse",
    fixture_file="ServiceBaseResponse.json",
)

runner.add(
    "add_item_notes",
    lambda api, data=None: api.jobs.add_item_notes(TEST_JOB_DISPLAY_ID, data=data or {}),
    request_model="ItemNotesRequest",
    request_fixture_file="ItemNotesRequest.json",
    response_model="ServiceBaseResponse",
    fixture_file="ServiceBaseResponse.json",
)

if __name__ == "__main__":
    runner.run()
