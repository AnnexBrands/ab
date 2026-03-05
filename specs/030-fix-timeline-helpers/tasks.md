# Tasks: Fix Timeline Helpers

**Input**: Design documents from `/specs/030-fix-timeline-helpers/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-endpoints.md, quickstart.md

**Tests**: Not explicitly requested. Existing test infrastructure (test_request_fixtures.py, gate regression) validates models and fixtures automatically.

**Organization**: Tasks grouped by user story. US4 (response model discriminated union) is **deferred** per D6 — existing unified `TimelineTask` with `extra="allow"` works correctly.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Exact file paths included in all descriptions

---

## Phase 1: Setup

**Purpose**: Branch verification and prerequisite fix

- [x] T001 Verify branch is `030-fix-timeline-helpers` and stage ChangeJobAgentRequest export fix already applied to ab/api/models/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Nested request models and base class that ALL per-type models depend on

**⚠️ CRITICAL**: US1 per-type models cannot be created until these exist

- [x] T002 Create nested request models (TimeLogRequest, TimeLogPauseRequest, WorkTimeLogRequest, InitialNoteRequest, TaskTruckInfoRequest) in ab/api/models/jobs.py — all extend RequestModel with `extra="forbid"`, field aliases match C# camelCase (see data-model.md)
- [x] T003 Create BaseTimelineTaskRequest abstract base class in ab/api/models/jobs.py — fields: task_code (str, required, alias taskCode), planned_start_date (Optional[str], alias plannedStartDate), work_time_logs (Optional[List[WorkTimeLogRequest]], alias workTimeLogs), initial_note (Optional[InitialNoteRequest], alias initialNote)

**Checkpoint**: Nested models and base class ready — per-type models can now be built

---

## Phase 3: User Story 1 — Per-Type Request Models (Priority: P1) 🎯 MVP

**Goal**: Replace broken `TimelineTaskCreateRequest` (4 generic fields) with three correct per-type request models matching C# `TaskModelDataBinder` polymorphic deserialization

**Independent Test**: Instantiate each model with valid fields — `extra="forbid"` rejects wrong fields. Run `test_request_fixtures.py` — all 3 new fixtures validate against their models.

### Implementation for User Story 1

- [x] T004 [US1] Create InTheFieldTaskRequest, SimpleTaskRequest, and CarrierTaskRequest in ab/api/models/jobs.py — each extends BaseTimelineTaskRequest with type-specific fields per data-model.md. Remove old TimelineTaskCreateRequest class.
- [x] T005 [US1] Update ab/api/models/__init__.py — export BaseTimelineTaskRequest, InTheFieldTaskRequest, SimpleTaskRequest, CarrierTaskRequest, TimeLogRequest, TimeLogPauseRequest, WorkTimeLogRequest, InitialNoteRequest, TaskTruckInfoRequest. Remove TimelineTaskCreateRequest export.
- [x] T006 [P] [US1] Remove `request_model="TimelineTaskCreateRequest"` from `_POST_TIMELINE` Route in ab/api/endpoints/jobs.py — validation moves to helper layer per D3 (same pattern as AgentHelpers)
- [x] T007 [P] [US1] Create InTheFieldTaskRequest.json request fixture in tests/fixtures/requests/ — PU task with plannedStartDate, onSiteTimeLog, completedDate per contracts/api-endpoints.md
- [x] T008 [P] [US1] Create SimpleTaskRequest.json request fixture in tests/fixtures/requests/ — PK task with timeLog.start per contracts/api-endpoints.md
- [x] T009 [P] [US1] Create CarrierTaskRequest.json request fixture in tests/fixtures/requests/ — CP task with scheduledDate, pickupCompletedDate, deliveryCompletedDate per contracts/api-endpoints.md
- [x] T010 [US1] Remove old TimelineTaskCreateRequest.json fixture from tests/fixtures/requests/

**Checkpoint**: All 3 per-type models exist, pass fixture validation, and `extra="forbid"` enforces correct fields per task type. The runtime crash (SC-001) is fixed at the model layer.

---

## Phase 4: User Story 2 — IDE Discoverability (Priority: P2)

**Goal**: IDE autocomplete shows all `TimelineHelpers` and `AgentHelpers` methods with full signatures when typing `api.jobs.tasks.` or `api.jobs.agent.`

**Independent Test**: Open VS Code with Pylance, type `api.jobs.tasks.` — autocomplete shows schedule, received, pack_start, pack_finish, storage_begin, storage_end, carrier_schedule, carrier_pickup, carrier_delivery with parameter names and types.

### Implementation for User Story 2

- [x] T011 [P] [US2] Add `TYPE_CHECKING` imports and type annotations `self.tasks: TimelineHelpers` and `self.agent: AgentHelpers` in JobsEndpoint.__init__() in ab/api/endpoints/jobs.py — use `from __future__ import annotations` or `if TYPE_CHECKING:` block per D4

**Checkpoint**: IDE resolves helper types, autocomplete works for both `tasks` and `agent` sub-APIs

---

## Phase 5: User Story 3 — Helper Rewrite (Priority: P3)

**Goal**: All timeline helper methods construct proper Pydantic model instances instead of raw dicts. Zero `_NEW_*_TASK` dict templates remain.

**Depends on**: US1 (per-type models must exist)

**Independent Test**: Read ab/api/helpers/timeline.py source — no raw dict construction (`{"taskCode": ...}`) remains. All payloads built via model instantiation (SC-007).

### Implementation for User Story 3

- [x] T012 [US3] Rewrite schedule() and received() helpers to construct InTheFieldTaskRequest instances in ab/api/helpers/timeline.py — schedule sets planned_start_date/planned_end_date, received sets completed_date and on_site_time_log via TimeLogRequest
- [x] T013 [P] [US3] Rewrite pack_start(), pack_finish(), storage_begin(), storage_end() helpers to construct SimpleTaskRequest instances in ab/api/helpers/timeline.py — each sets time_log via TimeLogRequest with start or end
- [x] T014 [P] [US3] Rewrite carrier_schedule(), carrier_pickup(), carrier_delivery() helpers to construct CarrierTaskRequest instances in ab/api/helpers/timeline.py — each sets scheduled_date, pickup_completed_date, or delivery_completed_date respectively
- [x] T015 [US3] Remove all _NEW_*_TASK dict templates, update set_task() to pass model instance to create_timeline_task() in ab/api/helpers/timeline.py, and update create_timeline_task() signature to accept `data: BaseTimelineTaskRequest | dict` in ab/api/endpoints/jobs.py

**Checkpoint**: All 9 helper methods construct model instances. `pack_start(job, start)` no longer crashes (SC-001, SC-002). Zero raw dict templates remain (SC-007).

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validation, gate regression, and progress tracking

- [x] T016 Run full test suite (`pytest`) and verify zero regressions (SC-005)
- [x] T017 Run gate regression (`pytest tests/test_gate_regression.py`) and update tests/gate_baseline.json
- [x] T018 Regenerate FIXTURES.md via progress report
- [x] T019 Validate quickstart scenarios from specs/030-fix-timeline-helpers/quickstart.md against source code

---

## Deferred: User Story 4 — Response Model Discrimination (Priority: P4)

**Status**: Deferred per D6. The existing unified `TimelineTask` response model with `extra="allow"` handles all task types correctly. No runtime errors or data loss. Splitting into per-type response models with a discriminated union would add complexity without benefit.

**Revisit when**: Consumers need type-narrowed response objects (e.g., `isinstance(task, InTheFieldTask)` instead of checking `task.task_code`).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational (nested models + base class)
- **US2 (Phase 4)**: Depends on Setup only — can run in PARALLEL with US1
- **US3 (Phase 5)**: Depends on US1 completion (models must exist for helpers to construct them)
- **Polish (Phase 6)**: Depends on US1 + US2 + US3 completion

### User Story Dependencies

- **US1 (P1)**: Depends on Phase 2 foundational models. No other story dependencies. **MVP**.
- **US2 (P2)**: Independent of US1 and US3. Can start after Phase 1.
- **US3 (P3)**: Depends on US1 (per-type models must exist). Cannot start until Phase 3 complete.
- **US4 (P4)**: Deferred — not in this release.

### Within Each User Story

- Models before exports (T004 → T005)
- Exports before fixtures can be validated (T005 → T007/T008/T009)
- Route fix (T006) is independent of model creation
- Helper rewrite (T012-T015) requires models from US1

### Parallel Opportunities

Within US1 (after T005 completes):
```
T006 (Route fix)     ─┐
T007 (ITF fixture)   ─┤── all parallel (different files)
T008 (Simple fixture) ─┤
T009 (Carrier fixture)─┘
```

US2 parallel with US1:
```
Phase 3 (US1 models) ──── runs concurrently with ──── Phase 4 (US2 annotations)
```

Within US3 (after T012):
```
T013 (PK/ST helpers) ─┐── parallel (same file but independent methods)
T014 (CP helpers)     ─┘
```

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Phase 1: Setup (verify branch, stage fix)
2. Complete Phase 2: Foundational (nested models, base class)
3. Complete Phase 3: US1 — per-type models, exports, fixtures
4. **STOP and VALIDATE**: Run `pytest tests/models/test_request_fixtures.py` — all 3 new fixtures pass
5. The runtime crash is fixed at the model layer even before helper rewrite

### Incremental Delivery

1. Setup + Foundational → model infrastructure ready
2. US1 (per-type models) → crash fixed, fixtures validated → **MVP complete**
3. US2 (IDE annotations) → developer experience improved (can ship independently)
4. US3 (helper rewrite) → architectural cleanup, model construction enforced
5. Polish → gate regression, FIXTURES.md, full validation

### Single Developer (Sequential)

1. Phase 1 → Phase 2 → Phase 3 (US1) → Phase 4 (US2) → Phase 5 (US3) → Phase 6
2. Each phase commits independently
3. Total: 19 tasks across 6 phases

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks in same phase
- [Story] label maps task to user story for traceability
- US4 (response model discrimination) deferred — existing `extra="allow"` works
- ChangeJobAgentRequest export fix (T001) is a carry-over from feature 029 session
- All models use `extra="forbid"` (RequestModel base) — this is the fix for the original crash
- Request fixture auto-discovery: `test_request_fixtures.py` matches JSON filename to model class name
- Gate ratchet: `test_gate_regression.py` ensures endpoint/gate count never decreases
