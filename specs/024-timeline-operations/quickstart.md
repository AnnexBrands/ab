# Quickstart: Timeline Operations

## Phase Execution Order

Follow the DISCOVER workflow. Each phase produces committed artifacts.

### Phase D — Determine (Research)

Already complete. See [research.md](research.md).

Key findings:
- GET /timeline returns `TimelineResponse` wrapper (not bare list)
- POST /timeline returns `TimelineSaveResponse` wrapper (not bare task)
- TimelineTask model needs all fields from C# BaseTask + task-code-specific fields
- TimelineAgent model needs correction (CompanyListItem shape, not contactId/companyName)
- Helpers follow get-then-set pattern from ABConnectTools

### Phase I — Implement Models

**Files to modify**:
- `ab/api/models/jobs.py` — Rewrite `TimelineTask`, `TimelineAgent`; add `TimelineResponse`, `TimelineSaveResponse`

**Steps**:
1. Rewrite `TimelineTask` with all C# BaseTask + task-code-specific fields (see data-model.md)
2. Rewrite `TimelineAgent` to match C# CompanyListItem (id, code, name, typeId)
3. Add `TimelineResponse` wrapper model
4. Add `TimelineSaveResponse` wrapper model
5. Update `__init__.py` exports

### Phase S — Scaffold Endpoints

**Files to modify**:
- `ab/api/endpoints/jobs.py` — Fix route response_models, add `get_timeline_response()` method

**Steps**:
1. Change `_GET_TIMELINE` response_model to `"TimelineResponse"`
2. Change `_POST_TIMELINE` response_model to `"TimelineSaveResponse"`
3. Add `get_timeline_response()` method returning `TimelineResponse`
4. Keep existing `get_timeline()` as convenience returning just the tasks list

### Phase C — Call & Capture

**Steps**:
1. Call GET /timeline for TEST_JOB_DISPLAY_ID — capture full `TimelineResponse`
2. Extract each task type (PU, PK, ST, CP) — save individual fixtures
3. Call GET /timeline/{taskCode}/agent for each code — capture `TimelineAgent`
4. Call POST /timeline with task data — capture `TimelineSaveResponse`
5. Verify all models validate with zero extra fields

### Phase O — Observe Tests

**Files to modify**:
- `tests/models/test_timeline_models.py` — Full model validation tests
- `tests/integration/test_jobs.py` — Timeline integration tests

**Steps**:
1. Add fixture validation tests for TimelineTask, TimelineAgent, TimelineResponse
2. Add integration tests for get/create/delete timeline operations
3. Run quality gates — verify G1-G6 pass for timeline endpoints
4. Update FIXTURES.md

### Timeline Helpers (new module)

**File to create**:
- `ab/api/helpers/timeline.py`

**Steps**:
1. Create `TimelineHelpers` class taking `JobsEndpoint` instance
2. Implement `get_task()`, `set_task()`, `delete()`, `delete_all()`
3. Implement status helpers: `schedule`, `received`, `pack_start`, `pack_finish`, `storage_begin`, `storage_end`, `carrier_schedule`, `carrier_pickup`, `carrier_delivery`
4. Add numeric aliases: `_2`, `_3`, `_4`, `_5`, `_6`, `_7`, `_8`, `_10`
5. Wire into `ABConnectAPI` as `api.jobs.timeline` or `api.timeline`
