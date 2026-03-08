# Jobs

```{eval-rst}
.. autoclass:: ab.api.endpoints.jobs.JobsEndpoint
   :members:
   :undoc-members:
```

The Jobs endpoint handles two API surfaces: ACPortal and ABC.
Access it via `api.jobs` for direct endpoint methods, `api.jobs.tasks` for timeline helpers,
and `api.jobs.agent` for agent assignment helpers.

## Endpoint Paths by Tag

| Tag | Method | Path | Description |
|-----|--------|------|-------------|
| **General** | POST | `/job` | Create a new job |
| | PUT | `/job/save` | Save/update a job |
| | GET | `/job/{jobDisplayId}` | Get job by display ID |
| | GET | `/job/search` | Search jobs via query params |
| | POST | `/job/searchByDetails` | Search jobs by detail criteria |
| | GET | `/job/{jobDisplayId}/price` | Get job pricing |
| | GET | `/job/{jobDisplayId}/calendaritems` | Get calendar items |
| | GET | `/job/{jobDisplayId}/updatePageConfig` | Get update page config |
| | POST | `/job/update` (ABC) | Update a job |
| **Timeline** | GET | `/job/{jobDisplayId}/timeline` | Get all timeline tasks |
| | POST | `/job/{jobDisplayId}/timeline` | Create or update a timeline task |
| | GET | `/job/{jobDisplayId}/timeline/{taskId}` | Get a single timeline task |
| | PATCH | `/job/{jobDisplayId}/timeline/{taskId}` | Update a timeline task |
| | DELETE | `/job/{jobDisplayId}/timeline/{taskId}` | Delete a timeline task |
| | GET | `/job/{jobDisplayId}/timeline/{taskCode}/agent` | Get agent for task code |
| | POST | `/job/{jobDisplayId}/timeline/incrementjobstatus` | Increment job status |
| | POST | `/job/{jobDisplayId}/timeline/undoincrementjobstatus` | Undo status increment |
| **Notes** | GET | `/job/{jobDisplayId}/note` | List job notes |
| | POST | `/job/{jobDisplayId}/note` | Create a note |
| | PUT | `/job/{jobDisplayId}/note/{id}` | Update a note |
| **Items** | GET | `/job/{jobDisplayId}/items` | List job items |
| | POST | `/job/{jobDisplayId}/items` | Add items |
| | DELETE | `/job/{jobDisplayId}/items/{itemId}` | Delete an item |
| **Freight** | GET | `/job/{jobDisplayId}/freightproviders` | List freight providers |
| | POST | `/job/{jobDisplayId}/freightproviders/{idx}/ratequote` | Get rate quote |
| | POST | `/job/{jobDisplayId}/freightitems` | Add freight items |
| **Agent** | POST | `/job/{jobDisplayId}/changeAgent` | Change job agent |

## Methods

### create

`POST /job` (ACPortal) — Create a new job.

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")
api.jobs.create({"companyId": "...", "contactId": "..."})
```

### save

`PUT /job/save` (ACPortal) — Save/update a job.

```python
api.jobs.save({"id": "...", "status": "Active"})
```

### get

`GET /job/{jobDisplayId}` (ACPortal) — Get job by display ID.

**Returns:** {class}`~ab.api.models.jobs.Job`

```python
job = api.jobs.get(2000001)
```

### search

`GET /job/search` (ACPortal) — Search jobs via query params.

**Returns:** `list[`{class}`~ab.api.models.jobs.JobSearchResult`]`

```python
results = api.jobs.search(status="Active")
```

### search_by_details

`POST /job/searchByDetails` (ACPortal) — Search jobs by detail criteria.

**Returns:** `list[`{class}`~ab.api.models.jobs.JobSearchResult`]`

```python
results = api.jobs.search_by_details({"searchText": "test"})
```

### get_price

`GET /job/{jobDisplayId}/price` (ACPortal) — Get job pricing.

**Returns:** {class}`~ab.api.models.jobs.JobPrice`

```python
price = api.jobs.get_price(2000001)
```

### get_calendar_items

`GET /job/{jobDisplayId}/calendaritems` (ACPortal) — Get job calendar items.

**Returns:** `list[`{class}`~ab.api.models.jobs.CalendarItem`]`

```python
items = api.jobs.get_calendar_items(2000001)
```

### get_update_page_config

`GET /job/{jobDisplayId}/updatePageConfig` (ACPortal) — Get job update page config.

**Returns:** {class}`~ab.api.models.jobs.JobUpdatePageConfig`

```python
config = api.jobs.get_update_page_config(2000001)
```

### update

`POST /job/update` (ABC API) — Update a job via the ABC API surface.

```python
api.jobs.update({"jobId": "...", "status": "Completed"})
```

---

## Timeline Helpers

Access via `api.jobs.tasks.*`.

Timeline helpers provide a high-level workflow for advancing a job through
its lifecycle. Each helper fetches the current task state, carries forward
the server's `id` and `modifiedDate` for optimistic concurrency, and
POSTs the update.

### Workflow

A job progresses through these statuses:

```
Status 1 (Booked)
  -> Status 2 (Scheduled)     — schedule() / _2
  -> Status 3 (Received)      — received() / _3
  -> Status 4 (Pack Start)    — pack_start() / _4
  -> Status 5 (Pack Finish)   — pack_finish() / _5
  -> Status 6 (Storage)       — storage_begin() / _6, storage_end()
  -> Status 7 (Carrier Sched) — carrier_schedule() / _7
  -> Status 8 (Carrier PU)    — carrier_pickup() / _8
  -> Status 10 (Delivered)    — carrier_delivery() / _10
```

### Optimistic Concurrency (`modifiedDate`)

Every timeline task returned by the server includes a `modifiedDate` timestamp.
When a helper updates an existing task, it sends this timestamp back in the
POST payload. If another caller modified the task since you read it, the server
rejects the stale write with `success=False`. Check `response.success` after
every call.

### Task Codes

| Code | Name | Request Model | Description |
|------|------|---------------|-------------|
| `PU` | Pickup | {class}`~ab.api.models.jobs.InTheFieldTaskRequest` | Field operations (pickup/delivery) |
| `PK` | Packing | {class}`~ab.api.models.jobs.SimpleTaskRequest` | Packaging with time log |
| `ST` | Storage | {class}`~ab.api.models.jobs.SimpleTaskRequest` | Storage with time log |
| `CP` | Carrier | {class}`~ab.api.models.jobs.CarrierTaskRequest` | Carrier schedule/pickup/delivery |

### Delete Helpers

```python
# Delete a specific task by code
api.jobs.tasks.delete(job_id, "PK")

# Delete all tasks in reverse order (CP -> ST -> PK -> PU)
api.jobs.tasks.delete_all(job_id)
```

---

### schedule() / _2

**Status 2 — Scheduled.** Sets planned pickup dates on a PU task.

**Model:** {class}`~ab.api.models.jobs.InTheFieldTaskRequest`
**Fields populated:** `task_code="PU"`, `planned_start_date`, `planned_end_date` (optional)
**Warning:** Logs at status >= 2

```python
resp = api.jobs.tasks.schedule(job_id, start="2024-06-01T11:00:00Z")
# or with alias:
resp = api.jobs.tasks._2(job_id, start="2024-06-01T11:00:00Z")

assert resp.success
print(resp.task.id)  # server-assigned task ID
```

---

### received() / _3

**Status 3 — Received.** Marks pickup completed on a PU task.

**Model:** {class}`~ab.api.models.jobs.InTheFieldTaskRequest`
**Fields populated:** `task_code="PU"`, `completed_date`, `on_site_time_log` (if start provided)
**Warning:** Logs at status >= 3

```python
resp = api.jobs.tasks.received(job_id, end="2024-06-01T12:00:00Z")

# With on-site time tracking:
resp = api.jobs.tasks.received(
    job_id,
    start="2024-06-01T11:00:00Z",
    end="2024-06-01T12:00:00Z",
)
```

---

### pack_start() / _4

**Status 4 — Pack Start.** Sets packaging start time on a PK task.

**Model:** {class}`~ab.api.models.jobs.SimpleTaskRequest`
**Fields populated:** `task_code="PK"`, `time_log.start`
**Warning:** Logs at status >= 4

```python
resp = api.jobs.tasks.pack_start(job_id, start="2024-06-02T10:00:00Z")
```

---

### pack_finish() / _5

**Status 5 — Pack Finish.** Sets packaging end time on a PK task.
Preserves the existing `time_log.start` from a prior `pack_start()` call.

**Model:** {class}`~ab.api.models.jobs.SimpleTaskRequest`
**Fields populated:** `task_code="PK"`, `time_log.start` (preserved), `time_log.end`
**Warning:** Logs at status >= 5

```python
resp = api.jobs.tasks.pack_finish(job_id, end="2024-06-02T10:59:59Z")
```

---

### storage_begin() / _6

**Status 6 — Storage.** Sets storage start time on an ST task.
Preserves existing `time_log.end` if present.

**Model:** {class}`~ab.api.models.jobs.SimpleTaskRequest`
**Fields populated:** `task_code="ST"`, `time_log.start`, `time_log.end` (preserved)

```python
resp = api.jobs.tasks.storage_begin(job_id, start="2024-06-03T10:00:00Z")
```

---

### storage_end()

**Status 6 — Storage.** Sets storage end time on an ST task.
Preserves existing `time_log.start` if present. No numeric alias.

**Model:** {class}`~ab.api.models.jobs.SimpleTaskRequest`
**Fields populated:** `task_code="ST"`, `time_log.start` (preserved), `time_log.end`

```python
resp = api.jobs.tasks.storage_end(job_id, end="2024-06-03T10:59:59Z")
```

---

### carrier_schedule() / _7

**Status 7 — Carrier Scheduled.** Sets carrier scheduled date on a CP task.

**Model:** {class}`~ab.api.models.jobs.CarrierTaskRequest`
**Fields populated:** `task_code="CP"`, `scheduled_date`
**Warning:** Logs at status >= 7

```python
resp = api.jobs.tasks.carrier_schedule(job_id, start="2024-06-04T10:00:00Z")
```

---

### carrier_pickup() / _8

**Status 8 — Carrier Pickup.** Sets carrier pickup completed date on a CP task.

**Model:** {class}`~ab.api.models.jobs.CarrierTaskRequest`
**Fields populated:** `task_code="CP"`, `pickup_completed_date`
**Warning:** Logs at status >= 8

```python
resp = api.jobs.tasks.carrier_pickup(job_id, start="2024-06-04T10:59:59Z")
```

---

### carrier_delivery() / _10

**Status 10 — Delivered.** Sets carrier delivery completed date on a CP task.

**Model:** {class}`~ab.api.models.jobs.CarrierTaskRequest`
**Fields populated:** `task_code="CP"`, `delivery_completed_date`

```python
resp = api.jobs.tasks.carrier_delivery(job_id, end="2024-06-05T11:00:00Z")
```
