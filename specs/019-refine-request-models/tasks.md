# Tasks: Refine Request Models

**Input**: Design documents from `/specs/019-refine-request-models/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing. Model refinement (US2+US4) and endpoint signature updates (US1) are batched by domain to keep changes cohesive and reviewable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Verify baseline — all existing tests pass before making changes

- [x] T001 Run full test suite to establish passing baseline: `pytest tests/ -v`
- [x] T002 Snapshot current `**kwargs`/`data: dict` method count across all endpoint files in `ab/api/endpoints/` for before/after comparison

**Checkpoint**: Baseline established — all existing tests pass, current state documented

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create shared infrastructure that ALL user stories depend on. Must complete before any user story work begins.

**CRITICAL**: No user story work can begin until this phase is complete.

- [x] T003 [P] Add request-specific mixin classes (`PaginatedRequestMixin`, `SortableRequestMixin`, `SearchableRequestMixin`, `DateRangeRequestMixin`) to `ab/api/models/mixins.py` per data-model.md section 2a-2d. Each mixin inherits from `RequestModel` with `Field(description=...)` on every field.
- [x] T004 [P] Create automated description enforcement test in `tests/models/test_request_descriptions.py` — iterate all `RequestModel` subclasses via `ab.api.models`, introspect `model_fields`, assert every field has a non-empty `description` attribute. Initially expect failures (use `@pytest.mark.xfail` or collect failures as warnings with a count).
- [x] T005 [P] Implement G6 gate evaluation function `evaluate_g6_request_quality()` in `ab/progress/gates.py` with three sub-criteria: G6a (typed signature — scan endpoint source for `**kwargs` on routes with request/params model), G6b (field descriptions — introspect model `FieldInfo`), G6c (optionality verified — scan for `# TODO: verify optionality` markers). Add `g6_request_quality: GateResult | None = None` field to `EndpointGateStatus` dataclass.
- [x] T006 Verify existing request fixture tests still pass after mixin additions: `pytest tests/models/test_request_fixtures.py -v`

**Checkpoint**: Foundation ready — mixins exist, G6 gate evaluates, description test runs. User story implementation can now begin.

---

## Phase 3: User Story 5 — Incremental Progress Tracking (Priority: P1) 🎯 MVP

**Goal**: `progress.html` shows per-endpoint request model quality status (G6 gate), enabling visibility into incremental refinement progress.

**Independent Test**: Run `python scripts/generate_progress.py`, open `progress.html`, confirm G6 column appears with PASS/FAIL per endpoint.

### Implementation for User Story 5

- [x] T007 [US5] Integrate G6 into `evaluate_endpoint_gates()` orchestrator in `ab/progress/gates.py` — call `evaluate_g6_request_quality()` and populate `EndpointGateStatus.g6_request_quality`.
- [x] T008 [US5] Update `ab/progress/fixtures_generator.py` to include G6 column in FIXTURES.md output — extend table header, add G6 PASS/FAIL per row, update summary stats to include G6 pass rate.
- [x] T009 [US5] Update `ab/progress/renderer.py` to render G6 in progress.html — add G6 metric card to `render_gate_summary()`, add G6 column to `render_gate_details()` table with color-coded cells.
- [x] T010 [US5] Regenerate FIXTURES.md and progress.html with G6 column: `python scripts/generate_progress.py --fixtures && python scripts/generate_progress.py`. Verify G6 appears with mostly FAIL (expected — models not yet refined).

**Checkpoint**: Progress tracking operational — G6 gate visible in FIXTURES.md and progress.html. All subsequent refinement work will be automatically tracked.

---

## Phase 4: User Story 3 — DRY Shared Patterns (Priority: P2)

**Goal**: Common request patterns (pagination, sorting, search, date range) defined once in mixins and composed into all models that need them. No duplicate field definitions.

**Independent Test**: Confirm `ListRequest`, `JobSearchRequest`, `ContactSearchRequest`, and report models all inherit pagination from `PaginatedRequestMixin` rather than defining `page`/`page_size` independently.

### Implementation for User Story 3

- [x] T011 [US3] Refactor `ListRequest` in `ab/api/models/shared.py` to inherit from `PaginatedRequestMixin` and `SortableRequestMixin` — remove inline `page`, `page_size`, `sort_by` fields that are now provided by mixins. Retain `filters` as domain-specific. Verify `pytest tests/models/test_request_fixtures.py -k ListRequest` passes.
- [x] T012 [US3] Refactor `JobSearchRequest` in `ab/api/models/jobs.py` to inherit from `PaginatedRequestMixin` and `SearchableRequestMixin` — override `page` field with alias `pageNo` (API-specific), keep `sort_by: SortByModel` as domain override. Verify fixture validates.
- [x] T013 [US3] Refactor `ContactSearchRequest` in `ab/api/models/contacts.py` to inherit from `PaginatedRequestMixin` and `SearchableRequestMixin` — align `page_number`/`page_size` field names with mixin. Verify fixture validates.
- [x] T014 [P] [US3] Refactor `CompanySearchRequest` in `ab/api/models/companies.py` to inherit from `SearchableRequestMixin` if it has a `search_text` field. Verify fixture validates.
- [x] T015 [P] [US3] Refactor report request models in `ab/api/models/reports.py` (`InsuranceReportRequest`, `SalesForecastReportRequest`, `SalesForecastSummaryRequest`, `ReferredByReportRequest`, `Web2LeadV2RequestModel`) — compose `DateRangeRequestMixin` and/or `PaginatedRequestMixin` where applicable based on C# source field analysis. Verify fixtures validate.
- [x] T016 [P] [US3] Refactor `CommoditySearchRequest` and `CommodityMapSearchRequest` in `ab/api/models/commodities.py` to inherit from `SearchableRequestMixin` and/or `PaginatedRequestMixin` where applicable. Verify fixtures validate.
- [x] T017 [US3] Run full request fixture validation to confirm no regressions: `pytest tests/models/test_request_fixtures.py -v`

**Checkpoint**: All shared patterns defined once in mixins. Duplicate pagination/search/sort/date-range fields eliminated.

---

## Phase 5: User Story 2 + User Story 4 — Correct Optionality & Field Descriptions (Priority: P1/P2)

**Goal**: Every request model field has correct required/optional designation (verified against C# source) and a meaningful `description`. These stories are combined because they modify the same model files and should be done together per domain.

**Independent Test (US2)**: For each updated model, required fields match C# DTO non-nullable properties; optional fields match nullable properties.

**Independent Test (US4)**: Run `pytest tests/models/test_request_descriptions.py` — zero failures (all fields have descriptions).

### Batch 1: Jobs domain (largest — ~20 request models)

- [x] T018 [P] [US2] Research required vs optional fields for Jobs request models by reading C# source: `JobController.cs`, job-related DTOs in `/src/ABConnect/ACPortal/ABC.ACPortal.WebAPI/Controllers/` and `/src/ABConnect/AB.ABCEntities/`. Document findings as comments in `ab/api/models/jobs.py`.
- [x] T019 [US2] [US4] Refine Jobs params models in `ab/api/models/jobs.py`: `JobSearchParams`, `FreightProvidersParams`, `TimelineCreateParams`, `TrackingV3Params`, `JobNoteListParams`, `JobRfqListParams` — correct optionality per C# source, add `description` to every field, add class docstrings referencing endpoint path.
- [x] T020 [US2] [US4] Refine Jobs body request models (group 1) in `ab/api/models/jobs.py`: `JobCreateRequest`, `JobSaveRequest`, `JobSearchRequest`, `JobUpdateRequest` — correct optionality per C# source, add `description` to every field. Retain `Optional[dict]` for nested objects per assumptions.
- [x] T021 [US2] [US4] Refine Jobs body request models (group 2) in `ab/api/models/jobs.py`: `TimelineTaskCreateRequest`, `TimelineTaskUpdateRequest`, `IncrementStatusRequest`, `JobNoteCreateRequest`, `JobNoteUpdateRequest` — correct optionality, add descriptions.
- [x] T022 [US2] [US4] Refine Jobs body request models (group 3) in `ab/api/models/jobs.py`: `ParcelItemCreateRequest`, `ItemNotesRequest`, `ItemUpdateRequest`, `SaveOnHoldRequest` — correct optionality, add descriptions.
- [x] T023 Verify Jobs fixtures pass: `pytest tests/models/test_request_fixtures.py -v -k "Job or Timeline or Increment or Note or Parcel or Item or OnHold"`

### Batch 2: Companies domain (~10 models)

- [x] T024 [P] [US2] Research required vs optional fields for Companies models by reading C# source: `CompaniesController.cs` and company DTOs. Document findings.
- [x] T025 [US2] [US4] Refine Companies params models in `ab/api/models/companies.py`: `CarrierAccountSearchParams`, `SuggestCarriersParams`, `GeoSettingsParams`, `InheritFromParams` — correct optionality, add descriptions.
- [x] T026 [US2] [US4] Refine Companies body request models in `ab/api/models/companies.py`: `CompanySearchRequest`, `CarrierAccountSaveRequest`, `GeoSettingsSaveRequest` — correct optionality, add descriptions.
- [x] T027 Verify Companies fixtures pass: `pytest tests/models/test_request_fixtures.py -v -k "Company or Carrier or Geo or Suggest"`

### Batch 3: Contacts domain (~4 models)

- [x] T028 [P] [US2] [US4] Refine Contacts models in `ab/api/models/contacts.py`: `ContactEditParams`, `ContactHistoryParams`, `ContactEditRequest`, `ContactSearchRequest` — correct optionality per C# source, add `description` to all fields (several currently missing).
- [x] T029 Verify Contacts fixtures pass: `pytest tests/models/test_request_fixtures.py -v -k "Contact"`

### Batch 4: Shipments domain (~6 models)

- [x] T030 [P] [US2] [US4] Refine Shipments models in `ab/api/models/shipments.py`: `ShipmentParams`, `RateQuotesParams`, `ShipmentDocumentParams`, `ShipmentBookRequest`, `AccessorialAddRequest` — correct optionality, add missing descriptions (especially `RateQuotesParams` fields).
- [x] T031 Verify Shipments fixtures pass: `pytest tests/models/test_request_fixtures.py -v -k "Shipment or RateQuote or Accessorial"`

### Batch 5: Commodities domain (~7 models)

- [x] T032 [P] [US2] [US4] Refine Commodities models in `ab/api/models/commodities.py`: `CommodityCreateRequest`, `CommodityUpdateRequest`, `CommoditySearchRequest`, `CommoditySuggestionRequest`, `CommodityMapCreateRequest`, `CommodityMapUpdateRequest`, `CommodityMapSearchRequest` — correct optionality, add descriptions.
- [x] T033 Verify Commodities fixtures pass: `pytest tests/models/test_request_fixtures.py -v -k "Commodity"`

### Batch 6: Remaining domains (reports, payments, catalog, lots, sellers, notes, rfq, views, dashboard, web2lead, users, documents, address, forms, lookup)

- [x] T034 [P] [US2] [US4] Refine Reports models in `ab/api/models/reports.py`: `InsuranceReportRequest`, `SalesForecastReportRequest`, `SalesForecastSummaryRequest`, `Web2LeadV2RequestModel`, `ReferredByReportRequest` — correct optionality, add descriptions.
- [x] T035 [P] [US2] [US4] Refine Payments models in `ab/api/models/payments.py`: `PaymentParams`, `PayBySourceRequest`, `ACHSessionRequest`, `ACHCreditTransferRequest`, `AttachBankRequest`, `VerifyACHRequest`, `BankSourceRequest` — correct optionality, add missing descriptions.
- [x] T036 [P] [US2] [US4] Refine Catalog/Lots/Sellers models in `ab/api/models/catalog.py`, `ab/api/models/lots.py`, `ab/api/models/sellers.py` — correct optionality, add descriptions for `AddCatalogRequest`, `UpdateCatalogRequest`, `BulkInsertRequest`, `CatalogListParams`, `AddLotRequest`, `UpdateLotRequest`, `LotListParams`, `AddSellerRequest`, `UpdateSellerRequest`, `SellerListParams`.
- [x] T037 [P] [US2] [US4] Refine remaining small-domain models: `ab/api/models/notes.py` (`NotesListParams`, `NotesSuggestUsersParams`, `GlobalNoteCreateRequest`, `GlobalNoteUpdateRequest`), `ab/api/models/rfq.py` (`RfqForJobParams`, `RfqAcceptWinnerParams`, `AcceptModel`), `ab/api/models/views.py` (`GridViewCreateRequest`), `ab/api/models/dashboard.py` (`DashboardParams`, `DashboardCompanyParams`), `ab/api/models/web2lead.py` (`Web2LeadGetParams`, `Web2LeadRequest`), `ab/api/models/users.py` (`UserCreateRequest`, `UserUpdateRequest`), `ab/api/models/documents.py` (`DocumentListParams`, `DocumentUpdateRequest`), `ab/api/models/lookup.py` (`LookupItemsParams`, `LookupDocumentTypesParams`, `LookupDensityClassMapParams`), `ab/api/models/autoprice.py` (`QuoteRequestModel`), `ab/api/models/partners.py` (`PartnerListParams`, `PartnerSearchRequest`), `ab/api/models/forms.py` (all params models) — correct optionality, add descriptions.
- [x] T038 Run full request fixture validation across all domains: `pytest tests/models/test_request_fixtures.py -v`
- [x] T039 Run description enforcement test — should now pass with zero xfails: `pytest tests/models/test_request_descriptions.py -v`

**Checkpoint**: All request model fields have correct required/optional designations and descriptions. SC-002 (100% descriptions) and SC-003 (correct optionality) verified.

---

## Phase 6: User Story 1 — IDE-Guided Endpoint Calls (Priority: P1)

**Goal**: Every endpoint method that accepts request body or query parameters exposes explicit, typed keyword arguments — no remaining `**kwargs: Any` or `data: dict | Any`. Developers see full parameter lists with types and descriptions in IDE autocomplete.

**Independent Test**: Open any refined endpoint method in VSCode/PyCharm, trigger autocomplete, and confirm every parameter appears with type and description — no `**kwargs`.

### Batch 1: Jobs endpoints (25 methods — largest)

- [x] T040 [US1] Replace `data: dict | Any` with typed signatures on Jobs body methods (group 1) in `ab/api/endpoints/jobs.py`: `create()`, `save()`, `search_by_details()`, `update()` — follow Pattern A (inline ≤8 fields) or Pattern B (data param >8 fields) from contracts/endpoint-method-contract.md. Add docstrings per docstring contract (Args section + Request model reference).
- [x] T041 [US1] Replace `data: dict | Any` with typed signatures on Jobs body methods (group 2) in `ab/api/endpoints/jobs.py`: `create_timeline_task()`, `update_timeline_task()`, `increment_status()`, `undo_increment_status()` — use Pattern C (combined body + params) for `create_timeline_task` which has both `request_model` and `params_model`.
- [x] T042 [US1] Replace `data: dict | Any` with typed signatures on Jobs body methods (group 3) in `ab/api/endpoints/jobs.py`: `create_note()`, `update_note()`, `create_parcel_item()`, `update_item()`, `add_item_notes()` — follow Pattern A or B per field count.
- [x] T043 [US1] Replace `**kwargs: Any` with typed signatures on Jobs methods (group 4) in `ab/api/endpoints/jobs.py`: `create_on_hold()`, `update_on_hold()`, `update_on_hold_dates()`, `send_document_email()`, `send_sms()`, `mark_sms_read()`, `save_freight_providers()` — follow Pattern A or B per field count. Add docstrings.
- [x] T044 [US1] Verify Jobs endpoint methods compile and existing tests pass: `pytest tests/ -v -k "job or Job"`

### Batch 2: Companies endpoints (8 methods)

- [x] T045 [P] [US1] Replace `**kwargs: Any` with typed signatures on Companies methods in `ab/api/endpoints/companies.py`: `update_fulldetails()`, `create()`, `search()`, `list()`, `save_geo_settings()`, `save_carrier_accounts()`, `save_packaging_settings()`, `save_packaging_labor()` — follow Pattern A or B per field count. Add docstrings.
- [x] T046 Verify Companies endpoint tests pass: `pytest tests/ -v -k "compan"`

### Batch 3: Contacts endpoints (6 methods)

- [x] T047 [P] [US1] Replace `data: dict | Any` and `**kwargs: Any` with typed signatures on Contacts methods in `ab/api/endpoints/contacts.py`: `update_details()`, `create()`, `search()`, `post_history()`, `merge_preview()`, `merge()` — use Pattern C for methods with both `request_model` and `params_model` (update_details, create). Add docstrings.
- [x] T048 Verify Contacts endpoint tests pass: `pytest tests/ -v -k "contact or Contact"`

### Batch 4: Reports endpoints (8 methods)

- [x] T049 [P] [US1] Replace `**kwargs: Any` with typed signatures on Reports methods in `ab/api/endpoints/reports.py`: `insurance()`, `sales()`, `sales_summary()`, `sales_drilldown()`, `top_revenue_customers()`, `top_revenue_sales_reps()`, `referred_by()`, `web2lead()` — follow Pattern A (all have defined request_models). Add docstrings.

### Batch 5: Dashboard endpoints (6 methods)

- [x] T050 [P] [US1] Replace `**kwargs: Any` with typed signatures on Dashboard methods in `ab/api/endpoints/dashboard.py`: `save_grid_view_state()`, `inbound()`, `in_house()`, `outbound()`, `local_deliveries()`, `recent_estimates()` — follow Pattern A. Add docstrings.

### Batch 6: Payments endpoints (6 methods)

- [x] T051 [P] [US1] Replace `data: dict | Any` with typed signatures on Payments methods in `ab/api/endpoints/payments.py`: `pay_by_source()`, `create_ach_session()`, `ach_credit_transfer()`, `attach_customer_bank()`, `verify_ach_source()`, `set_bank_source()` — follow Pattern A or B per field count. Add docstrings.

### Batch 7: Shipments endpoints (4 methods)

- [x] T052 [P] [US1] Replace `data: dict | Any` with typed signatures on Shipments methods in `ab/api/endpoints/shipments.py`: `request_rate_quotes()`, `book()`, `add_accessorial()`, `post_export_data()` — follow Pattern A. Add docstrings.

### Batch 8: Commodities + CommodityMaps endpoints (7 methods)

- [x] T053 [P] [US1] Replace `**kwargs: Any` with typed signatures on Commodities methods in `ab/api/endpoints/commodities.py`: `update()`, `create()`, `search()`, `suggestions()` and CommodityMaps methods in `ab/api/endpoints/commodity_maps.py`: `update()`, `create()`, `search()` — follow Pattern A. Add docstrings.

### Batch 9: Remaining small-domain endpoints (~15 methods across 11 files)

- [x] T054 [P] [US1] Replace `data: dict | Any` / `**kwargs: Any` with typed signatures on remaining endpoint methods: `ab/api/endpoints/catalog.py` (`create`, `update`, `bulk_insert`), `ab/api/endpoints/lots.py` (`create`, `update`), `ab/api/endpoints/sellers.py` (`create`, `update`), `ab/api/endpoints/notes.py` (`create`, `update`), `ab/api/endpoints/rfq.py` (`accept`, `add_comment`), `ab/api/endpoints/views.py` (`create`, `update_access`), `ab/api/endpoints/users.py` (`list`, `create`, `update`), `ab/api/endpoints/web2lead.py` (`post`), `ab/api/endpoints/autoprice.py` (`quick_quote`, `quote_request`), `ab/api/endpoints/partners.py` (`search`), `ab/api/endpoints/documents.py` (`update`) — follow Pattern A or B per field count. Add docstrings.
- [x] T055 [US1] Run full test suite to verify no regressions across all endpoint changes: `pytest tests/ -v`

**Checkpoint**: All endpoint methods have typed signatures. SC-001 (zero `**kwargs`) verified on updated endpoints. IDE autocomplete shows full parameter lists.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, progress report regeneration, and cleanup

- [x] T056 Regenerate FIXTURES.md with G6 gate results: `python scripts/generate_progress.py --fixtures`
- [x] T057 Regenerate progress.html and verify G6 pass rates reflect refinement work: `python scripts/generate_progress.py`
- [x] T058 Run description enforcement test with strict mode (remove xfail): `pytest tests/models/test_request_descriptions.py -v` — must pass with zero failures (SC-002)
- [x] T059 Run full test suite including all fixture validations: `pytest tests/ -v` — must pass with zero failures (SC-004)
- [x] T060 Audit for remaining `**kwargs: Any` patterns in endpoint files — confirm count matches expected (only endpoints without request_model should remain untyped, tracked as incomplete in progress.html)
- [x] T061 Verify `progress.html` accurately distinguishes refined (G6 PASS) vs unrefined (G6 FAIL) endpoints (SC-006)

**Checkpoint**: Feature complete — all success criteria verified.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **US5 (Phase 3)**: Depends on Foundational (specifically T005 G6 gate) — can proceed independently
- **US3 (Phase 4)**: Depends on Foundational (specifically T003 mixins) — can proceed in parallel with US5
- **US2+US4 (Phase 5)**: Depends on US3 completion (models need to compose mixins)
- **US1 (Phase 6)**: Depends on US2+US4 completion (endpoint signatures reference refined models)
- **Polish (Phase 7)**: Depends on US1 + US5 completion

### User Story Dependencies

- **US5 (Progress Tracking)**: Independent — only needs G6 gate from Foundational
- **US3 (DRY Mixins)**: Independent — only needs mixin classes from Foundational
- **US2+US4 (Optionality + Descriptions)**: Depends on US3 (models compose mixins)
- **US1 (Typed Signatures)**: Depends on US2+US4 (endpoints expose refined model fields)

### Within Each Domain Batch (Phase 5 + Phase 6)

1. Research C# source (if applicable)
2. Refine model (correct optionality + descriptions)
3. Verify fixtures pass
4. Update endpoint signatures
5. Verify endpoint tests pass

### Parallel Opportunities

- T003, T004, T005 can all run in parallel (different files)
- Within Phase 4: T014, T015, T016 can run in parallel (different model files)
- Within Phase 5: All C# research tasks can run in parallel; model refinement batches across different domains can run in parallel (T028, T030, T032, T034-T037)
- Within Phase 6: Endpoint batches across different domains can run in parallel (T045, T047, T049-T054)

---

## Parallel Example: Phase 5 Domain Batches

```text
# These can run in parallel (different model files):
T028 [US2][US4] Refine Contacts models in ab/api/models/contacts.py
T030 [US2][US4] Refine Shipments models in ab/api/models/shipments.py
T032 [US2][US4] Refine Commodities models in ab/api/models/commodities.py
T034 [US2][US4] Refine Reports models in ab/api/models/reports.py
T035 [US2][US4] Refine Payments models in ab/api/models/payments.py
T036 [US2][US4] Refine Catalog/Lots/Sellers models
T037 [US2][US4] Refine remaining small-domain models
```

## Parallel Example: Phase 6 Endpoint Batches

```text
# These can run in parallel (different endpoint files):
T045 [US1] Companies endpoints in ab/api/endpoints/companies.py
T047 [US1] Contacts endpoints in ab/api/endpoints/contacts.py
T049 [US1] Reports endpoints in ab/api/endpoints/reports.py
T050 [US1] Dashboard endpoints in ab/api/endpoints/dashboard.py
T051 [US1] Payments endpoints in ab/api/endpoints/payments.py
T052 [US1] Shipments endpoints in ab/api/endpoints/shipments.py
T053 [US1] Commodities endpoints in ab/api/endpoints/commodities.py
T054 [US1] Remaining small-domain endpoints
```

---

## Implementation Strategy

### MVP First (US5 + US3 + One Domain)

1. Complete Phase 1: Setup — verify baseline
2. Complete Phase 2: Foundational — mixins, G6 gate, description test
3. Complete Phase 3: US5 — G6 visible in progress.html
4. Complete Phase 4: US3 — mixins composed into models
5. Refine ONE domain batch (e.g., Jobs) through Phase 5 + Phase 6
6. **STOP and VALIDATE**: Regenerate progress.html, confirm G6 PASS for refined Jobs endpoints
7. Continue with remaining domains incrementally

### Incremental Delivery

1. Foundation + US5 + US3 → Infrastructure ready, progress tracking operational
2. Add Jobs domain (T018-T023 + T040-T044) → Largest domain refined, ~25 endpoints upgraded
3. Add Companies domain (T024-T027 + T045-T046) → Second domain, ~8 endpoints
4. Add remaining domains → Each batch independently verifiable via progress.html
5. Each batch adds G6 PASS count without breaking previous work

### Domain Priority Order (recommended)

1. **Jobs** — largest impact (25 methods, most used)
2. **Companies** — high usage (8 methods)
3. **Contacts** — high usage (6 methods)
4. **Reports** — moderate usage (8 methods)
5. **Remaining** — lower priority, can be done incrementally

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- US2 and US4 are combined in Phase 5 because they modify the same model files
- Domain batches keep changes cohesive — one model file + one endpoint file per batch
- Retain `Optional[dict]` for nested objects (e.g., `customer`, `items`) per assumptions — nested model typing is out of scope
- Endpoints without `request_model` on their Route remain untyped and are tracked as "incomplete" in progress.html — not failures
- Always run fixture validation after model changes to catch regressions (FR-006)
- Commit after each domain batch for clean context recovery (Constitution VIII)
