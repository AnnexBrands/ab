# PR Analysis: 030 — Fix Timeline Helpers

**PR**: (pending) — `fix(sdk): timeline helpers — per-type request models, IDE discoverability (#30)`
**Branch**: `030-fix-timeline-helpers`
**Reviewed**: 2026-03-05
**Reviewer level**: Senior — with model architecture and helper pattern analysis

---

## Summary

This PR replaces the broken `TimelineTaskCreateRequest` (4 wrong fields) with three
per-type request models matching the C# server's polymorphic `TaskModelDataBinder`
deserialization: `InTheFieldTaskRequest` (PU/DE), `SimpleTaskRequest` (PK/ST), and
`CarrierTaskRequest` (CP). All timeline helpers are rewritten to construct Pydantic
model instances instead of raw dicts. Type annotations are added to `JobsEndpoint`
for IDE discoverability. The attribute is renamed from `self.timeline` to `self.tasks`
for consistency.

**Scope**: 3 new request models + 6 nested request models (replacing 1 broken model),
helper rewrite (9 methods), type annotations, 3 new request fixtures, 1 removed fixture.

**Tests**: 548 passed, 57 skipped, 5 xfailed, 0 failures. Gate regression passes.
Mock coverage passes. Baseline: 232 endpoints, 1194 passing gates (G6 gained for
changeAgent, G6 lost for timeline POST — net zero gate count change).

---

## Verdict

This is a high-quality bug fix that addresses a real runtime crash. The root cause
was clear: `TimelineTaskCreateRequest` declared 4 fields (`task_code`, `scheduled_date`,
`comments`, `agent_contact_id`) that didn't match what the helpers actually sent
(`timeLog`, `onSiteTimeLog`, `completedDate`, etc.). With `extra="forbid"`, any
helper call would crash with "Extra inputs are not permitted."

The fix is architecturally sound. Three per-type models mirror the C# server's
polymorphic dispatch exactly. The helpers construct validated model instances instead
of raw dicts. The `request_model` is correctly removed from the Route (D3) since
polymorphic dispatch happens in the helper layer, not `_request()`. This follows
the same pattern established by `AgentHelpers` in feature 029.

The code formatting cleanup in `jobs.py` (multi-line Route definitions and method
calls) is a welcome side effect — it improves readability without changing behavior.

---

## Issues

### 1. POSITIVE — Per-type models match C# ground truth exactly

The three request models (`InTheFieldTaskRequest`, `SimpleTaskRequest`,
`CarrierTaskRequest`) inherit from `BaseTimelineTaskRequest` and declare exactly
the fields their C# counterparts accept:

- `InTheFieldTaskRequest`: 7 task-specific fields (planned_end_date, preferred_start/end,
  truck, on_site_time_log, trip_time_log, completed_date) + 4 base fields
- `SimpleTaskRequest`: 1 task-specific field (time_log) + 4 base fields
- `CarrierTaskRequest`: 4 task-specific fields (scheduled_date, pickup/delivery/expected
  dates) + 4 base fields

All use `extra="forbid"` (inherited from `RequestModel`), so passing the wrong
field for a task type is caught at construction time — not silently ignored by the server.

### 2. POSITIVE — Nested models are correctly typed

Six nested request models (`TimeLogRequest`, `TimeLogPauseRequest`, `WorkTimeLogRequest`,
`InitialNoteRequest`, `TaskTruckInfoRequest`) all extend `RequestModel` with proper
field aliases matching C# DTOs. This ensures nested structures are validated too —
a typo in a nested field name is caught immediately.

### 3. POSITIVE — Helper rewrite eliminates all raw dict construction

All `_NEW_*_TASK` dict templates are removed. Every helper method now constructs the
correct model type:

| Helper | Old pattern | New pattern |
|--------|------------|-------------|
| `schedule()` | `_NEW_FIELD_TASK_SCH.copy()` + dict mutation | `InTheFieldTaskRequest(task_code=PU, ...)` |
| `received()` | `_NEW_FIELD_TASK.copy()` + dict mutation | `InTheFieldTaskRequest(task_code=PU, ...)` |
| `pack_start()` | `_NEW_PACK_TASK.copy()` + dict mutation | `SimpleTaskRequest(task_code=PK, ...)` |
| `pack_finish()` | `_NEW_PACK_TASK.copy()` + dict mutation | `SimpleTaskRequest(task_code=PK, ...)` |
| `storage_begin()` | `_NEW_STORE_TASK.copy()` + dict mutation | `SimpleTaskRequest(task_code=ST, ...)` |
| `storage_end()` | `_NEW_STORE_TASK.copy()` + dict mutation | `SimpleTaskRequest(task_code=ST, ...)` |
| `carrier_schedule()` | `_NEW_CARRIER_TASK.copy()` + dict mutation | `CarrierTaskRequest(task_code=CP, ...)` |
| `carrier_pickup()` | `_NEW_CARRIER_TASK.copy()` + dict mutation | `CarrierTaskRequest(task_code=CP, ...)` |
| `carrier_delivery()` | `_NEW_CARRIER_TASK.copy()` + dict mutation | `CarrierTaskRequest(task_code=CP, ...)` |

### 4. POSITIVE — IDE discoverability fixed

Type annotations added via `TYPE_CHECKING` imports:

```python
self.agent: AgentHelpers = _AgentHelpers(self, self._resolver)
self.tasks: TimelineHelpers = _TimelineHelpers(self)
```

The runtime imports use aliases (`_AgentHelpers`, `_TimelineHelpers`) to avoid
shadowing the `TYPE_CHECKING` imports. IDEs now resolve `api.jobs.tasks.` and
`api.jobs.agent.` with full method signatures.

### 5. POSITIVE — Attribute renamed from `timeline` to `tasks`

`self.timeline` is renamed to `self.tasks`, matching the user's reported usage
pattern (`api.jobs.tasks.pack_start(...)`). The integration test is updated to
use the new name.

### 6. OBSERVATION — `set_task()` serializes model before passing to endpoint

The `set_task()` method calls `model_dump(by_alias=True, exclude_none=True,
exclude_unset=True, mode="json")` and passes the resulting dict to
`create_timeline_task()`. This is correct — the endpoint method accepts
`BaseTimelineTaskRequest | dict`, and serialization at the helper boundary
means the endpoint doesn't need to know about model types.

The `exclude_unset=True` flag is particularly important: helpers only set the
fields they care about (e.g., `pack_start` sets `task_code` and `time_log`
only). Unset optional fields are excluded from the payload, which avoids
sending `null` values that could overwrite existing data on the server.

### 7. OBSERVATION — Gate baseline changes are net-zero

| Endpoint | Gate | Change | Reason |
|----------|------|--------|--------|
| `/job/{_}/changeAgent POST` | G6 | gained | `ChangeJobAgentRequest` export was missing in 029; fixed in `__init__.py` |
| `/job/{_}/timeline POST` | G6 | lost | `request_model` removed from Route (D3); G6 checks Route.request_model |

Net: +1 G6 gained, -1 G6 lost = 1194 total gates (unchanged from 029 baseline).
The timeline G6 loss is expected and documented in D3 — validation happens in the
helper layer, not the Route.

### 8. OBSERVATION — `ck.py` remains a stray scratch file

Same as 029 analysis. Must not be committed with this feature.

---

## Constitution & Plan Coherence

All 9 principles satisfied. Notable:

- **Principle I (Model Fidelity)**: Three per-type request models with `extra="forbid"`,
  field aliases matching C# DTOs exactly. Six nested models with proper typing.
- **Principle III (Four-Way Harmony)**: Three request fixtures (one per task type)
  validate against their models via `test_request_fixtures.py` auto-discovery.
- **Principle IX (Input Validation)**: This is the primary fix. Per-type models
  enforce correct fields per task code at construction time. The `extra="forbid"`
  that caused the original crash now works correctly because the models declare
  the right fields.

All 7 design decisions (D1-D7) from research.md are implemented as specified.

---

## Files Changed

### New Files (4)

| File | Purpose |
|------|---------|
| `tests/fixtures/requests/InTheFieldTaskRequest.json` | PU task request fixture |
| `tests/fixtures/requests/SimpleTaskRequest.json` | PK task request fixture |
| `tests/fixtures/requests/CarrierTaskRequest.json` | CP task request fixture |
| `specs/030-fix-timeline-helpers/pr-analysis.md` | This analysis |

### Modified Files (7)

| File | Change |
|------|--------|
| `ab/api/models/jobs.py` | Replace `TimelineTaskCreateRequest` with 3 per-type + 6 nested request models |
| `ab/api/models/__init__.py` | Export new models, remove old export, add `ChangeJobAgentRequest` fix |
| `ab/api/helpers/timeline.py` | Rewrite all 9 helpers to construct model instances; remove dict templates |
| `ab/api/endpoints/jobs.py` | Type annotations, remove `request_model` from Route, formatting cleanup |
| `tests/integration/test_jobs.py` | `timeline` -> `tasks` attribute rename |
| `tests/test_mock_coverage.py` | Add `_HELPER_REQUEST_FIXTURES` set for polymorphic models |
| `tests/gate_baseline.json` | G6 swap (changeAgent gained, timeline POST lost) |
| `FIXTURES.md` | Regenerated — timeline POST request model column now shows `--` |
| `CLAUDE.md` | Updated recent changes |

### Removed Files (1)

| File | Reason |
|------|--------|
| `tests/fixtures/requests/TimelineTaskCreateRequest.json` | Replaced by 3 per-type fixtures |

### Excluded

| File | Reason |
|------|--------|
| `ck.py` | Unrelated scratch file |

---

## Success Criteria Status

| Criterion | Target | Actual | Verdict |
|-----------|--------|--------|---------|
| SC-001 | `pack_start()` succeeds without Pydantic errors | Model constructs correctly; `extra="forbid"` passes | **PASS** |
| SC-002 | All 9 timeline helpers work | All 9 rewritten with correct models | **PASS** |
| SC-003 | IDE autocomplete for `api.jobs.tasks.*` | Type annotations via `TYPE_CHECKING` | **PASS** |
| SC-004 | IDE autocomplete for `api.jobs.agent.*` | Type annotations via `TYPE_CHECKING` | **PASS** |
| SC-005 | Zero test regressions | 548 passed, 0 failures | **PASS** |
| SC-006 | Request fixtures validate per type | 3 fixtures, auto-discovered by test harness | **PASS** |
| SC-007 | Zero raw dict templates remain | All `_NEW_*_TASK` dicts removed | **PASS** |
| SC-008 | Discriminated response model | Deferred (D6) — unified `TimelineTask` works | **DEFERRED** |

---

## Forward-Looking Recommendations

### R1. LOW — Consider adding `InitialNoteRequest` and `TaskTruckInfoRequest` to helper signatures

The current helpers don't expose `initial_note` or `truck` parameters. These are
valid fields on `InTheFieldTaskRequest` but aren't used by any convenience method.
A future feature could add `schedule(job, start, end, note=...)` or accept `**kwargs`
that are forwarded to the model constructor.

### R2. LOW — Response model enrichment (SC-008)

The unified `TimelineTask` with `extra="allow"` works but loses type safety on
task-specific response fields. A future feature could add discriminated response
models (matching ABConnectTools' pattern) if consumers need typed access to
`time_log` vs `on_site_time_log` on response objects.
