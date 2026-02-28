# PR Review: 019-refine-request-models

**Reviewer**: Independent architectural review
**Date**: 2026-02-28
**Branch**: `019-refine-request-models` (uncommitted, 46 files, +1898/−572 lines)
**Verdict**: **Conditional merge** — good directional work with real design flaws that should be fixed first

---

## Executive Summary

This branch replaces ~60 endpoint methods using `**kwargs: Any` or `data: dict | Any` with explicit typed signatures, adds `description` to all request model fields, creates 4 reusable mixins, and introduces a G6 quality gate for progress tracking. The tests pass (412 passed, 0 failures). The spec, plan, and task documentation are thorough.

**The good**: This is a genuine DX improvement. IDE autocomplete now works for endpoint calls. The G6 gate and description enforcement test are well-designed infrastructure. The mixin extraction (pagination, search, date range, sort) is sound.

**The bad**: The refactoring introduced three inconsistent patterns for the same problem, made everything Optional when the spec promised correct required/optional fields, and the `body = dict(all_none_values)` pattern is a code smell that duplicates model field definitions in the method signatures. A better engineer would have chosen one pattern and applied it uniformly.

---

## Critical Issues (Fix Before Merge)

### 1. Three inconsistent patterns for the same problem

The branch uses three different approaches for the same "accept request body" problem, with no clear rule for when to use which:

**Pattern A** — Inline kwargs, manual dict construction (used ~50 times):
```python
def insurance(self, *, start_date: str | None = None, end_date: str | None = None):
    body = dict(start_date=start_date, end_date=end_date)
    return self._request(_INSURANCE, json=body)
```

**Pattern B** — `data: ModelType | dict` passthrough (used ~15 times):
```python
def create(self, *, data: JobCreateRequest | dict) -> Any:
    return self._request(_CREATE, json=data)
```

**Pattern C** — `data: dict | None = None` untyped passthrough (used ~8 times):
```python
def merge_preview(self, merge_to_id: str, *, data: dict | None = None):
    return self._request(_MERGE_PREVIEW.bind(...), json=data)
```

The spec's data-model.md says Pattern A is for ≤8 fields, Pattern B for >8 fields. But the actual code doesn't follow this rule: `send_document_email` uses Pattern A with 6 fields while `save_grid_view_state` uses Pattern B with 3 conceptual fields (a `GridViewState` model). Pattern C (`data: dict | None`) gives the IDE *nothing* — it's `**kwargs` with a different name and is actually a regression from the spec's stated goal.

**Impact**: Developers must learn three calling conventions. The spec promised *one* — "IDE-guided endpoint calls."

**Recommendation**: Settle on exactly two patterns:
- Pattern B (`data: ModelType | dict`) for *all* body-accepting endpoints. This is simpler, consistent, and the model class provides all the IDE hints. The request model already exists — don't duplicate its fields in the method signature.
- Pattern A *only* where an endpoint takes 1–3 obvious scalar params (e.g., `source_id`, `amount`) and no model exists.

Pattern C should not exist. Either create a model or use Pattern B with `dict`.

### 2. Every field is Optional — spec requirement unfulfilled

The spec (FR-003, SC-003, User Story 2) explicitly requires:

> Required vs optional designation for each request model field MUST be validated against the ABConnect C# source code as ground truth.

The branch actually *removed* required fields. On `main`, there were 6 `Field(...)` (required) declarations. On this branch, there is 1. Specifically removed as required:
- `TimelineTaskCreateRequest.task_code` — C# `Task.TaskCode` is `string` (nullable in C#, but the server code calls `GetTaskTitleByCode(timelineTask.TaskCode)` — it will fail on null)
- `JobNoteCreateRequest.comments` and `.task_code` — demoted to Optional
- `ParcelItemCreateRequest.description` — demoted to Optional
- `ItemNotesRequest.notes` — demoted to Optional

The C# source for `Task.TaskCode` is `public string TaskCode { get; set; }` — yes, C# reference types are technically nullable, but the *controller code* immediately uses `TaskCode` without null checks (`GetTaskTitleByCode(timelineTask.TaskCode)`), meaning a null value would cause a server-side `NullReferenceException`. The SDK should catch this at the call site.

**Impact**: The SDK now lets through invalid requests that the old SDK would have caught. This is a correctness regression, directly contradicting the spec's User Story 2: "if the SDK demands a field, the API truly needs it."

**Recommendation**: Audit each demoted field against the C# controller code (not just the entity class). Fields that the controller uses without null checks should remain `Field(...)`.

### 3. `body = dict(...)` duplicates model field definitions

Every Pattern A method reconstructs the model's fields in the method signature AND in a `dict()` call:

```python
# In the endpoint method (jobs.py:475-487):
def create_note(self, job_display_id: int, *,
    comments: str | None = None,       # duplicated from JobNoteCreateRequest
    task_code: str | None = None,       # duplicated from JobNoteCreateRequest
    is_important: bool | None = None,   # duplicated from JobNoteCreateRequest
    send_notification: bool | None = None,  # duplicated from JobNoteCreateRequest
    due_date: str | None = None,        # duplicated from JobNoteCreateRequest
) -> JobNote:
    body = dict(comments=comments, task_code=task_code, is_important=is_important,
                 send_notification=send_notification, due_date=due_date)
    return self._request(_POST_NOTE.bind(jobDisplayId=job_display_id), json=body)
```

```python
# The model that already defines all of this (jobs.py model):
class JobNoteCreateRequest(RequestModel):
    comments: Optional[str] = Field(None, description="Note content (max 8000 chars)")
    task_code: Optional[str] = Field(None, alias="taskCode", ...)
    is_important: Optional[bool] = Field(None, alias="isImportant", ...)
    send_notification: Optional[bool] = Field(None, alias="sendNotification", ...)
    due_date: Optional[str] = Field(None, alias="dueDate", ...)
```

These are *literally the same field list* in two places. When the API adds a field, you must update both the model AND the endpoint method signature. This is the opposite of DRY.

**Impact**: Doubles the maintenance surface for every field addition. Violates the spec's own User Story 3 ("common patterns defined once").

**Recommendation**: Use Pattern B uniformly. The IDE will show fields when constructing the model: `JobNoteCreateRequest(comments="...", task_code="...")`. The endpoint signature becomes `def create_note(self, job_display_id: int, *, data: JobNoteCreateRequest | dict)`. One source of truth for fields.

---

## Significant Issues (Should Fix)

### 4. Dashboard endpoints pass body as JSON for what are conceptually query params

```python
def inbound(self, *, company_id: str | None = None) -> Any:
    """POST /dashboard/inbound.
    Params model: :class:`DashboardCompanyParams`   # <-- says "Params model"
    """
    return self._request(_INBOUND, json=dict(company_id=company_id))  # <-- sends as JSON body
```

The docstring says "Params model" but the code sends it as a JSON body. This is semantically wrong per HTTP conventions and creates confusion about what the server actually expects.

### 5. G6 gate auto-passes too aggressively

The G6 gate has 5 separate "auto-pass" conditions:
- No request/params model → auto-pass
- Route not found in file → auto-pass
- Method not found for route → auto-pass
- Model source not found → auto-pass
- Can't infer endpoint module → auto-pass (returns FAIL, but many paths auto-pass before reaching this)

With all these escapes, the gate reports 161/161 pass. This looks good but gives false confidence — it means the gate *cannot detect* the Pattern C endpoints (`data: dict | None`) since those don't have a `request_model` on the Route. The gate should at least flag endpoints where `**kwargs` or `data: dict` exist in the method signature regardless of whether a request model is declared.

### 6. Mixin composition creates diamond inheritance with overridden fields

```python
class JobSearchRequest(PaginatedRequestMixin, SearchableRequestMixin):
    # Override PaginatedRequestMixin.page → pageNo (API-specific alias)
    page: Optional[int] = Field(None, alias="pageNo", description="Page number (1-based)")
```

This inherits `page` from `PaginatedRequestMixin` and then immediately overrides it with a different alias. The purpose of the mixin was to provide a single definition of pagination — but if every consumer overrides the fields, the mixin isn't providing consistency, it's providing the illusion of it. A mixin that gets overridden at every use site is worse than no mixin, because it suggests uniformity where none exists.

Similarly, the `PaginatedRequestMixin` defines `page` with no default (Optional, None), but the old `JobSearchRequest` had `page_no: int = Field(1, ...)` — a required integer with default 1. The mixin made this optional with no default, which is a semantic change.

### 7. Breaking change for camelCase kwargs callers

Old behavior allowed:
```python
api.reports.insurance(startDate="2024-01-01", endDate="2024-12-31")
```

New behavior raises `TypeError: unexpected keyword argument 'startDate'` because the method signature uses snake_case (`start_date`). The spec says "Backwards compatibility is essential — existing callers passing dicts must continue to work." The `data: dict` pattern preserves this; Pattern A does not.

---

## Minor Issues

### 8. `from typing import Any` still imported in most endpoint files but only used for return types — not a problem but worth noting the branch didn't clean unused imports

### 9. Reports endpoint is 8 near-identical methods that could be a single generic method with a route parameter

```python
def insurance(self, *, start_date=None, end_date=None): ...
def sales(self, *, start_date=None, end_date=None, agent_code=None): ...
def sales_summary(self, *, start_date=None, end_date=None): ...
def sales_drilldown(self, *, start_date=None, end_date=None): ...
# ... 4 more with identical signatures
```

Each builds `body = dict(start_date=start_date, end_date=end_date)` and calls `self._request(ROUTE, json=body)`. With Pattern B, these would be one-liners.

### 10. Docstrings reference `:class:` Sphinx cross-references but the project doesn't appear to generate Sphinx docs from these, making them visual noise rather than functional documentation.

---

## What's Done Well

1. **G6 gate infrastructure** — The three sub-criteria (typed signature, descriptions, optionality markers) are well-designed and composable. The gate framework is extensible.

2. **Description enforcement test** — `test_request_descriptions.py` is simple, parametrized, and catches regressions automatically. Good pattern.

3. **DateRangeRequestMixin** — The reports models use this cleanly. It's the best example of mixin reuse in the branch.

4. **Keyword-only separator (`*`)** — All methods correctly use `*` to force keyword arguments, preventing positional argument confusion.

5. **Documentation volume** — The spec, plan, research, data-model, quickstart, contracts, and tasks documents are thorough and well-organized.

6. **Test suite passes** — 412 tests pass with no regressions. The existing request fixture validation continues to work.

---

## The Deeper Question: Is This the Right Approach?

The spec asks: "IDE hints for all inputs." There are two ways to achieve this:

### Approach A (this branch): Duplicate model fields into method signatures
```python
def create_note(self, job_display_id, *, comments=None, task_code=None, ...):
    body = dict(comments=comments, task_code=task_code, ...)
    self._request(ROUTE, json=body)
```
- IDE shows hints when calling the method
- But: fields defined twice, maintenance doubles, risk of drift

### Approach B (not explored): Pass the model directly
```python
def create_note(self, job_display_id, *, data: JobNoteCreateRequest | dict):
    self._request(ROUTE, json=data)
```
- IDE shows hints when constructing the model: `JobNoteCreateRequest(comments=..., task_code=...)`
- Fields defined once, in the model
- Callers do: `api.jobs.create_note(123, data=JobNoteCreateRequest(comments="hi"))`
- Or: `api.jobs.create_note(123, data={"comments": "hi"})`

Approach B is what the branch already uses for large models (`JobCreateRequest`, `CompanyDetails`). It works. It's simpler. It doesn't duplicate field definitions. It's what the requests library does, what boto3 does (with TypedDicts), and what every API client generator produces.

The argument for Approach A is "fewer keystrokes at the call site." But the cost is doubled maintenance surface, three inconsistent patterns, and the need for Pattern B anyway for large models. A better design would commit fully to one approach.

### The ideal design

```python
# Every body-accepting method:
def create_note(self, job_display_id: int, *, data: JobNoteCreateRequest | dict) -> JobNote:
    """POST /job/{jobDisplayId}/note.

    Request model: :class:`JobNoteCreateRequest`
    """
    return self._request(_POST_NOTE.bind(jobDisplayId=job_display_id), json=data)

# Every params-accepting method with explicit params:
def get_notes(self, job_display_id: int, *, category: str | None = None, task_code: str | None = None) -> list[JobNote]:
    """GET /job/{jobDisplayId}/note."""
    params = dict(category=category, task_code=task_code)
    return self._request(_GET_NOTES.bind(jobDisplayId=job_display_id), params=params)

# Methods with both body + params:
def create_timeline_task(self, job_display_id: int, *, data: TimelineTaskCreateRequest | dict, create_email: bool | None = None) -> TimelineTask:
    """POST /job/{jobDisplayId}/timeline."""
    params = dict(create_email=create_email)
    return self._request(_POST_TIMELINE.bind(jobDisplayId=job_display_id), json=data, params=params)
```

This gives you:
- One pattern for all body-accepting endpoints
- GET query params stay as explicit kwargs (they're few and belong on the URL, not in a model)
- `data: Model | dict` for POST/PUT/PATCH bodies
- Zero field duplication
- IDE hints work via model constructors
- `check()` in `_request` handles validation automatically

---

## Recommended Path

### Option 1: Fix critical issues, then merge (recommended)

1. **Standardize on Pattern B** for all POST/PUT/PATCH body endpoints. Remove Pattern A and Pattern C. This is a ~2 hour refactor that simplifies the code and eliminates the DRY violation.
2. **Restore required fields** that the C# controller code actually uses without null checks. Audit the 5 demoted fields.
3. **Fix dashboard** JSON body vs query params semantic mismatch.

Keep: G6 gate, description enforcement test, mixins, all model description additions, keyword-only separators.

### Option 2: Merge as-is with documented tech debt

If time pressure demands it, merge with an issue tracking:
- Standardize endpoint patterns in a follow-up
- Audit required fields against C# controllers (not just entity classes)
- Remove Pattern C endpoints

### Option 3: Rework

Start fresh with the uniform Pattern B approach described above. Would produce a cleaner, smaller diff (~800 lines instead of ~1900) with one consistent pattern.

---

## Verdict

**Conditional merge.** The directional improvement is real — descriptions, typed signatures, mixins, and G6 tracking are all valuable. But three competing patterns for the same problem, weakened field validation, and doubled field definitions are design-level issues that compound over time. Fix the critical issues (or at minimum document them as immediate follow-up tech debt) before merging to main.
