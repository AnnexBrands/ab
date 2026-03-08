# Implementation Plan: Timeline Helper Upsert & Documentation

**Branch**: `031-timeline-upsert-docs` | **Date**: 2026-03-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/031-timeline-upsert-docs/spec.md`

## Summary

Timeline helpers (`ab/api/helpers/timeline.py`) currently always create new request models without the server's `id` or `modifiedDate`, bypassing optimistic concurrency. This plan adds upsert support by extending `BaseTimelineTaskRequest` with optional `id`/`modified_date` fields, removes all status guards (replacing with `logger.warning()`), creates a dedicated integration test suite at `tests/helpers/test_timeline_helpers.py`, and adds Sphinx documentation with training content for each of the 9 helpers.

## Technical Context

**Language/Version**: Python 3.11+ (existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps -- no new dependencies)
**Storage**: N/A -- SDK, no local storage
**Testing**: pytest against staging API
**Target Platform**: Python SDK (pip-installable library)
**Project Type**: single
**Performance Goals**: N/A (SDK helpers -- no special targets)
**Constraints**: None beyond existing SDK patterns
**Scale/Scope**: 9 helpers to modify, 1 test module to create, 1 Sphinx doc page to expand

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | Adding `id`/`modified_date` to `BaseTimelineTaskRequest` follows mixin-free Optional field pattern with camelCase alias. `RequestModel` (`extra="forbid"`) enforced. |
| II. Example-Driven Fixture Capture | PASS | No new endpoints. Existing fixtures (`TimelineSaveResponse.json`, `TimelineResponse.json`) already captured. Tests hit staging directly. |
| III. Four-Way Harmony | PASS | Modifying implementation (helpers) + documentation (Sphinx). Examples unchanged. Test coverage added. All four artifacts aligned. |
| IV. Swagger-Informed, Reality-Validated | PASS | No swagger changes needed. POST /timeline already documented. |
| V. Endpoint Status Tracking | PASS | No new endpoints to track in FIXTURES.md. |
| VI. Documentation Completeness | PASS (after) | Sphinx docs for helpers are a core deliverable. Will satisfy principle. |
| VII. Flywheel Evolution | PASS | Standard development iteration. |
| VIII. Phase-Based Context Recovery | PASS | Work organized into commit-per-phase. |
| IX. Endpoint Input Validation | PASS | Request models already validated via Pydantic. New fields are Optional -- no validation regression. |

No violations. Complexity Tracking not needed.

## Post-Design Constitution Re-check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | `id: Optional[int]` and `modified_date: Optional[str]` with `alias="modifiedDate"` added to `BaseTimelineTaskRequest`. `exclude_none=True` + `exclude_unset=True` in `model_dump()` ensures clean serialization. |
| III. Four-Way Harmony | PASS | Implementation (helpers), tests (new suite), docs (Sphinx) all updated. Examples remain valid (helpers are called same way). |
| VI. Documentation Completeness | PASS | Each helper gets a subsection with alias, model fields, guard behavior, and code example. |

## Project Structure

### Documentation (this feature)

```text
specs/031-timeline-upsert-docs/
+-- plan.md              # This file
+-- spec.md              # Feature specification
+-- research.md          # Phase 0: technical decisions
+-- data-model.md        # Phase 1: model changes
+-- quickstart.md        # Phase 1: developer guide
+-- contracts/           # Phase 1: payload shape (no new API contracts)
+-- checklists/
|   +-- requirements.md  # Spec quality checklist
+-- tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
ab/api/
+-- models/
|   +-- jobs.py                    # MODIFY: add id/modified_date to BaseTimelineTaskRequest
+-- helpers/
    +-- timeline.py                # MODIFY: upsert logic, guard removal, logging, return types

tests/
+-- helpers/                       # CREATE directory
|   +-- __init__.py                # CREATE
|   +-- test_timeline_helpers.py   # CREATE: integration test suite
+-- constants.py                   # READ ONLY: test constants

docs/
+-- api/
    +-- jobs.md                    # MODIFY: add timeline helpers documentation
```

**Structure Decision**: Single project. All changes are within the existing `ab/` package, `tests/`, and `docs/` directories. One new subdirectory (`tests/helpers/`) for helper-specific integration tests.

## Implementation Phases

### Phase A: Model Extension (FR-003)

1. Add `id: Optional[int] = Field(None, description="Server-assigned task ID (for upsert)")` to `BaseTimelineTaskRequest`
2. Add `modified_date: Optional[str] = Field(None, alias="modifiedDate", description="Optimistic concurrency token")` to `BaseTimelineTaskRequest`
3. Verify `model_dump(by_alias=True, exclude_none=True, exclude_unset=True)` correctly excludes these when None/unset and includes when populated

**Exit gate**: Existing tests pass (`pytest tests/models/test_timeline_models.py`)

### Phase B: Helper Upsert Logic (FR-001, FR-002, FR-004, FR-011)

1. Add `import logging` and `logger = logging.getLogger(__name__)` to `timeline.py`
2. Import `TimelineSaveResponse` for return type annotations
3. For each of the 9 helpers:
   - Remove the `if curr >= N: return None` guard
   - Add `logger.warning("helper_name() called at status %.1f (>= N); proceeding", curr)` when guard condition would have triggered
   - After constructing the request model, if `task` (existing server task dict) is not None, set `model.id = task.get("id")` and `model.modified_date = task.get("modifiedDate")`
   - Pass model to `set_task()` as before
4. Update `set_task()` return type from `Any` to `TimelineSaveResponse`
5. Update all helper return types from `Any | None` to `TimelineSaveResponse`
6. Remove `None` return paths (guards no longer short-circuit)

**Exit gate**: `ruff check ab/api/helpers/timeline.py` passes, existing model tests pass

### Phase C: Sphinx Documentation (FR-008, FR-009, FR-010)

1. Expand `docs/api/jobs.md`:
   - Add introductory overview paragraph
   - Add endpoint path table organized by tag (General, Timeline, Notes, Items, Freight, etc.)
   - Add "Timeline Helpers" section with:
     - Workflow explanation (status 1 -> 10 progression)
     - `modifiedDate` concurrency explanation
     - Task code taxonomy (PU, PK, ST, CP)
   - Add per-helper subsection (9 total) each containing:
     - Helper name and alias (e.g., `schedule()` / `_2`)
     - Which request model it uses and key fields populated
     - Warning behavior (former guard threshold)
     - Code example

**Exit gate**: `cd docs && make html` builds without warnings

### Phase D: Integration Test Suite (FR-005, FR-006, FR-007)

1. Create `tests/helpers/__init__.py`
2. Create `tests/helpers/test_timeline_helpers.py` with ordered test sequence:
   - `test_step_00_delete_all` — Clean slate on `TEST_JOB_DISPLAY_ID2`
   - `test_step_01_pack_start` — Create PK task with `TEST_PK_START_DATE`, verify `get_task()`
   - `test_step_02_schedule` — Create PU task with `TEST_PU_START_DATE` (despite status > 2), verify `get_task()`
   - `test_step_03_received_stale_fails` — Call `received()` with stale/missing `modifiedDate`+`id`, assert `success=False`
   - `test_step_04_received_fresh_succeeds` — Call `received()` with fresh server object, assert `success=True`
   - `test_step_05_pack_finish` — Add `TEST_PK_END_DATE` to PK task
   - `test_step_06_storage_begin` — Add `TEST_ST_START_DATE` to ST task
   - `test_step_07_storage_end` — Add `TEST_ST_END_DATE` to ST task
   - `test_step_08_carrier_schedule` — Add `TEST_TR_SCHEDULED_DATE` to CP task
   - `test_step_09_carrier_pickup` — Add `TEST_TR_PICKUP_COMPLETED_DATE` to CP task
   - `test_step_10_carrier_delivery` — Add `TEST_TR_DELIVERY_COMPLETED_DATE` to CP task
   - `test_step_11_verify_final_state` — `get_timeline()` returns all tasks with expected dates
3. Use `@pytest.mark.live` and import all constants from `tests/constants.py`
4. Use `pytest.mark.dependency` or class-level ordering to ensure sequential execution

**Exit gate**: `pytest tests/helpers/test_timeline_helpers.py -v` passes with 0 failures

### Phase E: Cleanup & Commit

1. Run full test suite: `pytest`
2. Run linter: `ruff check .`
3. Verify Sphinx build: `cd docs && make html`
4. Checkpoint commit per Phase-Based Context Recovery (Principle VIII)

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Server does not actually enforce `modifiedDate` rejection | Test step 03 would pass unexpectedly | Investigate server source (`/src/ABConnect/`) for concurrency check logic; adjust test expectation if server is permissive |
| `TEST_JOB_DISPLAY_ID2` (4000000) unavailable on staging | All integration tests fail | Tests use `@pytest.mark.live` and can be skipped in CI; verify staging access before running |
| Adding `id` to `BaseTimelineTaskRequest` conflicts with Pydantic reserved names | Model construction error | Pydantic v2 allows `id` as a field name; verified in existing models (e.g., `TimelineTask.id`) |
