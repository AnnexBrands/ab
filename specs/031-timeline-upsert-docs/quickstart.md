# Quickstart: 031-timeline-upsert-docs

**Date**: 2026-03-07

## What Changes

1. **Timeline helpers now upsert** — When a task already exists, helpers carry the server's `id` and `modifiedDate` into the POST payload. The server uses `modifiedDate` as an optimistic concurrency token. If another caller modified the task since you read it, the server rejects your update (`success=False`).

2. **Status guards removed** — Helpers no longer return `None` when the job is at or past a certain status. They always proceed with the operation and log a warning if the old guard would have blocked.

3. **Return type is always `TimelineSaveResponse`** — Check `response.success` to determine if the operation succeeded.

## Usage Examples

### Create a new task (no existing task)

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")
resp = api.jobs.tasks.schedule(4000000, start="2024-06-01T11:00:00Z")
print(resp.success)  # True
print(resp.task.id)   # server-assigned ID
```

### Update an existing task (automatic upsert)

```python
# Second call to schedule() on same job — helper detects existing PU task,
# carries forward id + modifiedDate automatically
resp = api.jobs.tasks.schedule(4000000, start="2024-07-01T11:00:00Z")
print(resp.success)       # True (server accepted the update)
print(resp.task_exists)   # True (task already existed)
```

### Handle stale write rejection

```python
resp = api.jobs.tasks.received(4000000, end="2024-06-01T11:59:59Z")
if not resp.success:
    print(f"Update rejected: {resp.error_message}")
    # Re-fetch and retry if needed
```

### Full workflow sequence

```python
api = ABConnectAPI(env="staging")
job = 4000000

# Clean slate
api.jobs.tasks.delete_all(job)

# Step through timeline
api.jobs.tasks.pack_start(job, start="2024-06-02T10:00:00Z")
api.jobs.tasks.schedule(job, start="2024-06-01T11:00:00Z")
api.jobs.tasks.received(job, end="2024-06-01T11:59:59Z")
api.jobs.tasks.pack_finish(job, end="2024-06-02T10:59:59Z")
api.jobs.tasks.storage_begin(job, start="2024-06-03T10:00:00Z")
api.jobs.tasks.storage_end(job, end="2024-06-03T10:59:59Z")
api.jobs.tasks.carrier_schedule(job, start="2024-06-04T10:00:00Z")
api.jobs.tasks.carrier_pickup(job, start="2024-06-04T10:59:59Z")
api.jobs.tasks.carrier_delivery(job, end="2024-06-05T11:00:00Z")
```

## Running Tests

```bash
pytest tests/helpers/test_timeline_helpers.py -v
```

## Building Docs

```bash
cd docs && make html
# Open docs/_build/html/api/jobs.html — scroll to "Timeline Helpers"
```
