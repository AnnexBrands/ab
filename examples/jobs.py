"""Example: Job operations (31 methods).

Covers the full JobsEndpoint surface area, grouped by domain:
Core CRUD, Pricing, Status, Timeline, Tracking, Notes, Parcels, Items.
"""

from examples._runner import ExampleRunner
from tests.constants import LIVE_JOB_DISPLAY_ID

runner = ExampleRunner("Jobs", env="staging")

# ═══════════════════════════════════════════════════════════════════════
# Core CRUD
# ═══════════════════════════════════════════════════════════════════════

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "get",
    lambda api: api.jobs.get(LIVE_JOB_DISPLAY_ID),
    response_model="Job",
    fixture_file="Job.json",
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
    lambda api, data=None: api.jobs.search_by_details(data or {}),
    request_model="JobSearchRequest",
    request_fixture_file="JobSearchRequest.json",
    response_model="List[JobSearchResult]",
)

runner.add(
    "create",
    lambda api, data=None: api.jobs.create(data or {}),
    request_model="JobCreateRequest",
    request_fixture_file="JobCreateRequest.json",
)

runner.add(
    "save",
    lambda api, data=None: api.jobs.save(data or {}),
    request_model="JobSaveRequest",
    request_fixture_file="JobSaveRequest.json",
)

runner.add(
    "update",
    lambda api, data=None: api.jobs.update(data or {}),
    request_model="JobUpdateRequest",
    request_fixture_file="JobUpdateRequest.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Pricing
# ═══════════════════════════════════════════════════════════════════════

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "get_price",
    lambda api: api.jobs.get_price(LIVE_JOB_DISPLAY_ID),
    response_model="JobPrice",
    fixture_file="JobPrice.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Status
# ═══════════════════════════════════════════════════════════════════════

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "get_update_page_config",
    lambda api: api.jobs.get_update_page_config(LIVE_JOB_DISPLAY_ID),
    response_model="JobUpdatePageConfig",
    fixture_file="JobUpdatePageConfig.json",
)

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "increment_status",
    lambda api: api.jobs.increment_status(LIVE_JOB_DISPLAY_ID),
    request_model="IncrementStatusRequest",
    response_model="ServiceBaseResponse",
)

runner.add(
    "undo_increment_status",
    lambda api: api.jobs.undo_increment_status(LIVE_JOB_DISPLAY_ID),
    request_model="IncrementStatusRequest",
    response_model="ServiceBaseResponse",
)

runner.add(
    "set_quote_status",
    lambda api: api.jobs.set_quote_status(LIVE_JOB_DISPLAY_ID),
    response_model="ServiceBaseResponse",
)

# ═══════════════════════════════════════════════════════════════════════
# Timeline
# ═══════════════════════════════════════════════════════════════════════

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "get_calendar_items",
    lambda api: api.jobs.get_calendar_items(LIVE_JOB_DISPLAY_ID),
    response_model="List[CalendarItem]",
    fixture_file="CalendarItem.json",
)

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get_timeline",
    lambda api: api.jobs.get_timeline(LIVE_JOB_DISPLAY_ID),
    response_model="List[TimelineTask]",
)

runner.add(
    "create_timeline_task",
    lambda api, data=None: api.jobs.create_timeline_task(LIVE_JOB_DISPLAY_ID, data or {}),
    request_model="TimelineTaskCreateRequest",
    request_fixture_file="TimelineTaskCreateRequest.json",
    response_model="TimelineTask",
)

runner.add(
    "get_timeline_task",
    lambda api: api.jobs.get_timeline_task(LIVE_JOB_DISPLAY_ID, "TASK_ID"),
    response_model="TimelineTask",
)

runner.add(
    "update_timeline_task",
    lambda api, data=None: api.jobs.update_timeline_task(LIVE_JOB_DISPLAY_ID, "TASK_ID", data or {}),
    request_model="TimelineTaskUpdateRequest",
    request_fixture_file="TimelineTaskUpdateRequest.json",
    response_model="TimelineTask",
)

runner.add(
    "delete_timeline_task",
    lambda api: api.jobs.delete_timeline_task(LIVE_JOB_DISPLAY_ID, "TASK_ID"),
    # destructive — no fixture
)

runner.add(
    "get_timeline_agent",
    lambda api: api.jobs.get_timeline_agent(LIVE_JOB_DISPLAY_ID, "SCH"),
    response_model="TimelineAgent",
)

# ═══════════════════════════════════════════════════════════════════════
# Tracking
# ═══════════════════════════════════════════════════════════════════════

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get_tracking",
    lambda api: api.jobs.get_tracking(LIVE_JOB_DISPLAY_ID),
    response_model="TrackingInfo",
)

runner.add(
    "get_tracking_v3",
    lambda api: api.jobs.get_tracking_v3(LIVE_JOB_DISPLAY_ID, history_amount=10),
    response_model="TrackingInfoV3",
)

# ═══════════════════════════════════════════════════════════════════════
# Notes
# ═══════════════════════════════════════════════════════════════════════

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "get_notes",
    lambda api: api.jobs.get_notes(LIVE_JOB_DISPLAY_ID),
    response_model="List[JobNote]",
)

runner.add(
    "create_note",
    lambda api, data=None: api.jobs.create_note(LIVE_JOB_DISPLAY_ID, data or {}),
    request_model="JobNoteCreateRequest",
    request_fixture_file="JobNoteCreateRequest.json",
    response_model="JobNote",
)

runner.add(
    "get_note",
    lambda api: api.jobs.get_note(LIVE_JOB_DISPLAY_ID, "NOTE_ID"),
    response_model="JobNote",
)

runner.add(
    "update_note",
    lambda api, data=None: api.jobs.update_note(LIVE_JOB_DISPLAY_ID, "NOTE_ID", data or {}),
    request_model="JobNoteUpdateRequest",
    request_fixture_file="JobNoteUpdateRequest.json",
    response_model="JobNote",
)

# ═══════════════════════════════════════════════════════════════════════
# Parcels
# ═══════════════════════════════════════════════════════════════════════

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "get_parcel_items",
    lambda api: api.jobs.get_parcel_items(LIVE_JOB_DISPLAY_ID),
    response_model="List[ParcelItem]",
)

runner.add(
    "create_parcel_item",
    lambda api, data=None: api.jobs.create_parcel_item(LIVE_JOB_DISPLAY_ID, data or {}),
    request_model="ParcelItemCreateRequest",
    request_fixture_file="ParcelItemCreateRequest.json",
    response_model="ParcelItem",
)

runner.add(
    "delete_parcel_item",
    lambda api: api.jobs.delete_parcel_item(LIVE_JOB_DISPLAY_ID, "PARCEL_ITEM_ID"),
)

runner.add(
    "get_parcel_items_with_materials",
    lambda api: api.jobs.get_parcel_items_with_materials(LIVE_JOB_DISPLAY_ID),
    response_model="List[ParcelItemWithMaterials]",
)

runner.add(
    "get_packaging_containers",
    lambda api: api.jobs.get_packaging_containers(LIVE_JOB_DISPLAY_ID),
    response_model="List[PackagingContainer]",
)

# ═══════════════════════════════════════════════════════════════════════
# Items
# ═══════════════════════════════════════════════════════════════════════

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "update_item",
    lambda api, data=None: api.jobs.update_item(LIVE_JOB_DISPLAY_ID, "ITEM_ID", data or {}),
    request_model="ItemUpdateRequest",
    request_fixture_file="ItemUpdateRequest.json",
    response_model="ServiceBaseResponse",
)

runner.add(
    "add_item_notes",
    lambda api, data=None: api.jobs.add_item_notes(LIVE_JOB_DISPLAY_ID, data or {}),
    request_model="ItemNotesRequest",
    request_fixture_file="ItemNotesRequest.json",
    response_model="ServiceBaseResponse",
)

if __name__ == "__main__":
    runner.run()
