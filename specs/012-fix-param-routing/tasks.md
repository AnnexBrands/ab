# Tasks: Fix Parameter Routing

**Input**: Design documents from `/specs/012-fix-param-routing/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in the spec. Test tasks included only where existing tests need updating (test_example_params.py).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `ab/` (SDK source), `tests/` at repository root
- Swagger specs: `ab/api/schemas/acportal.json`

---

## Phase 1: Setup

**Purpose**: Verify existing infrastructure supports params_model dispatch — no new setup required

- [x] T001 Verify `BaseEndpoint._request()` params_model validation path works by reading ab/api/base.py lines 69-74 and confirming the `route.params_model` → `.check()` → `kwargs["params"]` flow requires no code changes
- [x] T002 Verify `Route.params_model` field exists and is correctly passed through `Route.bind()` by reading ab/api/route.py

**Checkpoint**: Confirmed that zero infrastructure changes are needed — params_model dispatch is already wired in base.py and route.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create the first params model to validate the pattern end-to-end before scaling to all endpoints

**⚠️ CRITICAL**: This model proves the pattern works before Tier 1/Tier 2 rollout

- [x] T003 Create `AddressValidateParams` model in ab/api/models/address.py — extend `RequestModel` with fields: `line1: Optional[str] = Field(None, alias="Line1", description="Street address line 1")`, `city: Optional[str] = Field(None, alias="City", description="City name")`, `state: Optional[str] = Field(None, alias="State", description="State abbreviation")`, `zip: Optional[str] = Field(None, alias="Zip", description="ZIP/postal code")` per data-model.md
- [x] T004 Export `AddressValidateParams` from ab/api/models/__init__.py
- [x] T005 Add `params_model="AddressValidateParams"` to the `_IS_VALID` Route definition in ab/api/endpoints/address.py
- [x] T006 Refactor `AddressEndpoint.validate()` in ab/api/endpoints/address.py — replace manual dict construction (`params = {}; if line1: params["Line1"] = line1; ...`) with `params=dict(line1=line1, city=city, state=state, zip=zip)` while keeping typed signature for IDE autocomplete. The Route's params_model handles alias mapping and None exclusion via `.check()`

**Checkpoint**: `api.address.validate(line1="123 Main St", city="Columbus", state="OH", zip="43213")` sends correct query params via params_model dispatch — SC-006 verified

---

## Phase 3: User Story 1 — SDK Callers Get Correct Parameter Routing (Priority: P1) 🎯 MVP

**Goal**: All 5 manual-dict endpoints refactored to use params_model dispatch with typed signatures. Zero manual dict construction remains.

**Independent Test**: Call each refactored endpoint and confirm query params arrive as URL query string with correct aliased names.

### Implementation for User Story 1

- [x] T007 [P] [US1] Create `AddressPropertyTypeParams` model in ab/api/models/address.py — fields: `address1: Optional[str] = Field(None, alias="Address1", description="Street address line 1")`, `address2: Optional[str] = Field(None, alias="Address2", description="Street address line 2")`, `city: Optional[str] = Field(None, alias="City", description="City name")`, `state: Optional[str] = Field(None, alias="State", description="State abbreviation")`, `zip_code: Optional[str] = Field(None, alias="ZipCode", description="ZIP/postal code")` per data-model.md
- [x] T008 [P] [US1] Create `BillOfLadingParams` model in ab/api/models/forms.py — fields: `shipment_plan_id: Optional[str] = Field(None, alias="shipmentPlanId", description="Shipment plan identifier")`, `provider_option_index: Optional[int] = Field(None, alias="providerOptionIndex", description="Provider option index")` per data-model.md
- [x] T009 [US1] Create `OperationsFormParams` model in ab/api/models/forms.py — fields: `ops_type: Optional[str] = Field(None, alias="type", description="Operations form type")` per data-model.md (sequence after T008 — same file)
- [x] T010 [P] [US1] Create `DocumentListParams` model in ab/api/models/documents.py — fields: `job_display_id: Optional[str] = Field(None, alias="jobDisplayId", description="Job display identifier")` per data-model.md
- [x] T011 [US1] Export `AddressPropertyTypeParams`, `BillOfLadingParams`, `OperationsFormParams`, `DocumentListParams` from ab/api/models/__init__.py
- [x] T012 [US1] Add `params_model="AddressPropertyTypeParams"` to the `_PROPERTY_TYPE` Route in ab/api/endpoints/address.py and refactor `get_property_type()` — replace manual dict construction with `params=dict(address1=address1, address2=address2, city=city, state=state, zip_code=zip_code)` keeping typed signature
- [x] T013 [US1] Add `params_model="BillOfLadingParams"` to the `_GET_BOL` Route in ab/api/endpoints/forms.py and refactor `get_bill_of_lading()` — replace manual dict construction with `params=dict(shipment_plan_id=shipment_plan_id, provider_option_index=provider_option_index)` keeping typed signature with path param bound via `.bind()`
- [x] T014 [US1] Add `params_model="OperationsFormParams"` to the `_GET_OPERATIONS` Route in ab/api/endpoints/forms.py and refactor `get_operations()` — replace manual dict construction with `params=dict(ops_type=ops_type)` keeping typed signature with path param bound via `.bind()`
- [x] T015 [US1] Add `params_model="DocumentListParams"` to the `_LIST` Route in ab/api/endpoints/documents.py and refactor `list()` — replace `if job_display_id: params["jobDisplayId"] = job_display_id` pattern with `params=dict(job_display_id=job_display_id, **params)` keeping typed signature. Note: this method also accepts `**params` for additional query params — preserve that capability
- [x] T016 [US1] Run `ruff check ab/api/endpoints/address.py ab/api/endpoints/forms.py ab/api/endpoints/documents.py ab/api/models/address.py ab/api/models/forms.py ab/api/models/documents.py` to verify no lint violations

**Checkpoint**: All 5 manual-dict methods refactored. SC-003 verified for Tier 1 — zero manual dict construction in address.py, forms.py, documents.py

---

## Phase 4: User Story 2 — Single Unified Pattern for All Endpoint Methods (Priority: P1)

**Goal**: All 12 kwargs-params endpoints gain params_model validation with typed signatures. Every query-param endpoint uses the same dispatch pattern.

**Independent Test**: Call any kwargs-params endpoint with an invalid parameter name and confirm a ValidationError is raised before the HTTP request is sent.

### Implementation for User Story 2

> Each task below requires: (1) research swagger spec in ab/api/schemas/acportal.json for exact query param names, (2) create params model, (3) add params_model to Route, (4) update endpoint method signature from `**kwargs`/`**params` to explicit typed params. All model tasks are parallelizable (different files).

- [x] T017 [P] [US2] Research swagger params for `GET /companies/geoAreaCompanies`, `GET /companies/search/carrier-accounts`, `GET /companies/suggest-carriers` in ab/api/schemas/acportal.json and create `GeoAreaCompaniesParams`, `CarrierAccountSearchParams`, `SuggestCarriersParams` models in ab/api/models/companies.py — include `description=` on every Field, derived from swagger parameter description
- [x] T018 [P] [US2] Research swagger params for `GET /dashboard` in ab/api/schemas/acportal.json and create `DashboardParams` model in ab/api/models/dashboard.py — include `description=` on every Field, derived from swagger parameter description
- [x] T019 [P] [US2] Research swagger params for `GET /job/search`, `GET /job/{jobId}/notes`, `GET /job/{jobId}/freight-providers` in ab/api/schemas/acportal.json and create `JobSearchParams`, `JobNotesParams`, `FreightProvidersParams` models in ab/api/models/jobs.py — include `description=` on every Field, derived from swagger parameter description
- [x] T020 [P] [US2] Research swagger params for `GET /notes`, `GET /notes/suggest-users` in ab/api/schemas/acportal.json and create `NotesListParams`, `NotesSuggestUsersParams` models in ab/api/models/notes.py — include `description=` on every Field, derived from swagger parameter description
- [x] T021 [P] [US2] Research swagger params for `GET /shipment/{id}` in ab/api/schemas/acportal.json and create `ShipmentParams` model in ab/api/models/shipments.py — include `description=` on every Field, derived from swagger parameter description
- [x] T022 [P] [US2] Research swagger params for `GET /web2lead` in ab/api/schemas/acportal.json and create `Web2LeadGetParams` model in ab/api/models/web2lead.py — include `description=` on every Field, derived from swagger parameter description
- [x] T023 [US2] Export all new Tier 2 params models from ab/api/models/__init__.py — `GeoAreaCompaniesParams`, `CarrierAccountSearchParams`, `SuggestCarriersParams`, `DashboardParams`, `JobSearchParams`, `JobNotesParams`, `FreightProvidersParams`, `NotesListParams`, `NotesSuggestUsersParams`, `ShipmentParams`, `Web2LeadGetParams`
- [x] T024 [US2] Update ab/api/endpoints/companies.py — add `params_model=` to Routes for `_GET_GEO_AREA_COMPANIES`, `_SEARCH_CARRIER_ACCOUNTS`, `_SUGGEST_CARRIERS`; refactor `get_geo_area_companies()`, `search_carrier_accounts()`, `suggest_carriers()` from `**params` to typed signatures with `params=dict(...)`
- [x] T025 [US2] Update ab/api/endpoints/dashboard.py — add `params_model="DashboardParams"` to the `_GET` Route; refactor `get()` from `**params` to typed signature
- [x] T026 [US2] Update ab/api/endpoints/jobs.py — add `params_model=` to Routes for `_SEARCH`, `_GET_NOTES`, `_LIST_FREIGHT_PROVIDERS`; refactor `search()`, `get_notes()`, `list_freight_providers()` from `**kwargs`/`**params` to typed signatures
- [x] T027 [US2] Update ab/api/endpoints/notes.py — add `params_model=` to Routes for `_LIST`, `_SUGGEST_USERS`; refactor `list()`, `suggest_users()` from `**kwargs`/`**params` to typed signatures
- [x] T028 [US2] Update ab/api/endpoints/shipments.py — add `params_model="ShipmentParams"` to `_GET_SHIPMENT` Route; refactor `get_shipment()` from `**params` to typed signature
- [x] T029 [US2] Update ab/api/endpoints/web2lead.py — add `params_model="Web2LeadGetParams"` to `_GET` Route; refactor `get()` from `**params` to typed signature
- [x] T030 [US2] Run `ruff check ab/api/endpoints/companies.py ab/api/endpoints/dashboard.py ab/api/endpoints/jobs.py ab/api/endpoints/notes.py ab/api/endpoints/shipments.py ab/api/endpoints/web2lead.py` to verify no lint violations

**Checkpoint**: All 17 query-param endpoints (5 Tier 1 + 12 Tier 2) use params_model dispatch with typed signatures. SC-001, SC-003, SC-005 verified.

---

## Phase 5: User Story 3 — Quality Gates and Progress Report (Priority: P2)

**Goal**: New G5 gate evaluates parameter routing correctness. Progress HTML report and FIXTURES.md display G5 alongside G1-G4. G5 auto-passes for endpoints with no query/body params.

**Independent Test**: Run `python scripts/generate_progress.py` and confirm G5 column appears in the output with correct pass/fail per endpoint.

### Implementation for User Story 3

- [x] T031 [P] [US3] Add `g5_param_routing: GateResult | None = None` field to `EndpointGateStatus` dataclass in ab/progress/models.py; update `compute_overall()` to include G5 in gate check only when G5 is not None (auto-pass for no-param endpoints per FR-009 clarification)
- [x] T032 [US3] Implement `evaluate_g5()` function in ab/progress/gates.py — load swagger spec for the endpoint path, check: (1) if swagger has `"in": "query"` params → Route must have `params_model`, (2) if swagger has `requestBody` → Route must have `request_model`, (3) if swagger has `"in": "path"` params → Route `_path_params` must match. Auto-pass if no params. Return GateResult with gate="G5"
- [x] T033 [US3] Update `evaluate_endpoint_gates()` in ab/progress/gates.py to call `evaluate_g5()` and assign result to `status.g5_param_routing`. Pass Route definitions needed for G5 evaluation (will need to load Route objects from endpoint modules or accept params_model/request_model as arguments)
- [x] T034 [US3] Update HTML renderer in ab/progress/renderer.py — add G5 column to the per-endpoint gate details table, add G5 summary card alongside G1-G4 cards, update column count/CSS styling
- [x] T035 [US3] Update FIXTURES.md generator in ab/progress/fixtures_generator.py — add G5 column to table header, include G5 badge (PASS/FAIL) in each endpoint row, update summary statistics to include G5 pass rate
- [x] T036 [US3] Update `evaluate_all_gates()` in ab/progress/gates.py to pass the necessary Route metadata (params_model, request_model) to `evaluate_endpoint_gates()` for G5 evaluation. This may require extending the `fixtures_data` dict format or loading Route definitions from endpoint modules
- [x] T037 [US3] Run `python scripts/generate_progress.py` and verify G5 column appears correctly; run `python scripts/generate_progress.py --fixtures` and verify FIXTURES.md includes G5 column

**Checkpoint**: Progress report shows G5 alongside G1-G4. SC-004 verified. Endpoints with params_model show G5 PASS; those without (but needing one) show G5 FAIL.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Test updates, documentation, and final validation across all stories

- [x] T038 [P] Extend tests/test_example_params.py — add test that verifies every Route with query-param endpoints (identified from swagger `"in": "query"`) has `params_model` set. This enforces the new pattern going forward
- [x] T039 [P] Run full test suite via `pytest` from repository root to verify no regressions from endpoint method signature changes
- [x] T040 Run `ruff check .` across the entire repository to verify no lint violations
- [x] T041 Verify SC-006 end-to-end: confirm `api.address.validate(line1="...", city="...", state="...", zip="...")` produces correct HTTP query string via params_model dispatch (manual or integration test verification)
- [x] T042 Verify all files in examples/ still work after endpoint signature changes — run each example script and confirm no TypeError or missing-argument errors from refactored typed signatures in address.py, forms.py, documents.py, companies.py, dashboard.py, jobs.py, notes.py, shipments.py, web2lead.py
- [x] T043 [P] Update Sphinx docs to include all new params models — add autodoc entries for AddressValidateParams, AddressPropertyTypeParams, BillOfLadingParams, OperationsFormParams, DocumentListParams, and all Tier 2 params models in the appropriate docs/api/models/*.rst files

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — verification only, can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — creates the first params model and proves the pattern
- **US1 (Phase 3)**: Depends on Phase 2 — extends the proven pattern to remaining Tier 1 endpoints
- **US2 (Phase 4)**: Depends on Phase 2 — can run in parallel with US1 (different files)
- **US3 (Phase 5)**: Can start after Phase 2 — independent of US1/US2 (different files: progress/ vs endpoints/)
- **Polish (Phase 6)**: Depends on Phases 3, 4, 5 all being complete

### User Story Dependencies

- **US1 (P1)**: Depends on Foundational (Phase 2) — no dependency on other stories
- **US2 (P1)**: Depends on Foundational (Phase 2) — no dependency on US1 (different endpoint files)
- **US3 (P2)**: Depends on Foundational (Phase 2) — no dependency on US1/US2 (gates/progress files are independent)

### Within Each User Story

- Models before Route updates
- Route updates before endpoint refactors
- Endpoint refactors before lint checks
- All [P] model tasks within a phase can run in parallel

### Parallel Opportunities

- T007, T008, T009, T010 can all run in parallel (different model files)
- T017–T022 can all run in parallel (Tier 2 swagger research + model creation, different files)
- T031, T032 can run in parallel (models.py vs gates.py)
- US1 (Phase 3) and US2 (Phase 4) can run in parallel after Foundational
- US3 (Phase 5) can run in parallel with US1 and US2

---

## Parallel Example: User Story 1

```bash
# Launch all Tier 1 model creation tasks in parallel (different files):
Task: "Create AddressPropertyTypeParams in ab/api/models/address.py"      # T007
Task: "Create BillOfLadingParams in ab/api/models/forms.py"               # T008
Task: "Create OperationsFormParams in ab/api/models/forms.py"             # T009 (same file as T008 — sequence after T008)
Task: "Create DocumentListParams in ab/api/models/documents.py"           # T010

# After models created, refactor endpoints in parallel (different files):
Task: "Refactor address.py get_property_type()"                           # T012
Task: "Refactor forms.py get_bill_of_lading() and get_operations()"       # T013, T014
Task: "Refactor documents.py list()"                                       # T015
```

---

## Parallel Example: User Story 2

```bash
# Launch all Tier 2 swagger research + model creation in parallel (different files):
Task: "Research + create company params models"    # T017
Task: "Research + create dashboard params model"   # T018
Task: "Research + create job params models"        # T019
Task: "Research + create notes params models"      # T020
Task: "Research + create shipment params model"    # T021
Task: "Research + create web2lead params model"    # T022
```

---

## Implementation Strategy

### MVP First (Foundational + User Story 1 Only)

1. Complete Phase 1: Setup (verify infrastructure)
2. Complete Phase 2: Foundational (create AddressValidateParams, prove pattern works)
3. Complete Phase 3: User Story 1 (remaining Tier 1 endpoints)
4. **STOP and VALIDATE**: SC-006 — `api.address.validate()` works correctly
5. The original reported bug is fixed at this point

### Incremental Delivery

1. Foundational → Pattern validated with address.validate
2. US1 → All 5 manual-dict endpoints fixed → Deploy/Demo (Tier 1 complete)
3. US2 → All 12 kwargs-params endpoints gain validation → Deploy/Demo (Tier 2 complete)
4. US3 → G5 gate + progress report → Deploy/Demo (quality tracking complete)
5. Polish → Tests, lint, final validation

### Parallel Team Strategy

With multiple developers after Foundational is done:
- Developer A: US1 (Tier 1 endpoints — address.py, forms.py, documents.py)
- Developer B: US2 (Tier 2 endpoints — companies.py, dashboard.py, jobs.py, notes.py, shipments.py, web2lead.py)
- Developer C: US3 (G5 gate + progress report — gates.py, models.py, renderer.py, fixtures_generator.py)

All three work on completely different files with zero conflicts.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Typed signatures preserved per clarification — methods keep explicit named params for IDE autocomplete
- G5 auto-passes for path-only/parameterless endpoints per clarification
- T008 and T009 both modify forms.py models — T009 has no [P] marker, must sequence after T008
- Commit after each phase checkpoint
- The `_request()` method in base.py requires NO changes — params_model validation is already wired
