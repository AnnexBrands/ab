# Tasks: Fix Contact Search

**Input**: Design documents from `/specs/022-fix-contact-search/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/contact-search.md, quickstart.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: No project initialization needed — existing SDK, existing branch.

_(No setup tasks — project structure and dependencies already in place.)_

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create shared sub-models that both user stories depend on

**CRITICAL**: US1 needs PageOrderedRequest and ContactSearchParams before restructuring ContactSearchRequest.

- [x] T001 Create `ContactSearchParams` sub-model (7 optional fields from swagger `MergeContactsSearchRequestParameters`) in `ab/api/models/contacts.py`
- [x] T002 Create `PageOrderedRequest` sub-model (4 fields: pageNumber, pageSize, sortingBy, sortingDirection) in `ab/api/models/contacts.py`
- [x] T003 Export `ContactSearchParams` and `PageOrderedRequest` from `ab/api/models/__init__.py`

**Checkpoint**: Sub-models exist and are importable. No existing behavior broken.

---

## Phase 3: User Story 1 — Request model matches API nested structure (Priority: P1)

**Goal**: Restructure `ContactSearchRequest` from flat mixin inheritance to nested `mainSearchRequest` + `loadOptions` structure so the request fixture validates.

**Independent Test**: `pytest tests/models/test_request_fixtures.py -k ContactSearchRequest -x -q` passes with zero extra fields and round-trip.

### Implementation for User Story 1

- [x] T004 [US1] Restructure `ContactSearchRequest` in `ab/api/models/contacts.py`: remove `PaginatedRequestMixin, SearchableRequestMixin` inheritance, add `main_search_request: Optional[ContactSearchParams]` (alias `mainSearchRequest`) and `load_options: PageOrderedRequest` (alias `loadOptions`) fields with descriptions
- [x] T005 [US1] Remove unused mixin imports (`PaginatedRequestMixin`, `SearchableRequestMixin`) from `ab/api/models/contacts.py` if no other model uses them in this file
- [x] T006 [US1] Validate request fixture: run `pytest tests/models/test_request_fixtures.py -k ContactSearchRequest -x -q` — must pass (isinstance, assert_no_extra_fields, round-trip)

**Checkpoint**: ContactSearchRequest fixture validates with zero extra fields. Existing tests unbroken.

---

## Phase 4: User Story 2 — Response model declares all API-returned fields (Priority: P1)

**Goal**: Rewrite `SearchContactEntityResult` with all 22 C# source fields, fix the mislabeled fixture, and enable assert_no_extra_fields in the test.

**Independent Test**: `pytest tests/models/test_contact_models.py::TestContactModels::test_search_contact_entity_result -x -q` passes with assert_no_extra_fields active.

### Implementation for User Story 2

- [x] T007 [US2] Rewrite `SearchContactEntityResult` in `ab/api/models/contacts.py` with all 22 fields from C# source (contactID, customerCell, contactDisplayId, contactFullName, contactPhone, contactHomePhone, contactEmail, masterConstantValue, contactDept, address1, address2, city, state, zipCode, countryName, companyCode, companyID, companyName, companyDisplayId, isPrefered, industryType, totalRecords) — each with alias and description
- [x] T008 [US2] Create mock fixture at `tests/fixtures/mocks/SearchContactEntityResult.json` matching the contract response shape from `specs/022-fix-contact-search/contracts/contact-search.md`
- [x] T009 [US2] Delete mislabeled fixture `tests/fixtures/SearchContactEntityResult.json` (contains ContactDetailedInfo data, not search results)
- [x] T010 [US2] Update `test_search_contact_entity_result` in `tests/models/test_contact_models.py`: uncomment `assert_no_extra_fields(model)`, update fixture loading to use mock path if needed
- [x] T011 [US2] Update search section in `docs/api/contacts.md`: replace `{"searchText": "Justine"}` example with correct nested request structure, add response field examples

**Checkpoint**: Response model validates against mock fixture with zero extra fields. Test passes with assert_no_extra_fields active.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Full validation, gate check, regression sweep

- [x] T012 Run full test suite: `pytest tests/ -x -q -m "not live"` — zero failures
- [x] T013 Run gate check: `python scripts/generate_progress.py --fixtures | grep "v2/search"` — all gates PASS
- [x] T014 Run quickstart verification steps from `specs/022-fix-contact-search/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 2)**: No dependencies — can start immediately
- **US1 (Phase 3)**: Depends on Phase 2 (needs ContactSearchParams and PageOrderedRequest)
- **US2 (Phase 4)**: No dependency on US1 — can run in parallel after Phase 2
- **Polish (Phase 5)**: Depends on Phase 3 and Phase 4 completion

### Within Each User Story

- Models/restructuring before test validation
- Fixture changes before test assertions

### Parallel Opportunities

- T001 and T002 can run in parallel (different sub-models, same file but independent sections)
- US1 (Phase 3) and US2 (Phase 4) can run in parallel after Phase 2 completes
- T008 and T009 can run in parallel (different files)

---

## Parallel Example: Phase 2

```bash
# Both sub-models can be created together (same file, different sections):
T001: Create ContactSearchParams sub-model
T002: Create PageOrderedRequest sub-model
```

## Parallel Example: US1 + US2

```bash
# After Phase 2, both stories can proceed in parallel:
Phase 3 (US1): Restructure ContactSearchRequest + validate fixture
Phase 4 (US2): Rewrite SearchContactEntityResult + create mock + update test
```

---

## Implementation Strategy

### MVP First (Both stories are P1 — implement sequentially)

1. Complete Phase 2: Create sub-models
2. Complete Phase 3: Fix request model (US1) — validate with fixture
3. Complete Phase 4: Fix response model (US2) — validate with mock
4. Complete Phase 5: Full regression + gate check
5. Single commit with all changes

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- No new dependencies needed — existing pydantic + requests
- The mislabeled fixture (`SearchContactEntityResult.json` in `tests/fixtures/`) must be deleted, not moved
- Mock fixture goes to `tests/fixtures/mocks/SearchContactEntityResult.json` (gate evaluator checks mocks/ as fallback)
- The user specifically requested: exclude `contactDisplayId` and `company` from tests — these belong to `ContactDetailedInfo`, not search results. The spec already reflects this.
