# Data Model: 030 — Fix Timeline Helpers

## Request Models (New — Replace `TimelineTaskCreateRequest`)

### BaseTimelineTaskRequest (Abstract Base)

Shared fields for all timeline task creation requests. Maps to C# `BaseTaskModel`.

| Field | Type | Required | Alias | Notes |
|-------|------|----------|-------|-------|
| task_code | str | **Yes** | taskCode | One of: PU, PK, ST, CP, DE |
| planned_start_date | Optional[str] | No | plannedStartDate | ISO 8601 datetime |
| work_time_logs | Optional[List[WorkTimeLogRequest]] | No | workTimeLogs | Work time entries |
| initial_note | Optional[InitialNoteRequest] | No | initialNote | Task note on creation |

### InTheFieldTaskRequest (PU/DE tasks)

Maps to C# `InTheFieldTaskModel`. Used by helpers: `schedule()`, `received()`.

| Field | Type | Required | Alias | Notes |
|-------|------|----------|-------|-------|
| *(base fields)* | | | | Inherited from BaseTimelineTaskRequest |
| planned_end_date | Optional[str] | No | plannedEndDate | ISO 8601 datetime |
| preferred_start_date | Optional[str] | No | preferredStartDate | ISO 8601 datetime |
| preferred_end_date | Optional[str] | No | preferredEndDate | ISO 8601 datetime |
| truck | Optional[TaskTruckInfoRequest] | No | truck | Truck assignment |
| on_site_time_log | Optional[TimeLogRequest] | No | onSiteTimeLog | On-site time period |
| trip_time_log | Optional[TimeLogRequest] | No | tripTimeLog | Trip time period |
| completed_date | Optional[str] | No | completedDate | Pickup completed date |

### SimpleTaskRequest (PK/ST tasks)

Maps to C# `SimpleTaskModel`. Used by helpers: `pack_start()`, `pack_finish()`, `storage_begin()`, `storage_end()`.

| Field | Type | Required | Alias | Notes |
|-------|------|----------|-------|-------|
| *(base fields)* | | | | Inherited from BaseTimelineTaskRequest |
| time_log | Optional[TimeLogRequest] | No | timeLog | Single time period |

### CarrierTaskRequest (CP tasks)

Maps to C# `CarrierTaskModel`. Used by helpers: `carrier_schedule()`, `carrier_pickup()`, `carrier_delivery()`.

| Field | Type | Required | Alias | Notes |
|-------|------|----------|-------|-------|
| *(base fields)* | | | | Inherited from BaseTimelineTaskRequest |
| scheduled_date | Optional[str] | No | scheduledDate | Carrier schedule date |
| pickup_completed_date | Optional[str] | No | pickupCompletedDate | Carrier pickup date |
| delivery_completed_date | Optional[str] | No | deliveryCompletedDate | Carrier delivery date |
| expected_delivery_date | Optional[str] | No | expectedDeliveryDate | Expected delivery |

## Nested Request Models (New)

### TimeLogRequest

Maps to C# `TimeLogModel`. Used by PK/ST (`time_log`) and PU (`on_site_time_log`, `trip_time_log`).

| Field | Type | Required | Alias | Notes |
|-------|------|----------|-------|-------|
| start | Optional[str] | No | start | ISO 8601 datetime |
| end | Optional[str] | No | end | ISO 8601 datetime |
| pauses | Optional[List[TimeLogPauseRequest]] | No | pauses | Pause periods within the time log |

### TimeLogPauseRequest

Maps to C# `TimeLogPauseModel`.

| Field | Type | Required | Alias | Notes |
|-------|------|----------|-------|-------|
| start | Optional[str] | No | start | Pause start datetime |
| end | Optional[str] | No | end | Pause end datetime |

### WorkTimeLogRequest

Maps to C# `WorkTimeLogModel`.

| Field | Type | Required | Alias | Notes |
|-------|------|----------|-------|-------|
| date | Optional[str] | No | date | Work date |
| start_time | Optional[str] | No | startTime | Start time of day (TimeSpan as string) |
| end_time | Optional[str] | No | endTime | End time of day (TimeSpan as string) |

### InitialNoteRequest

Maps to C# `InitialNoteModel`.

| Field | Type | Required | Alias | Notes |
|-------|------|----------|-------|-------|
| comments | str | **Yes** | comments | Note text (1-8000 chars) |
| due_date | Optional[str] | No | dueDate | Due date |
| is_important | Optional[bool] | No | isImportant | Importance flag |
| is_completed | Optional[bool] | No | isCompleted | Completion flag |
| send_notification | Optional[bool] | No | sendNotification | Email notification flag |

### TaskTruckInfoRequest

Maps to C# `TaskTruckInfo`.

| Field | Type | Required | Alias | Notes |
|-------|------|----------|-------|-------|
| id | int | **Yes** | id | Truck lookup ID |
| name | Optional[str] | No | name | Display name |
| is_active | Optional[bool] | No | isActive | Active flag |

## Response Models (Existing — No Changes)

### TimelineTask (Unified)

Existing unified response model. All task-type fields in one class with `extra="allow"`. No changes needed (D6).

### TimelineSaveResponse

Existing response model for POST. Contains `task: TimelineTask`, `task_exists`, `email_log_id`, `job_sub_management_status`. No changes needed.

### TimelineResponse

Existing response model for GET. Contains `tasks: List[TimelineTask]`. No changes needed.

## Models to Remove

| Model | Reason |
|-------|--------|
| `TimelineTaskCreateRequest` | Replaced by 3 per-type request models |

## Relationships

```text
BaseTimelineTaskRequest
├── InTheFieldTaskRequest (PU/DE)
│   ├── on_site_time_log → TimeLogRequest
│   ├── trip_time_log → TimeLogRequest
│   └── truck → TaskTruckInfoRequest
├── SimpleTaskRequest (PK/ST)
│   └── time_log → TimeLogRequest
└── CarrierTaskRequest (CP)

TimeLogRequest
└── pauses → List[TimeLogPauseRequest]

BaseTimelineTaskRequest (shared)
├── work_time_logs → List[WorkTimeLogRequest]
└── initial_note → InitialNoteRequest

TaskModelDataBinder routing (C# ground truth):
  taskCode="PU" or "DE" → InTheFieldTaskRequest
  taskCode="CP"         → CarrierTaskRequest
  default ("PK","ST")   → SimpleTaskRequest
```
