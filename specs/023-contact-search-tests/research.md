# Research: Contact Search Tests

## Decision: Use fixture-driven parametrized testing for key-exclusion permutations

**Rationale**: The request fixture (`tests/fixtures/requests/ContactSearchRequest.json`) is the canonical payload. By loading it and programmatically removing keys, each test case is automatically aligned with the real fixture structure. `pytest.mark.parametrize` generates one test per exclusion, making failures immediately attributable to a specific key.

**Alternatives considered**: Hand-written individual test functions per key (rejected — verbose, doesn't scale), hypothesis/property-based testing (rejected — overkill for a fixed 13-key structure).

## Decision: Separate test file at `tests/models/test_contact_search.py`

**Rationale**: The existing `test_contact_models.py` contains live-marked fixture validation tests for multiple contact models. The new permutation tests are structurally different (parametrized, non-live, focused on one endpoint). A dedicated file keeps concerns clean and allows `pytest -k contact_search` to run the full search test suite in isolation.

**Alternatives considered**: Adding to `test_contact_models.py` (rejected — mixes live fixture tests with offline permutation tests, harder to navigate).

## Decision: Test required-field omissions with `pytest.raises(ValidationError)`

**Rationale**: `ContactSearchRequest` uses `RequestModel` (which sets `extra="forbid"`), and `PageOrderedRequest.page_number`/`.page_size` use `Field(...)` (required). Pydantic raises `ValidationError` when required fields are missing. Testing with `pytest.raises` confirms the SDK boundary validation works correctly.

**Alternatives considered**: Testing HTTP-level rejection (rejected — requires live API, out of scope).

## Decision: Regenerate progress.html via existing script

**Rationale**: `scripts/generate_progress.py` already reads FIXTURES.md gate data and generates `html/progress.html`. No script changes needed — just run it after tests are in place. The endpoint already shows PASS on all 6 gates in FIXTURES.md (from 022).

**Alternatives considered**: Manually editing progress.html (rejected — fragile, contradicts the generated artifact pattern).

## Model Structure Reference

### ContactSearchRequest (top-level)

| Field | Type | Required | Alias |
|-------|------|----------|-------|
| `main_search_request` | `Optional[ContactSearchParams]` | No | `mainSearchRequest` |
| `load_options` | `PageOrderedRequest` | **Yes** | `loadOptions` |

### ContactSearchParams (mainSearchRequest sub-object) — 7 optional fields

| Field | Type | Alias |
|-------|------|-------|
| `contact_display_id` | `Optional[int]` | `contactDisplayId` |
| `full_name` | `Optional[str]` | `fullName` |
| `company_name` | `Optional[str]` | `companyName` |
| `company_code` | `Optional[str]` | `companyCode` |
| `email` | `Optional[str]` | `email` |
| `phone` | `Optional[str]` | `phone` |
| `company_display_id` | `Optional[int]` | `companyDisplayId` |

### PageOrderedRequest (loadOptions sub-object) — 2 required + 2 optional

| Field | Type | Required | Alias |
|-------|------|----------|-------|
| `page_number` | `int` | **Yes** | `pageNumber` |
| `page_size` | `int` | **Yes** | `pageSize` |
| `sorting_by` | `Optional[str]` | No | `sortingBy` |
| `sorting_direction` | `Optional[int]` | No | `sortingDirection` |

### SearchContactEntityResult — 22 fields (all Optional)

All fields are Optional. Mock fixture at `tests/fixtures/mocks/SearchContactEntityResult.json` contains sample values for all 22.

## Key-Exclusion Test Matrix

| # | What's omitted | Expected | Category |
|---|---------------|----------|----------|
| 1 | `mainSearchRequest` entirely | PASS | Optional top-level |
| 2–8 | Each of 7 fields in `mainSearchRequest` | PASS | Optional sub-fields |
| 9 | All fields in `mainSearchRequest` (empty `{}`) | PASS | Optional sub-fields |
| 10 | `sortingBy` from `loadOptions` | PASS | Optional sub-field |
| 11 | `sortingDirection` from `loadOptions` | PASS | Optional sub-field |
| 12 | Both optional fields from `loadOptions` | PASS | Optional sub-fields |
| 13 | `pageNumber` from `loadOptions` | FAIL (ValidationError) | Required sub-field |
| 14 | `pageSize` from `loadOptions` | FAIL (ValidationError) | Required sub-field |
| 15 | `loadOptions` entirely | FAIL (ValidationError) | Required top-level |
| 16 | Extra unknown key at top level | FAIL (ValidationError) | extra="forbid" |
| 17 | Extra unknown key in `mainSearchRequest` | FAIL (ValidationError) | extra="forbid" |
| 18 | Extra unknown key in `loadOptions` | FAIL (ValidationError) | extra="forbid" |
