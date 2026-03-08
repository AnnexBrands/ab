# Tasks: Timeline Helper Upsert & Documentation

**Input**: Design documents from `/specs/031-timeline-upsert-docs/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Explicitly requested (FR-005, FR-006, FR-007). Integration test suite is a core deliverable (US2).

**Organization**: Tasks grouped by user story. User explicitly requested Sphinx docs before tests, so US3 (docs) is sequenced before US2 (tests) despite both being high priority.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Foundational (Blocking Prerequisites)

**Purpose**: Model extension and logging infrastructure that all user stories depend on

- [x] T001 Add `id: Optional[int] = Field(None, description="Server-assigned task ID (for upsert)")` and `modified_date: Optional[str] = Field(None, alias="modifiedDate", description="Optimistic concurrency token")` to `BaseTimelineTaskRequest` in `ab/api/models/jobs.py` (line ~858, before `task_code` field). Both fields Optional with None default — inherited by `InTheFieldTaskRequest`, `SimpleTaskRequest`, `CarrierTaskRequest` automatically.
- [x] T002 Add `import logging` and `logger = logging.getLogger(__name__)` at module top of `ab/api/helpers/timeline.py`. Add `from ab.api.models.jobs import TimelineSaveResponse` to the imports section (outside TYPE_CHECKING block since it's used at runtime for return type).
- [x] T003 Verify foundational changes: run `ruff check ab/api/models/jobs.py ab/api/helpers/timeline.py` and `pytest tests/models/test_timeline_models.py` — all must pass with no regressions.

**Checkpoint**: Model has upsert fields, logging is available. No behavior changes yet.

---

## Phase 2: User Story 1 — Upsert Existing Tasks (Priority: P1)

**Goal**: All 9 timeline helpers carry forward `id` and `modifiedDate` from existing server tasks into the POST payload. Status guards removed, replaced with `logger.warning()`. Return type is always `TimelineSaveResponse`.

**Independent Test**: Call any helper on a job with an existing task and verify the outgoing payload includes `id`/`modifiedDate`. Call on a job with no task and verify they are omitted.

### Implementation for User Story 1

- [x] T004 [US1] Update `set_task()` in `ab/api/helpers/timeline.py`: change return type from `Any` to `TimelineSaveResponse`. No logic changes — just the annotation (line ~68).
- [x] T005 [US1] Refactor `schedule()`/`_2` in `ab/api/helpers/timeline.py`: remove `if curr >= 2: return None` guard. Add `if curr >= 2: logger.warning("schedule() called at status %.1f (>= 2); proceeding", curr)`. After constructing `InTheFieldTaskRequest`, if `task` is not None, set `model.id = task.get("id")` and `model.modified_date = task.get("modifiedDate")`. Update return type to `TimelineSaveResponse`.
- [x] T006 [US1] Refactor `received()`/`_3` in `ab/api/helpers/timeline.py`: same pattern as T005 — remove `curr >= 3` guard, add warning, add upsert from existing task dict, update return type to `TimelineSaveResponse`.
- [x] T007 [US1] Refactor `pack_start()`/`_4` in `ab/api/helpers/timeline.py`: remove `curr >= 4` guard, add warning, add upsert from existing task dict, update return type to `TimelineSaveResponse`.
- [x] T008 [US1] Refactor `pack_finish()`/`_5` in `ab/api/helpers/timeline.py`: remove `curr >= 5` guard, add warning, add upsert from existing task dict, update return type to `TimelineSaveResponse`. Note: preserve existing `timeLog.start` merge logic.
- [x] T009 [US1] Refactor `storage_begin()`/`_6` in `ab/api/helpers/timeline.py`: no guard to remove (already allows update). Add upsert from existing task dict, update return type to `TimelineSaveResponse`. Preserve existing `timeLog.end` merge logic.
- [x] T010 [US1] Refactor `storage_end()` in `ab/api/helpers/timeline.py`: no guard to remove. Add upsert from existing task dict, update return type to `TimelineSaveResponse`. Preserve existing `timeLog.start` merge logic.
- [x] T011 [US1] Refactor `carrier_schedule()`/`_7` in `ab/api/helpers/timeline.py`: remove `curr >= 7` guard, add warning, add upsert from existing task dict, update return type to `TimelineSaveResponse`.
- [x] T012 [US1] Refactor `carrier_pickup()`/`_8` in `ab/api/helpers/timeline.py`: remove `curr >= 8` guard, add warning, add upsert from existing task dict, update return type to `TimelineSaveResponse`.
- [x] T013 [US1] Refactor `carrier_delivery()`/`_10` in `ab/api/helpers/timeline.py`: no guard to remove (already allows update). Add upsert from existing task dict, update return type to `TimelineSaveResponse`.
- [x] T014 [US1] Clean up unused imports in `ab/api/helpers/timeline.py`: remove `Any` from typing imports (no longer used). Verify `ruff check ab/api/helpers/timeline.py` passes.

**Checkpoint**: All 9 helpers upsert-aware. Existing tests still pass. `ruff` clean.

---

## Phase 3: User Story 3 — Sphinx Documentation (Priority: P2)

**Goal**: Jobs page in Sphinx docs has an intro with endpoint paths by tag, a Timelines section with workflow/concurrency writeup, and per-helper training content with model fields and code examples.

**Independent Test**: `cd docs && make html` builds without warnings. Jobs page has 9 helper subsections.

**Note**: User requested "update sphinx before writing the test" — docs provide reference material for test authoring.

### Implementation for User Story 3

- [x] T015 [US3] Add Jobs introductory overview and endpoint path table organized by tag (General, Timeline, Notes, Items, Freight, etc.) at the top of `docs/api/jobs.md`, before the existing Methods section. Reference existing endpoint methods from `JobsEndpoint`.
- [x] T016 [US3] Add "Timeline Helpers" top-level section in `docs/api/jobs.md` after the endpoint methods. Include: workflow explanation (status 1 → 2 → 3 → ... → 10 progression), `modifiedDate` optimistic concurrency explanation, task code taxonomy (PU=Pickup, PK=Packing, ST=Storage, CP=Carrier), and access pattern (`api.jobs.tasks.*`).
- [x] T017 [P] [US3] Add training subsection for `schedule()` (alias `_2`) in `docs/api/jobs.md`: describe `InTheFieldTaskRequest` fields populated (`task_code=PU`, `planned_start_date`), former guard (>= 2 now warns), and code example. Add training subsection for `received()` (alias `_3`): describe fields (`completed_date`, `on_site_time_log`), former guard (>= 3), and code example.
- [x] T018 [P] [US3] Add training subsections for `pack_start()` (alias `_4`) and `pack_finish()` (alias `_5`) in `docs/api/jobs.md`: describe `SimpleTaskRequest` fields (`time_log.start`, `time_log.end`), former guards (>= 4, >= 5), timeLog merge behavior, and code examples.
- [x] T019 [P] [US3] Add training subsections for `storage_begin()` (alias `_6`) and `storage_end()` (no alias) in `docs/api/jobs.md`: describe `SimpleTaskRequest` fields, no former guard (always allowed), timeLog preservation logic, and code examples.
- [x] T020 [P] [US3] Add training subsections for `carrier_schedule()` (alias `_7`), `carrier_pickup()` (alias `_8`), and `carrier_delivery()` (alias `_10`) in `docs/api/jobs.md`: describe `CarrierTaskRequest` fields (`scheduled_date`, `pickup_completed_date`, `delivery_completed_date`), former guards (>= 7, >= 8, none), and code examples.
- [x] T021 [US3] Run `cd docs && make html` and verify zero warnings related to Jobs/Timeline sections. Fix any broken cross-references.

**Checkpoint**: Sphinx docs build clean. Jobs page has intro, tag table, timeline writeup, and 9 helper subsections with examples.

---

## Phase 4: User Story 2 — Integration Test Suite (Priority: P1)

**Goal**: Dedicated test module exercises full create-update-verify sequence against staging API, including stale-write negative test.

**Independent Test**: `pytest tests/helpers/test_timeline_helpers.py -v` passes with 0 failures.

**Depends on**: US1 (helpers must have upsert logic). US3 docs provide reference.

### Implementation for User Story 2

- [x] T022 [US2] Create `tests/helpers/__init__.py` (empty) and `tests/helpers/test_timeline_helpers.py` with: class `TestTimelineHelperSequence`, `@pytest.mark.live` marker, `api` fixture (session-scoped `ABConnectAPI`), and imports from `tests.constants` (`TEST_JOB_DISPLAY_ID2`, `TEST_PK_START_DATE`, `TEST_PU_START_DATE`, `TEST_PU_END_DATE`, `TEST_PK_END_DATE`, `TEST_ST_START_DATE`, `TEST_ST_END_DATE`, `TEST_TR_SCHEDULED_DATE`, `TEST_TR_PICKUP_COMPLETED_DATE`, `TEST_TR_DELIVERY_COMPLETED_DATE`).
- [x] T023 [US2] Implement `test_step_00_delete_all` in `tests/helpers/test_timeline_helpers.py`: call `api.jobs.tasks.delete_all(TEST_JOB_DISPLAY_ID2)`, then verify `api.jobs.get_timeline(TEST_JOB_DISPLAY_ID2)` returns empty task list (or no tasks matching PU/PK/ST/CP codes).
- [x] T024 [US2] Implement `test_step_01_pack_start` in `tests/helpers/test_timeline_helpers.py`: call `api.jobs.tasks.pack_start(TEST_JOB_DISPLAY_ID2, start=TEST_PK_START_DATE)`, assert `resp.success is True`, then call `api.jobs.tasks.get_task(TEST_JOB_DISPLAY_ID2, "PK")` and verify task exists with `timeLog.start` matching `TEST_PK_START_DATE`.
- [x] T025 [US2] Implement `test_step_02_schedule` in `tests/helpers/test_timeline_helpers.py`: call `api.jobs.tasks.schedule(TEST_JOB_DISPLAY_ID2, start=TEST_PU_START_DATE)`, assert `resp.success is True` (despite status > 2 — helper should log warning and proceed), verify PU task has `plannedStartDate` matching `TEST_PU_START_DATE`.
- [x] T026 [US2] Implement `test_step_03_received_stale_fails` in `tests/helpers/test_timeline_helpers.py`: build a manual `InTheFieldTaskRequest` with `task_code="PU"`, `completed_date=TEST_PU_END_DATE` but WITHOUT `id` and `modifiedDate` from server. Call `api.jobs.tasks.set_task(TEST_JOB_DISPLAY_ID2, "PU", model)` directly. Server returns HTTP 409 (RequestError).
- [x] T027 [US2] Implement `test_step_04_received_fresh_succeeds` in `tests/helpers/test_timeline_helpers.py`: call `api.jobs.tasks.received(TEST_JOB_DISPLAY_ID2, end=TEST_PU_END_DATE)` (helper auto-fetches fresh id/modifiedDate). Assert `resp.success is True`. Verify PU task now has `completedDate` set.
- [x] T028 [US2] Implement `test_step_05_pack_finish` through `test_step_10_carrier_delivery` in `tests/helpers/test_timeline_helpers.py`: call each remaining helper in sequence (`pack_finish` with `TEST_PK_END_DATE`, `storage_begin` with `TEST_ST_START_DATE`, `storage_end` with `TEST_ST_END_DATE`, `carrier_schedule` with `TEST_TR_SCHEDULED_DATE`, `carrier_pickup` with `TEST_TR_PICKUP_COMPLETED_DATE`, `carrier_delivery` with `TEST_TR_DELIVERY_COMPLETED_DATE`). Assert `resp.success is True` for each.
- [x] T029 [US2] Implement `test_step_11_verify_final_state` in `tests/helpers/test_timeline_helpers.py`: call `api.jobs.get_timeline(TEST_JOB_DISPLAY_ID2)` and verify: PU task has completedDate, PK task has `timeLog.start`/`timeLog.end`, ST task has `timeLog.start`/`timeLog.end`, CP task has `deliveryCompletedDate`.
- [x] T030 [US2] Run `pytest tests/helpers/test_timeline_helpers.py -v` and verify all 12 tests pass with 0 failures.

**Checkpoint**: Full integration test suite passes against staging.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Validation across all stories, final cleanup

- [x] T031 Run full test suite `pytest` — verify no regressions across entire project (560 passed, 57 skipped, 5 xfailed)
- [x] T032 Run linter `ruff check .` — changed files clean; pre-existing errors in other files unchanged
- [x] T033 Run `cd docs && make html` — final Sphinx build verification (no new warnings)
- [x] T034 Validate quickstart.md code examples match actual API (spot-check 2-3 examples against staging)
- [x] T035 Checkpoint commit with all changes per Constitution Principle VIII

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Foundational)**: No dependencies — start immediately
- **Phase 2 (US1 - Upsert)**: Depends on Phase 1 (model fields + logging must exist)
- **Phase 3 (US3 - Docs)**: Depends on Phase 2 (docs describe the new helper behavior)
- **Phase 4 (US2 - Tests)**: Depends on Phase 2 (tests exercise the new helper behavior). User requested docs before tests.
- **Phase 5 (Polish)**: Depends on all prior phases

### User Story Dependencies

- **US1 (Upsert Logic)**: Depends on Foundational only — core code change
- **US3 (Sphinx Docs)**: Depends on US1 — documents the new behavior
- **US2 (Integration Tests)**: Depends on US1 — tests the new behavior. Sequenced after US3 per user request.

### Within Each User Story

- US1: `set_task()` type first → then helpers by task code group (PU → PK → ST → CP) → cleanup
- US3: Overview first → timeline section → per-helper subsections (T017-T020 parallelizable) → build verification
- US2: Scaffolding → sequential test steps (must execute in order against staging) → run verification

### Parallel Opportunities

- T017, T018, T019, T020 in Phase 3 (US3) can run in parallel — each writes to a different section of `docs/api/jobs.md` (but be careful of merge conflicts; safer to run sequentially in practice since same file)
- T001 and T002 in Phase 1 are in different files and can run in parallel

---

## Parallel Example: Phase 1

```text
# These touch different files and can run simultaneously:
Task T001: Add id/modified_date to BaseTimelineTaskRequest in ab/api/models/jobs.py
Task T002: Add logging + TimelineSaveResponse import in ab/api/helpers/timeline.py
```

## Parallel Example: Phase 3 (US3)

```text
# After T015-T016 complete (intro + timeline section), these subsections can be written in parallel:
Task T017: PU helpers training content (schedule, received)
Task T018: PK helpers training content (pack_start, pack_finish)
Task T019: ST helpers training content (storage_begin, storage_end)
Task T020: CP helpers training content (carrier_schedule, carrier_pickup, carrier_delivery)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Foundational (T001-T003)
2. Complete Phase 2: US1 Upsert Logic (T004-T014)
3. **STOP and VALIDATE**: Helpers now upsert correctly — test manually against staging
4. This alone fixes the core correctness bug

### Incremental Delivery

1. Phase 1 + Phase 2 → Upsert logic working (MVP)
2. Add Phase 3 (US3) → Docs available for training
3. Add Phase 4 (US2) → Automated test coverage
4. Phase 5 → Polish and commit

---

## Notes

- All helpers are in the same file (`ab/api/helpers/timeline.py`) — T005-T013 must be sequential
- Test steps (T023-T029) are sequential by design — each builds on the state left by the previous step
- Sphinx doc subsections (T017-T020) write to the same file — parallel in principle but serialize in practice
- The stale-write test (T026) calls `set_task()` directly to bypass the helper's auto-fetch — this is intentional to prove the concurrency check
