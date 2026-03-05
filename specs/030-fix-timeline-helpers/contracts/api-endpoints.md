# API Contracts: 030 — Fix Timeline Helpers

## POST /job/{jobDisplayId}/timeline

**Existing route** — no new endpoints. This feature fixes the request model and helper construction for the existing timeline POST endpoint.

### Request (Polymorphic by taskCode)

The server uses `TaskModelDataBinder` to deserialize based on `taskCode`:

#### When taskCode = "PU" or "DE" → InTheFieldTaskRequest

```json
{
  "taskCode": "PU",
  "plannedStartDate": "2026-03-03T09:00:00",
  "plannedEndDate": "2026-03-03T17:00:00",
  "completedDate": "2026-03-03T14:30:00",
  "onSiteTimeLog": {
    "start": "2026-03-03T10:00:00",
    "end": "2026-03-03T14:30:00"
  },
  "tripTimeLog": {
    "start": "2026-03-03T09:00:00",
    "end": "2026-03-03T10:00:00"
  }
}
```

#### When taskCode = "PK" or "ST" → SimpleTaskRequest

```json
{
  "taskCode": "PK",
  "timeLog": {
    "start": "2026-03-03T11:00:00",
    "end": "2026-03-03T16:00:00"
  }
}
```

#### When taskCode = "CP" → CarrierTaskRequest

```json
{
  "taskCode": "CP",
  "scheduledDate": "2026-03-05T08:00:00",
  "pickupCompletedDate": "2026-03-05T10:00:00",
  "deliveryCompletedDate": "2026-03-06T14:00:00"
}
```

### Response → TimelineSaveResponse (existing, unchanged)

```json
{
  "success": true,
  "taskExists": false,
  "task": { "...task fields based on taskCode..." },
  "emailLogId": null,
  "jobSubManagementStatus": { "id": "...", "name": "4 - Packaging started" }
}
```

## Helper Method Signatures (Updated)

All helpers on `api.jobs.tasks`:

| Method | Task Code | Model | Key Fields Set |
|--------|-----------|-------|----------------|
| `schedule(job, start, end=None)` | PU | InTheFieldTaskRequest | plannedStartDate, plannedEndDate |
| `received(job, end=None, start=None)` | PU | InTheFieldTaskRequest | completedDate, onSiteTimeLog |
| `pack_start(job, start)` | PK | SimpleTaskRequest | timeLog.start |
| `pack_finish(job, end)` | PK | SimpleTaskRequest | timeLog.end |
| `storage_begin(job, start)` | ST | SimpleTaskRequest | timeLog.start |
| `storage_end(job, end)` | ST | SimpleTaskRequest | timeLog.end |
| `carrier_schedule(job, start)` | CP | CarrierTaskRequest | scheduledDate |
| `carrier_pickup(job, start)` | CP | CarrierTaskRequest | pickupCompletedDate |
| `carrier_delivery(job, end)` | CP | CarrierTaskRequest | deliveryCompletedDate |
