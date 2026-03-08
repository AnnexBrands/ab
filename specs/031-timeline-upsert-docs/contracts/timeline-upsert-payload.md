# Contract: Timeline Upsert Payload

**Endpoint**: `POST /job/{jobDisplayId}/timeline`
**Change**: Existing endpoint, no new routes. Payload shape extended with optional upsert fields.

## Create (new task — no existing task)

```json
{
  "taskCode": "PU",
  "plannedStartDate": "2024-06-01T11:00:00Z"
}
```

`id` and `modifiedDate` are **omitted** (excluded by `exclude_none`).

## Update (existing task — upsert)

```json
{
  "taskCode": "PU",
  "id": 612643,
  "modifiedDate": "2026-02-28 20:26:04.310000",
  "plannedStartDate": "2024-07-01T11:00:00Z"
}
```

`id` and `modifiedDate` are **included** from the server's last-known task state. Server validates `modifiedDate` for optimistic concurrency.

## Server Response (unchanged)

```json
{
  "success": true,
  "errorMessage": null,
  "taskExists": false,
  "task": {
    "id": 612643,
    "modifiedDate": "2026-03-07 15:00:00.000000",
    "taskCode": "PU",
    "plannedStartDate": "2024-07-01T11:00:00Z"
  },
  "emailLogId": null,
  "jobSubManagementStatus": {
    "id": "9736bc14-cf49-4181-926e-2501312fec3f",
    "name": "2 - Scheduled"
  }
}
```

## Stale Write Rejection (expected)

When `modifiedDate` does not match server's current value:

```json
{
  "success": false,
  "errorMessage": "The record has been modified by another user...",
  "taskExists": true,
  "task": null,
  "emailLogId": null,
  "jobSubManagementStatus": null
}
```
