# Tasks: Fix FreightProviders Drift

**Input**: Design documents from `/specs/033-fix-freightproviders-drift/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: No new project setup needed — existing SDK. Verify current state.

- [x] T001 Verify current freight model test skips by running `pytest tests/models/test_freight_models.py -v` and confirm empty-fixture skip behavior
- [x] T002 Verify CLI warning output by running `abs job list_freight_providers 2000000` and capturing the list of extra fields reported

**Checkpoint**: Baseline captured — extra fields and skip behavior documented for comparison

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create shared models (CarrierAPI enum, CarrierAccountInfo) that both PricedFreightProvider and ShipmentPlanProvider depend on

- [x] T003 [P] Add `CarrierAPI` IntEnum class with values (0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14, 20) in `ab/api/models/jobs.py` — place before PricedFreightProvider definition
- [x] T004 [P] Add `CarrierAccountInfo` ResponseModel class with fields `id` (int), `key` (Optional[str]), `friendly_name` (Optional[str], alias="friendlyName") in `ab/api/models/jobs.py` — place before PricedFreightProvider definition
- [x] T005 Research RateQuoteRequest and FreightItemsRequest swagger schemas in `ab/api/schemas/acportal.json` — search for the POST freightproviders/{optionIndex}/ratequote and POST freightitems requestBody definitions; document found fields in research.md under R3/R4

**Checkpoint**: Foundation ready — shared models exist, request schema research complete

---

## Phase 3: User Story 1 - Accurate Response Model (Priority: P1)

**Goal**: Expand all freight models from stubs to full swagger-matching typed fields so the SDK produces zero extra-field warnings

**Independent Test**: `abs job list_freight_providers 2000000` produces no "extra fields not in model" warnings

### Implementation for User Story 1

- [x] T006 [US1] Expand `PricedFreightProvider` in `ab/api/models/jobs.py` — replace 3 stub fields (`provider_name`, `service_types`, `rate_available`) with 15 typed fields per data-model.md: `option_index` (int), `shipment_type` (str), `provider_api` (CarrierAPI), `provider_id` (Optional[str]), `provider_code` (Optional[str]), `provider_company_name` (Optional[str]), `total_sell` (float), `transit` (Optional[int]), `quote_no` (Optional[str]), `pro_num` (Optional[str]), `option_active` (bool), `shipment_accepted` (bool), `shipment_accepted_date` (Optional[str]), `obtain_nfm_job_state` (Optional[str]), `used_carrier_account_info` (CarrierAccountInfo) — each with alias and description
- [x] T007 [US1] Expand `ShipmentPlanProvider` in `ab/api/models/jobs.py` — replace stub `provider_data: dict` with 22+ typed fields per data-model.md including `job_id`, `freight_quote_options_id`, `provider_id`, `is_primary`, `provider_company_code`, `provider_company_name`, `original_company_name`, `freight_amount`, `accessorial_amount`, `caf_note`, `quote_no`, `pro_num`, `transit`, `shipment_type`, `miles`, `logo`, `option_index`, `option_active`, `shipment_accepted`, `shipment_accepted_date`, `used_api` (CarrierAPI), `bill_to_franchisee_id`, `bill_to_company_code`, `obtain_nfm_job_state`, `used_carrier_account_info` (CarrierAccountInfo) — each with alias and description
- [x] T008 [US1] Expand `RateQuoteRequest` in `ab/api/models/jobs.py` — replace stub `options: dict` with typed fields based on T005 swagger research findings
- [x] T009 [US1] Expand `FreightItemsRequest` in `ab/api/models/jobs.py` — replace stub `items: List[dict]` with typed fields based on T005 swagger research findings
- [x] T010 [US1] Update imports in `ab/api/models/jobs.py` if needed — add `IntEnum` import, ensure `CarrierAPI` and `CarrierAccountInfo` are exported in `__all__` or public namespace
- [x] T011 [US1] Verify expanded models compile and pass basic validation by running `python -c "from ab.api.models.jobs import PricedFreightProvider, ShipmentPlanProvider, CarrierAccountInfo, CarrierAPI"`

**Checkpoint**: All freight models expanded with typed fields — zero-warning SDK calls expected

---

## Phase 4: User Story 2 - Realistic Fixtures and Passing Tests (Priority: P1)

**Goal**: Replace empty/null fixtures with real captured data and ensure all tests execute against populated data (no skips)

**Independent Test**: `pytest tests/models/test_freight_models.py -v` — all tests PASS with no skips

**Depends on**: US1 (models must be expanded before fixtures can validate against them)

### Implementation for User Story 2

- [x] T012 [US2] Capture live response fixture by running `python examples/freight_providers.py` (or `abs job list_freight_providers 2000000 --raw`) and saving the populated response to `tests/fixtures/PricedFreightProvider.json` — must contain at least one fully populated object, not `[]`
- [x] T013 [US2] Update request fixture `tests/fixtures/requests/ShipmentPlanProvider.json` — replace null stubs with realistic non-null sample values matching the expanded ShipmentPlanProvider model fields
- [x] T014 [US2] Update request fixture `tests/fixtures/requests/FreightProvidersParams.json` — replace null stubs with realistic non-null sample values (e.g., `ProviderIndexes: [0, 1]`, `OnlyActive: true`)
- [x] T015 [US2] Create or update request fixture `tests/fixtures/requests/RateQuoteRequest.json` — populate with realistic fields matching the expanded RateQuoteRequest model
- [x] T016 [US2] Update request fixture `tests/fixtures/requests/FreightItemsRequest.json` — replace null stubs with realistic fields matching the expanded FreightItemsRequest model
- [x] T017 [US2] Update `tests/models/test_freight_models.py` — add test methods for `CarrierAccountInfo`, `ShipmentPlanProvider`, `RateQuoteRequest`, `FreightItemsRequest`; ensure `test_priced_freight_provider` validates against populated fixture (no skip); add `assert_no_extra_fields` assertion to each test
- [x] T018 [US2] Run full freight test suite: `pytest tests/models/test_freight_models.py -v` — confirm all tests PASS (zero skips, zero extra-field warnings)

**Checkpoint**: All fixtures populated with real data, all model tests pass without skips

---

## Phase 5: User Story 3 - Consistent Progress Artifacts (Priority: P1)

**Goal**: Reconcile api-surface.md, FIXTURES.md, and progress.html so they all agree on freight provider implementation status

**Independent Test**: Regenerate progress artifacts and verify no contradictions in freight provider section

**Depends on**: US2 (fixtures must be populated before gates can be evaluated legitimately)

### Implementation for User Story 3

- [x] T019 [US3] Update `specs/api-surface.md` — in the "Job — Freight Providers" group (around line 485), change the AB column from "—" to done markers for all 3 endpoints and update "AB done: 0 of 3" to "AB done: 3 of 3"
- [x] T020 [US3] Regenerate FIXTURES.md by running `python scripts/generate_progress.py --fixtures` — verify freight provider gate columns reflect true status based on expanded models and populated fixtures
- [x] T021 [US3] Regenerate progress.html by running `python scripts/generate_progress.py` — verify freightproviders group shows consistent status with no "not started" tier classification for implemented endpoints
- [x] T022 [US3] Manually verify consistency: freight provider endpoints show matching status across api-surface.md (done), FIXTURES.md (gate results), and progress.html (tier classification)

**Checkpoint**: All three progress artifacts agree on freight provider status — no contradictions

---

## Phase 6: User Story 4 - Updated Documentation and Examples (Priority: P2)

**Goal**: Update runnable example and Sphinx docs to reflect complete freight models

**Independent Test**: Run example script without warnings; Sphinx docs show all model fields

**Depends on**: US1 (expanded models needed for doc generation)

### Implementation for User Story 4

- [x] T023 [P] [US4] Update `examples/freight_providers.py` — ensure `save_freight_providers` call uses a realistic `ShipmentPlanProvider` instance (not `data={}`) and `add_freight_items` call uses a typed `FreightItemsRequest` (not `items=[]`); ensure `get_freight_provider_rate_quote` passes a typed `RateQuoteRequest`
- [x] T024 [P] [US4] Rebuild Sphinx documentation by running `make html` in `docs/` — verify `PricedFreightProvider`, `ShipmentPlanProvider`, `CarrierAccountInfo`, and `CarrierAPI` pages show all expanded fields with types and descriptions
- [x] T025 [US4] Verify example runs cleanly: `python examples/freight_providers.py` — confirm no extra-field warnings in output

**Checkpoint**: Example and docs reflect expanded models

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final verification across all stories

- [x] T026 Run full test suite: `pytest` — confirm no regressions across the entire SDK
- [x] T027 Run `ruff check ab/api/models/jobs.py` — confirm code style compliance for modified models
- [x] T028 Run quickstart.md verification scenarios 1-5 to validate all acceptance criteria
- [x] T029 Final consistency check: run `python scripts/generate_progress.py` and `python scripts/generate_progress.py --fixtures` one last time to confirm all gate results are legitimate

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — baseline capture
- **Foundational (Phase 2)**: No dependencies — creates shared enum/model
- **US1 (Phase 3)**: Depends on Phase 2 (needs CarrierAPI + CarrierAccountInfo)
- **US2 (Phase 4)**: Depends on US1 (needs expanded models before fixture capture validates)
- **US3 (Phase 5)**: Depends on US2 (needs populated fixtures before gates evaluate truthfully)
- **US4 (Phase 6)**: Depends on US1 (needs expanded models for docs); can run in parallel with US2/US3
- **Polish (Phase 7)**: Depends on all user stories complete

### User Story Dependencies

- **US1 (P1)**: Starts after Phase 2 — no other story dependencies
- **US2 (P1)**: Starts after US1 — needs expanded models to validate fixtures against
- **US3 (P1)**: Starts after US2 — needs populated fixtures for gate evaluation
- **US4 (P2)**: Starts after US1 — can run in parallel with US2/US3

### Within Each User Story

- Models before fixtures (US1 → US2)
- Fixtures before progress artifacts (US2 → US3)
- Models before docs (US1 → US4)

### Parallel Opportunities

- T003 and T004 (CarrierAPI and CarrierAccountInfo) can run in parallel
- T023 and T024 (example update and docs rebuild) can run in parallel
- US4 (docs/examples) can run in parallel with US2/US3 once US1 is complete

---

## Parallel Example: Phase 2 (Foundational)

```bash
# Launch shared model tasks together:
Task T003: "Add CarrierAPI IntEnum in ab/api/models/jobs.py"
Task T004: "Add CarrierAccountInfo ResponseModel in ab/api/models/jobs.py"
```

## Parallel Example: User Story 4

```bash
# Launch docs tasks together (after US1):
Task T023: "Update examples/freight_providers.py"
Task T024: "Rebuild Sphinx documentation"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (baseline capture)
2. Complete Phase 2: Foundational (CarrierAPI + CarrierAccountInfo)
3. Complete Phase 3: US1 (expand all models)
4. **STOP and VALIDATE**: `abs job list_freight_providers 2000000` — zero warnings
5. This alone resolves the primary user complaint

### Incremental Delivery

1. Setup + Foundational → shared models ready
2. US1 → Models expanded → CLI/SDK warnings eliminated (MVP!)
3. US2 → Fixtures captured → Tests pass legitimately
4. US3 → Progress artifacts reconciled → No more contradictory status
5. US4 → Docs and examples updated → Four-Way Harmony restored
6. Each story adds confidence without breaking previous stories

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- T005 (swagger research) may update T008/T009 scope — adjust model expansion based on findings
- T012 (fixture capture) requires live API access — may need staging environment credentials
- The empty fixture `[]` root cause should inform a future quality gate improvement (gate should fail on empty fixtures, not pass)
