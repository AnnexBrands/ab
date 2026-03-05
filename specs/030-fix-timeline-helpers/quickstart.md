# Quickstart: 030 — Fix Timeline Helpers

## Scenario 1: Set job as pickup scheduled (Status 2)

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

# Schedule pickup for a job
result = api.jobs.tasks.schedule(2000000, start="2026-03-03T09:00:00")
# Constructs InTheFieldTaskRequest(task_code="PU", planned_start_date="2026-03-03T09:00:00")

# With end date
result = api.jobs.tasks.schedule(2000000, start="2026-03-03T09:00:00", end="2026-03-03T17:00:00")
```

## Scenario 2: Set job as received (Status 3)

```python
# Mark pickup completed with on-site time logging
result = api.jobs.tasks.received(2000000, start="2026-03-03T10:00:00", end="2026-03-03T14:30:00")
# Constructs InTheFieldTaskRequest with completedDate and onSiteTimeLog

# Mark pickup completed without on-site time
result = api.jobs.tasks.received(2000000, end="2026-03-03T14:30:00")
```

## Scenario 3: Start packaging (Status 4)

```python
from datetime import datetime

start = datetime(2026, 3, 3, 11).isoformat()
result = api.jobs.tasks.pack_start(2000000, start)
# Constructs SimpleTaskRequest(task_code="PK", time_log=TimeLogRequest(start="2026-03-03T11:00:00"))
```

## Scenario 4: Carrier operations (Status 7/8/10)

```python
# Schedule carrier
result = api.jobs.tasks.carrier_schedule(2000000, start="2026-03-05T08:00:00")
# Constructs CarrierTaskRequest(task_code="CP", scheduled_date="2026-03-05T08:00:00")

# Mark carrier pickup
result = api.jobs.tasks.carrier_pickup(2000000, start="2026-03-05T10:00:00")

# Mark delivery
result = api.jobs.tasks.carrier_delivery(2000000, end="2026-03-06T14:00:00")
```

## Scenario 5: IDE autocomplete

```python
from ab import ABConnectAPI

api = ABConnectAPI()

# Typing api.jobs.tasks. shows all methods with full signatures:
# - schedule(job_id: int, start: str, end: str | None = None) -> Any | None
# - received(job_id: int, end: str | None = None, start: str | None = None) -> Any | None
# - pack_start(job_id: int, start: str) -> Any | None
# - pack_finish(job_id: int, end: str) -> Any | None
# - storage_begin(job_id: int, start: str) -> Any
# - storage_end(job_id: int, end: str) -> Any
# - carrier_schedule(job_id: int, start: str) -> Any | None
# - carrier_pickup(job_id: int, start: str) -> Any | None
# - carrier_delivery(job_id: int, end: str) -> Any

# Similarly, api.jobs.agent. shows:
# - oa(job, agent, ...) -> ServiceBaseResponse
# - da(job, agent, ...) -> ServiceBaseResponse
# - change(job, agent, ...) -> ServiceBaseResponse
```
