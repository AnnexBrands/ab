# Tasks: G1 Model Fidelity Sweep

**Input**: Design documents from `/specs/034-g1-model-fidelity-sweep/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: No new project setup needed — this feature modifies an existing SDK.

- [x] T001 Verify branch `034-g1-model-fidelity-sweep` is checked out and tests pass (`pytest`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No blocking prerequisites — ServiceBaseResponse and ShipmentWeight already exist.

- [x] T002 Read fixture `tests/fixtures/ServiceBaseResponse.json` and model `ab/api/models/shared.py` to confirm the 13-field gap matches research.md

**Checkpoint**: Gap confirmed — user story implementation can begin.

---

## Phase 3: User Story 1 — Close G1 Gap for All G2-Passing Endpoints (Priority: P1) MVP

**Goal**: Expand `ServiceBaseResponse` from 3 to 16 fields so all 21 endpoints pass G1.

**Independent Test**: Run gate evaluation — all 21 endpoints report G1=pass; `__pydantic_extra__` is empty when validating the fixture.

### Implementation for User Story 1

- [x] T003 [US1] Import `ShipmentWeight` from `ab.api.models.shipments` in `ab/api/models/shared.py`
- [x] T004 [US1] Add 13 new Optional fields to `ServiceBaseResponse` in `ab/api/models/shared.py` per data-model.md field table: documents, errors, confirm_required, notifications, shipment_id, shipment_accept_identifier, weight (ShipmentWeight), total_net_charge_amount, currency_code, international_info_required, ship_out_date_required, fed_ex_express_freight_detail_required, carrier_api
- [x] T005 [US1] Verify `ServiceBaseResponse` is already exported from `ab/api/models/__init__.py` and present in `__all__` (no change expected)
- [x] T006 [US1] Run `pytest tests/test_gate_regression.py -v` to confirm no regressions; validate fixture `tests/fixtures/ServiceBaseResponse.json` against expanded model manually (`python -c "from ab.api.models.shared import ServiceBaseResponse; import json; data=json.load(open('tests/fixtures/ServiceBaseResponse.json')); m=ServiceBaseResponse.model_validate(data); print(m.__pydantic_extra__)"` — should print `None` or `{}`)

**Checkpoint**: ServiceBaseResponse declares all 16 fixture fields. G1 gap closed for all 21 endpoints.

---

## Phase 4: User Story 2 — Verify Test Coverage for Expanded Models (Priority: P2)

**Goal**: Add fixture-validation test ensuring G3 passes for ServiceBaseResponse.

**Independent Test**: `pytest tests/models/test_shared_models.py -v` — all tests pass with no extra fields.

### Implementation for User Story 2

- [x] T007 [US2] Create `tests/models/test_shared_models.py` with a `TestServiceBaseResponse` class containing: (1) `test_service_base_response` — loads `ServiceBaseResponse.json` fixture via `require_fixture`, validates with `model_validate`, asserts `isinstance` and `assert_no_extra_fields`; (2) `test_service_base_response_fields` — asserts key fields populated (success is not None, documents is not None, weight is not None); (3) `test_weight_nested_model` — asserts `model.weight` is an instance of `ShipmentWeight` and passes `assert_no_extra_fields`
- [x] T008 [US2] Run `pytest tests/models/test_shared_models.py -v` to confirm all 3 tests pass

**Checkpoint**: Fixture-validation tests exist and pass. G3 covered for ServiceBaseResponse.

---

## Phase 5: User Story 3 — Verify Example Script Coverage (Priority: P3)

**Goal**: Confirm example scripts exist for all 21 affected endpoints and reference the correct endpoint methods.

**Independent Test**: Review examples directory — each endpoint group has a script that calls the affected endpoints.

### Implementation for User Story 3

- [x] T009 [P] [US3] Verify `examples/payments.py` demonstrates all 6 payment endpoints: ACHCreditTransfer, attachCustomerBank, banksource, bysource, cancelJobACHVerification, verifyJobACHSource
- [x] T010 [P] [US3] Verify `examples/shipments.py` demonstrates all 5 shipment endpoints: shipment DELETE, accessorial POST, accessorial DELETE, book, exportdata
- [x] T011 [P] [US3] Verify `examples/timeline.py` demonstrates: incrementjobstatus, undoincrementjobstatus, timeline task DELETE
- [x] T012 [P] [US3] Verify `examples/jobs.py` demonstrates: changeAgent, item/notes, item PUT
- [x] T013 [P] [US3] Verify `examples/commodities.py` demonstrates commodity-map DELETE and `examples/views.py` demonstrates views DELETE and `examples/parcels.py` demonstrates parcelitems DELETE

**Checkpoint**: All 21 endpoints have example coverage. No new example scripts needed.

---

## Phase 6: User Story 4 — Verify Sphinx Documentation Completeness (Priority: P3)

**Goal**: Create missing Sphinx doc stubs so all expanded models and affected endpoint groups have documentation.

**Independent Test**: `sphinx-build` completes with zero warnings referencing expanded or new models.

### Implementation for User Story 4

- [x] T014 [P] [US4] Create `docs/api/payments.md` with autoclass directive for `PaymentsEndpoint` and method summary table
- [x] T015 [P] [US4] Create `docs/api/shipments.md` with autoclass directive for `ShipmentsEndpoint` and method summary table
- [x] T016 [P] [US4] Create `docs/models/payments.md` with automodule directive for `ab.api.models.payments`
- [x] T017 [P] [US4] Create `docs/models/commodities.md` with automodule directive for `ab.api.models.commodities`
- [x] T018 [P] [US4] Create `docs/models/views.md` with automodule directive for `ab.api.models.views`
- [x] T019 [US4] Add new doc pages to `docs/index.md` toctree (if not auto-discovered)
- [x] T020 [US4] Run `sphinx-build -b html docs/ docs/_build/html` and verify zero warnings for new/expanded models

**Checkpoint**: All affected models and endpoint groups have Sphinx documentation.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Update gate baseline, run full validation, confirm all success criteria met.

- [x] T021 Update `tests/gate_baseline.json` — add `"G1"` to the gate arrays for all 21 endpoints that now pass G1
- [x] T022 Run `pytest tests/test_gate_regression.py -v` to confirm baseline ratchet passes with updated baseline
- [x] T023 Run full test suite `pytest` — confirm no new failures or skips attributable to this feature (expect ≥567 passed)
- [x] T024 Verify SC-001: G1 count ≥92 (was 71 + 21 new)
- [x] T025 Run quickstart.md validation steps

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — verify environment
- **Foundational (Phase 2)**: Depends on Phase 1 — confirm gap
- **US1 (Phase 3)**: Depends on Phase 2 — the core model expansion
- **US2 (Phase 4)**: Depends on US1 (needs expanded model to validate)
- **US3 (Phase 5)**: Independent of US1/US2 — pure verification
- **US4 (Phase 6)**: Independent of US1/US2 — doc stubs can be created in parallel
- **Polish (Phase 7)**: Depends on US1 and US2 (needs expanded model and tests for baseline update)

### User Story Dependencies

- **US1 (P1)**: Blocking — must complete before US2 and Phase 7
- **US2 (P2)**: Depends on US1 — needs expanded model to write tests against
- **US3 (P3)**: Independent — can run in parallel with US1
- **US4 (P3)**: Independent — can run in parallel with US1

### Parallel Opportunities

- T009–T013 (US3 verification) can all run in parallel
- T014–T018 (US4 doc stubs) can all run in parallel
- US3 and US4 can run in parallel with each other and with US1

---

## Parallel Example: User Story 4

```text
# All doc stubs can be created simultaneously (different files):
Task T014: "Create docs/api/payments.md"
Task T015: "Create docs/api/shipments.md"
Task T016: "Create docs/models/payments.md"
Task T017: "Create docs/models/commodities.md"
Task T018: "Create docs/models/views.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Verify environment (T001)
2. Complete Phase 2: Confirm gap (T002)
3. Complete Phase 3: Expand ServiceBaseResponse (T003–T006)
4. **STOP and VALIDATE**: All 21 endpoints pass G1
5. This single change delivers the core value of the feature

### Incremental Delivery

1. US1 → Model expanded → 21 endpoints gain G1 (MVP!)
2. US2 → Tests lock in fidelity → G3 covered
3. US3 → Examples verified → Four-Way Harmony check
4. US4 → Docs created → Principle VI satisfied
5. Polish → Baseline updated → Ratchet prevents regression

---

## Notes

- The entire G1 gap is caused by one underdeclared model (`ServiceBaseResponse`)
- `ShipmentWeight` already exists — reuse it, don't recreate
- `ServiceWarningResponse` inherits from `ServiceBaseResponse` — it gains all new fields automatically
- Gate baseline update (T021) must happen after model expansion and test creation
- No new dependencies added; no `__init__.py` changes needed for `ServiceBaseResponse` (already exported)
