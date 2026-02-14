# Tasks: Extended API Endpoints

**Input**: Design documents from `/specs/002-extended-endpoints/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/endpoints.md, quickstart.md

**Tests**: Fixture validation tests are REQUIRED per constitution Principle II (Fixture-Driven Development) and FR-009. Binary form endpoints get content-type/non-empty tests instead of JSON fixture validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Verify existing project health and create scaffolding for new endpoint groups

- [x] T001 Verify existing tests pass with `pytest tests/ --ignore=tests/integration -v` to establish regression baseline
- [x] T002 [P] Create empty model file `ab/api/models/shipments.py` with module docstring and base imports (ResponseModel, RequestModel, Field, Optional, List from typing)
- [x] T003 [P] Create empty model file `ab/api/models/payments.py` with module docstring and base imports
- [x] T004 [P] Create empty model file `ab/api/models/forms.py` with module docstring and base imports
- [x] T005 [P] Create empty endpoint file `ab/api/endpoints/shipments.py` with module docstring and BaseEndpoint/Route imports
- [x] T006 [P] Create empty endpoint file `ab/api/endpoints/payments.py` with module docstring and BaseEndpoint/Route imports
- [x] T007 [P] Create empty endpoint file `ab/api/endpoints/forms.py` with module docstring and BaseEndpoint/Route imports

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Register new modules in `__init__.py` files and client so all user stories can add content to established files

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Update `ab/api/models/__init__.py` to import from new model files (shipments, payments, forms) — initially empty `__all__` entries; models will be added as each user story implements them
- [x] T009 Update `ab/api/endpoints/__init__.py` to import ShipmentsEndpoint, PaymentsEndpoint, FormsEndpoint and add to `__all__`
- [x] T010 Update `ab/client.py` `_init_endpoints()` to instantiate and register `self.forms = FormsEndpoint(self._acportal)`, `self.shipments = ShipmentsEndpoint(self._acportal)`, `self.payments = PaymentsEndpoint(self._acportal)` — classes must exist as empty BaseEndpoint subclasses first
- [x] T011 Verify project still imports and existing tests pass after registration changes

**Checkpoint**: Foundation ready — user story implementation can now begin

---

## Phase 3: User Story 1 — Manage Job Lifecycle Through Timeline and Status (Priority: P1) MVP

**Goal**: Developers can advance jobs through their lifecycle — viewing timeline tasks, creating/updating/deleting tasks, incrementing/undoing status, getting timeline task agents, and setting quote status.

**Independent Test**: Retrieve a job's timeline, create a timeline task, and advance job status. Each response is a validated Pydantic model.

### Models for User Story 1

- [x] T012 [P] [US1] Add TimelineTask response model to `ab/api/models/jobs.py` — fields: id, task_code, status, status_name, agent_contact_id, scheduled_date, completed_date, comments, is_completed, sort_order (all Optional, camelCase aliases). See data-model.md Timeline section.
- [x] T013 [P] [US1] Add TimelineAgent response model to `ab/api/models/jobs.py` — fields: contact_id, name, company_name
- [x] T014 [P] [US1] Add TimelineTaskCreateRequest, TimelineTaskUpdateRequest, and IncrementStatusRequest request models to `ab/api/models/jobs.py` — see data-model.md for fields
- [x] T015 [US1] Update `ab/api/models/__init__.py` to re-export TimelineTask, TimelineAgent, TimelineTaskCreateRequest, TimelineTaskUpdateRequest, IncrementStatusRequest

### Endpoints for User Story 1

- [x] T016 [US1] Add 9 timeline/status Route constants to `ab/api/endpoints/jobs.py` — _GET_TIMELINE, _POST_TIMELINE, _GET_TIMELINE_TASK, _PATCH_TIMELINE_TASK, _DELETE_TIMELINE_TASK, _GET_TIMELINE_AGENT, _INCREMENT_STATUS, _UNDO_INCREMENT_STATUS, _SET_QUOTE_STATUS. All use `api_surface="acportal"`. See contracts/endpoints.md Timeline section for paths.
- [x] T017 [US1] Add 9 methods to JobsEndpoint in `ab/api/endpoints/jobs.py`: get_timeline(job_display_id), create_timeline_task(job_display_id, data), get_timeline_task(job_display_id, task_id), update_timeline_task(job_display_id, task_id, data), delete_timeline_task(job_display_id, task_id), get_timeline_agent(job_display_id, task_code), increment_status(job_display_id, data=None), undo_increment_status(job_display_id, data=None), set_quote_status(job_display_id). Each calls `self._request(route.bind(...), ...)`.

### Fixtures & Tests for User Story 1

- [ ] T018 [P] [US1] Capture or create fixture `tests/fixtures/TimelineTask.json` from staging API (GET /job/{id}/timeline) — if live capture fails, create mock and add entry to MOCKS.md
- [ ] T019 [P] [US1] Capture or create fixture `tests/fixtures/TimelineAgent.json` from staging API (GET /job/{id}/timeline/{taskCode}/agent) — mock if needed
- [ ] T020 [US1] Write fixture validation tests in `tests/models/test_timeline.py` — load each fixture JSON, construct model (`TimelineTask(**data)`, `TimelineAgent(**data)`), assert no validation errors and key fields are accessible
- [ ] T021 [US1] Write unit tests in `tests/unit/test_jobs_timeline.py` — mock HttpClient, test each of the 9 timeline methods returns correct model type, test route binding produces correct paths

### Docs & Examples for User Story 1

- [ ] T022 [P] [US1] Create `examples/timeline.py` — runnable example showing get_timeline, create_timeline_task, increment_status per quickstart.md
- [ ] T023 [US1] Update `docs/api/jobs.md` — add Timeline & Status section with method docs, HTTP paths, code examples, and cross-references to TimelineTask/TimelineAgent models

**Checkpoint**: Timeline/status operations are fully functional. Developer can manage job lifecycle programmatically.

---

## Phase 4: User Story 2 — Book and Track Shipments with Rate Quotes (Priority: P2)

**Goal**: Developers can request rate quotes, review accessorials, book shipments, and track progress including PRO number tracking and v3 history.

**Independent Test**: Request rate quotes for a job, list accessorials, and retrieve tracking information. Each response is a validated Pydantic model.

### Models for User Story 2

- [x] T024 [P] [US2] Add shipment response models to `ab/api/models/shipments.py` — RateQuote, ShipmentOriginDestination, Accessorial, ShipmentExportData, RatesState, ShipmentInfo, GlobalAccessorial. See data-model.md Shipments section for all fields.
- [x] T025 [P] [US2] Add shipment request models to `ab/api/models/shipments.py` — ShipmentBookRequest, AccessorialAddRequest. See data-model.md.
- [x] T026 [P] [US2] Add tracking response models to `ab/api/models/jobs.py` — TrackingInfo (v1) and TrackingInfoV3. See data-model.md Tracking section.
- [x] T027 [US2] Update `ab/api/models/__init__.py` to re-export all new shipment and tracking models

### Endpoints for User Story 2

- [x] T028 [US2] Define 14 Route constants in `ab/api/endpoints/shipments.py` — 11 job-scoped shipment routes + 3 global shipment routes. See contracts/endpoints.md Shipments sections for all paths. Global routes use paths without `job/{jobDisplayId}` prefix.
- [x] T029 [US2] Implement ShipmentsEndpoint class in `ab/api/endpoints/shipments.py` extending BaseEndpoint — 14 methods: get_rate_quotes, request_rate_quotes, book, delete_shipment, get_accessorials, add_accessorial, remove_accessorial, get_origin_destination, get_export_data, post_export_data, get_rates_state, get_shipment (global), get_global_accessorials (global), get_shipment_document (global, returns bytes via `response_model="bytes"`).
- [x] T030 [US2] Add 2 tracking Route constants to `ab/api/endpoints/jobs.py` — _GET_TRACKING (v1) and _GET_TRACKING_V3. V3 path is `/v3/job/{jobDisplayId}/tracking/{historyAmount}`.
- [x] T031 [US2] Add 2 tracking methods to JobsEndpoint in `ab/api/endpoints/jobs.py` — get_tracking(job_display_id) and get_tracking_v3(job_display_id, history_amount).

### Fixtures & Tests for User Story 2

- [ ] T032 [P] [US2] Capture or create fixtures for shipment models: `tests/fixtures/RateQuote.json`, `tests/fixtures/ShipmentOriginDestination.json`, `tests/fixtures/Accessorial.json`, `tests/fixtures/RatesState.json`, `tests/fixtures/ShipmentInfo.json`, `tests/fixtures/GlobalAccessorial.json`. Mock and track in MOCKS.md as needed.
- [ ] T033 [P] [US2] Capture or create fixtures for tracking models: `tests/fixtures/TrackingInfo.json`, `tests/fixtures/TrackingInfoV3.json`. Mock and track as needed.
- [ ] T034 [US2] Write fixture validation tests in `tests/models/test_shipments.py` — load each shipment fixture, validate against model, assert key fields
- [ ] T035 [US2] Write fixture validation tests in `tests/models/test_tracking.py` — load each tracking fixture, validate against model
- [ ] T036 [US2] Write unit tests in `tests/unit/test_shipments.py` — mock HttpClient, test all 14 ShipmentsEndpoint methods, verify route binding and response model types
- [ ] T037 [US2] Write unit tests in `tests/unit/test_jobs_tracking.py` — mock HttpClient, test get_tracking and get_tracking_v3 methods

### Docs & Examples for User Story 2

- [ ] T038 [P] [US2] Create `examples/shipments.py` — runnable example showing get_rate_quotes, book, get_accessorials per quickstart.md
- [ ] T039 [P] [US2] Create `examples/tracking.py` — runnable example showing get_tracking and get_tracking_v3 per quickstart.md
- [ ] T040 [US2] Create `docs/api/shipments.md` — Sphinx docs for ShipmentsEndpoint with method docs, paths, examples, model cross-refs
- [ ] T041 [US2] Create `docs/models/shipments.md` — Sphinx model reference for all shipment models
- [ ] T042 [US2] Update `docs/api/jobs.md` — add Tracking section with get_tracking, get_tracking_v3 docs

**Checkpoint**: Shipment lifecycle (rate quotes → booking → tracking) is fully functional.

---

## Phase 5: User Story 3 — Process Payments and Manage Payment Sources (Priority: P3)

**Goal**: Developers can retrieve payment info, list payment sources, and process payments via ACH or stored methods.

**Independent Test**: Retrieve payment info and list payment sources for a job. Each response is a validated Pydantic model.

### Models for User Story 3

- [x] T043 [P] [US3] Add payment response models to `ab/api/models/payments.py` — PaymentInfo, PaymentSource, ACHSessionResponse. See data-model.md Payments section.
- [x] T044 [P] [US3] Add payment request models to `ab/api/models/payments.py` — PayBySourceRequest, ACHSessionRequest, ACHCreditTransferRequest, AttachBankRequest, VerifyACHRequest, BankSourceRequest. See data-model.md.
- [x] T045 [US3] Update `ab/api/models/__init__.py` to re-export all payment models

### Endpoints for User Story 3

- [x] T046 [US3] Define 10 Route constants in `ab/api/endpoints/payments.py`. See contracts/endpoints.md Payments section for all paths. Note: ACH endpoint paths preserve original casing (e.g., `/payment/ACHPaymentSession`).
- [x] T047 [US3] Implement PaymentsEndpoint class in `ab/api/endpoints/payments.py` extending BaseEndpoint — 10 methods: get(job_display_id), get_create(job_display_id), get_sources(job_display_id), pay_by_source(job_display_id, data), create_ach_session(job_display_id, data), ach_credit_transfer(job_display_id, data), attach_customer_bank(job_display_id, data), verify_ach_source(job_display_id, data), cancel_ach_verification(job_display_id), set_bank_source(job_display_id, data).

### Fixtures & Tests for User Story 3

- [ ] T048 [P] [US3] Capture or create fixtures: `tests/fixtures/PaymentInfo.json`, `tests/fixtures/PaymentSource.json`, `tests/fixtures/ACHSessionResponse.json`. Mock and track in MOCKS.md as needed (payment endpoints likely need mocks — financial operations risky on staging).
- [ ] T049 [US3] Write fixture validation tests in `tests/models/test_payments.py` — load each fixture, validate against model, assert key fields
- [ ] T050 [US3] Write unit tests in `tests/unit/test_payments.py` — mock HttpClient, test all 10 PaymentsEndpoint methods, verify route binding and response types

### Docs & Examples for User Story 3

- [ ] T051 [P] [US3] Create `examples/payments.py` — runnable example showing get payment info, list sources, pay by source per quickstart.md
- [ ] T052 [US3] Create `docs/api/payments.md` — Sphinx docs for PaymentsEndpoint with method docs, paths, examples, model cross-refs
- [ ] T053 [US3] Create `docs/models/payments.md` — Sphinx model reference for all payment models

**Checkpoint**: Payment operations (info, sources, ACH, pay-by-source) are fully functional.

---

## Phase 6: User Story 4 — Generate Job Forms and Documents (Priority: P4)

**Goal**: Developers can programmatically generate 15 types of printable business documents (invoices, BOLs, packing slips, etc.) as raw bytes.

**Independent Test**: Request an invoice for a valid job. SDK returns non-empty bytes.

### Models for User Story 4

- [x] T054 [US4] Add FormsShipmentPlan response model to `ab/api/models/forms.py` — fields: shipment_plan_id, provider_option_index, carrier_name, service_type. This is the only JSON-returning form endpoint.
- [x] T055 [US4] Update `ab/api/models/__init__.py` to re-export FormsShipmentPlan

### Endpoints for User Story 4

- [x] T056 [US4] Define 15 Route constants in `ab/api/endpoints/forms.py`. 14 routes use `response_model="bytes"`. One route (get_form_shipments) uses `response_model="List[FormsShipmentPlan]"`. See contracts/endpoints.md Forms section. Note: bill-of-lading route accepts optional query params (shipmentPlanId, providerOptionIndex).
- [x] T057 [US4] Implement FormsEndpoint class in `ab/api/endpoints/forms.py` extending BaseEndpoint — 15 methods: get_invoice, get_invoice_editable, get_bill_of_lading(job_display_id, shipment_plan_id=None, provider_option_index=None), get_packing_slip, get_customer_quote, get_quick_sale, get_operations(job_display_id, ops_type=None), get_shipments (returns List[FormsShipmentPlan]), get_address_label, get_item_labels, get_packaging_labels, get_packaging_specification, get_credit_card_authorization, get_usar, get_usar_editable. Binary methods return raw bytes via `response_model="bytes"`.

### Fixtures & Tests for User Story 4

- [ ] T058 [US4] Capture or create fixture `tests/fixtures/FormsShipmentPlan.json` for the JSON-returning get_shipments endpoint. Mock and track in MOCKS.md if needed.
- [ ] T059 [US4] Write fixture validation test in `tests/models/test_forms.py` — load FormsShipmentPlan fixture, validate against model
- [ ] T060 [US4] Write unit tests in `tests/unit/test_forms.py` — mock HttpClient, test all 15 FormsEndpoint methods. For 14 binary methods: verify they return bytes and route binding is correct. For get_shipments: verify it returns List[FormsShipmentPlan].

### Docs & Examples for User Story 4

- [ ] T061 [P] [US4] Create `examples/forms.py` — runnable example showing get_invoice, get_bill_of_lading, get_packing_slip, get_shipments per quickstart.md
- [ ] T062 [US4] Create `docs/api/forms.md` — Sphinx docs for FormsEndpoint with method docs, paths, examples. Note binary return type for most methods.
- [ ] T063 [US4] Create `docs/models/forms.md` — Sphinx model reference for FormsShipmentPlan

**Checkpoint**: All 15 form types are accessible. Binary forms return raw bytes; shipment plans return typed models.

---

## Phase 7: User Story 5 — Manage Job Notes, Items, and Parcels (Priority: P5)

**Goal**: Developers can add notes to jobs, manage line items, and handle parcel/packaging data.

**Independent Test**: Create a note on a job, list parcel items, update an item. Each response is a validated Pydantic model.

### Models for User Story 5

- [x] T064 [P] [US5] Add note models to `ab/api/models/jobs.py` — JobNote (ResponseModel, IdentifiedModel), JobNoteCreateRequest, JobNoteUpdateRequest. Note: API has typo "modifiyDate" — use `modify_date` as field name with `alias="modifiyDate"`. See data-model.md Notes section.
- [x] T065 [P] [US5] Add parcel/item models to `ab/api/models/jobs.py` — ParcelItem, ParcelItemWithMaterials, PackagingContainer (ResponseModel), ParcelItemCreateRequest, ItemNotesRequest, ItemUpdateRequest (RequestModel). See data-model.md Parcels section.
- [x] T066 [US5] Update `ab/api/models/__init__.py` to re-export all note and parcel models

### Endpoints for User Story 5

- [x] T067 [US5] Add 4 note Route constants to `ab/api/endpoints/jobs.py` — _GET_NOTES, _POST_NOTE, _GET_NOTE, _PUT_NOTE. See contracts/endpoints.md Notes section.
- [x] T068 [US5] Add 7 parcel/item Route constants to `ab/api/endpoints/jobs.py` — _GET_PARCEL_ITEMS, _POST_PARCEL_ITEM, _DELETE_PARCEL_ITEM, _GET_PARCEL_ITEMS_MATERIALS, _GET_PACKAGING_CONTAINERS, _PUT_ITEM, _POST_ITEM_NOTES. See contracts/endpoints.md Items & Parcels section.
- [x] T069 [US5] Add 4 note methods to JobsEndpoint in `ab/api/endpoints/jobs.py` — get_notes(job_display_id, **params), create_note(job_display_id, data), get_note(job_display_id, note_id), update_note(job_display_id, note_id, data).
- [x] T070 [US5] Add 7 parcel/item methods to JobsEndpoint in `ab/api/endpoints/jobs.py` — get_parcel_items(job_display_id), create_parcel_item(job_display_id, data), delete_parcel_item(job_display_id, parcel_item_id), get_parcel_items_with_materials(job_display_id), get_packaging_containers(job_display_id), update_item(job_display_id, item_id, data), add_item_notes(job_display_id, data).

### Fixtures & Tests for User Story 5

- [ ] T071 [P] [US5] Capture or create note fixtures: `tests/fixtures/JobNote.json`. Mock and track in MOCKS.md if needed.
- [ ] T072 [P] [US5] Capture or create parcel fixtures: `tests/fixtures/ParcelItem.json`, `tests/fixtures/ParcelItemWithMaterials.json`, `tests/fixtures/PackagingContainer.json`. Mock and track as needed.
- [ ] T073 [US5] Write fixture validation tests in `tests/models/test_notes.py` — load JobNote fixture, validate against model
- [ ] T074 [US5] Write fixture validation tests in `tests/models/test_parcels.py` — load parcel fixtures, validate each against its model
- [ ] T075 [US5] Write unit tests in `tests/unit/test_jobs_notes.py` — mock HttpClient, test all 4 note methods on JobsEndpoint
- [ ] T076 [US5] Write unit tests in `tests/unit/test_jobs_parcels.py` — mock HttpClient, test all 7 parcel/item methods on JobsEndpoint

### Docs & Examples for User Story 5

- [ ] T077 [P] [US5] Create `examples/notes.py` — runnable example showing list_notes, create_note per quickstart.md
- [ ] T078 [P] [US5] Create `examples/parcels.py` — runnable example showing list_parcel_items, create_parcel_item, get_parcel_items_with_materials per quickstart.md
- [ ] T079 [US5] Update `docs/api/jobs.md` — add Notes section and Items & Parcels section with method docs, paths, examples, model cross-refs

**Checkpoint**: Notes and parcel operations are fully functional. JobsEndpoint now covers timeline, tracking, notes, and parcels.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Ensure Four-Way Harmony across all endpoint groups, update shared tracking files, and validate end-to-end

- [ ] T080 Update `MOCKS.md` — add entries for all newly mocked fixtures with endpoint path, HTTP method, model name, reason, date, and status "mock"
- [ ] T081 Update swagger compliance tests in `tests/swagger/` to reflect newly implemented endpoints — reduce unimplemented count from ~269 to ~207
- [ ] T082 [P] Update `docs/index.md` to add navigation links to new endpoint group pages (forms, shipments, payments) and note expanded jobs coverage
- [ ] T083 Run full test suite `pytest tests/ --ignore=tests/integration -v` — verify zero regressions in feature 001 tests and all new tests pass
- [ ] T084 [P] Verify Four-Way Harmony: for each new endpoint group, confirm all 4 artifacts exist (implementation + fixture/test + example + Sphinx docs)
- [ ] T085 Run `ruff check .` and fix any linting issues across all new and modified files
- [ ] T086 Build Sphinx documentation `cd docs && make html` — verify zero warnings and all cross-references resolve
- [ ] T087 Validate quickstart.md examples match actual implemented API surface — verify method names, parameter signatures, and return types are accurate

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup (T001-T007) — BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational (Phase 2) completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 — Timeline/Status (P1)**: Can start after Phase 2. No dependencies on other stories.
- **US2 — Shipments + Tracking (P2)**: Can start after Phase 2. No dependencies on other stories. ShipmentsEndpoint is a new class; tracking extends JobsEndpoint independently.
- **US3 — Payments (P3)**: Can start after Phase 2. No dependencies on other stories. PaymentsEndpoint is a new class.
- **US4 — Forms (P4)**: Can start after Phase 2. No dependencies on other stories. FormsEndpoint is a new class.
- **US5 — Notes + Parcels (P5)**: Can start after Phase 2. No dependencies on other stories. Extends JobsEndpoint independently of US1 timeline additions (different methods/routes).

**Note**: US1, US2 (tracking part), and US5 all extend `jobs.py`. They modify different sections (routes + methods) with no overlap, so they CAN proceed in parallel if care is taken to avoid merge conflicts. Sequential execution by priority order is the safer default.

### Within Each User Story

1. Models first (parallelizable within a story)
2. Update `__init__.py` re-exports
3. Endpoint routes + methods (depends on models)
4. Fixtures (parallelizable, can start as soon as routes are defined)
5. Tests (depends on models + fixtures)
6. Docs + examples (parallelizable, depends on endpoint methods existing)
7. Story complete

### Parallel Opportunities

- T002-T007: All new file stubs can be created in parallel
- T012-T014: All US1 models can be created in parallel
- T018-T019: US1 fixtures can be captured in parallel
- T024-T026: All US2 models can be created in parallel
- T032-T033: US2 fixtures can be captured in parallel
- T038-T039: US2 examples can be created in parallel
- T043-T044: US3 models can be created in parallel
- T064-T065: US5 models can be created in parallel
- T071-T072: US5 fixtures can be captured in parallel
- T077-T078: US5 examples can be created in parallel
- Across stories: US1-US5 can all run in parallel after Phase 2 (with care on shared files)

---

## Parallel Example: User Story 1

```bash
# Launch all models in parallel:
Task: "Add TimelineTask response model to ab/api/models/jobs.py"
Task: "Add TimelineAgent response model to ab/api/models/jobs.py"
Task: "Add request models to ab/api/models/jobs.py"

# After models, launch fixtures in parallel:
Task: "Capture TimelineTask fixture"
Task: "Capture TimelineAgent fixture"

# After fixtures, launch tests + docs in parallel:
Task: "Write fixture validation tests in tests/models/test_timeline.py"
Task: "Write unit tests in tests/unit/test_jobs_timeline.py"
Task: "Create examples/timeline.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T007)
2. Complete Phase 2: Foundational (T008-T011)
3. Complete Phase 3: User Story 1 — Timeline/Status (T012-T023)
4. **STOP and VALIDATE**: Test timeline operations independently
5. Deploy/demo if ready — developers can now manage job lifecycle

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (Timeline) → Test → Deploy (MVP — 9 endpoints)
3. Add US2 (Shipments + Tracking) → Test → Deploy (25 endpoints cumulative)
4. Add US3 (Payments) → Test → Deploy (35 endpoints cumulative)
5. Add US4 (Forms) → Test → Deploy (50 endpoints cumulative)
6. Add US5 (Notes + Parcels) → Test → Deploy (62 endpoints cumulative)
7. Polish → Final validation → Release

### Parallel Team Strategy

With multiple developers after Phase 2 completes:

- Developer A: US1 (Timeline) + US5 (Notes/Parcels) — both extend `jobs.py`, manage merge
- Developer B: US2 (Shipments + Tracking) — new `shipments.py` + tracking on `jobs.py`
- Developer C: US3 (Payments) + US4 (Forms) — two new independent classes

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- All new models go in existing or new files under `ab/api/models/`
- All new endpoint methods go in existing or new files under `ab/api/endpoints/`
- Fixtures follow naming convention `{ModelName}.json` in `tests/fixtures/`
- Binary form endpoints do NOT get JSON fixtures — content-type/non-empty tests instead
- API typos (e.g., "modifiyDate") are preserved in aliases but corrected in field names
- ServiceBaseResponse is reused for confirmation/status responses — no new model needed
- Commit after each completed task or logical group within a story
