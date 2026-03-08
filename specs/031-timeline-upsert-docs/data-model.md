# Data Model: 031-timeline-upsert-docs

**Date**: 2026-03-07

## Model Changes

### BaseTimelineTaskRequest (modified)

**File**: `ab/api/models/jobs.py` (line ~852)

Add two Optional fields for upsert support:

| Field | Type | Alias | Default | Description |
|-------|------|-------|---------|-------------|
| `id` | `Optional[int]` | (none — native camelCase) | `None` | Server-assigned task ID for update targeting |
| `modified_date` | `Optional[str]` | `modifiedDate` | `None` | Optimistic concurrency token from server |

These fields are inherited by all three subclasses:
- `InTheFieldTaskRequest` (PU/DE tasks)
- `SimpleTaskRequest` (PK/ST tasks)
- `CarrierTaskRequest` (CP tasks)

**Serialization behavior**: `set_task()` uses `model_dump(by_alias=True, exclude_none=True, exclude_unset=True)`. When `id`/`modified_date` are `None` (new task), they are excluded from the payload. When populated from an existing server task, they are included.

### TimelineHelpers (modified)

**File**: `ab/api/helpers/timeline.py`

**Return type changes**:

| Method | Old Return | New Return |
|--------|-----------|------------|
| `set_task()` | `Any` | `TimelineSaveResponse` |
| `schedule()` / `_2` | `Any \| None` | `TimelineSaveResponse` |
| `received()` / `_3` | `Any \| None` | `TimelineSaveResponse` |
| `pack_start()` / `_4` | `Any \| None` | `TimelineSaveResponse` |
| `pack_finish()` / `_5` | `Any \| None` | `TimelineSaveResponse` |
| `storage_begin()` / `_6` | `Any` | `TimelineSaveResponse` |
| `storage_end()` | `Any` | `TimelineSaveResponse` |
| `carrier_schedule()` / `_7` | `Any \| None` | `TimelineSaveResponse` |
| `carrier_pickup()` / `_8` | `Any \| None` | `TimelineSaveResponse` |
| `carrier_delivery()` / `_10` | `Any` | `TimelineSaveResponse` |

**Guard removal**: Each helper that had `if curr >= N: return None` now logs a warning and proceeds.

## State Transitions

The timeline workflow progression:

```
Status 1 (Booked)
  → Status 2 (Scheduled)     — schedule()/_2 sets PU.plannedStartDate
  → Status 3 (Received)      — received()/_3 sets PU.completedDate
  → Status 4 (Pack Start)    — pack_start()/_4 sets PK.timeLog.start
  → Status 5 (Pack Finish)   — pack_finish()/_5 sets PK.timeLog.end
  → Status 6 (Storage)       — storage_begin()/_6 sets ST.timeLog.start
                               storage_end() sets ST.timeLog.end
  → Status 7 (Carrier Sched) — carrier_schedule()/_7 sets CP.scheduledDate
  → Status 8 (Carrier PU)    — carrier_pickup()/_8 sets CP.pickupCompletedDate
  → Status 10 (Delivered)    — carrier_delivery()/_10 sets CP.deliveryCompletedDate
```

With guards removed, helpers proceed at any status (logging a warning when the old guard would have blocked). The server's `modifiedDate` check is the safety mechanism.

## Entities Unchanged

- **TimelineTask** (response model) — no changes
- **TimelineSaveResponse** (response model) — no changes
- **TimelineResponse** (response model) — no changes
- **InTheFieldTaskRequest**, **SimpleTaskRequest**, **CarrierTaskRequest** — inherit new fields from base, no direct changes
