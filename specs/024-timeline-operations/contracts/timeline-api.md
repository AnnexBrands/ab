# API Contracts: Timeline Operations

## Existing Routes (response model corrections)

### GET /job/{jobDisplayId}/timeline
- **Current**: `response_model="List[TimelineTask]"` (WRONG)
- **Corrected**: `response_model="TimelineResponse"`
- **Response**: `TimelineResponse` wrapper with `tasks` list + job status metadata

### POST /job/{jobDisplayId}/timeline
- **Current**: `response_model="TimelineTask"` (WRONG)
- **Corrected**: `response_model="TimelineSaveResponse"`
- **Request**: Task dict with `taskCode` + task-specific fields
- **Query params**: `createEmail` (bool)
- **Response**: `TimelineSaveResponse` with `success`, `taskExists`, `task`, `jobSubManagementStatus`

### GET /job/{jobDisplayId}/timeline/{timelineTaskIdentifier}
- **Current**: `response_model="TimelineTask"` — verify against live API
- **Response**: Single `TimelineTask` object

### PATCH /job/{jobDisplayId}/timeline/{timelineTaskId}
- **Current**: `response_model="TimelineTask"` — verify against live API
- **Request**: `TimelineTaskUpdateRequest` with partial fields

### DELETE /job/{jobDisplayId}/timeline/{timelineTaskId}
- **Current**: `response_model="ServiceBaseResponse"` — correct
- **Response**: `ServiceBaseResponse` with `success`, `errorMessage`

### GET /job/{jobDisplayId}/timeline/{taskCode}/agent
- **Current**: `response_model="TimelineAgent"` — model fields need correction
- **Response**: `TimelineAgent` (verify: CompanyListItem shape from C#)

### POST /job/{jobDisplayId}/timeline/incrementjobstatus
- **Current**: correct
- **Response**: `ServiceBaseResponse`

### POST /job/{jobDisplayId}/timeline/undoincrementjobstatus
- **Current**: correct
- **Response**: `ServiceBaseResponse`

## New Helper Methods (TimelineHelpers class)

### Core Methods

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `get_task` | `(job_id, taskcode)` | `(status_info, task_or_None)` | Fetch timeline + extract specific task |
| `set_task` | `(job_id, taskcode, task, create_email=False)` | `TimelineSaveResponse` | Create or update task via POST |
| `delete` | `(job_id, taskcode)` | `ServiceBaseResponse or None` | Delete specific task by code |
| `delete_all` | `(job_id)` | `list` | Delete all tasks (reset to status 1) |

### Status Helpers

| Method | Alias | Status | Task Code | Key Fields Set |
|--------|-------|--------|-----------|----------------|
| `schedule` | `_2` | 2 | PU | plannedStartDate, plannedEndDate |
| `received` | `_3` | 3 | PU | completedDate, onSiteTimeLog |
| `pack_start` | `_4` | 4 | PK | timeLog.start |
| `pack_finish` | `_5` | 5 | PK | timeLog.end |
| `storage_begin` | `_6` | 6 | ST | timeLog.start |
| `storage_end` | — | 6 | ST | timeLog.end |
| `carrier_schedule` | `_7` | 7 | CP | scheduledDate |
| `carrier_pickup` | `_8` | 8 | CP | pickupCompletedDate |
| `carrier_delivery` | `_10` | 10 | CP | deliveryCompletedDate |
