# Tasks: Endpoint Request Mocks

**Input**: Design documents from `/specs/015-endpoint-request-mocks/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested. Existing test suite (232 passed) must remain green. The `test_request_fixtures.py` already auto-discovers and validates request fixtures — no new test files needed.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Fixture generation infrastructure

- [x] T001 Create a fixture generation script at `scripts/generate_request_fixtures.py` that introspects all endpoint classes in `ab/api/endpoints/`, finds Route class attributes with `params_model` or `request_model`, resolves each model class from `ab.api.models`, extracts field aliases via `model_fields`, and writes `tests/fixtures/requests/{ModelClassName}.json` with all fields set to `null`. Skip files that already exist. Print a summary of generated vs skipped files. Follow the algorithm in `specs/015-endpoint-request-mocks/contracts/fixture-generation.md`.

- [x] T002 Run `python scripts/generate_request_fixtures.py` to generate all ~82 null-populated request fixture files in `tests/fixtures/requests/`. Verify the count matches the unique model names from research (37 params_model + ~49 request_model minus overlap). Verify existing `CompanySearchRequest.json` was not overwritten. Verify all generated files are valid JSON with camelCase keys.

- [x] T003 Add `load_request_fixture(model_name: str) -> dict` helper to `tests/conftest.py` that loads from `tests/fixtures/requests/{model_name}.json`. This supplements the existing `load_fixture()` which checks the response fixture directories. Integration tests will use this to load request data.

**Checkpoint**: All fixture files exist on disk. Loading infrastructure ready. Existing tests still pass (232/0/73).

---

## Phase 2: Foundational (Model Tightening)

**Purpose**: Ensure models accurately reflect API-required fields so null fixtures trigger validation errors

- [x] T004 Verify `ab/api/models/address.py` has `AddressValidateParams` with all fields as required (`str = Field(...)` not `Optional[str] = Field(None)`). This was done during clarification — confirm it's committed and tests pass.

- [x] T005 [P] Review `ab/api/models/address.py` — check if `AddressPropertyTypeParams` fields should also be tightened. The API likely requires at least `address1`, `city`, `state`, `zip_code` for property type lookup. If swagger or API behavior confirms, update from `Optional[str]` to `str` with `Field(...)`.

- [x] T006 Run `pytest tests/ --tb=short -q` to confirm 232 passed, 0 failures after model changes. If any test breaks due to model tightening, fix the test to provide valid values or update the model if the field is genuinely optional.

**Checkpoint**: Models reflect API reality. Null fixtures for tightened models will fail validation. Existing tests green.

---

## Phase 3: User Story 1 — Request Mock Fixture Scaffolding (Priority: P1) 🎯 MVP

**Goal**: Every endpoint Route with a params_model or request_model has a null-populated JSON fixture file on disk. Running `pytest tests/integration/test_address.py` after updating it to use fixtures fails with a validation error.

**Independent Test**: `ls tests/fixtures/requests/ | wc -l` shows ~82 files. `python -c "import json; d=json.load(open('tests/fixtures/requests/AddressValidateParams.json')); print(d)"` shows `{"Line1": null, "City": null, "State": null, "Zip": null}`. Loading and validating raises `ValidationError`.

- [x] T007 [US1] Verify the generated `tests/fixtures/requests/AddressValidateParams.json` contains keys `Line1`, `City`, `State`, `Zip` all set to `null`. If the generated file uses wrong keys, fix the generation script to use field aliases (camelCase), not Python field names (snake_case).

- [x] T008 [US1] Write a quick validation test: load `AddressValidateParams.json` from `tests/fixtures/requests/`, attempt `AddressValidateParams.model_validate(data)`, and confirm it raises `ValidationError` because required fields are `null`. This can be done as a manual check or added to `tests/models/test_request_fixtures.py` if it doesn't already cover this case.

- [x] T009 [US1] Spot-check 5 other generated fixtures across different endpoint groups (e.g., `JobSearchParams.json`, `CompanySearchRequest.json`, `QuoteRequestModel.json`, `ContactEditRequest.json`, `ShipmentBookRequest.json`). Verify each is valid JSON with the expected camelCase keys matching their model's field aliases.

**Checkpoint**: All fixture files exist, correctly formatted, and the fail-first pattern is proven with AddressValidateParams.

---

## Phase 4: User Story 2 — Examples Load Request Data from Fixtures (Priority: P2)

**Goal**: Examples load request parameters from fixture files instead of hardcoded values.

**Independent Test**: `python -m examples address --list` shows `request_fixture_file` set. Example code no longer contains hardcoded address values.

- [x] T010 [US2] Modify `examples/_runner.py` — wire `ExampleRunner._run_entry()` to load request data from `tests/fixtures/requests/{entry.request_fixture_file}` when `entry.request_fixture_file` is set. For params_model fixtures (GET endpoints), unpack the dict as `**kwargs` to the endpoint method. For request_model fixtures (POST endpoints), pass the dict as the body argument. Fall back to `entry.call(api)` when `request_fixture_file` is not set.

- [x] T011 [US2] Update `examples/address.py` — set `request_fixture_file="AddressValidateParams.json"` on the `validate` entry. Remove hardcoded `line1`, `city`, `state`, `zip` kwargs from the lambda. Update the lambda to be a method reference or adjust the ExampleRunner call pattern to use fixture data. Keep `response_model` and `fixture_file` unchanged.

- [x] T012 [P] [US2] Update `examples/address.py` — set `request_fixture_file="AddressPropertyTypeParams.json"` on the `get_property_type` entry. Remove hardcoded kwargs.

- [x] T013 [US2] Update remaining examples that have hardcoded request params across `examples/*.py`. For each example entry that has a corresponding request fixture file, set `request_fixture_file` and remove the hardcoded kwargs from the lambda. Priority order: `companies.py`, `jobs.py`, `contacts.py`, `shipments.py`, `autoprice.py`, then all others. Preserve entries that don't have request fixtures (no changes needed).

- [x] T014 [US2] Run `python -m examples --list` to verify all updated examples show their `request_fixture_file` values. Run `ex --list` to confirm examples still render correctly.

**Checkpoint**: Examples load from fixtures. No hardcoded request data remains where a fixture exists.

---

## Phase 5: User Story 3 — Tests Use Fixture-Loaded Request Data (Priority: P2)

**Goal**: Integration tests load request data from the same fixture files as examples. Null fixtures cause validation failures.

**Independent Test**: `pytest tests/integration/test_address.py -v` fails with `ValidationError` when fixture has null values. All fixtures remain null-populated in this feature — populating with real "golden" data is deferred to a follow-up feature.

- [x] T015 [US3] Update `tests/integration/test_address.py` — replace hardcoded address values in `test_validate_address` with `params = load_request_fixture("AddressValidateParams")` followed by `api.address.validate(**params)`. Import `load_request_fixture` from `tests.conftest`.

- [x] T016 [US3] Run `pytest tests/integration/test_address.py -v` and verify it fails with a `ValidationError` because `AddressValidateParams.json` has all `null` values for required fields. Capture the error message to confirm it identifies the null required fields. This failure is the intended outcome — it proves the fail-first pattern works.

- [x] T017 [US3] Update remaining integration tests in `tests/integration/test_*.py` to load request data from fixtures where corresponding fixture files exist. Priority: `test_companies.py`, `test_jobs.py`, `test_contacts.py`, `test_shipments.py`, then others. For each test, replace hardcoded kwargs with `load_request_fixture("ModelName")` unpacked as `**kwargs`.

- [x] T018 [US3] Run `pytest tests/ --tb=short -q` full suite. Verify tests that do NOT load null fixtures still pass (232 baseline). Document the count of fixture-loading tests that now fail with `ValidationError` — these are the expected backlog. Populating these fixtures with real "golden" data is deferred to the next feature.

**Checkpoint**: Tests share fixture data with examples. Null fixtures cause expected validation failures. Baseline tests remain green.

---

## Phase 6: User Story 4 — Progress Review and Fixture Tracking (Priority: P3)

**Goal**: FIXTURES.md and progress report reflect the new request fixtures.

**Independent Test**: `docs/FIXTURES.md` lists all request fixture files. `python scripts/generate_progress.py` runs without errors.

- [x] T020 [P] [US4] Update `docs/FIXTURES.md` to include a section for request fixtures listing every file in `tests/fixtures/requests/` with its status (null-populated vs populated with real data). Follow the existing tracking format used for response fixtures.

- [x] T021 [P] [US4] Run `python scripts/generate_progress.py` and verify it completes without errors. Review the output to ensure fixture gate (G2) counts reflect the new request fixtures if applicable.

- [x] T022 [US4] Run `pytest tests/test_mock_coverage.py -v` to verify the fixture tracking validator passes with the new request fixture files. If the test needs updates to recognize request fixtures, update it.

**Checkpoint**: All fixture tracking documentation is current. Progress report reflects new state.

---

## Phase 7: Polish & Final Verification

**Purpose**: End-to-end validation and cleanup

- [x] T023 Run `ruff check .` on the full codebase. Fix any lint violations introduced by this feature (new script, modified examples, modified tests).

- [x] T024 Run `pytest tests/ --tb=short -q` final full suite verification. Document the expected test count (should be 232+ passed).

- [x] T025 Verify SC-001: `ls tests/fixtures/requests/ | wc -l` matches expected count (~82). Every Route with params_model or request_model has a fixture.

- [x] T026 Verify SC-002: `pytest tests/integration/test_address.py` fails with validation error when fixture has null values. All fixtures remain null-populated in this feature — no revert needed.

- [x] T027 Verify SC-004: Grep examples and tests for hardcoded request parameters that now have fixture files. `grep -r "line1=" examples/address.py` should return no matches.

---

## Dependencies

```
T001 ──> T002 (script must exist before running)
T002 ──> T007, T008, T009 (fixtures must exist before validation)
T003 ──> T015 (load helper must exist before tests use it)
T004 ──> T008 (model must be tightened before validation test)

Phase 1 (T001-T003) ──> Phase 2 (T004-T006)
Phase 2 ──> Phase 3 (T007-T009) [US1 — fixture scaffolding]
Phase 1 ──> Phase 4 (T010-T014) [US2 — examples, needs ExampleRunner wiring]
Phase 1+3 ──> Phase 5 (T015-T018) [US3 — tests, needs fixtures + load helper]
All ──> Phase 6 (T020-T022) [US4 — tracking]
All ──> Phase 7 (T023-T027) [final verification]
```

## Parallel Execution Opportunities

```
Phase 1: T001 creates script → T002 runs it → T003 creates load helper (sequential)
Phase 2: T004 || T005 (different models in same file, but independent checks)
Phase 3: T007 || T008 || T009 (independent fixture validations)
Phase 4: T011 || T012 (different example entries in same file, independent)
Phase 5: T015 then T016 (sequential — update, verify fail). T017 || T018 after T016 (independent test files)
Phase 6: T020 || T021 || T022 (independent documentation/reporting tasks)
Phase 7: T023 || T024 || T025 || T026 || T027 (independent verification)

Cross-phase: Phase 4 (US2) and Phase 5 (US3) can run in parallel after Phase 3 completes
```

## Implementation Strategy

### MVP First (Phase 1-3: US1 Only)

1. Complete Phase 1: Generate all ~82 fixture files + load helper
2. Complete Phase 2: Tighten AddressValidateParams (already done)
3. Complete Phase 3: Validate fixtures are correct and fail-first pattern works
4. **STOP and VALIDATE**: `AddressValidateParams.json` exists with null values, loading it raises ValidationError
5. This alone delivers the core value: visible inventory of all request data needed

### Incremental from MVP

- Phase 4 (US2): Wire examples to fixtures — replaces hardcoded kwargs
- Phase 5 (US3): Wire tests to fixtures — enables fail-first test workflow
- Phase 6 (US4): Update docs — visibility for maintainers
- Phase 7: Final polish and verification
