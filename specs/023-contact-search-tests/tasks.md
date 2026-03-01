# Tasks: Contact Search Tests

**Input**: Design documents from `/specs/023-contact-search-tests/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/test-contract.md, quickstart.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: No project initialization needed — existing SDK, existing branch.

_(No setup tasks — project structure, fixtures, and models already in place.)_

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create the test file skeleton with shared imports and fixture loading helpers

- [x] T001 Create `tests/models/test_contact_search.py` with module docstring, imports (`pytest`, `ValidationError`, `ContactSearchRequest`, `ContactSearchParams`, `PageOrderedRequest`, `SearchContactEntityResult`, `load_request_fixture`, `require_fixture`, `assert_no_extra_fields`), and a helper function that loads the request fixture via `load_request_fixture("ContactSearchRequest")` and returns a deep copy

**Checkpoint**: Test file exists, imports resolve, `pytest --collect-only tests/models/test_contact_search.py` succeeds.

---

## Phase 3: User Story 1 — Request key-exclusion permutation tests (Priority: P1)

**Goal**: Verify `ContactSearchRequest` correctly accepts payloads when optional keys are omitted and rejects payloads when required keys are missing or extra keys are present.

**Independent Test**: `pytest tests/models/test_contact_search.py -k "request" -v` — all request permutation tests pass.

### Implementation for User Story 1

**Optional field omissions (should succeed)**:

- [x] T002 [US1] Write a parametrized test `test_request_optional_search_field_omitted` in `tests/models/test_contact_search.py` that loads the request fixture, removes one optional field from `mainSearchRequest` per parameter (`contactDisplayId`, `fullName`, `companyName`, `companyCode`, `email`, `phone`, `companyDisplayId` — 7 cases), validates against `ContactSearchRequest`, and asserts success
- [x] T003 [US1] Write test `test_request_main_search_request_omitted` in `tests/models/test_contact_search.py` that loads the request fixture, removes `mainSearchRequest` entirely, validates against `ContactSearchRequest`, and asserts success
- [x] T004 [US1] Write test `test_request_main_search_request_empty` in `tests/models/test_contact_search.py` that loads the request fixture, sets `mainSearchRequest` to `{}`, validates against `ContactSearchRequest`, and asserts success
- [x] T005 [US1] Write a parametrized test `test_request_optional_load_option_omitted` in `tests/models/test_contact_search.py` that loads the request fixture, removes one optional field from `loadOptions` per parameter (`sortingBy`, `sortingDirection` — 2 cases), validates against `ContactSearchRequest`, and asserts success
- [x] T006 [US1] Write test `test_request_load_options_only_required` in `tests/models/test_contact_search.py` that loads the request fixture, removes both `sortingBy` and `sortingDirection` from `loadOptions`, validates against `ContactSearchRequest`, and asserts success

**Required field omissions (should fail with ValidationError)**:

- [x] T007 [US1] Write a parametrized test `test_request_required_field_omitted_fails` in `tests/models/test_contact_search.py` that loads the request fixture, removes one required field per parameter (`pageNumber` from `loadOptions`, `pageSize` from `loadOptions` — 2 cases), and asserts `pytest.raises(ValidationError)`
- [x] T008 [US1] Write test `test_request_load_options_omitted_fails` in `tests/models/test_contact_search.py` that loads the request fixture, removes `loadOptions` entirely, and asserts `pytest.raises(ValidationError)`

**Extra field rejection (should fail with ValidationError)**:

- [x] T009 [US1] Write a parametrized test `test_request_extra_field_rejected` in `tests/models/test_contact_search.py` that loads the request fixture, adds an unknown key (`{"bogus": 1}`) at three levels (top-level, inside `mainSearchRequest`, inside `loadOptions` — 3 cases), and asserts `pytest.raises(ValidationError)`

- [x] T010 [US1] Run `pytest tests/models/test_contact_search.py -k "request" -v` and verify all request tests pass

**Checkpoint**: All 18 request permutation test cases pass (12 succeed + 3 fail-as-expected + 3 extra-rejected).

---

## Phase 4: User Story 2 — Response model validation tests (Priority: P2)

**Goal**: Verify `SearchContactEntityResult` field-level values and types from mock fixture, plus all-null edge case.

**Independent Test**: `pytest tests/models/test_contact_search.py -k "response" -v` — all response tests pass.

### Implementation for User Story 2

- [x] T011 [US2] Write test `test_response_field_values` in `tests/models/test_contact_search.py` that loads the mock fixture via `require_fixture("SearchContactEntityResult", "POST", "/contacts/v2/search", required=True)`, unwraps the list, validates against `SearchContactEntityResult`, calls `assert_no_extra_fields`, and asserts: `contact_id == 30760` (int), `contact_full_name == "Justine Yigitbasi"` (str), `contact_email == "oh14004@goNavis.com"` (str), `company_name == "Navis Pack & Ship #14004OH"` (str), `is_prefered is True` (bool), `total_records == 1` (int)
- [x] T012 [US2] Write test `test_response_all_null_fields` in `tests/models/test_contact_search.py` that constructs a `SearchContactEntityResult` with all 22 fields as `None` (pass empty dict `{}`), validates, and asserts all fields are `None`

- [x] T013 [US2] Run `pytest tests/models/test_contact_search.py -k "response" -v` and verify all response tests pass

**Checkpoint**: Response tests confirm field binding and all-null edge case.

---

## Phase 5: User Story 3 — Progress report reflects completion (Priority: P1)

**Goal**: Regenerate `html/progress.html` so `/contacts/v2/search` shows as complete with all gates passing.

**Independent Test**: Open `html/progress.html` in browser; `/contacts/v2/search` row shows all PASS + complete.

### Implementation for User Story 3

- [x] T014 [US3] Run `python scripts/generate_progress.py` to regenerate `html/progress.html`
- [x] T015 [US3] Verify `/contacts/v2/search` shows as complete in the regenerated `html/progress.html` (grep for the endpoint path and confirm "complete" or all-PASS status)

**Checkpoint**: Progress report is current and reflects endpoint completion.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Full validation, regression sweep, quickstart verification

- [x] T016 Run full test suite: `pytest tests/ -x -q -m "not live"` — zero failures, zero regressions (413+ passed baseline)
- [x] T017 Run quickstart verification steps from `specs/023-contact-search-tests/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 2)**: No dependencies — can start immediately
- **US1 (Phase 3)**: Depends on Phase 2 (needs test file with imports and helpers)
- **US2 (Phase 4)**: Depends on Phase 2 (needs test file) — can run in parallel with US1
- **US3 (Phase 5)**: No dependency on US1 or US2 (progress.html reflects gate status, not test count) — can run in parallel
- **Polish (Phase 6)**: Depends on Phase 3, 4, and 5 completion

### Within Each User Story

- Fixture loading helpers before test functions
- Parametrized tests before validation runs

### Parallel Opportunities

- T002–T009 can all be written in parallel (different test functions, same file but independent sections)
- US1 (Phase 3) and US2 (Phase 4) can run in parallel after Phase 2 completes
- US3 (Phase 5) can run in parallel with US1 and US2

---

## Parallel Example: Phase 3 + Phase 4

```bash
# After Phase 2, both user stories can proceed in parallel:
Phase 3 (US1): Write request permutation tests (T002–T010)
Phase 4 (US2): Write response validation tests (T011–T013)
```

---

## Implementation Strategy

### MVP First (User Story 1)

1. Complete Phase 2: Create test file skeleton (T001)
2. Complete Phase 3: Request permutation tests (T002–T010)
3. **STOP and VALIDATE**: `pytest tests/models/test_contact_search.py -k "request" -v`
4. All 18 request test cases pass → MVP delivered

### Incremental Delivery

1. Complete Phase 2 → Test file ready
2. Add US1 (Phase 3) → Request permutation tests passing
3. Add US2 (Phase 4) → Response validation tests passing
4. Add US3 (Phase 5) → Progress report regenerated
5. Complete Phase 6 → Full regression verified, quickstart confirmed

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- No new dependencies needed — existing pytest + pydantic
- All tests go in a single file: `tests/models/test_contact_search.py`
- Tests use `load_request_fixture` for request fixture and `require_fixture` for response mock
- The feature is test-only — no model or endpoint changes
