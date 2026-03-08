# PR Analysis: Timeline Helper Upsert, Integration Tests, Sphinx Docs (#31)

**Branch**: `031-timeline-upsert-docs`
**Base**: `main`
**Date**: 2026-03-07
**Files changed**: 16 (+1308, -73)

---

## 1. Problem Statement

The timeline helpers (`ab/api/helpers/timeline.py`) had three correctness issues:

1. **Silent data loss on upsert.** Every helper created a fresh request model with only its own fields, then POSTed it. When updating an existing task this overwrote the entire server-side record, silently destroying fields set by prior operations or user input — preferred date ranges, carrier dates, work time logs, initial notes, etc. For example, calling `carrier_delivery()` after `carrier_schedule()` and `carrier_pickup()` wiped both `scheduledDate` and `pickupCompletedDate` from the CP task.

2. **Missing optimistic concurrency.** Helpers never sent the server's `id` or `modifiedDate` back in the POST payload. Without these the server could not detect concurrent modifications, and the POST for an existing task was rejected outright (HTTP 409) instead of performing an update.

3. **Status guards blocked legitimate re-entry.** Helpers returned `None` when the job was at or past their target status (e.g. `schedule()` returned `None` at status >= 2). This prevented re-scheduling or correcting data once a job advanced, with no logging to explain the silent no-op.

## 2. Solution Architecture

### 2.1 Deep-merge upsert (`_deep_merge` + `_upsert`)

The core fix replaces the "create new model, backfill two fields" pattern with "update the existing task":

```
Before (lossy):
  1. GET  existing task from server
  2. CREATE fresh model with only helper's fields
  3. COPY  id + modifiedDate onto the model          ← only 2 fields preserved
  4. POST  model → server overwrites entire task

After (preserving):
  1. GET  existing task dict from server
  2. CREATE model with only helper's fields
  3. DUMP  model to a minimal overlay dict            ← exclude_none, exclude_unset
  4. DEEP-MERGE overlay onto full server task dict    ← all prior data preserved
  5. POST  merged dict → server applies the update
```

The `_deep_merge(base, overlay)` function (line 40) recursively merges nested dicts. This is critical for `timeLog` — when `pack_finish()` sets only `timeLog.end`, the existing `timeLog.start` (and any `pauses`) survives the merge automatically. Scalars and lists in the overlay replace the base value; nested dicts are merged key-by-key.

When no existing task is found (`existing is None`), the model is sent as-is — the create path is unchanged.

### 2.2 Public vs internal write paths

| Method | Visibility | Merges existing? | Used by |
|--------|-----------|-----------------|---------|
| `set_task()` | Public | No — sends model as-is | External callers, stale-write test |
| `_upsert()` | Private | Yes — deep-merges onto existing task | All 9 helpers |

`set_task()` is preserved with its original signature for backward compatibility and for the stale-write test (which intentionally bypasses the merge to prove the server rejects a bare POST on an existing task).

### 2.3 Status guards → warnings

All six `if curr >= N: return None` guards are replaced with `logger.warning()`. The helpers always proceed. This is safe because:

- The server enforces its own status transition rules independently.
- The `modifiedDate` optimistic concurrency token (now always sent on upsert) protects against stale writes.
- The return type is always `TimelineSaveResponse` — callers check `resp.success`.

### 2.4 Model changes

Two fields added to `BaseTimelineTaskRequest` (line 859-860 of `jobs.py`):

```python
id: Optional[int] = Field(None, description="Server-assigned task ID (for upsert)")
modified_date: Optional[str] = Field(None, alias="modifiedDate", description="Optimistic concurrency token")
```

These are inherited by `InTheFieldTaskRequest`, `SimpleTaskRequest`, and `CarrierTaskRequest`. With `exclude_none=True` in serialization, they are omitted from the payload on create (when None) and included on upsert (when populated from the existing task dict via deep merge).

## 3. What the Deep Merge Preserves

The following table shows which fields survive across sequential helper calls. "Preserved" means the field's value from a prior operation is carried forward unchanged.

### PU task (InTheFieldTaskRequest)

| Field | Set by | Preserved through |
|-------|--------|-------------------|
| `plannedStartDate` | `schedule()` | `received()` ✓ |
| `plannedEndDate` | `schedule()` | `received()` ✓ |
| `preferredStartDate` | User/external | All PU helpers ✓ |
| `preferredEndDate` | User/external | All PU helpers ✓ |
| `completedDate` | `received()` | — (terminal) |
| `onSiteTimeLog` | `received()` | — (terminal) |
| `workTimeLogs` | User/external | All PU helpers ✓ |

### PK/ST tasks (SimpleTaskRequest)

| Field | Set by | Preserved through |
|-------|--------|-------------------|
| `timeLog.start` | `pack_start()` / `storage_begin()` | `pack_finish()` / `storage_end()` ✓ |
| `timeLog.end` | `pack_finish()` / `storage_end()` | `pack_start()` / `storage_begin()` ✓ |
| `timeLog.pauses` | User/external | All PK/ST helpers ✓ |
| `workTimeLogs` | User/external | All PK/ST helpers ✓ |

### CP task (CarrierTaskRequest)

| Field | Set by | Preserved through |
|-------|--------|-------------------|
| `scheduledDate` | `carrier_schedule()` | `carrier_pickup()` ✓, `carrier_delivery()` ✓ |
| `pickupCompletedDate` | `carrier_pickup()` | `carrier_delivery()` ✓ |
| `deliveryCompletedDate` | `carrier_delivery()` | — (terminal) |
| `expectedDeliveryDate` | User/external | All CP helpers ✓ |
| `workTimeLogs` | User/external | All CP helpers ✓ |

## 4. Code Simplification

The deep-merge approach eliminated manual field preservation code that was previously scattered across individual helpers:

| Helper | Before | After |
|--------|--------|-------|
| `pack_finish()` | 4 lines manually extracting `timeLog.start` from existing task, constructing `TimeLogRequest(start=existing_start, end=end)` | `TimeLogRequest(end=end)` — merge handles it |
| `storage_begin()` | 4 lines manually extracting `timeLog.end`, constructing `TimeLogRequest(start=start, end=existing_end)` | `TimeLogRequest(start=start)` — merge handles it |
| `storage_end()` | 4 lines manually extracting `timeLog.start`, constructing `TimeLogRequest(start=existing_start, end=end)` | `TimeLogRequest(end=end)` — merge handles it |

Each helper is now uniform: construct a model with only the fields it owns, then `self._upsert(job_id, model, task)`. The merge logic is centralized in one place (`_upsert` + `_deep_merge`).

## 5. Integration Test Suite

**File**: `tests/helpers/test_timeline_helpers.py` (205 lines, 12 tests)
**Marker**: `@pytest.mark.live` — runs against staging with `TEST_JOB_DISPLAY_ID2` (4000000).
**Fixture**: Session-scoped `api` from `conftest.py`.

### Test sequence

| Step | Test | Validates |
|------|------|-----------|
| 00 | `delete_all` | Clean slate — all 4 task codes removed |
| 01 | `pack_start` | Create PK task on clean job, verify `timeLog.start` |
| 02 | `schedule` | Create PU task despite status > 2 (warning logged), verify `plannedStartDate` |
| 03 | `received_stale_fails` | Direct `set_task()` without id/modifiedDate → HTTP 409 |
| 04 | `received_fresh_succeeds` | Helper auto-merges existing → success; **`plannedStartDate` preserved** |
| 05 | `pack_finish` | Upsert PK with end; **`timeLog.start` preserved** |
| 06 | `storage_begin` | Create ST task with start |
| 07 | `storage_end` | Upsert ST with end; **`timeLog.start` preserved** |
| 08 | `carrier_schedule` | Create CP task with scheduledDate |
| 09 | `carrier_pickup` | Upsert CP with pickupCompletedDate; **`scheduledDate` preserved** |
| 10 | `carrier_delivery` | Upsert CP with deliveryCompletedDate; **both prior dates preserved** |
| 11 | `verify_final_state` | All 4 tasks exist with all expected fields intact |

The stale-write test (step 03) is the concurrency proof: it calls `set_task()` (not `_upsert()`) to send a bare model without the server's `id`/`modifiedDate`. The server returns HTTP 409, confirming the optimistic concurrency check works.

The preservation assertions (bolded above) are the data-integrity proofs: each verifies that a subsequent helper did not destroy fields set by a prior helper.

## 6. Sphinx Documentation

**File**: `docs/api/jobs.md` (+228 lines)

### Additions

1. **Introductory overview** — describes the two API surfaces (ACPortal + ABC) and the three access patterns (`api.jobs`, `api.jobs.tasks`, `api.jobs.agent`).

2. **Endpoint path table** — 30+ routes organized by tag (General, Timeline, Notes, Items, Freight, Agent) with HTTP method, path, and description.

3. **Timeline Helpers section**:
   - Workflow diagram showing status 1 → 2 → ... → 10 progression with helper names and aliases.
   - Optimistic concurrency explanation (`modifiedDate` semantics, `response.success` checking).
   - Task code taxonomy table (PU, PK, ST, CP) with request model cross-references.
   - Delete helpers (`delete`, `delete_all`).

4. **Per-helper training subsections** (9 total): Each includes the status number, model class reference, fields populated, warning behavior, and a copy-pasteable code example. Uses `{class}` cross-references to Pydantic model docs.

## 7. Risk Assessment

### Low risk

- **Server ignores unknown POST fields.** The deep-merge sends the full server task dict (including read-only response fields like `createdDate`, `createdBy`) back in the POST. ASP.NET model binders ignore unknown properties by default. If a future server version rejects unknown fields, the fix is to filter the merged dict to known request-model aliases before sending.

- **No field-clearing semantics.** With `exclude_none=True`, a helper cannot explicitly clear a field to null. This is consistent with the helper design (forward progression only). Users who need to clear fields can use `set_task()` directly with a custom model, or call the raw endpoint.

### Mitigated

- **Status guards removed.** Server-side enforcement + `modifiedDate` concurrency token replaces client-side guards. The `logger.warning()` calls provide operational visibility.

- **TOCTOU window in get-then-set.** Inherent in optimistic concurrency — the `modifiedDate` token exists precisely to detect and reject stale writes during this window. The stale-write test proves this works.

## 8. Files Changed

| File | Change | Lines |
|------|--------|-------|
| `ab/api/helpers/timeline.py` | Core rewrite: `_deep_merge` + `_upsert`, guard→warning, return types | +166 -73 |
| `ab/api/models/jobs.py` | `id` + `modified_date` on `BaseTimelineTaskRequest` | +2 |
| `docs/api/jobs.md` | Endpoint table, timeline writeup, 9 helper subsections | +228 |
| `tests/helpers/test_timeline_helpers.py` | 12-step sequential integration test suite | +205 (new) |
| `tests/helpers/__init__.py` | Package init | +0 (new) |
| `tests/constants.py` | `TEST_JOB_DISPLAY_ID2` + 10 date constants | +11 |
| `CLAUDE.md` | Technology entry for feature 031 | +4 -2 |
| `specs/031-timeline-upsert-docs/*` | Spec, plan, research, data-model, contracts, tasks, quickstart, checklist | +578 (new) |

## 9. Test Results

```
tests/helpers/test_timeline_helpers.py    12 passed                   (5.13s)
full suite                               560 passed, 57 skipped, 5 xfailed (10.66s)
ruff check (changed files)               All checks passed
docs build (make html)                   0 new warnings
```
