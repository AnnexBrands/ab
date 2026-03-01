# Feature Specification: Contact Search Tests

**Feature Branch**: `023-contact-search-tests`
**Created**: 2026-02-28
**Status**: Draft
**Input**: User description: "create tests for /contacts/v2/search including permutations of excluding keys from request fixture. get this completed in progress.html"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Request key-exclusion permutation tests (Priority: P1)

An SDK developer wants confidence that `ContactSearchRequest` correctly accepts payloads when optional keys are omitted and correctly rejects payloads when required keys are missing. By testing every permutation of key exclusion against the request fixture, the team catches regressions where field optionality changes silently.

**Why this priority**: The request model has a nested structure with a mix of required and optional fields at multiple levels (`mainSearchRequest` is optional, its 7 children are optional; `loadOptions` is required, `pageNumber`/`pageSize` are required, `sortingBy`/`sortingDirection` are optional). Incorrect optionality leads to silent HTTP 400s in production. This is the core deliverable.

**Independent Test**: Run `pytest tests/models/test_contact_search.py -k permut` — each permutation test passes or raises `ValidationError` as expected.

**Acceptance Scenarios**:

1. **Given** the full request fixture JSON, **When** `mainSearchRequest` is omitted entirely, **Then** validation succeeds (it is Optional).
2. **Given** the full request fixture JSON, **When** any single optional field within `mainSearchRequest` is omitted, **Then** validation succeeds for each permutation (7 fields, 7 passing tests).
3. **Given** the full request fixture JSON, **When** all optional fields within `mainSearchRequest` are omitted (empty object), **Then** validation succeeds.
4. **Given** the full request fixture JSON, **When** `sortingBy` or `sortingDirection` is omitted from `loadOptions`, **Then** validation succeeds (both are optional).
5. **Given** the full request fixture JSON, **When** `pageNumber` is omitted from `loadOptions`, **Then** validation raises `ValidationError` (required field).
6. **Given** the full request fixture JSON, **When** `pageSize` is omitted from `loadOptions`, **Then** validation raises `ValidationError` (required field).
7. **Given** the full request fixture JSON, **When** `loadOptions` is omitted entirely, **Then** validation raises `ValidationError` (required field).
8. **Given** the full request fixture JSON, **When** an unknown key is added to any sub-model, **Then** validation raises `ValidationError` (`extra="forbid"`).

---

### User Story 2 - Response model validation tests (Priority: P2)

An SDK developer wants comprehensive test coverage for `SearchContactEntityResult` beyond the basic fixture validation that already exists. This ensures all 22 fields bind correctly, type coercion works, and the mock fixture is fully exercised.

**Why this priority**: The response model was just rewritten (022) with 22 fields. The existing test covers basic `isinstance` + `assert_no_extra_fields` but does not assert individual field values or type correctness. This story adds field-level assertions.

**Independent Test**: Run `pytest tests/models/test_contact_search.py -k response` — all response field assertions pass.

**Acceptance Scenarios**:

1. **Given** the mock response fixture, **When** validated against `SearchContactEntityResult`, **Then** specific fields (`contact_id`, `contact_full_name`, `contact_email`, `company_name`, `is_prefered`, `total_records`) have correct values and types.
2. **Given** a response with all null optional fields, **When** validated, **Then** model construction succeeds with all fields as None.

---

### User Story 3 - Progress report reflects completion (Priority: P1)

The team's progress dashboard (`progress.html`) must reflect the completed state of the `/contacts/v2/search` endpoint after the new tests are in place.

**Why this priority**: The progress report is the team's primary visibility tool. Without regeneration, the HTML report is stale and does not reflect the gate improvements from 022 or the new test coverage from this feature.

**Independent Test**: Open `html/progress.html` in a browser and verify `/contacts/v2/search` shows as complete with all gates passing.

**Acceptance Scenarios**:

1. **Given** the new tests are written and passing, **When** `python scripts/generate_progress.py` runs, **Then** `html/progress.html` is regenerated with current gate status.
2. **Given** the regenerated report, **When** the `/contacts/v2/search` row is inspected, **Then** all quality gates show PASS and status shows complete.

---

### Edge Cases

- What if the request fixture is malformed JSON? The test loader (`load_request_fixture`) raises `ValueError` — tests should not handle this; it's a developer error.
- What if a required field's type is wrong (e.g., `pageNumber: "abc"`)? Pydantic raises `ValidationError` with a type error — include one type-mismatch test.
- What if `mainSearchRequest` is an empty object `{}`? Should succeed — all 7 fields are optional.
- What if `loadOptions` has only required fields and omits both optional fields? Should succeed.

## Requirements *(mandatory)*

### Functional Requirements

**Request Permutation Tests**

- **FR-001**: Tests MUST cover omitting `mainSearchRequest` entirely from the request.
- **FR-002**: Tests MUST cover omitting each of the 7 optional fields in `mainSearchRequest` individually (7 parametrized cases).
- **FR-003**: Tests MUST cover omitting all optional fields in `mainSearchRequest` (empty object).
- **FR-004**: Tests MUST cover omitting each of the 2 optional fields in `loadOptions` individually (`sortingBy`, `sortingDirection`).
- **FR-005**: Tests MUST cover omitting both optional fields in `loadOptions` (only required fields remain).
- **FR-006**: Tests MUST verify that omitting required field `pageNumber` from `loadOptions` raises `ValidationError`.
- **FR-007**: Tests MUST verify that omitting required field `pageSize` from `loadOptions` raises `ValidationError`.
- **FR-008**: Tests MUST verify that omitting `loadOptions` entirely raises `ValidationError`.
- **FR-009**: Tests MUST verify that adding an unknown key to the request or any sub-model raises `ValidationError` (`extra="forbid"`).

**Response Validation Tests**

- **FR-010**: Tests MUST assert specific field values from the mock fixture (at minimum: `contact_id`, `contact_full_name`, `contact_email`, `company_name`, `is_prefered`, `total_records`).
- **FR-011**: Tests MUST verify that an all-null response validates successfully.

**Progress Report**

- **FR-012**: The progress report (`html/progress.html`) MUST be regenerated after tests are complete.
- **FR-013**: The `/contacts/v2/search` endpoint MUST show as complete with all gates passing in the regenerated report.

**Test Infrastructure**

- **FR-014**: All new tests MUST live in a single test file: `tests/models/test_contact_search.py`.
- **FR-015**: Tests MUST use the existing `load_request_fixture` and `require_fixture` helpers from `conftest.py`.
- **FR-016**: Tests MUST NOT require live API access (no `@pytest.mark.live`).
- **FR-017**: The full test suite MUST pass with zero regressions after changes.

### Key Entities

- **ContactSearchRequest**: Top-level request body with nested `mainSearchRequest` (Optional) and `loadOptions` (required).
- **ContactSearchParams**: 7 optional filter fields within `mainSearchRequest`.
- **PageOrderedRequest**: 2 required pagination fields + 2 optional sort fields within `loadOptions`.
- **SearchContactEntityResult**: 22-field response model for a single search result row.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Request permutation tests cover all 15+ key-exclusion scenarios (optional omissions succeed, required omissions fail).
- **SC-002**: Response field-level assertions verify at least 6 typed fields from the mock fixture.
- **SC-003**: Full test suite passes with zero failures and zero regressions.
- **SC-004**: `html/progress.html` is regenerated and shows `/contacts/v2/search` as complete.

## Assumptions

- The request fixture at `tests/fixtures/requests/ContactSearchRequest.json` is the canonical fixture for permutation testing.
- The response mock fixture at `tests/fixtures/mocks/SearchContactEntityResult.json` is the canonical fixture for response validation.
- `pytest.mark.parametrize` is the appropriate mechanism for enumerating key-exclusion permutations.
- The progress report script (`scripts/generate_progress.py`) runs without errors in the current environment.
- No changes to the models themselves are needed — this feature is test-only + progress regeneration.

## Scope

### In Scope

- Creating `tests/models/test_contact_search.py` with request permutation and response validation tests
- Parametrizing key-exclusion permutations for the request fixture
- Regenerating `html/progress.html`
- Verifying zero test regressions

### Out of Scope

- Modifying the `ContactSearchRequest`, `ContactSearchParams`, `PageOrderedRequest`, or `SearchContactEntityResult` models
- Adding live API integration tests
- Testing other endpoints beyond `/contacts/v2/search`
- Modifying the progress report template or generation script
