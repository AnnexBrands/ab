# Tasks: Unified Test Mock Framework

**Input**: Design documents from `/specs/013-test-mock-framework/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested. Model validation tests already exist and will be enabled by this feature. New tests are only created where infrastructure changes require verification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the mock fixtures directory structure

- [X] T001 Create `tests/fixtures/mocks/` directory with `.gitkeep` file for the manually-authored mock fixture subdirectory

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure changes that MUST complete before user stories — fixture loader fallback, G2 gate enhancement, and coverage tracking update

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T002 Update `load_fixture()` and `require_fixture()` in `tests/conftest.py` to add mock fixture fallback: check `tests/fixtures/{model_name}.json` first, then fall back to `tests/fixtures/mocks/{model_name}.json`. Add `MOCKS_DIR = FIXTURES_DIR / "mocks"` constant. Live fixtures always take precedence. When `require_fixture()` finds a mock fixture, it should still execute the test (not skip). Update the `FileNotFoundError` message to mention both paths when neither exists. Ensure variant fixture names (e.g., `SellerExpandedDto_detail`) also fall back correctly to `mocks/` — the naming convention `{ModelName}_{variant}.json` must work in both directories (FR-008).

- [X] T003 [P] Update G2 gate evaluation in `ab/progress/gates.py` (around line 135-143) to check both `FIXTURES_DIR / f"{model_name}.json"` and `FIXTURES_DIR / "mocks" / f"{model_name}.json"`. Return PASS with provenance info ("live fixture" vs "mock fixture") when either exists. Live path checked first.

- [X] T004 [P] Update `tests/test_mock_coverage.py` to handle the `tests/fixtures/mocks/` subdirectory: (1) `test_all_fixture_files_tracked` should scan both `FIXTURES_DIR.glob("*.json")` and `MOCKS_DIR.glob("*.json")`, (2) `test_captured_fixtures_exist_on_disk` should check both directories for G2=PASS entries, (3) `test_pending_fixtures_do_not_exist_on_disk` should check both directories for G2=FAIL entries.

**Checkpoint**: Fixture loader, G2 gate, and coverage tracking all support mock fixtures in `tests/fixtures/mocks/`. User story implementation can now begin.

---

## Phase 3: User Story 1 — Centralized Test Constants (Priority: P1)

**Goal**: Eliminate all duplicated test identifiers across example files. All consumers import from `tests/constants.py`.

**Independent Test**: Run `grep -rn "TEST_JOB_DISPLAY_ID\|TEST_COMPANY_UUID\|TEST_CONTACT_ID\|TEST_SELLER_ID\|TEST_CATALOG_ID" examples/` and verify zero local definitions — only `from tests.constants import` lines appear.

- [X] T005 [P] [US1] Add docstring comments to each constant in `tests/constants.py` documenting what the identifier represents, its provenance (staging), and which example/test files use it. No value changes needed — just documentation.

- [X] T006 [P] [US1] Replace hardcoded `TEST_JOB_DISPLAY_ID = 2000000` in 11 example files with `from tests.constants import TEST_JOB_DISPLAY_ID`. Files: `examples/notes.py`, `examples/shipments.py`, `examples/onhold.py`, `examples/rfq.py`, `examples/tracking.py`, `examples/documents.py`, `examples/forms.py`, `examples/parcels.py`, `examples/freight_providers.py`, `examples/timeline.py`, `examples/email_sms.py`. Also update `examples/payments.py` and `examples/jobs.py` if they duplicate this constant.

- [X] T007 [P] [US1] Replace hardcoded `TEST_COMPANY_UUID` in `examples/companies.py` (line 7) with `from tests.constants import TEST_COMPANY_UUID`. Replace hardcoded contact ID `30760` in `examples/contacts.py` (3 locations in lambda calls) with `from tests.constants import TEST_CONTACT_ID`. Replace any other hardcoded `TEST_SELLER_ID` or `TEST_CATALOG_ID` duplicates found in example files.

**Checkpoint**: All test identifiers sourced from `tests/constants.py`. No duplicates remain in `examples/`.

---

## Phase 4: User Story 4 — Resolve Currently Failing Endpoints (Priority: P1)

**Goal**: Fix the 13 currently-failing tests (model mismatches, HTTP 404s) and resolve the 32 xfailed tests (missing params_model classes).

**Independent Test**: Run `pytest --tb=short` and verify: (1) zero unexpected failures (previously 13), (2) xfail count reduced from 32 toward 0, (3) no new regressions.

### Model Missing-Field Fixes

- [X] T008 [P] [US4] Add 2 missing fields (`companyName`, `typeId`) to `CompanySimple` model in `ab/api/models/companies.py`. Use the live fixture `tests/fixtures/CompanySimple.json` to determine field types. Fields should be `Optional` with camelCase aliases. After fix, `tests/integration/test_companies.py::test_available_by_current_user` and `tests/models/test_company_models.py::test_company_simple` should pass `assert_no_extra_fields`.

- [X] T009 [US4] Add 97 missing fields to `CompanyDetails` model in `ab/api/models/companies.py` (depends on T008 — same file). Use the live fixture `tests/fixtures/CompanyDetails.json` to determine field names and types. All fields should be `Optional` with camelCase aliases following the existing pattern (snake_case Python name, alias matching JSON key). After fix, `tests/integration/test_companies.py::test_get_details` should pass `assert_no_extra_fields`.

- [X] T010 [P] [US4] Add 30 missing fields to `ContactSimple` model in `ab/api/models/contacts.py`. Fields include: `addressesList`, `assistant`, `birthDate`, `bolNotes`, `careOf`, `company`, `contactDisplayId`, `contactTypeId`, `department`, `editable`, `emailsList`, `fax`, `fullNameUpdateRequired`, `isActive`, `isBusiness`, `isEmpty`, `isPayer`, `isPrefered`, `isPrimary`, `isPrivate`, `jobTitle`, `jobTitleId`, `legacyGuid`, `ownerFranchiseeId`, `phonesList`, `primaryEmail`, `primaryPhone`, `rootContactId`, `taxId`, `webSite`. Use live fixture to determine types. After fix, contact integration tests should pass `assert_no_extra_fields`.

- [X] T011 [P] [US4] Add 6 missing fields (`agent`, `customerCatalogId`, `endDate`, `isCompleted`, `lots`, `startDate`) to `CatalogExpandedDto` model in `ab/api/models/catalog.py`. Use swagger and any available live response data to determine types. After fix, `tests/integration/test_catalog.py::test_list_catalogs` and `test_get_catalog` should pass `assert_no_extra_fields`.

- [X] T012 [P] [US4] Add 4 missing fields (`catalogs`, `imageLinks`, `initialData`, `overridenData`) to `LotDto` model in `ab/api/models/lots.py`. Use swagger to determine types (`catalogs` is likely `List`, `imageLinks` likely `List[str]`, etc.). After fix, `tests/integration/test_lots.py` tests should pass `assert_no_extra_fields`.

### Model Type-Mismatch Fixes

- [X] T013 [P] [US4] Fix `PropertyType` model in `ab/api/models/address.py` — API returns a raw `int` (e.g., `3`) but the model expects `{propertyType: str, confidence: float}`. Either change the endpoint's response_model to `int` or redesign the model to handle integer input. Update `tests/integration/test_address.py::test_get_property_type` accordingly. Check the `address.get_property_type()` method in `ab/api/endpoints/address.py` to see how the response is cast — may need to change the Route's `response_model`.

- [X] T014 [P] [US4] Fix `UserRole` model in `ab/api/models/users.py` — API returns `List[str]` (e.g., `["CorporateAccounting", "Admin"]`) but the model expects `{id: str, name: str}` dicts. Options: (a) change the endpoint return type from `List[UserRole]` to `List[str]` and remove UserRole, or (b) add a string validator to UserRole that wraps strings as `UserRole(name=value)`. Update `tests/integration/test_users.py::test_get_roles` and `tests/models/test_user_models.py` accordingly. Check `tests/fixtures/UserRole.json` for the actual captured data shape.

### HTTP 404 Fixes

- [X] T015 [US4] Investigate and fix HTTP 404 failures for 3 endpoints: (1) `documents.list` in `ab/api/endpoints/documents.py`, (2) `jobs.search` in `ab/api/endpoints/jobs.py`, (3) `jobs.search_by_details` in `ab/api/endpoints/jobs.py`. For each: check the Route path against swagger specs in `ab/api/schemas/acportal.json`, verify the URL pattern is correct, and check if the endpoint requires specific request data. If the 404 is a staging-only issue, add a mock fixture in `tests/fixtures/mocks/` and update the integration test to gracefully handle the 404 (try/except with skip or xfail with reason).

### Params Model Additions (32 xfail resolutions)

- [X] T016 [P] [US4] Create params_model classes for `ab/api/endpoints/companies.py` (3 routes): `_GET_GLOBAL_GEO_SETTINGS`, `_GET_INHERITED_PACKAGING_TARIFFS`, `_GET_INHERITED_PACKAGING_LABOR`. For each: (1) read swagger params from `ab/api/schemas/acportal.json`, (2) create `RequestModel` subclass in `ab/api/models/companies.py` with matching fields, (3) add `params_model="ClassName"` to the Route definition. Follow the pattern established in PR #12.

- [X] T017 [P] [US4] Create params_model classes for `ab/api/endpoints/contacts.py` (4 routes): `_UPDATE_DETAILS`, `_CREATE`, `_GET_HISTORY_AGGREGATED`, `_GET_HISTORY_GRAPH_DATA`. Read swagger params from `ab/api/schemas/acportal.json`, create `RequestModel` subclasses in `ab/api/models/contacts.py`, add `params_model=` to each Route.

- [X] T018 [P] [US4] Create params_model classes for `ab/api/endpoints/dashboard.py` (6 routes): `_GET_GRID_VIEWS`, `_INBOUND`, `_IN_HOUSE`, `_OUTBOUND`, `_LOCAL_DELIVERIES`, `_RECENT_ESTIMATES`. Read swagger params from `ab/api/schemas/acportal.json`, create `RequestModel` subclasses in `ab/api/models/dashboard.py`, add `params_model=` to each Route.

- [X] T019 [P] [US4] Create params_model classes for `ab/api/endpoints/jobs.py` (4 routes): `_POST_TIMELINE`, `_GET_TRACKING_V3`, `_GET_NOTES`, `_LIST_RFQS`. Read swagger params from `ab/api/schemas/acportal.json`, create `RequestModel` subclasses in `ab/api/models/jobs.py`, add `params_model=` to each Route.

- [X] T020 [P] [US4] Create params_model classes for `ab/api/endpoints/forms.py` (3 routes): `_GET_INVOICE`, `_GET_PACKAGING_LABELS`, `_GET_USAR`. Read swagger params from `ab/api/schemas/acportal.json`, create `RequestModel` subclasses in `ab/api/models/forms.py`, add `params_model=` to each Route.

- [X] T021 [P] [US4] Create params_model classes for `ab/api/endpoints/lookup.py` (3 routes): `_ITEMS`, `_DOCUMENT_TYPES`, `_DENSITY_CLASS_MAP`. Read swagger params from `ab/api/schemas/acportal.json`, create `RequestModel` subclasses in `ab/api/models/lookup.py`, add `params_model=` to each Route.

- [X] T022 [P] [US4] Create params_model classes for 4 small endpoint files (1 route each): (1) `ab/api/endpoints/catalog.py` — `_LIST`, (2) `ab/api/endpoints/lots.py` — `_LIST`, (3) `ab/api/endpoints/partners.py` — `_LIST`, (4) `ab/api/endpoints/sellers.py` — `_LIST`. Read swagger params from `ab/api/schemas/catalog.json` (for catalog, lots, sellers) and `ab/api/schemas/acportal.json` (for partners). Create `RequestModel` subclasses in corresponding model files, add `params_model=` to each Route.

- [X] T023 [P] [US4] Create params_model classes for 3 endpoint files: (1) `ab/api/endpoints/payments.py` — `_GET_PAYMENT` (1 route), (2) `ab/api/endpoints/rfq.py` — `_GET_FOR_JOB`, `_ACCEPT_WINNER` (2 routes), (3) `ab/api/endpoints/shipments.py` — `_GET_RATE_QUOTES`, `_GET_SHIPMENT_DOCUMENT` (2 routes). Read swagger params from `ab/api/schemas/acportal.json`, create `RequestModel` subclasses in corresponding model files, add `params_model=` to each Route.

**Checkpoint**: All 13 previously-failing tests either pass or have documented xfails. All 32 xfailed tests have params_model classes and pass. Run `pytest --tb=short` to confirm.

---

## Phase 5: User Story 2 — Offline Model Validation (Priority: P2)

**Goal**: Enable all model validation tests to run without staging credentials by providing mock fixtures for models that lack live fixtures.

**Independent Test**: Run `pytest tests/models/ -v` without staging credentials. Zero skips due to missing fixtures — tests either pass (against mock data) or xfail with documented reasons.

- [ ] T024 [US2] Author mock fixture JSON files in `tests/fixtures/mocks/` for all response models that currently cause test skips (66 model tests). Use the Pydantic model field definitions in `ab/api/models/` to determine the correct JSON structure, field names (camelCase), and realistic placeholder values. Each fixture should be a valid JSON file named `{ModelClassName}.json` that would pass `model_validate()` for the corresponding model. Prioritize models needed to reach the SC-006 target of 50% G2 coverage (at least 45 new fixtures needed). For paginated endpoints (FR-007), mock fixtures MUST include the wrapper structure (`{"data": [...]}` or `{"items": [...]}` or `PaginatedList` shape) — not just the inner model. For variant fixtures (FR-008), use the existing naming convention `{ModelClassName}_{variant}.json` (e.g., `SellerExpandedDto_detail.json`).

- [X] T025 [US2] Update model tests in `tests/models/` that currently use `@pytest.mark.live` and call `require_fixture(..., required=True)` to support both live and mock fixtures: (1) tests backed by live fixtures keep `@pytest.mark.live` and `required=True`, (2) tests backed by mock-only fixtures should use `@pytest.mark.mock` and `required=False` (the fallback loader handles the rest). Verify that `pytest tests/models/` produces zero skips and all tests either pass or are explicitly xfailed.

**Checkpoint**: `pytest tests/models/` runs fully offline with no fixture-related skips. SC-001 satisfied.

---

## Phase 6: User Story 3 — Reusable Mock Data for Sphinx Documentation (Priority: P3)

**Goal**: Sphinx documentation builds offline using mock fixture data for example responses.

**Independent Test**: Run `make html` in `docs/` without staging credentials. Verify documentation renders with example response data.

- [X] T026 [US3] Verify Sphinx documentation builds successfully without staging credentials (`cd docs && make html`). If build fails due to missing fixture data or import errors from example files, fix the issues: (1) ensure example files import from `tests.constants` (completed in US1), (2) ensure mock fixtures provide data for any Sphinx autodoc references, (3) fix any broken cross-references. Document any remaining gaps in build output.

**Checkpoint**: Sphinx docs build cleanly without staging access. SC-004 satisfied.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Regenerate tracking artifacts, validate all success criteria, and ensure consistency

- [X] T027 Regenerate `FIXTURES.md` by running the gate evaluation: `python -m ab.progress.fixtures_generator` (or equivalent script in `scripts/generate_progress.py`). Verify that G2 counts reflect the new mock fixtures and that the total fixture coverage meets SC-006 target (≥50%).

- [X] T028 Run full test suite validation: `pytest --tb=short -v`. Verify all success criteria: (1) SC-001: zero model test skips, (2) SC-002: zero unexpected failures + xfail triage complete, (3) SC-003: no duplicate constants, (4) SC-005: mock fixture authoring pattern is clear, (5) SC-006: G2 coverage ≥50%.

- [X] T029 Run `ruff check .` to verify no linting regressions from the changes. Fix any issues introduced by new model fields, params models, or import changes.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **US1 Constants (Phase 3)**: Depends on Phase 2 — can run in parallel with US4
- **US4 Resolve Failures (Phase 4)**: Depends on Phase 2 — can run in parallel with US1
  - Model fixes (T008-T014) can all run in parallel
  - HTTP 404 fix (T015) independent of model fixes
  - Params model additions (T016-T023) can all run in parallel, independent of model fixes
- **US2 Offline Testing (Phase 5)**: Depends on Phase 2 (loader fallback) and Phase 4 (model fixes)
- **US3 Sphinx Docs (Phase 6)**: Depends on Phase 3 (constants) and Phase 5 (mock fixtures available)
- **Polish (Phase 7)**: Depends on all user stories complete

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational — no dependencies on other stories
- **US4 (P1)**: Can start after Foundational — no dependencies on other stories
- **US2 (P2)**: Depends on US4 (model fixes must be done before mock fixtures make sense)
- **US3 (P3)**: Depends on US1 (constants) + US2 (mock fixtures)

### Within Each User Story

- Models before tests (fix the model, then tests pass)
- Infrastructure before content (loader fallback before mock fixtures)
- Commit after each logical group of changes

### Parallel Opportunities

- T002, T003, T004 are partially parallelizable (T003 and T004 touch different files)
- T005, T006, T007 can all run in parallel (different files)
- T008–T014 can all run in parallel (different model files, except T008+T009 share companies.py)
- T016–T023 can all run in parallel (different endpoint files)
- US1 and US4 can run in parallel after Phase 2

---

## Parallel Example: User Story 4

```bash
# Launch all model fixes in parallel (different files):
Task: "Fix CompanySimple in ab/api/models/companies.py"        # T008
Task: "Fix ContactSimple in ab/api/models/contacts.py"          # T010
Task: "Fix CatalogExpandedDto in ab/api/models/catalog.py"      # T011
Task: "Fix LotDto in ab/api/models/lots.py"                     # T012
Task: "Fix PropertyType in ab/api/models/address.py"            # T013
Task: "Fix UserRole in ab/api/models/users.py"                  # T014

# After T008 completes, launch T009 (same file):
Task: "Fix CompanyDetails in ab/api/models/companies.py"        # T009

# Launch all params model tasks in parallel (different files):
Task: "Params models for companies.py"    # T016
Task: "Params models for contacts.py"     # T017
Task: "Params models for dashboard.py"    # T018
Task: "Params models for jobs.py"         # T019
Task: "Params models for forms.py"        # T020
Task: "Params models for lookup.py"       # T021
Task: "Params models for catalog/lots/partners/sellers"  # T022
Task: "Params models for payments/rfq/shipments"         # T023
```

---

## Implementation Strategy

### MVP First (US1 + US4)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational (T002–T004)
3. Complete Phase 3: US1 Constants (T005–T007) — in parallel with Phase 4
4. Complete Phase 4: US4 Resolve Failures (T008–T023)
5. **STOP and VALIDATE**: Run `pytest --tb=short` — all 13 failures and 32 xfails resolved
6. This is the MVP — test suite is green

### Incremental Delivery

1. Setup + Foundational → Loader + gates ready
2. Add US1 (Constants) → No more duplicate identifiers
3. Add US4 (Fix Failures) → Test suite green (MVP!)
4. Add US2 (Mock Fixtures) → Offline model testing enabled
5. Add US3 (Sphinx Docs) → Docs build offline
6. Polish → FIXTURES.md regenerated, all SC verified

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- T008 and T009 share `ab/api/models/companies.py` — run T008 first (2 fields), then T009 (97 fields)
- T024 is the largest task (authoring ~45+ mock fixture JSON files) — this is intentionally manual work per clarification session
- Params model tasks (T016–T023) follow the pattern from PR #12: read swagger → create RequestModel → add params_model to Route
- Commit after each phase checkpoint
