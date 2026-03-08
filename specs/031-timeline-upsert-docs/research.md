# Research: 031-timeline-upsert-docs

**Date**: 2026-03-07

## Decision 1: How to Carry `id` and `modifiedDate` Through to POST Payload

**Decision**: Add `id` and `modified_date` as Optional fields on `BaseTimelineTaskRequest`.

**Rationale**: Constitution Principle I (Pydantic Model Fidelity) requires all request fields to be validated through models. `RequestModel` uses `extra="forbid"`, so injecting extra dict keys after `model_dump()` would be inconsistent with the pattern. Adding them as Optional fields with `exclude_none=True` + `exclude_unset=True` (already used in `set_task()`) means they are omitted when not provided (create) and included when set (update).

**Alternatives considered**:
- **Dict merge after model_dump()**: Simpler but bypasses Pydantic validation and is inconsistent with `extra="forbid"` philosophy. Rejected.
- **Separate update endpoint (PATCH)**: The PATCH endpoint exists (`update_timeline_task`) but the helpers use POST for create-or-update. Adding a conditional PATCH path would double the code paths without benefit. Rejected.

## Decision 2: Logging Pattern for Status Guard Warnings

**Decision**: Use standard `logging.getLogger(__name__)` pattern, `logger.warning()` for guard conditions.

**Rationale**: 9+ modules in the `ab/` package already use this exact pattern (`base.py`, `http.py`, `client.py`, etc.). Neither `timeline.py` nor `agent.py` currently use logging, but the convention is established. `logger.warning()` (not `logger.warn()` which is deprecated) at the guard check point.

**Alternatives considered**:
- **Python `warnings` module**: Different mechanism, not used anywhere in the project. Rejected.
- **Custom exception with catch**: Over-engineered for an informational signal. Rejected.

## Decision 3: Helper Return Type

**Decision**: Change return type annotations from `Any | None` to `TimelineSaveResponse`. Remove `None` return paths since guards no longer short-circuit.

**Rationale**: `set_task()` calls `create_timeline_task()` which returns `TimelineSaveResponse`. The `Any` annotation was a carry-over from early development. With guards removed, every code path returns the server response. Per FR-011, server rejections are surfaced via `response.success == False`, not via `None`.

**Alternatives considered**:
- **Keep `Any`**: Loses type safety, IDE discoverability. Rejected.
- **Return `TimelineTask` (unwrapped)**: Would lose `success`, `errorMessage`, `taskExists` metadata needed for FR-011. Rejected.

## Decision 4: Test Location

**Decision**: Create `tests/helpers/test_timeline_helpers.py` as specified.

**Rationale**: The user explicitly requested "helper/timeline should have its own test suite." Existing test directories are `tests/models/`, `tests/unit/`, `tests/integration/`. A `tests/helpers/` directory parallels the source structure (`ab/api/helpers/`). These are integration tests hitting staging but are helper-specific, not endpoint-specific.

**Alternatives considered**:
- **`tests/integration/test_timeline_helpers.py`**: Valid structure but user specified `tests/helpers/`. Rejected.
- **`tests/unit/test_timeline_helpers.py`**: These are not unit tests (they hit staging). Rejected.

## Decision 5: Sphinx Documentation Structure

**Decision**: Expand `docs/api/jobs.md` to add a tagged section structure. Add a "Timeline Helpers" section with per-helper subsections after the existing endpoint methods.

**Rationale**: The existing `docs/api/jobs.md` lists endpoint methods directly. Adding a tag-based organization (General, Timeline, Notes, Items) with the timeline helpers documented inline follows the MyST markdown + `eval-rst` autodoc pattern already used. No new files needed.

**Alternatives considered**:
- **Separate `docs/api/timeline.md`**: Would fragment the Jobs page. Helpers are accessed via `api.jobs.tasks.*`, so they belong under Jobs. Rejected.
- **Autodoc only (no manual training content)**: Autodoc extracts docstrings but the user wants explicit training content with model fields and code examples beyond what docstrings provide. Rejected.
