# PR Analysis: 020 — Uniform Endpoint Pattern

**PR**: #20 — `feat(sdk): standardize all body-accepting endpoints on uniform data pattern`
**Branch**: `020-uniform-endpoint-pattern`
**Reviewed**: 2026-02-28
**Reviewer level**: Senior

---

## Summary

This PR standardizes ~75 body-accepting SDK endpoint methods from three
competing calling conventions (Pattern A: inline kwargs→`dict()`, Pattern B:
`data: Model | dict`, Pattern C: `data: dict | None`) onto a single
Pattern B interface.  It also creates 7 new request models, restores 5
incorrectly-demoted required fields, fixes ~75 broken example lambdas, and
converts 5 dashboard POST routes from `params_model` to `request_model`.

**Tests**: 416 passed, 70 skipped, 5 xfailed.  No regressions.

---

## Verdict

The PR accomplishes its stated goal and the mechanical transformation is
applied consistently across the vast majority of endpoints.  The direction is
correct.  However, a senior reviewer would flag several issues — two of which
are real defects (incomplete conversion), and the rest are design/sustainability
concerns that should at minimum be tracked.

---

## Issues

### 1. DEFECT — Two endpoints still use `data: dict` (Pattern C survives)

**Files**: `ab/api/endpoints/companies.py:242`, `companies.py:257`

```python
def save_packaging_settings(self, company_id: str, *, data: dict) -> Any:
def save_packaging_labor(self, company_id: str, *, data: dict) -> Any:
```

The PR description claims "grep `data: dict | None` → 0 hits", but the
actual residual pattern is `data: dict` (without `| None`), so the grep
check passes while two methods remain untyped.  SC-002 is met on a technicality
(`dict | None` is gone) but the spirit of FR-001 and FR-003 — every
body-accepting method takes `data: ModelType | dict` — is violated.

**Fix**: Create `PackagingSettingsSaveRequest` and `PackagingLaborSaveRequest`
placeholder models (matching the approach used for the other 7 new models),
add `request_model` to the Route definitions, and update the signatures.

**Why a senior catches this**: A senior reviews the success criteria against
the *intent*, not just the literal grep regex.  They'd also run
`grep "data: dict" endpoints/` (without `| None`) as a second pass.

---

### 2. DEFECT — `GeoSettingsParams` and `InheritFromParams` removed from TYPE_CHECKING import but still referenced by Routes

**File**: `ab/api/endpoints/companies.py`

The diff removes `GeoSettingsParams` and `InheritFromParams` from the
`TYPE_CHECKING` import block.  These models are still referenced by Route
definitions via string (`params_model="GeoSettingsParams"`) so they resolve
at runtime — meaning this doesn't cause a crash.  However, removing them from
the import block is a false cleanup: it suggests these models are no longer
needed by the file, when they still are (just indirectly).

**Severity**: Low (no runtime impact).  A linter with stricter import
analysis could flag it in the future, and it makes the import block less
self-documenting.

**Why a senior catches this**: Seniors check that import removals match
actual usage removals.  Here the models were removed from the
*keyword-argument signature* (since `save_carrier_accounts` was refactored)
but their Route-level string references remain.

---

### 3. DESIGN — Placeholder models are barely more typed than raw `dict`

Seven new models were created for former Pattern C endpoints:

| Model | Fields |
|---|---|
| `OnHoldCommentRequest` | `comment: Optional[str]` |
| `ResolveOnHoldRequest` | `resolution_notes: Optional[str]` |
| `SendEmailRequest` | 5x `Optional[...]` |
| `RateQuoteRequest` | `options: Optional[dict]` |
| `FreightItemsRequest` | `items: Optional[List[dict]]` |
| `ContactHistoryCreateRequest` | `statuses: Optional[str]` |
| `ContactMergeRequest` | `merge_from_id: Optional[str]` |

Every field on every model is `Optional` with a `None` default.  A caller can
pass `SendEmailRequest()` with zero fields and send an empty JSON body to the
server, which will likely return a 400.

Worse, `RateQuoteRequest.options` is `Optional[dict]` and
`FreightItemsRequest.items` is `Optional[List[dict]]` — these provide no
more type information than the `data: dict` they replaced.

**What a senior would do**: At minimum, add a `# TODO: refine from API docs`
comment to flag these as known-weak.  Ideally, mark at least one field per
model as required (e.g., `SendEmailRequest.to` should be required — you can't
send an email without recipients).  For `RateQuoteRequest.options`, define
a nested model or at least use `dict[str, Any]` with a docstring describing
the expected shape.

**Why a senior catches this**: A senior evaluates whether the
*abstraction actually adds safety*.  If the model can't reject any invalid
input, it's ceremony without value.  `extra="forbid"` on RequestModel at least
catches typo keys, so there is *some* value — but it's marginal.

---

### 4. DESIGN — `DashboardCompanyParams` used as a request body model

The five dashboard POST routes were changed from:
```python
_INBOUND = Route("POST", "/dashboard/inbound", params_model="DashboardCompanyParams")
```
to:
```python
_INBOUND = Route("POST", "/dashboard/inbound", request_model="DashboardCompanyParams")
```

This is semantically correct — the old code was using `json=dict(...)` despite
the Route declaring `params_model`, so the params validation was never
running.  The fix to use `request_model` actually *enables* validation that was
previously silently skipped.

However, the model is still named `DashboardCompanyParams`, which follows the
`*Params` naming convention used for query parameters throughout the codebase.
Using a `*Params` model as a `request_model` (JSON body) violates the naming
convention established elsewhere:

- `*Params` → query parameters (used with `params=`)
- `*Request` → request body (used with `json=`)

**What a senior would do**: Either rename to `DashboardCompanyRequest` or
add a comment explaining the exception.  The underlying model class is the same
(`RequestModel`), so technically it works, but naming conventions exist for
humans scanning the code.

---

### 5. DESIGN — Breaking change without migration guidance

This PR changes the public API for ~75 methods.  Any consumer calling:
```python
api.commodities.create(description="foo", freight_class="50")
```
must now call:
```python
api.commodities.create(data={"description": "foo", "freight_class": "50"})
# or
api.commodities.create(data=CommodityCreateRequest(description="foo", freight_class="50"))
```

The PR description and spec make no mention of:
- A major/minor version bump
- A CHANGELOG entry
- A migration guide for existing consumers
- Deprecation warnings (as an alternative to a hard break)

**What a senior would do**: At minimum, document the breaking change in a
CHANGELOG.  Ideally, for an SDK with external consumers, either bump the major
version or provide a one-release deprecation cycle where both old and new
calling conventions work (via an `*args` adapter).

If the SDK is internal-only with few consumers, a hard break is acceptable but
should still be documented.

---

### 6. RISK — No runtime guard against `data=None`

The type annotation is `data: ModelType | dict`, but nothing prevents a caller
from passing `data=None`.  Inside `_request`, this reaches:
```python
if "json" in kwargs and route.request_model:
    model_cls.check(body)  # body is None
```

`model_validate(None)` will raise a `ValidationError`, but the error message
won't clearly say "you passed None to data=".  The spec identifies this as an
edge case ("A `None` value should either be rejected at the method level or
result in no body being sent") but the implementation doesn't address it.

**Severity**: Low — the error is still raised; it's just not as clear.  A
senior would note it for a follow-up.

---

### 7. QUALITY — Formulaic docstrings add verbosity without information

Every converted method now has:
```
data: Foo bar payload.
    Accepts a :class:`FooBarRequest` instance or a dict.

Request model: :class:`FooBarRequest`
```

This is three lines saying the same thing that the type annotation
`data: FooBarRequest | dict` already conveys.  The old Pattern A docstrings
at least described individual fields (`title: Catalog title.`,
`agent_id: Assigned agent ID.`), which added genuine information.

The new docstrings are correct but mechanically generated and provide no
additional insight beyond what the IDE shows from the type hint.  Over ~75
methods, this adds substantial line count with minimal signal.

**What a senior would do**: Either keep it terse
(`data: Catalog creation payload.`) without the boilerplate "Accepts a..." and
"Request model:" lines, or include a brief description of the *key* fields
(e.g., "Payload with `to`, `subject`, and `body` fields.") to preserve the
discoverability the old docstrings had.

---

### 8. POSITIVE — Dashboard `params_model` → `request_model` fix

The conversion of the 5 dashboard POST routes from `params_model` to
`request_model` is a genuine correctness fix, not just a pattern alignment.
The old code declared `params_model` but passed data via `json=`, meaning the
`_request` validation path for params was never triggered.  The new code
correctly routes through `request_model` validation.

---

### 9. POSITIVE — Required field restorations are well-targeted

The 5 restored fields (`task_code` on `TimelineTaskCreateRequest`,
`comments` and `task_code` on `JobNoteCreateRequest`, `description` on
`ParcelItemCreateRequest`, `notes` on `ItemNotesRequest`) are logical
candidates.  The fixture files were updated accordingly.  This is the kind of
detail that often gets missed in a refactor of this scope.

---

### 10. POSITIVE — Example lambda fixes are comprehensive

The ~75 example lambda conversions from positional/kwargs to `data=` keyword
syntax were applied consistently.  The `data=data or {}` fallback pattern is
used uniformly, which keeps examples runnable even without fixture data.

---

## Summary Table

| # | Category | Severity | Status |
|---|----------|----------|--------|
| 1 | Defect | Medium | **FIXED** in #21-followup — `PackagingSettingsSaveRequest`, `PackagingLaborSaveRequest` added |
| 2 | Defect | Low | **FIXED** in #21-followup — `GeoSettingsParams`, `InheritFromParams` restored in TYPE_CHECKING |
| 3 | Design | Medium | Placeholder models are barely typed |
| 4 | Design | Low | **FIXED** in #21-followup — `DashboardCompanyRequest` created for POST routes |
| 5 | Design | Medium | Breaking change without migration docs |
| 6 | Risk | Low | No `None` guard on `data` parameter |
| 7 | Quality | Low | Formulaic docstrings replace informative ones |
| 8 | Positive | — | Dashboard route model fix |
| 9 | Positive | — | Well-targeted required field restorations |
| 10 | Positive | — | Comprehensive example fixes |

---

## Recommendation

Issues #1, #2, and #4 have been resolved in the follow-up PR.  The remaining
items (#3, #5, #6, #7) can be addressed in future work.
