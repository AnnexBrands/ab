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

runner.add(
    "search_by_details",
    lambda api: api.jobs.search_by_details({"searchText": "test"}),
    request_model="JobSearchRequest",
    response_model="List[JobSearchResult]",
)

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "create",
    lambda api: api.jobs.create(
        # TODO: capture fixture — needs JobCreateRequest body
        {},
    ),
    request_model="JobCreateRequest",
)

runner.add(
    "save",
    lambda api: api.jobs.save(
        # TODO: capture fixture — needs JobSaveRequest body
        {},
    ),
    request_model="JobSaveRequest",
)

runner.add(
    "update",
    lambda api: api.jobs.update(
        # TODO: capture fixture — needs JobUpdateRequest body (ABC API)
        {},
    ),
    request_model="JobUpdateRequest",
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

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "increment_status",
    lambda api: api.jobs.increment_status(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — mutates job status; run with caution
    ),
    request_model="IncrementStatusRequest",
    response_model="ServiceBaseResponse",
)

runner.add(
    "undo_increment_status",
    lambda api: api.jobs.undo_increment_status(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — mutates job status; run with caution
    ),
    request_model="IncrementStatusRequest",
    response_model="ServiceBaseResponse",
)

runner.add(
    "set_quote_status",
    lambda api: api.jobs.set_quote_status(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — mutates job status; run with caution
    ),
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
    lambda api: api.jobs.get_timeline(
        # TODO: capture fixture — needs job ID with active timeline
        LIVE_JOB_DISPLAY_ID,
    ),
    response_model="List[TimelineTask]",
)

runner.add(
    "create_timeline_task",
    lambda api: api.jobs.create_timeline_task(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs TimelineTaskCreateRequest body
        {},
    ),
    request_model="TimelineTaskCreateRequest",
    response_model="TimelineTask",
)

runner.add(
    "get_timeline_task",
    lambda api: api.jobs.get_timeline_task(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid task_id
        "TASK_ID",
    ),
    response_model="TimelineTask",
)

runner.add(
    "update_timeline_task",
    lambda api: api.jobs.update_timeline_task(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid task_id and TimelineTaskUpdateRequest body
        "TASK_ID",
        {},
    ),
    request_model="TimelineTaskUpdateRequest",
    response_model="TimelineTask",
)

runner.add(
    "delete_timeline_task",
    lambda api: api.jobs.delete_timeline_task(
        LIVE_JOB_DISPLAY_ID,
        # TODO: destructive — no fixture needed
        "TASK_ID",
    ),
    # destructive — no fixture
)

runner.add(
    "get_timeline_agent",
    lambda api: api.jobs.get_timeline_agent(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid task code
        "SCH",
    ),
    response_model="TimelineAgent",
)

# ═══════════════════════════════════════════════════════════════════════
# Tracking
# ═══════════════════════════════════════════════════════════════════════

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get_tracking",
    lambda api: api.jobs.get_tracking(
        # TODO: capture fixture — needs shipped job ID
        LIVE_JOB_DISPLAY_ID,
    ),
    response_model="TrackingInfo",
)

runner.add(
    "get_tracking_v3",
    lambda api: api.jobs.get_tracking_v3(
        # TODO: capture fixture — needs shipped job ID
        LIVE_JOB_DISPLAY_ID,
        history_amount=10,
    ),
    response_model="TrackingInfoV3",
)

# ═══════════════════════════════════════════════════════════════════════
# Notes
# ═══════════════════════════════════════════════════════════════════════

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get_notes",
    lambda api: api.jobs.get_notes(
        # TODO: capture fixture — needs job ID with notes
        LIVE_JOB_DISPLAY_ID,
    ),
    response_model="List[JobNote]",
)

runner.add(
    "create_note",
    lambda api: api.jobs.create_note(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs JobNoteCreateRequest body
        {},
    ),
    request_model="JobNoteCreateRequest",
    response_model="JobNote",
)

runner.add(
    "get_note",
    lambda api: api.jobs.get_note(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid note_id
        "NOTE_ID",
    ),
    response_model="JobNote",
)

runner.add(
    "update_note",
    lambda api: api.jobs.update_note(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid note_id and JobNoteUpdateRequest body
        "NOTE_ID",
        {},
    ),
    request_model="JobNoteUpdateRequest",
    response_model="JobNote",
)

# ═══════════════════════════════════════════════════════════════════════
# Parcels
# ═══════════════════════════════════════════════════════════════════════

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

# ═══════════════════════════════════════════════════════════════════════
# Items
# ═══════════════════════════════════════════════════════════════════════

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "update_item",
    lambda api: api.jobs.update_item(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid item_id and ItemUpdateRequest body
        "ITEM_ID",
        {},
    ),
    request_model="ItemUpdateRequest",
    response_model="ServiceBaseResponse",
)

runner.add(
    "add_item_notes",
    lambda api: api.jobs.add_item_notes(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs ItemNotesRequest body
        {},
    ),
    request_model="ItemNotesRequest",
    response_model="ServiceBaseResponse",
)

if __name__ == "__main__":
    runner.run()
