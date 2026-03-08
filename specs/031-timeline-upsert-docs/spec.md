# Feature Specification: Timeline Helper Upsert & Documentation

**Feature Branch**: `031-timeline-upsert-docs`
**Created**: 2026-03-07
**Status**: Draft
**Input**: User description: "Update timeline helpers to upsert with modifiedDate concurrency, add integration test suite for multi-step sequences, and create Sphinx documentation with training content for each helper."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Upsert Existing Tasks Instead of Always Creating (Priority: P1)

A developer uses `api.jobs.tasks.schedule()` to set a pickup date on a job that already has a PU task. Today, the helper always builds a brand-new request model without the server-assigned `id` or `modifiedDate`, meaning the server cannot detect stale writes. The helper should detect the existing task from `get_task()`, carry forward `id` and `modifiedDate` into the outgoing POST payload, and let the server enforce optimistic concurrency.

**Why this priority**: Without `modifiedDate` pass-through, every helper call risks a silent overwrite or server-side rejection. This is a correctness bug that blocks reliable multi-step workflows.

**Independent Test**: Call `schedule()` on a job with an existing PU task and verify the outgoing payload contains `id` and `modifiedDate` from the server object. Confirm the server accepts the update and returns the updated task.

**Acceptance Scenarios**:

1. **Given** a job with an existing PU task (id=X, modifiedDate=T), **When** `schedule(job_id, start=...)` is called, **Then** the POST payload includes `id=X` and `modifiedDate=T`, and the server returns a `TimelineSaveResponse` with `success=True`.
2. **Given** a job with no existing PU task, **When** `schedule(job_id, start=...)` is called, **Then** the POST payload omits `id` and `modifiedDate`, and the server creates a new task.
3. **Given** a job with an existing PU task (modifiedDate=T), **When** a second caller already updated the task (modifiedDate is now T+1), **And** the first caller sends `modifiedDate=T`, **Then** the server rejects the stale write.

---

### User Story 2 - Integration Test Suite for Multi-Step Timeline Sequences (Priority: P1)

A developer needs confidence that the full timeline workflow operates correctly against the staging API. A dedicated test module (`tests/helpers/test_timeline_helpers.py`) exercises a realistic sequence: delete all tasks, create tasks step by step, verify state after each, and confirm that stale `modifiedDate` values cause failures while fresh values succeed.

**Why this priority**: The upsert logic (P1-US1) cannot be validated without end-to-end tests that exercise real server behavior with `modifiedDate` enforcement.

**Independent Test**: Run `pytest tests/helpers/test_timeline_helpers.py` against staging and verify all assertions pass including the stale-write rejection test.

**Acceptance Scenarios**:

1. **Given** `TEST_JOB_DISPLAY_ID2` (4000000), **When** `delete_all()` is called, **Then** all existing tasks are removed and `get_timeline()` returns an empty task list for all relevant codes.
2. **Given** a clean job, **When** `pack_start(job_id, TEST_PK_START_DATE)` is called, **Then** a PK task is created with `timeLog.start` matching `TEST_PK_START_DATE`, and `get_task()` confirms the task exists.
3. **Given** a job at status > 2, **When** `schedule(job_id, TEST_PU_START_DATE)` is called, **Then** a PU task is created with `plannedStartDate` set (the helper proceeds despite current status, logging a warning that the old guard would have blocked at status >= 2).
4. **Given** a freshly created PU task, **When** `received(job_id, end=TEST_PU_END_DATE)` is called with a stale/missing `modifiedDate` and `id`, **Then** the server rejects the request (non-success response or error).
5. **Given** the same PU task, **When** `received(job_id, end=TEST_PU_END_DATE)` is called with the latest server object's `modifiedDate` and `id`, **Then** the server accepts the update and the PU task reflects the completed date.
6. **Given** a fully populated timeline, **When** all date fields have been set (PK start/end, PU start/end/completed, ST start/end, CP scheduled/pickup/delivery), **Then** `get_timeline()` returns all tasks with expected date values matching the test constants.

---

### User Story 3 - Sphinx Documentation with Training Content (Priority: P2)

A developer clicks on the "Jobs" section in the Sphinx docs and sees an introductory overview followed by a list of endpoint paths organized by tag. Under the "Timelines" tag there is a brief writeup explaining the timeline workflow and the role of `modifiedDate`. Each helper method has training content showing the request model fields and a code example.

**Why this priority**: Documentation is essential for adoption but does not affect runtime correctness. The helpers must work correctly (P1) before they can be documented.

**Independent Test**: Build Sphinx docs (`make html` in `docs/`) and verify the Jobs page contains the Timelines section, each helper has a code example, and all model cross-references resolve without warnings.

**Acceptance Scenarios**:

1. **Given** the Sphinx docs site, **When** a user navigates to the Jobs page, **Then** they see an intro paragraph and a table/list of all endpoint paths grouped by tag (General, Timeline, Notes, Items, etc.).
2. **Given** the Jobs page, **When** a user clicks or scrolls to the Timelines section, **Then** they see a brief explanation of the timeline workflow, the role of `modifiedDate` in optimistic concurrency, and the task code taxonomy (PU, PK, ST, CP).
3. **Given** the Timelines section, **When** a user reads a specific helper (e.g., `schedule` / `_2`), **Then** they see the alias, the request model fields it populates, the status guard behavior, and a copy-pasteable code example.
4. **Given** all 9 helpers (`schedule`/`_2`, `received`/`_3`, `pack_start`/`_4`, `pack_finish`/`_5`, `storage_begin`/`_6`, `storage_end`, `carrier_schedule`/`_7`, `carrier_pickup`/`_8`, `carrier_delivery`/`_10`), **When** the docs are built, **Then** each helper has its own subsection with model reference and example.

---

### Edge Cases

- What happens when the server returns a task with `modifiedDate=null`? The helper should still send it (the server may accept null for tasks that have never been modified).
- What happens when `delete_all()` is called on a job that already has no tasks? It should return an empty list without errors.
- What happens when a helper is called with dates in a non-ISO format? The request model validation (Pydantic) should reject invalid input before the server call.
- What happens when two helpers race on the same task? The second call should fail server-side due to stale `modifiedDate`. The helper returns the `TimelineSaveResponse` as-is (with `success=False` and `errorMessage`); the caller checks `response.success`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: All timeline helpers (`schedule`, `received`, `pack_start`, `pack_finish`, `storage_begin`, `storage_end`, `carrier_schedule`, `carrier_pickup`, `carrier_delivery`) MUST include the server-assigned `id` and `modifiedDate` in the POST payload when updating an existing task.
- **FR-002**: When no existing task is found by `get_task()`, helpers MUST omit `id` and `modifiedDate` from the payload (create-new behavior).
- **FR-003**: The request model serialization path MUST support carrying `id` (int) and `modifiedDate` (string) fields through to the server payload for upsert operations.
- **FR-004**: ALL timeline helpers MUST remove their status guards and always proceed with the create/update operation regardless of current job status. When the operation would have been blocked by the old guard (e.g., `schedule()` called at status >= 2, `pack_start()` at status >= 4), the helper MUST emit a `logger.warn` indicating the status condition before proceeding.
- **FR-005**: A dedicated test module `tests/helpers/test_timeline_helpers.py` MUST exist with tests covering the full create-update-verify sequence described in User Story 2.
- **FR-006**: The test suite MUST include a negative test that proves stale `modifiedDate` values cause server rejection.
- **FR-007**: The test suite MUST use constants from `tests/constants.py` (`TEST_JOB_DISPLAY_ID2`, `TEST_PK_START_DATE`, `TEST_PU_START_DATE`, `TEST_PU_END_DATE`, etc.).
- **FR-008**: The Sphinx documentation for Jobs MUST include an introductory overview with endpoint paths organized by tag.
- **FR-009**: The Sphinx documentation MUST include a Timelines section under Jobs with a workflow explanation, `modifiedDate` concurrency explanation, and task code taxonomy.
- **FR-010**: Each timeline helper MUST have a documentation subsection with alias, request model fields, status guard behavior, and a code example.
- **FR-011**: When the server rejects an update (e.g., stale `modifiedDate`), helpers MUST return the `TimelineSaveResponse` as-is (with `success=False` and `errorMessage`). Helpers MUST NOT raise exceptions or return `None` for server-side rejections — the caller inspects `response.success`.

### Key Entities

- **TimelineTask**: Server-side task with `id`, `modifiedDate`, `taskCode`, and type-specific date fields. Returned by `get_timeline()` and `create_timeline_task()`.
- **BaseTimelineTaskRequest** (and subclasses: `InTheFieldTaskRequest`, `SimpleTaskRequest`, `CarrierTaskRequest`): Client-side request models for POST /timeline. The serialization path must optionally carry `id` and `modifiedDate` for upsert.
- **TimelineSaveResponse**: Wrapper returned by POST /timeline containing `success`, `taskExists`, `task` (with updated `modifiedDate`), and `jobSubManagementStatus`.
- **Test Constants**: `TEST_JOB_DISPLAY_ID2=4000000`, `TEST_PK_START_DATE="2024-06-02T10:00:00Z"`, `TEST_PU_START_DATE="2024-06-01T11:00:00Z"`, `TEST_PU_END_DATE="2024-06-01T11:59:59Z"`, etc. defined in `tests/constants.py`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 9 timeline helpers pass the upsert integration test -- existing tasks are updated with server `id`/`modifiedDate`, new tasks are created without them.
- **SC-002**: The stale-write negative test consistently fails at the server (non-success or error response) when given an outdated `modifiedDate`.
- **SC-003**: The full create-update-verify sequence test passes against staging with zero manual intervention.
- **SC-004**: `pytest tests/helpers/test_timeline_helpers.py` exits with 0 failures.
- **SC-005**: `make html` in `docs/` builds without warnings related to Jobs/Timelines sections.
- **SC-006**: The Jobs documentation page contains at least 9 helper subsections under the Timelines tag, each with a code example.

## Clarifications

### Session 2026-03-07

- Q: Should only `schedule()`'s status guard be relaxed, or all helpers? → A: Remove ALL status guards; helpers always proceed but emit `logger.warn` when the old guard condition would have blocked.
- Q: When the server rejects a stale `modifiedDate`, should the helper raise an exception, return None, or return the response as-is? → A: Return the `TimelineSaveResponse` as-is; caller checks `response.success`.

## Assumptions

- The staging API at `TEST_JOB_DISPLAY_ID2` (4000000) is available and writable for integration tests.
- The server enforces `modifiedDate` as an optimistic concurrency token -- sending a stale value returns a non-success response rather than silently overwriting.
- All status guards across helpers were intentionally conservative but are now removed; helpers always proceed and log a warning when the old guard condition is met.
- The POST /timeline endpoint accepts `id` and `modifiedDate` as top-level fields in the request body alongside `taskCode` and type-specific fields.
- Sphinx documentation follows the existing pattern in `docs/api/jobs.md` using MyST markdown with `eval-rst` blocks for autodoc.
