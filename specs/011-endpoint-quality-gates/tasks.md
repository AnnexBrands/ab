# Tasks: Endpoint Quality Gates

**Input**: Design documents from `/specs/011-endpoint-quality-gates/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test updates are REQUIRED by the feature spec (FR-004, FR-005). Tests are rewritten with substantive assertions.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **SDK package**: `ab/api/models/`, `ab/api/endpoints/`
- **Tests**: `tests/integration/`, `tests/models/`
- **Progress module**: `ab/progress/`
- **Scripts**: `scripts/`
- **Docs**: `docs/api/`, `docs/models/`
- **Tracking**: `FIXTURES.md` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create shared sub-models and test helpers that all user stories depend on

- [x] T001 Create shared sub-models module with Coordinates and CompanyAddress in ab/api/models/common.py
- [x] T002 Add `assert_no_extra_fields(model)` helper to tests/conftest.py that asserts `not model.__pydantic_extra__` with descriptive error message listing undeclared fields
- [x] T003 Register common.py exports (Coordinates, CompanyAddress) in ab/api/models/__init__.py

---

## Phase 2: Foundational — Gate Infrastructure

**Purpose**: Build the gate evaluation engine that MUST be complete before status tracking can work

**CRITICAL**: No progress reporting (US1, US5) can function until gates are evaluable

- [x] T004 Create GateResult and EndpointGateStatus dataclasses in ab/progress/gates.py per data-model.md entities
- [x] T005 [P] Implement G1 (Model Fidelity) evaluator in ab/progress/gates.py — loads fixture, validates against model, checks `__pydantic_extra__`; handles list fixtures, paginated wrappers, and missing model edge cases per contracts/gate-evaluation.md
- [x] T006 [P] Implement G2 (Fixture Status) evaluator in ab/progress/gates.py — checks `tests/fixtures/{ModelName}.json` existence
- [x] T007 [P] Implement G3 (Test Quality) evaluator in ab/progress/gates.py — static analysis of test files for `isinstance` and `__pydantic_extra__` assertions
- [x] T008 [P] Implement G4 (Documentation Accuracy) evaluator in ab/progress/gates.py — reads endpoint method return type annotation and checks docs files for correct `{class}` references
- [x] T009 Implement `evaluate_all_gates()` orchestrator in ab/progress/gates.py that runs G1-G4 for every endpoint in FIXTURES.md, respecting exemptions for no-body endpoints (FR-010)

**Checkpoint**: Gate evaluation engine ready — all four gate dimensions evaluable programmatically

---

## Phase 3: User Story 1 — SDK Developer Trusts Endpoint Status (Priority: P1) MVP

**Goal**: FIXTURES.md and progress.html reflect TRUE endpoint readiness with per-gate pass/fail columns. All currently "complete" endpoints that fail any gate are demoted.

**Independent Test**: Run `python scripts/generate_progress.py` and verify FIXTURES.md shows granular per-gate columns and no false "complete" entries.

### Implementation for User Story 1

- [x] T010 [US1] Create FIXTURES.md generator in ab/progress/fixtures_generator.py — parses existing FIXTURES.md to extract Notes column, evaluates all gates, generates new markdown table with columns: Path, Method, Req Model, Resp Model, G1, G2, G3, G4, Status, Notes; Status="complete" only when all applicable gates pass
- [x] T011 [US1] Add EndpointGateStatus fields (g1-g4 results) to Endpoint dataclass in ab/progress/models.py
- [x] T012 [US1] Update ab/progress/parsers.py to support parsing the new FIXTURES.md format with per-gate columns (backward compatible with old format)
- [x] T013 [US1] Integrate gate evaluation and FIXTURES.md generation into scripts/generate_progress.py — add `--fixtures` flag to regenerate FIXTURES.md from source artifacts
- [x] T014 [US1] Run FIXTURES.md generation against current codebase and commit the result showing all endpoints at their TRUE status (most "complete" endpoints will be demoted due to failing G1/G3/G4)

**Checkpoint**: FIXTURES.md is now truth-based — every "complete" entry has passed all gates. Run `python scripts/generate_progress.py --fixtures` to verify.

---

## Phase 4: User Story 2 — Models Fully Represent API Reality (Priority: P1)

**Goal**: All 15 models with warnings have their missing fields declared as fully typed Pydantic sub-models. Zero `__pydantic_extra__` across all captured fixtures.

**Independent Test**: `pytest tests/models/ -v` — all fixture validation tests pass with zero `__pydantic_extra__` assertions.

### 4a: Simple flat-field models (no sub-models needed)

- [x] T015 [P] [US2] Add missing fields to AddressIsValidResult in ab/api/models/address.py — add dontValidate (bool), countryId (str), countryCode (str), latitude (float), longitude (float), propertyType (int) with camelCase aliases and Field descriptions; verify against tests/fixtures/AddressIsValidResult.json
- [x] T016 [P] [US2] Add notedConditions field (Optional[str]) to CalendarItem in ab/api/models/jobs.py; verify against tests/fixtures/CalendarItem.json
- [x] T017 [P] [US2] Add missing fields to CompanySimple in ab/api/models/companies.py — add parentCompanyId (str), companyName (str), typeId (str) with camelCase aliases; verify against tests/fixtures/CompanySimple.json
- [x] T018 [P] [US2] Add value field (Optional[str]) to ContactTypeEntity in ab/api/models/lookup.py; verify against tests/fixtures/ContactTypeEntity.json
- [x] T019 [P] [US2] Add missing fields to CountryCodeDto in ab/api/models/lookup.py — add id (str), iataCode (str) with camelCase aliases; verify against tests/fixtures/CountryCodeDto.json
- [x] T020 [P] [US2] Add 11 missing fields to FormsShipmentPlan in ab/api/models/forms.py — jobShipmentID, jobID, fromAddressId, toAddressId, providerID, sequenceNo, fromLocationCompanyName, toLocationCompanyName, transportType, providerCompanyName, optionIndex; types derived from tests/fixtures/FormsShipmentPlan.json
- [x] T021 [P] [US2] Add 7 missing fields to RatesState in ab/api/models/shipments.py — fromZip (str), toZip (str), itemWeight (float), services (list), parcelItems (list), parcelServices (list), shipOutDate (str); verify against tests/fixtures/RatesState.json
- [x] T022 [P] [US2] Add customerDisplayId (int) and isActive (bool) to SellerExpandedDto in ab/api/models/sellers.py; verify against tests/fixtures/SellerExpandedDto.json
- [x] T023 [P] [US2] Add SubmitNewLeadPOSTResult field (Optional[Web2LeadGETResult], alias="SubmitNewLeadPOSTResult") to Web2LeadResponse in ab/api/models/web2lead.py

### 4b: ContactSimple — many flat fields

- [x] T024 [US2] Add 23+ missing fields to ContactSimple in ab/api/models/contacts.py — editable, isEmpty, fullNameUpdateRequired, emailsList, phonesList, addressesList, fax, primaryPhone, primaryEmail, and all remaining fields shown in tests/fixtures/ContactSimple.json; derive types from fixture data

### 4c: ContactPrimaryDetails — has nested address

- [x] T025 [US2] Add cellPhone (str), fax (str), and address (Optional[CompanyAddress]) fields to ContactPrimaryDetails in ab/api/models/contacts.py; reuse CompanyAddress from ab/api/models/common.py

### 4d: User — paginated wrapper mismatch

- [x] T026 [US2] Add 18+ missing fields to User in ab/api/models/users.py — login, fullName, contactId, contactDisplayId, contactCompanyName, contactCompanyId, contactCompanyDisplayId, emailConfirmed, contactPhone, contactEmail, password, lockoutDateUtc, lockoutEnabled, role, isActive, legacyId, additionalUserCompanies, additionalUserCompaniesNames, crmContactId; types from tests/fixtures/User.json data[0]
- [x] T027 [US2] Update /users/list endpoint in ab/api/endpoints/users.py to use `_paginated_request()` instead of `_request()` — the fixture shows `{totalCount, data}` wrapper that PaginatedList already handles

### 4e: CompanyDetails — ~20 sub-models (highest complexity)

- [x] T028 [US2] Create CompanyDetailsInfo sub-model (20 fields: displayId, name, taxId, code, parentId, etc.) in ab/api/models/companies.py; type details field as Optional[CompanyDetailsInfo]
- [x] T029 [P] [US2] Create FileInfo sub-model (filePath, newFile) and CompanyPreferences sub-model (18 fields including 4 FileInfo logos) in ab/api/models/companies.py; type preferences field as Optional[CompanyPreferences]
- [x] T030 [P] [US2] Create 10 carrier account sub-models in ab/api/models/companies.py — FedExAccount, UPSAccount, RoadRunnerAccount, MaerskAccount, TeamWWAccount, EstesAccount, ForwardAirAccount, BTXAccount, GlobalTranzAccount, USPSAccount; create AccountInformation parent model referencing all carriers
- [x] T031 [P] [US2] Create pricing sub-models in ab/api/models/companies.py — TransportationCharge, MarkupTier, LaborCharge, AccessorialCharge, Royalties, PaymentSettings; create CompanyPricing parent model referencing all pricing sub-models
- [x] T032 [P] [US2] Create InsuranceOption sub-model and CompanyInsurance parent model (isp, nsp, ltl as InsuranceOption) in ab/api/models/companies.py
- [x] T033 [P] [US2] Create TariffGroup sub-model (groupId, from_, to, toCurb, intoGarage, roomOfChoice, whiteGlove, deleteGroup) in ab/api/models/companies.py; note `from` is a Python keyword — use alias
- [x] T034 [P] [US2] Create TaxCategory sub-model and CompanyTaxes parent model (7 tax categories) in ab/api/models/companies.py
- [x] T035 [US2] Update CompanyDetails model in ab/api/models/companies.py — change details from dict to CompanyDetailsInfo, preferences to CompanyPreferences, add address (CompanyAddress), accountInformation (AccountInformation), pricing (CompanyPricing), insurance (CompanyInsurance), finalMileTariff (List[TariffGroup]), taxes (CompanyTaxes), readOnlyAccess (bool)

### 4f: ShipmentInfo and GlobalAccessorial — nested sub-models

- [x] T036 [P] [US2] Create ShipmentWeight sub-model (pounds, originalWeight, originalWeightMeasureUnit) in ab/api/models/shipments.py; add 10 missing fields to ShipmentInfo (usedAPI, historyProviderName, historyStatuses, weight as ShipmentWeight, jobWeight, successfully, errorMessage, multipleShipments, packages, estimatedDelivery)
- [x] T037 [P] [US2] Create AccessorialOption and RadioButtonOption sub-models in ab/api/models/shipments.py; add 5 missing fields to GlobalAccessorial (description, price, options as List[AccessorialOption], uniqueId, sourceAPIs)

### 4g: Register all new models

- [x] T038 [US2] Register all new sub-model classes in ab/api/models/__init__.py and add to __all__ — includes ~30 new classes from companies.py, shipments.py, common.py

### 4h: Validate zero warnings

- [x] T039 [US2] Run `pytest tests/models/ -v` to verify all 15 updated models validate their fixtures with zero `__pydantic_extra__`; fix any type mismatches discovered during validation

**Checkpoint**: `model_validate(fixture_data)` produces zero `__pydantic_extra__` for ALL captured fixtures.

---

## Phase 5: User Story 3 — Tests Are Substantive and Enforceable (Priority: P1)

**Goal**: Every integration test and fixture-validation test makes substantive assertions. No test contains only `assert result is not None`.

**Independent Test**: `pytest tests/ -v` — all tests pass with isinstance + zero-extra assertions.

### 5a: Rewrite fixture-validation tests (tests/models/)

- [x] T040 [P] [US3] Rewrite tests/models/test_company_models.py — add `assert not model.__pydantic_extra__` after every `model_validate()` call; add domain-specific assertions (e.g., CompanyDetails.id is not None, CompanyDetails.details is not None)
- [x] T041 [P] [US3] Rewrite tests/models/test_contact_models.py — add `__pydantic_extra__` assertions after every model_validate()
- [x] T042 [P] [US3] Rewrite tests/models/test_user_models.py — add `__pydantic_extra__` assertions; handle paginated wrapper (validate data[0] as User)
- [x] T043 [P] [US3] Rewrite tests/models/test_job_models.py — add `__pydantic_extra__` assertions for CalendarItem and all other job models
- [x] T044 [P] [US3] Rewrite tests/models/test_shipment_models.py (or equivalent file) — add `__pydantic_extra__` assertions for ShipmentInfo, RatesState, GlobalAccessorial
- [x] T045 [P] [US3] Rewrite tests/models/test_document_models.py, test_catalog_models.py, test_web2lead_models.py — add `__pydantic_extra__` assertions
- [x] T046 [P] [US3] Rewrite all remaining tests/models/ files — add `__pydantic_extra__` assertions to every test that calls model_validate()

### 5b: Rewrite integration tests (tests/integration/)

- [x] T047 [P] [US3] Rewrite tests/integration/test_companies.py — replace `assert result is not None` with `assert isinstance(result, CompanySimple)` / `CompanyDetails` / etc. + `assert not result.__pydantic_extra__` + domain field assertion
- [x] T048 [P] [US3] Rewrite tests/integration/test_contacts.py — replace trivial assertions with isinstance + __pydantic_extra__ checks for ContactSimple, ContactPrimaryDetails
- [x] T049 [P] [US3] Rewrite tests/integration/test_users.py — replace trivial assertions; handle paginated response from /users/list
- [x] T050 [P] [US3] Rewrite tests/integration/test_jobs.py — replace all 6 trivial assertions with isinstance + __pydantic_extra__ checks
- [x] T051 [P] [US3] Rewrite tests/integration/test_sellers.py, test_catalog.py, test_lots.py — replace trivial assertions
- [x] T052 [P] [US3] Rewrite tests/integration/test_address.py, test_documents.py, test_lookup.py — replace trivial assertions; some already have partial assertions
- [x] T053 [P] [US3] Rewrite tests/integration/test_web2lead.py, test_autoprice.py — update skipped tests to use correct assertion pattern for when they are enabled

### 5c: Verify all tests pass

- [x] T054 [US3] Run full test suite `pytest tests/ -v --tb=short` and fix any failures introduced by model updates or test rewrites

**Checkpoint**: `pytest tests/ -v` passes — every test makes substantive assertions (isinstance + zero extra fields).

---

## Phase 6: User Story 4 — Documentation Shows Correct Types (Priority: P2)

**Goal**: Sphinx docs show actual return types (not `Any`) and model autodoc pages include all new sub-models.

**Independent Test**: `cd docs && make html` builds with zero warnings; spot-check that companies endpoint shows `CompanyDetails` return type.

### 6a: Fix endpoint return type annotations

- [x] T055 [P] [US4] Replace `-> Any` with actual return types in ab/api/endpoints/companies.py — e.g., `get_fulldetails() -> CompanyDetails`, `get_by_id() -> CompanySimple`, `available_by_current_user() -> list[CompanySimple]`
- [x] T056 [P] [US4] Replace `-> Any` with actual return types in ab/api/endpoints/contacts.py
- [x] T057 [P] [US4] Replace `-> Any` with actual return types in ab/api/endpoints/jobs.py
- [x] T058 [P] [US4] Replace `-> Any` with actual return types in ab/api/endpoints/users.py
- [x] T059 [P] [US4] Replace `-> Any` with actual return types in ab/api/endpoints/address.py, documents.py, lookup.py
- [x] T060 [P] [US4] Replace `-> Any` with actual return types in ab/api/endpoints/sellers.py, catalog.py, lots.py
- [x] T061 [P] [US4] Replace `-> Any` with actual return types in ab/api/endpoints/autoprice.py, web2lead.py
- [x] T062 [P] [US4] Replace `-> Any` with actual return types in all remaining endpoint files (shipments.py, forms.py, payments.py, rfq.py, notes.py, partners.py, reports.py, dashboard.py, views.py, commodities.py)

### 6b: Add shared models doc page

- [x] T063 [US4] Create docs/models/common.md with automodule directive for ab.api.models.common (Coordinates, CompanyAddress)
- [x] T064 [US4] Add common.md to the models toctree in docs/index.md

### 6c: Verify docs build

- [x] T065 [US4] Run `cd docs && make html` and fix any warnings — verify endpoint pages show correct return types (not Any) and model pages show all new sub-model fields

**Checkpoint**: `make html` builds with zero warnings. CompanyDetails autodoc shows address, pricing, insurance, etc.

---

## Phase 7: User Story 5 — Progress Dashboard Reflects Gate Status (Priority: P2)

**Goal**: progress.html shows per-endpoint gate status with pass/fail indicators and summary statistics.

**Independent Test**: Run `python scripts/generate_progress.py` and open progress.html; verify per-gate columns visible.

### Implementation for User Story 5

- [x] T066 [US5] Update ab/progress/renderer.py — add per-gate pass/fail badge columns (G1, G2, G3, G4) to endpoint rows in HTML; add summary cards showing per-gate pass rates and overall completion percentage
- [x] T067 [US5] Integrate gate evaluation into scripts/generate_progress.py main flow — evaluate gates for every endpoint and pass results to renderer
- [x] T068 [US5] Generate progress.html with gate status against current codebase and verify output shows multi-dimensional per-endpoint status

**Checkpoint**: `python scripts/generate_progress.py` produces both progress.html and FIXTURES.md with accurate per-gate status.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, cleanup, and documentation

- [x] T069 Run `ruff check .` and fix any lint violations introduced by new code
- [x] T070 Regenerate FIXTURES.md one final time to capture the post-fix state (models updated, tests rewritten, docs fixed) — many previously-demoted endpoints should now pass all gates
- [x] T071 Run full test suite `pytest tests/ -v` as final validation — all tests must pass
- [x] T072 Verify Model Warning Summary in FIXTURES.md is empty (all 15 models fixed) or accurately reflects any remaining issues
- [x] T073 Update specs/011-endpoint-quality-gates/spec.md status from "Draft" to "Implemented"

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 (shared models exist) — BLOCKS US1 and US5
- **US1 — Status Tracking (Phase 3)**: Depends on Phase 2 (gate engine exists)
- **US2 — Model Updates (Phase 4)**: Depends on Phase 1 (shared models) — can start in parallel with Phase 2-3
- **US3 — Test Hardening (Phase 5)**: Depends on Phase 4 (models updated first so tests can pass)
- **US4 — Documentation (Phase 6)**: Depends on Phase 4 (models exist for autodoc) — can parallel with Phase 5
- **US5 — Dashboard (Phase 7)**: Depends on Phase 2 (gate engine) and Phase 3 (FIXTURES.md generator)
- **Polish (Phase 8)**: Depends on all user story phases complete

### User Story Dependencies

```
Phase 1 (Setup)
  └─→ Phase 2 (Gate Infrastructure)
  │     └─→ Phase 3 (US1: Status Tracking)
  │     └─→ Phase 7 (US5: Dashboard) — can parallel with US1
  └─→ Phase 4 (US2: Model Updates) — can parallel with Phase 2
        └─→ Phase 5 (US3: Test Hardening)
        └─→ Phase 6 (US4: Documentation) — can parallel with Phase 5
              └─→ Phase 8 (Polish)
```

### Within Each User Story

- Models before tests (US2 before US3)
- Gate engine before status generation (Phase 2 before US1/US5)
- Return type annotations before doc verification (T055-T062 before T065)

### Parallel Opportunities

- **Phase 1**: T001-T003 are sequential (T003 depends on T001)
- **Phase 2**: T005, T006, T007, T008 can all run in parallel (different gate evaluators)
- **Phase 4a**: T015-T023 can ALL run in parallel (different model files)
- **Phase 4e**: T029-T034 can run in parallel (sub-model groups in same file but independent sections)
- **Phase 5a**: T040-T046 can ALL run in parallel (different test files)
- **Phase 5b**: T047-T053 can ALL run in parallel (different test files)
- **Phase 6a**: T055-T062 can ALL run in parallel (different endpoint files)

---

## Parallel Example: User Story 2 (Model Updates)

```bash
# Launch all simple flat-field model updates in parallel:
T015: AddressIsValidResult in ab/api/models/address.py
T016: CalendarItem in ab/api/models/jobs.py
T017: CompanySimple in ab/api/models/companies.py
T018: ContactTypeEntity in ab/api/models/lookup.py
T019: CountryCodeDto in ab/api/models/lookup.py  # same file as T018 — run sequentially
T020: FormsShipmentPlan in ab/api/models/forms.py
T021: RatesState in ab/api/models/shipments.py
T022: SellerExpandedDto in ab/api/models/sellers.py
T023: Web2LeadResponse in ab/api/models/web2lead.py

# Then launch CompanyDetails sub-model groups in parallel:
T029: FileInfo + CompanyPreferences
T030: 10 carrier account sub-models + AccountInformation
T031: Pricing sub-models + CompanyPricing
T032: InsuranceOption + CompanyInsurance
T033: TariffGroup
T034: TaxCategory + CompanyTaxes
```

---

## Parallel Example: User Story 3 (Test Hardening)

```bash
# Launch all fixture-validation test rewrites in parallel:
T040: test_company_models.py
T041: test_contact_models.py
T042: test_user_models.py
T043: test_job_models.py
T044: test_shipment_models.py (or equivalent)
T045: test_document_models.py, test_catalog_models.py, test_web2lead_models.py
T046: all remaining test files

# Launch all integration test rewrites in parallel:
T047: test_companies.py
T048: test_contacts.py
T049: test_users.py
T050: test_jobs.py
T051: test_sellers.py, test_catalog.py, test_lots.py
T052: test_address.py, test_documents.py, test_lookup.py
T053: test_web2lead.py, test_autoprice.py
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2)

1. Complete Phase 1: Setup (shared models + test helpers)
2. Complete Phase 2: Gate Infrastructure
3. Complete Phase 3: US1 — Generate truthful FIXTURES.md (shows the problem)
4. Complete Phase 4: US2 — Fix all 15 models (fixes the biggest problem)
5. **STOP and VALIDATE**: Regenerate FIXTURES.md — G1 gates should now pass for all 15 models
6. This alone demonstrates massive value: honest status + model fidelity

### Incremental Delivery

1. Setup + Gate Infrastructure → Gate engine ready
2. US1 (Status Tracking) → FIXTURES.md shows honest baseline (MVP!)
3. US2 (Model Updates) → Zero warnings on all fixtures → Regenerate FIXTURES.md (big improvement)
4. US3 (Test Hardening) → All tests substantive → Regenerate FIXTURES.md (G3 gates pass)
5. US4 (Documentation) → Return types fixed → Regenerate FIXTURES.md (G4 gates pass)
6. US5 (Dashboard) → progress.html shows full multi-dimensional view
7. Polish → Final FIXTURES.md reflects reality across all gates

### Critical Path

The critical path is: T001 → T004 → T009 → T010 → T014 (first truthful FIXTURES.md). This can be achieved quickly because it only requires the gate evaluation engine and FIXTURES.md generator — no model updates needed for the initial "honest baseline" generation.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- T018 and T019 both modify ab/api/models/lookup.py — run sequentially
- T028-T035 all modify ab/api/models/companies.py — T028 first (CompanyDetailsInfo), then T029-T034 in parallel (sub-model groups), then T035 last (wires everything into CompanyDetails)
- TariffGroup (T033) must use `from_` with alias `"from"` since `from` is a Python reserved word
- User model (T026-T027) involves both field additions AND endpoint method change — do field additions first
- Commit after each phase checkpoint for context recovery (Constitution Principle VIII)
