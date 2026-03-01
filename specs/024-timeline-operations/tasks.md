# Tasks: Timeline Operations

**Input**: Design documents from `/specs/024-timeline-operations/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Integration tests are included — the spec requires fixture validation, model fidelity tests, and delete/restore round-trip tests.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Create new files and directories needed for timeline work

- [X] T001 Create `ab/api/helpers/` package with `__init__.py`
- [X] T002 [P] Create `ab/api/helpers/timeline.py` skeleton with class stub and task code constants (PU, PK, ST, CP)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Fix response models and route definitions that ALL user stories depend on

**CRITICAL**: Timeline response shapes are currently wrong — GET returns a wrapper, not a bare list. POST returns a wrapper, not a bare task. These must be fixed before any fixture capture or helper work.

- [X] T003 Rewrite `TimelineTask` model in `ab/api/models/jobs.py` with all C# BaseTask + task-code-specific fields from data-model.md (unified model, not discriminated union)
- [X] T004 Add `TimelineResponse` model in `ab/api/models/jobs.py` — wrapper with `success`, `errorMessage`, `tasks`, `onHolds`, `daysPerSla`, `deliveryServiceDoneBy`, `jobSubManagementStatus`, `jobBookedDate`
- [X] T005 [P] Add `TimelineSaveResponse` model in `ab/api/models/jobs.py` — wrapper with `success`, `errorMessage`, `taskExists`, `task`, `emailLogId`, `jobSubManagementStatus`
- [X] T006 [P] Rewrite `TimelineAgent` model in `ab/api/models/jobs.py` to match C# CompanyListItem (`id`, `code`, `name`, `typeId`)
- [X] T007 Update model exports in `ab/api/models/__init__.py` for new/changed models
- [X] T008 Fix `_GET_TIMELINE` route in `ab/api/endpoints/jobs.py`: change `response_model` from `"List[TimelineTask]"` to `"TimelineResponse"`
- [X] T009 [P] Fix `_POST_TIMELINE` route in `ab/api/endpoints/jobs.py`: change `response_model` from `"TimelineTask"` to `"TimelineSaveResponse"`
- [X] T010 Add `get_timeline_response()` method on `JobsEndpoint` in `ab/api/endpoints/jobs.py` returning full `TimelineResponse`; update existing `get_timeline()` to extract and return just the tasks list for backward compatibility

**Checkpoint**: Routes and models are correct. Ready for live fixture capture.

---

## Phase 3: User Story 1 — Retrieve Timeline with Correct Models (Priority: P1) MVP

**Goal**: Call `get_timeline()` and get properly typed task objects with all task-code-specific fields and modified dates.

**Independent Test**: `get_timeline(TEST_JOB_DISPLAY_ID)` returns typed `TimelineTask` instances with zero `__pydantic_extra__` fields.

### Implementation for User Story 1

- [X] T011 [US1] Write `_scratch.py` to call `get_timeline_response(TEST_JOB_DISPLAY_ID)` and dump raw JSON to verify wrapper shape
- [X] T012 [US1] Verify `TimelineResponse` model validates the raw response with zero extra fields; fix any field mismatches
- [X] T013 [US1] Verify each task in the response validates as `TimelineTask` with zero extra fields; fix any field mismatches against live data
- [X] T014 [US1] Verify `TimelineAgent` model by calling `get_timeline_agent()` for each task code; fix field mismatches

**Checkpoint**: All timeline models validate cleanly against live API responses.

---

## Phase 4: User Story 2 — Capture Fixtures for Every Task Code (Priority: P1)

**Goal**: Save fixture JSON files for each timeline entity from live API responses.

**Independent Test**: Fixture files exist on disk and validate against their models with zero extra fields.

### Implementation for User Story 2

- [X] T015 [US2] Capture `TimelineTask.json` fixture — save first task from `get_timeline()` response (prefer PU task with populated fields)
- [X] T016 [P] [US2] Capture `TimelineAgent.json` fixture from `get_timeline_agent()` for a task code that has an assigned agent
- [X] T017 [P] [US2] Capture `TimelineResponse.json` fixture — full wrapper response from `get_timeline_response()`
- [X] T018 [P] [US2] Capture `TimelineSaveResponse.json` fixture — POST a task and save the response (or capture from mock if staging is destructive)

### Tests for User Story 2

- [X] T019 [US2] Update `tests/models/test_timeline_models.py` — add fixture validation tests for `TimelineTask`, `TimelineAgent`, `TimelineResponse`, `TimelineSaveResponse` with `assert_no_extra_fields`
- [X] T020 [US2] Add timeline integration tests in `tests/integration/test_jobs.py` — `test_get_timeline`, `test_get_timeline_response`, `test_get_timeline_agent`

**Checkpoint**: All fixtures captured, model tests pass, G1/G2 gates should pass.

---

## Phase 5: User Story 3 — Set Any Status Value Idempotently (Priority: P1)

**Goal**: TimelineHelpers class with get-then-set pattern for all status transitions.

**Independent Test**: Each status helper can advance a job from prerequisite status to target status.

### Implementation for User Story 3

- [X] T021 [US3] Implement `get_task(job_id, taskcode)` in `ab/api/helpers/timeline.py` — fetch timeline, extract task by code, return `(status_info, task_or_None)`
- [X] T022 [US3] Implement `set_task(job_id, taskcode, task, create_email=False)` in `ab/api/helpers/timeline.py` — POST task data via endpoint
- [X] T023 [US3] Implement `schedule()` / `_2()` helper — PU task with `plannedStartDate`, `plannedEndDate`
- [X] T024 [P] [US3] Implement `received()` / `_3()` helper — PU task with `completedDate`, `onSiteTimeLog` (with start/end time log rules from ABConnectTools)
- [X] T025 [P] [US3] Implement `pack_start()` / `_4()` and `pack_finish()` / `_5()` helpers — PK task with `timeLog.start` / `timeLog.end`
- [X] T026 [P] [US3] Implement `storage_begin()` / `_6()` and `storage_end()` helpers — ST task with `timeLog.start` / `timeLog.end`
- [X] T027 [P] [US3] Implement `carrier_schedule()` / `_7()`, `carrier_pickup()` / `_8()`, `carrier_delivery()` / `_10()` helpers — CP task fields
- [X] T028 [US3] Wire `TimelineHelpers` into `ABConnectAPI` — accessible as `api.timeline` or `api.jobs.timeline`
- [X] T029 [US3] Add status downgrade prevention — each helper checks current status via `get_task()` and returns None if job is already past target

### Tests for User Story 3

- [X] T030 [US3] Test `get_task()` returns correct task for each code and None for missing codes

**Checkpoint**: All 9 status helpers work with get-then-set pattern.

---

## Phase 6: User Story 4 — Delete and Restore Timeline Tasks (Priority: P2)

**Goal**: Delete individual or all tasks, recreate from fixtures.

**Independent Test**: Delete a task, verify gone, post it back from fixture, verify restored.

### Implementation for User Story 4

- [X] T032 [US4] Implement `delete(job_id, taskcode)` in `ab/api/helpers/timeline.py` — find task by code, call `delete_timeline_task()` with its ID
- [X] T033 [US4] Implement `delete_all(job_id)` in `ab/api/helpers/timeline.py` — delete all tasks in reverse order (CP, ST, PK, PU)

### Tests for User Story 4

- [X] T034 [US4] Test delete-and-restore round-trip: delete PU task → verify timeline has no PU → `set_task()` with PU fixture data → verify PU task exists again
- [X] T035 [US4] Test `delete_all()` resets job to status 1 — delete all tasks, verify empty timeline
- [X] T036 [US4] Test full status progression: `delete_all()` → `schedule()` → `received()` → `pack_start()` → `pack_finish()` → `carrier_schedule()` → `carrier_pickup()` → `carrier_delivery()` — verify status advances at each step

**Checkpoint**: Delete/restore works. Test isolation is possible.

---

## Phase 7: User Story 5 — Timeline Quality Gates Pass (Priority: P2)

**Goal**: All timeline endpoints pass G1-G6 quality gates.

**Independent Test**: Run progress report and verify timeline endpoints show PASS.

### Implementation for User Story 5

- [X] T036 [US5] Update `examples/timeline.py` with correct method signatures and fixture capture
- [X] T037 [US5] Regenerate FIXTURES.md and `progress.html` — verify timeline endpoints show all gates PASS
- [X] T038 [US5] Copy FIXTURES.md to `docs/FIXTURES.md`

**Checkpoint**: Timeline endpoints at full quality gate compliance.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup and integration

- [X] T039 Restore test job to known good state — run `delete_all()` then re-create tasks from fixtures to leave staging clean
- [X] T040 [P] Remove `_scratch.py` if present
- [X] T041 Run full test suite (`pytest tests/ -q`) — verify no regressions
- [X] T042 Commit, push, create PR

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 — BLOCKS all user stories
- **Phase 3 (US1)**: Depends on Phase 2 — live API validation of models
- **Phase 4 (US2)**: Depends on Phase 3 — needs correct models before capturing fixtures
- **Phase 5 (US3)**: Depends on Phase 2 — can start in parallel with US1/US2 if models are stable
- **Phase 6 (US4)**: Depends on Phase 5 — uses helpers from US3
- **Phase 7 (US5)**: Depends on Phases 4 + 5 — needs fixtures and tests complete
- **Phase 8 (Polish)**: Depends on all prior phases

### User Story Dependencies

- **US1 (P1)**: Foundational only — model validation against live API
- **US2 (P1)**: US1 — needs correct models before fixture capture
- **US3 (P1)**: Foundational — helpers use corrected routes/models
- **US4 (P2)**: US3 — delete/restore uses helper methods
- **US5 (P2)**: US2 + US3 — quality gates need fixtures + tests

### Within Each User Story

- Models before endpoints
- Endpoints before fixtures
- Fixtures before tests
- Tests before quality gates

### Parallel Opportunities

- T004/T005 (TimelineResponse/SaveResponse models) can run in parallel
- T005/T006 (SaveResponse/TimelineAgent) can run in parallel
- T008/T009 (route fixes) can run in parallel
- T015/T016/T017/T018 (fixture captures) can run in parallel
- T024/T025/T026/T027 (status helpers by task code) can run in parallel

---

## Parallel Example: User Story 3

```bash
# After get_task/set_task are done (T021-T022), all status helpers can run in parallel:
Task: "T024 - Implement received() / _3() helper"
Task: "T025 - Implement pack_start() / _4() and pack_finish() / _5()"
Task: "T026 - Implement storage_begin() / _6() and storage_end()"
Task: "T027 - Implement carrier helpers _7/_8/_10"
```

---

## Implementation Strategy

### MVP First (User Stories 1-2)

1. Complete Phase 1 + 2: Fix models and routes
2. Complete Phase 3: Verify models against live API
3. Complete Phase 4: Capture fixtures, pass G1/G2
4. **STOP and VALIDATE**: Models correct, fixtures captured, basic tests pass

### Full Delivery

5. Complete Phase 5: TimelineHelpers with all status transitions
6. Complete Phase 6: Delete/restore for test isolation
7. Complete Phase 7: Quality gates pass
8. Complete Phase 8: Clean up, PR

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Commit after each phase completion
- Always verify against live staging API — never fabricate fixtures
- The test job may need timeline tasks created before fixture capture — use `_scratch.py` for exploratory work
