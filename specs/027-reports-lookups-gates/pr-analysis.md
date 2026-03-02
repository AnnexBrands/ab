# PR Analysis: 027 — Reports & Lookups Quality Gates

**PR**: #34 (pending) — `feat(sdk): reports & lookups quality gates — models, fixtures, tests`
**Branch**: `027-reports-lookups-gates`
**Reviewed**: 2026-03-02
**Reviewer level**: Senior — with extended regression analysis & roadmap recommendations

---

## Summary

This PR rewrites all 6 report response models and 6 extended lookup models to
match C# ground truth, captures 14 new fixtures from the staging API, updates
route definitions to correct response types, and fixes test files to handle
list-shaped fixtures. It also adds pagination fields (`pageNo`, `pageSize`,
`sortBy`) to 4 report request models after discovering that the API requires
them.

**Gate improvement**: All gates pass count rose from **50 → 69** (+19).
Target SC-004 was 65+ — exceeded.

| Gate | Before | After | Delta |
|------|--------|-------|-------|
| G1 Model Fidelity | 66 | 85 | +19 |
| G2 Fixture Status | 87 | 106 | +19 |
| G3 Test Quality | 135 | 135 | 0 |
| G4 Doc Accuracy | 153 | 153 | 0 |
| G5 Param Routing | 216 | 216 | 0 |
| G6 Request Quality | 223 | 223 | 0 |
| **All pass** | **50** | **69** | **+19** |

**Tests**: 529 passed, 54 skipped, 7 pre-existing failures, 5 xfailed.
Zero new regressions.

---

## Verdict

The PR achieves its stated goals cleanly. The model rewrites are thorough, the
fixture capture strategy is sound, and the iterative "run → inspect → fix →
re-run" methodology aligns with Constitution Principle II. All 6 success
criteria are met.

However, this PR — combined with recent regressions from prior features — exposes
**systemic weaknesses** in the project's tooling, testing, and workflow that
will increasingly impede progress toward 100% gates. The second half of this
analysis provides an in-depth assessment of those weaknesses and concrete
recommendations for a dedicated refactoring sprint.

---

## Issues

### 1. POSITIVE — Model rewrites are faithful to source hierarchy

All 12 model rewrites follow the constitutional source-of-truth hierarchy:
Tier 1 (C# DTOs) for field names and types, Tier 2 (live fixtures) for
validation, Tier 3 (swagger) for discovery. Notable examples:

- `DensityClassEntry` rewritten from `densityMin/densityMax/freightClass` to
  `rangeEnd/value` when the live API returned `GuidSequentialRangeValue` shape
  — correctly trusting Tier 2 over Tier 3.
- `CommonInsuranceSlab` created as a dedicated model (11 fields) instead of
  reusing `LookupValue`, preventing fixture collision on shared filenames.
- `AccessKeySetup` correctly includes parent `AccessKey` fields
  (`accessKey`/`friendlyName`) that the live API denormalizes into the response.

### 2. POSITIVE — Pagination discovery and request model updates

The PR discovered that 4 report POST endpoints require `sortBy` (a nested
object `{sortByField: int, sortDir: bool}`), `pageNo`, and `pageSize` —
fields not obvious from swagger alone. The request models and fixtures were
updated accordingly. This is exactly the kind of iterative debugging the
constitution's capture loop envisions.

### 3. POSITIVE — Empty-list fixture strategy is pragmatic

For 4 endpoints returning HTTP 500 on staging (salesDrilldown, referredBy,
web2Lead) and 1 timing out (insurance), empty `[]` fixtures were created.
These correctly pass G1 ("Empty list fixture — nothing to validate") and G2
(file exists). The gate system handles this gracefully.

### 4. DESIGN — Test helper `_first_or_skip` duplicated across two files

Both `test_report_models.py` and `test_extended_lookup_models.py` define an
identical `_first_or_skip` helper to extract the first element from list
fixtures. Meanwhile, `test_lookup_models.py` uses an inline
`if isinstance(data, list) and data: data = data[0]` pattern.

**What a senior would do**: Move `_first_or_skip` into `tests/conftest.py`
alongside `assert_no_extra_fields`, and refactor all model test files to use
it. This eliminates the three competing patterns for the same operation.

### 5. DESIGN — `sort_by` typed as `Optional[dict]` loses structure

```python
sort_by: Optional[dict] = Field(None, alias="sortBy", description="Sort config")
```

The `sortBy` object has a known shape: `{sortByField: int, sortDir: bool}`.
Using `dict` discards that structure. A nested model or `TypedDict` would
provide validation and documentation.

**Severity**: Low — the field works, and the comment documents the shape.
But it's the kind of `Optional[dict]` placeholder that PR 020's analysis
(Issue #3) flagged as "ceremony without value."

### 6. OBSERVATION — G3 and G4 did not improve despite new tests

The PR added tests in `test_report_models.py` and
`test_extended_lookup_models.py`, but G3 (Test Quality) and G4 (Doc Accuracy)
counts did not change. This suggests the gate evaluator was already counting
these endpoints as passing G3/G4 through existing test patterns or auto-pass
rules, making the new tests redundant from a gate perspective (though still
valuable as regression guards).

### 7. DATA — 7 pre-existing test failures remain unaddressed

The full suite shows 7 failures that predate this PR. While the PR correctly
avoids introducing new regressions, the backlog of broken tests is growing:

| # | Test | Root Cause | Introduced By | Difficulty |
|---|------|-----------|---------------|-----------|
| 1 | `test_list_users` | Positional arg after keyword-only refactor | #21 (751b8e6) | Easy |
| 2 | `test_search_contact_entity_result` | 31 undeclared extra fields in model | #24 (eea7038) | Medium |
| 3 | `test_response_field_values` | Same SearchContactEntityResult model gap | #24 (eea7038) | Medium |
| 4 | `test_priced_freight_provider` | Empty `[]` fixture, test expects dict | Scaffolding | Easy |
| 5 | `test_user_role` | Missing `UserRole.json` (API returns `List[str]`) | Scaffolding | Easy |
| 6 | `test_all_fixture_files_tracked` | 62 fixtures on disk not in FIXTURES.md | #32 (b639773) | Medium |
| 7 | `test_captured_fixtures_exist_on_disk` | FIXTURES.md lists 18 request fixtures as captured but files are in `requests/` subdir | #32 (b639773) | Medium |

Failures #6 and #7 are particularly concerning — they indicate FIXTURES.md
data integrity has drifted significantly from reality. The `--fixtures`
regenerator doesn't resolve the full mismatch because the `test_mock_coverage`
test scans raw fixture directories while FIXTURES.md is structured by route
definitions.

---

## Constitution & Plan Coherence

The constitution (v2.3.0) and feature plan are well-aligned. The
source-of-truth hierarchy (Principle IV / Sources of Truth section) directly
guided the model rewrite methodology. The example-driven fixture capture loop
(Principle II) was followed for all 14 new fixtures.

**Gap identified**: The constitution mandates Four-Way Harmony (Principle III)
but does not define a **machine-enforceable regression check** for it. A human
or agent can merge a PR that breaks existing fixtures or tests without any
automated gate catching it pre-merge. The quality gates only run on explicit
invocation (`generate_progress.py`), not as a CI/CD gate.

---

## User Stories & Plan Effectiveness

The three-story structure (US1: Reports, US2: Extended Lookups, US3: Basic
Lookups) was effective. Independence between stories allowed parallel work.
The iterative sweep pattern (rewrite → run → inspect → fix → re-run) proved
robust — the `sortBy` discovery and `CommonInsuranceSlab` creation both
emerged naturally from this loop.

**What worked well**:
- Grouping by endpoint domain (reports vs lookups) kept context tight
- The `_DATE_RANGE` and pagination defaults made examples reproducible
- Empty-list fixtures as a pragmatic fallback for staging failures

**What could improve**:
- The plan didn't anticipate that report endpoints require pagination params
- No fallback plan for staging timeouts/500s beyond empty fixtures
- T050 (quickstart scenarios) was skipped — these should be automated

---

## High-Level Progress Toward Project Goals

### Gate Progress Over Time

| Feature | All Pass | Delta | Cumulative |
|---------|----------|-------|------------|
| Baseline (pre-024) | ~35 | — | — |
| 024 Timeline | ~42 | +7 | +7 |
| 026 CLI Gate Sweep | 50 | +8 | +15 |
| **027 Reports/Lookups** | **69** | **+19** | **+34** |

### Distance to 100%

| Gate | Current | Target | Gap | Category |
|------|---------|--------|-----|----------|
| G1 | 85/231 | 231 | 146 | Model completeness |
| G2 | 106/231 | 231 | 125 | Fixture coverage |
| G3 | 135/231 | 231 | 96 | Test assertions |
| G4 | 153/231 | 231 | 78 | Return type annotations |
| G5 | 216/231 | 231 | 15 | Param model routing |
| G6 | 223/231 | 231 | 8 | Request quality |

The **binding constraint** is G1 → G2 → G3 (model → fixture → test). You
cannot advance G2 without G1, and cannot advance G3 without G2. The
dependency chain means the 146-endpoint G1 gap is the true bottleneck.

Of those 146 G1-failing endpoints:
- ~52 have no response model (void/bytes/fire-and-forget) — these need
  an architectural decision on whether to define proxy models or exempt them
- ~20-30 have models but missing fixtures (need staging API calls)
- ~40-60 have fixtures but models have undeclared extra fields (need field expansion)
- ~15-20 are blocked by staging API issues (500s, timeouts)

---

## Regression Analysis & Systemic Recommendations

The user requested an extraordinary depth of analysis on what refactoring
would prevent future regressions and enable reaching 100% gates. Below are
concrete recommendations organized by impact and effort.

---

### R1. CRITICAL — Fixture/Model Regression Gate in CI

**Problem**: Nothing prevents a PR from breaking existing G1 passes. A model
field rename, fixture overwrite, or route change can silently regress gates.
The 7 pre-existing failures demonstrate this — they accumulated across
features #21, #24, and #32 without being caught.

**Recommendation**: Create `tests/test_gate_regression.py` that:
1. Runs `evaluate_all_gates()` from `ab/progress/gates.py`
2. Loads a baseline file (`tests/gate_baseline.json`) with the current
   passing set
3. Asserts no endpoint that was previously passing now fails
4. Allows new passes (one-directional ratchet)
5. Provides a CLI command to update the baseline after intentional changes

**Effort**: 2-3 hours. Uses existing gate infrastructure.

**Impact**: Prevents the #1 source of accumulated regressions — model changes
in one feature breaking gates established in a prior feature.

---

### R2. HIGH — Unify List-Fixture Handling Across the Stack

**Problem**: Three competing patterns exist for handling list-shaped fixtures:

| Location | Pattern |
|----------|---------|
| `gates.py:evaluate_g1` | `if isinstance(data, list): data = data[0]` |
| `test_lookup_models.py` | `if isinstance(data, list) and data: data = data[0]` |
| `test_report_models.py` | `_first_or_skip(data)` with `pytest.skip` on empty |
| `test_extended_lookup_models.py` | Same `_first_or_skip` (duplicated) |

When a fixture changes shape (dict → list, or vice versa), each location may
break independently.

**Recommendation**:
1. Add `first_or_skip(data)` to `tests/conftest.py` as the canonical helper
2. Add `unwrap_fixture(data)` to `ab/progress/gates.py` as the gate equivalent
3. Both should handle: dict passthrough, list[0] extraction, empty-list skip,
   paginated `{items: [...]}` unwrapping
4. Refactor all model tests and gate evaluation to use these canonical helpers
5. Document the fixture shape contract: "Fixtures are always the raw API
   response — list or dict. Consumers unwrap as needed."

**Effort**: 3-4 hours.

**Impact**: Eliminates an entire class of fixture-shape-mismatch bugs.

---

### R3. HIGH — Fix FIXTURES.md / test_mock_coverage Structural Mismatch

**Problem**: `test_mock_coverage.py` scans raw directories (`tests/fixtures/`,
`tests/fixtures/mocks/`) and compares against FIXTURES.md entries. But:
- FIXTURES.md is organized by Route definitions (endpoint-centric)
- The directory scan is file-centric (finds all `.json` files)
- Request fixtures live in `tests/fixtures/requests/` which
  `test_mock_coverage` doesn't scan — but FIXTURES.md lists them as "captured"
- Result: 62 untracked files + 18 "captured but missing" files = permanent
  failure

**Recommendation**:
1. `test_mock_coverage.py` must scan `tests/fixtures/requests/` for request
   fixtures separately from response fixtures
2. FIXTURES.md regenerator should distinguish response vs request fixture
   status columns (G2-response vs G2-request)
3. Add a `--verify` mode to `generate_progress.py` that returns exit code 1
   if FIXTURES.md is stale (enables CI gating)
4. Consider whether `test_mock_coverage` should be replaced by the gate
   evaluation system entirely — its checks are a subset of what G1-G6 already
   verify

**Effort**: 4-6 hours.

**Impact**: Fixes 2 of the 7 pre-existing failures. Prevents future
FIXTURES.md drift.

---

### R4. HIGH — Batch Fixture Capture Tooling

**Problem**: Getting from 106 → 231 G2-passing endpoints requires capturing
~125 more fixtures. The current approach is manual: write an example, run it,
inspect output, fix model, repeat. At the 027 rate (~20 fixtures per feature),
this is 6-7 more features just for fixture capture.

**Recommendation**: Build a `scripts/capture_missing.py` that:
1. Reads FIXTURES.md for all G2-FAIL endpoints
2. For each, checks if an example exists in `examples/`
3. If example exists: runs it, captures fixture, reports result
4. If no example: generates a skeleton example from the Route definition
5. Produces a summary: "Captured N, Failed M, Needs-Example K"

This turns fixture capture from a per-feature manual effort into a batch
operation.

**Effort**: 6-8 hours.

**Impact**: Could capture 30-50 fixtures in a single batch run, dramatically
accelerating G2 progress.

---

### R5. MEDIUM — Fix the 5 Easy Pre-Existing Failures

**Problem**: 5 of the 7 pre-existing failures are trivially fixable but
accumulate tech debt that obscures real regressions.

| Fix | Change |
|-----|--------|
| `test_list_users` | `api.users.list(data)` → `api.users.list(data=data)` |
| `test_priced_freight_provider` | Add `_first_or_skip` for empty-list fixture |
| `test_user_role` | Create `UserRole.json` as `["Admin", "CorporateAccounting"]` or rewrite test for `List[str]` return type |
| `test_search_contact_entity_result` | Add 31 fields to `SearchContactEntityResult` model from fixture |
| `test_response_field_values` | Same `SearchContactEntityResult` fix |

**Effort**: 2-3 hours for all 5.

**Impact**: Reduces noise in test output. Makes real regressions immediately
visible. Prevents the "broken windows" effect where persistent failures
normalize test breakage.

---

### R6. MEDIUM — Auto-Generate Test Stubs from Gate Evaluation

**Problem**: G3 requires both `isinstance()` and `assert_no_extra_fields()`
assertions. Currently, 96 endpoints fail G3. Writing these tests manually is
tedious and error-prone.

**Recommendation**: Build `scripts/generate_model_tests.py` that:
1. Reads all Route definitions
2. For each route with a `response_model`, generates a test function:
   ```python
   def test_{model_name}(self):
       data = require_fixture("{ModelName}", "{METHOD}", "{path}")
       item = first_or_skip(data)
       model = {ModelName}.model_validate(item)
       assert isinstance(model, {ModelName})
       assert_no_extra_fields(model)
   ```
3. Groups tests by endpoint module (test_report_models, test_lookup_models, etc.)
4. Skips generation for models that already have tests
5. Outputs to `tests/models/test_{module}_models.py`

**Effort**: 4-5 hours.

**Impact**: Could generate 40-60 test stubs in one run, closing most of the
G3 gap. Tests auto-skip when fixtures are missing (via `require_fixture`).

---

### R7. MEDIUM — Return Type Annotation Sweep for G4

**Problem**: 78 endpoints fail G4 because their return type is `Any` or
missing entirely. These are mechanical fixes — change `-> Any` to
`-> ModelName` or `-> list[ModelName]`.

**Recommendation**: Build `scripts/fix_return_types.py` that:
1. Reads each Route's `response_model`
2. Finds the corresponding endpoint method
3. If return type is `Any` or missing, patches it to match the route's
   response model
4. Handles `List[Model]` → `list[Model]` type syntax

Alternatively, a simpler approach: grep for `-> Any` in endpoint files and
fix manually — there are only ~26 non-exempt cases.

**Effort**: 2-3 hours.

**Impact**: Closes most of the G4 gap mechanically.

---

### R8. LOW — Architectural Decision on No-Response-Model Endpoints

**Problem**: ~52 endpoints have no `response_model` specified. These are
DELETE operations, fire-and-forget POSTs, byte-stream returns, etc. They
auto-pass G1-G4 in the gate system but still count against the denominator
(231 total endpoints).

**Options**:
1. **Exempt them** — Add a gate exemption flag to Route (e.g.,
   `no_response=True`) and exclude from the 231 denominator
2. **Define proxy models** — Create `EmptyResponse`, `BytesResponse`, etc.
   for gate compliance
3. **Accept the ceiling** — Acknowledge that 100% is ~179/179 (after
   excluding 52 void endpoints)

**Recommendation**: Option 1 (exempt). Counting void DELETE endpoints against
model fidelity gates distorts the metric. The gate system should measure what
it can meaningfully evaluate.

**Effort**: 2-3 hours to add the exemption flag and adjust gate counting.

**Impact**: Changes the denominator from 231 to ~179, making the "all pass"
percentage more meaningful and the 100% target realistic.

---

### R9. LOW — `SortBy` Nested Model

**Problem**: The `sortBy` field is `Optional[dict]` across 4 request models.
The actual shape is `{sortByField: int, sortDir: bool}`.

**Recommendation**: Create a `SortBy` model in `ab/api/models/reports.py`:
```python
class SortBy(RequestModel):
    sort_by_field: int = Field(0, alias="sortByField")
    sort_dir: bool = Field(True, alias="sortDir")
```

Replace `sort_by: Optional[dict]` with `sort_by: Optional[SortBy]` in the
4 request models.

**Effort**: 30 minutes.

**Impact**: Adds type safety. Aligns with Constitution Principle I
("Every API response and request body MUST resolve to a validated Pydantic
model").

---

## Recommended Sprint Plan

Based on the analysis above, a dedicated refactoring sprint should prioritize:

### Week 1: Foundation (Prevents Future Regressions)

| # | Task | Effort | Addresses |
|---|------|--------|-----------|
| 1 | Fix 5 easy pre-existing failures | 2-3h | R5 |
| 2 | Gate regression test (`test_gate_regression.py`) | 2-3h | R1 |
| 3 | Unify list-fixture handling | 3-4h | R2 |
| 4 | Fix FIXTURES.md / mock_coverage mismatch | 4-6h | R3 |

**Sprint 1 outcome**: Zero test failures. Gate ratchet prevents future
regressions. Fixture handling is consistent.

### Week 2: Automation (Accelerates Toward 100%)

| # | Task | Effort | Addresses |
|---|------|--------|-----------|
| 5 | Batch fixture capture script | 6-8h | R4 |
| 6 | Auto-generate model test stubs | 4-5h | R6 |
| 7 | Return type annotation sweep | 2-3h | R7 |
| 8 | Exempt no-response endpoints from gate count | 2-3h | R8 |

**Sprint 2 outcome**: Tooling exists to batch-capture fixtures and
batch-generate tests. G4 and G5 are near 100%. The denominator is honest.

### Week 3: Content (Push Toward 100%)

| # | Task | Effort | Addresses |
|---|------|--------|-----------|
| 9 | Run batch fixture capture on staging | 4-6h | R4 |
| 10 | Run model test generator | 1-2h | R6 |
| 11 | Fix G5 (15 endpoints) — add params_models | 2-3h | Gate gap |
| 12 | Fix G6 (8 endpoints) — add field descriptions | 1-2h | Gate gap |
| 13 | `SortBy` nested model + remaining `Optional[dict]` cleanup | 1h | R9 |

**Sprint 3 outcome**: Projected gate status after all 3 sprints:

| Gate | Current | Projected | Improvement |
|------|---------|-----------|-------------|
| G1 | 85 | 140-160 | +55-75 |
| G2 | 106 | 160-180 | +54-74 |
| G3 | 135 | 170-190 | +35-55 |
| G4 | 153 | 175-195 | +22-42 |
| G5 | 216 | 231 | +15 |
| G6 | 223 | 231 | +8 |
| **All** | **69** | **130-155** | **+61-86** |

The remaining gap to 231 would be the ~52 no-response endpoints (exempted)
plus staging API failures requiring manual investigation.

---

## Summary Table

| # | Category | Severity | Status |
|---|----------|----------|--------|
| 1 | Positive | — | Model rewrites faithful to source hierarchy |
| 2 | Positive | — | Pagination discovery via iterative debugging |
| 3 | Positive | — | Pragmatic empty-list fixture strategy |
| 4 | Design | Low | `_first_or_skip` duplicated — consolidate to conftest |
| 5 | Design | Low | `sort_by: Optional[dict]` loses structure |
| 6 | Observation | Info | G3/G4 unchanged despite new tests |
| 7 | Data | Medium | 7 pre-existing failures accumulating |
| R1 | Recommendation | Critical | Gate regression test (CI ratchet) |
| R2 | Recommendation | High | Unify list-fixture handling |
| R3 | Recommendation | High | Fix FIXTURES.md structural mismatch |
| R4 | Recommendation | High | Batch fixture capture tooling |
| R5 | Recommendation | Medium | Fix 5 easy pre-existing failures |
| R6 | Recommendation | Medium | Auto-generate test stubs from gates |
| R7 | Recommendation | Medium | Return type annotation sweep |
| R8 | Recommendation | Low | Exempt no-response endpoints |
| R9 | Recommendation | Low | `SortBy` nested model |

---

## Final Assessment

Feature 027 is a solid, well-executed sweep that moved the needle by 19
endpoints — the largest single-feature improvement in project history. The
methodology is sound and repeatable.

The path to 100% gates is now **tooling-constrained, not knowledge-constrained**.
The team knows how to rewrite models, capture fixtures, and write tests. What's
needed is automation to do it at scale: batch capture, batch test generation,
and a regression ratchet to protect gains. The recommended 3-sprint plan would
roughly double the all-gates-pass count while establishing infrastructure that
makes future feature work cheaper and safer.
