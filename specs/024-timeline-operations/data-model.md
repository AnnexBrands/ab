# Data Model: Timeline Operations

**Feature**: 024-timeline-operations | **Date**: 2026-02-28

## Entity Reference

Sources: C# server DTOs (Tier 1), ABConnectTools models (Tier 1), live API fixtures (Tier 2, to be captured).

---

### TimelineTask (Response Model — unified)

All task codes (PU, PK, ST, CP) share one model. Task-code-specific fields are null when not applicable.

**Common fields** (from C# BaseTask + TimestampedModel):

| Python field | JSON alias | Type | Source |
|---|---|---|---|
| id | id | Optional[int] | BaseTask |
| job_id | jobId | Optional[str] | BaseTask |
| task_code | taskCode | Optional[str] | BaseTask ("PU"/"PK"/"ST"/"CP") |
| planned_start_date | plannedStartDate | Optional[str] | BaseTask |
| target_start_date | targetStartDate | Optional[str] | BaseTask |
| actual_end_date | actualEndDate | Optional[str] | BaseTask |
| notes | notes | Optional[List[dict]] | BaseTask (JobTaskNote objects) |
| work_time_logs | workTimeLogs | Optional[List[dict]] | BaseTask (WorkTimeLog objects) |
| initial_note | initialNote | Optional[dict] | BaseTask (InitialNoteModel) |
| time_log | timeLog | Optional[dict] | BaseTask (TimeLog — PK/ST tasks) |
| created_date | createdDate | Optional[str] | TimestampedModel |
| modified_date | modifiedDate | Optional[str] | TimestampedModel |
| created_by | createdBy | Optional[str] | TimestampedModel |
| modified_by | modifiedBy | Optional[str] | TimestampedModel |

**PU-specific fields** (from InTheFieldTaskModel):

| Python field | JSON alias | Type |
|---|---|---|
| planned_end_date | plannedEndDate | Optional[str] |
| preferred_start_date | preferredStartDate | Optional[str] |
| preferred_end_date | preferredEndDate | Optional[str] |
| truck | truck | Optional[dict] |
| on_site_time_log | onSiteTimeLog | Optional[dict] |
| trip_time_log | tripTimeLog | Optional[str] |
| completed_date | completedDate | Optional[str] |

**CP-specific fields** (from CarrierTaskModel):

| Python field | JSON alias | Type |
|---|---|---|
| scheduled_date | scheduledDate | Optional[str] |
| pickup_completed_date | pickupCompletedDate | Optional[str] |
| delivery_completed_date | deliveryCompletedDate | Optional[str] |
| expected_delivery_date | expectedDeliveryDate | Optional[str] |

---

### TimelineResponse (Response Model — GET wrapper)

| Python field | JSON alias | Type |
|---|---|---|
| success | success | Optional[bool] |
| error_message | errorMessage | Optional[str] |
| tasks | tasks | Optional[List[TimelineTask]] |
| on_holds | onHolds | Optional[List[dict]] |
| days_per_sla | daysPerSla | Optional[int] |
| delivery_service_done_by | deliveryServiceDoneBy | Optional[str] |
| job_sub_management_status | jobSubManagementStatus | Optional[dict] |
| job_booked_date | jobBookedDate | Optional[str] |

---

### TimelineSaveResponse (Response Model — POST wrapper)

| Python field | JSON alias | Type |
|---|---|---|
| success | success | Optional[bool] |
| error_message | errorMessage | Optional[str] |
| task_exists | taskExists | Optional[bool] |
| task | task | Optional[TimelineTask] |
| email_log_id | emailLogId | Optional[int] |
| job_sub_management_status | jobSubManagementStatus | Optional[dict] |

---

### TimelineAgent (Response Model — existing, verify fields)

| Python field | JSON alias | Type | Source |
|---|---|---|---|
| id | id | Optional[Union[str, int]] | C# CompanyListItem.id |
| code | code | Optional[str] | C# CompanyListItem.code |
| name | name | Optional[str] | C# CompanyListItem.name |
| type_id | typeId | Optional[str] | C# CompanyListItem.typeId |

Note: Current Python model has `contactId`, `name`, `companyName` — likely wrong. The C# ground truth is `CompanyListItem` with `id`, `code`, `name`, `typeId`. Must verify against live API.

---

### ServiceBaseResponse (Response Model — DELETE response)

Already exists in SDK. Fields: `success`, `errorMessage`.

---

## State Transitions

Job statuses are driven by timeline task changes:

```
1 (New Job) → schedule() → 2 (Scheduled) → received() → 3 (Received)
    → pack_start() → 4 (Packaging Started) → pack_finish() → 5 (Packaging Completed)
    → storage_begin() → 6 (Storage)
    → carrier_schedule() → 7 (Carrier Scheduled) → carrier_pickup() → 8 (Carrier Pickup)
    → carrier_delivery() → 10 (Delivered)
```

Sub-statuses (2.1, 2.2, 9.1-9.4) are set automatically by the server.

## Relationships

- `TimelineResponse.tasks` → List of `TimelineTask`
- `TimelineResponse.jobSubManagementStatus` → `LookupItem` (id + name)
- `TimelineSaveResponse.task` → single `TimelineTask`
- `TimelineHelpers` uses `JobsEndpoint` methods for API calls
