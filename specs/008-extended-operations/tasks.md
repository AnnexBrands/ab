# Tasks: Extended Operations Endpoints

**Input**: Design documents from `/specs/008-extended-operations/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/endpoints.md

**Tests**: Fixture validation tests and swagger compliance tests are included per Constitution Principles III, IV, and V.

**Organization**: Tasks are grouped by user story (DISCOVER workflow batches) to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Branch preparation and research groundwork

- [x] T001 Verify all existing tests pass on branch 008-extended-operations by running `pytest`
- [x] T002 Research ABConnectTools reference implementation for all 14 endpoint groups — document swagger path details, request bodies, query parameters, transport types, and realistic test values in working notes. Reference files: `/usr/src/pkgs/ABConnectTools/ABConnect/api/endpoints/` and `ab/api/schemas/acportal.json`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared infrastructure that MUST be complete before any user story

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Register 8 new endpoint class imports in `ab/api/endpoints/__init__.py` — add RFQEndpoint, ReportsEndpoint, DashboardEndpoint, ViewsEndpoint, CommoditiesEndpoint, CommodityMapsEndpoint, NotesEndpoint, PartnersEndpoint
- [x] T004 Register 8 new endpoint attributes in `ab/client.py` `_init_endpoints()` — add `self.rfq`, `self.reports`, `self.dashboard`, `self.views`, `self.commodities`, `self.commodity_maps`, `self.notes`, `self.partners` using `self._acportal`
- [x] T005 Create empty endpoint files with BaseEndpoint scaffolds: `ab/api/endpoints/rfq.py`, `ab/api/endpoints/reports.py`, `ab/api/endpoints/dashboard.py`, `ab/api/endpoints/views.py`, `ab/api/endpoints/commodities.py`, `ab/api/endpoints/commodity_maps.py`, `ab/api/endpoints/notes.py`, `ab/api/endpoints/partners.py`
- [x] T006 Create empty model files with module docstrings: `ab/api/models/rfq.py`, `ab/api/models/reports.py`, `ab/api/models/dashboard.py`, `ab/api/models/views.py`, `ab/api/models/commodities.py`, `ab/api/models/notes.py`, `ab/api/models/partners.py`

**Checkpoint**: All new files exist, imports resolve, `pytest` still passes with no regressions

---

## Phase 3: User Story 1 — RFQ Lifecycle (Priority: P1) MVP

**Goal**: Enable developers to manage the full Request-for-Quote lifecycle — list RFQs for a job, check status, accept/decline/cancel quotes, and select winners

**Independent Test**: Call `api.jobs.list_rfqs(job_display_id)` and `api.rfq.get(rfq_id)`, verify responses are validated Pydantic models

### Implementation for User Story 1

- [x] T007 [US1] Create RFQ response models in `ab/api/models/rfq.py` — QuoteRequestDisplayInfo (rfq_id, provider_company_id, service_type, quoted_price, transit_days, status), QuoteRequestStatus (status, rfq_id, is_active). Use ResponseModel base, snake_case fields with camelCase aliases, all Optional. Research swagger and ABConnectTools `rfq.py` for actual field names.
- [x] T008 [US1] Create RFQ request model in `ab/api/models/rfq.py` — AcceptModel (notes: Optional[str]). Use RequestModel base with extra="forbid".
- [x] T009 [US1] Re-export all RFQ models in `ab/api/models/__init__.py` and add to `__all__`
- [x] T010 [US1] Implement 7 standalone RFQ Route definitions and RFQEndpoint methods in `ab/api/endpoints/rfq.py` — get(rfq_id), get_for_job(job_id), accept(rfq_id, **kwargs), decline(rfq_id), cancel(rfq_id), accept_winner(rfq_id), add_comment(rfq_id, **kwargs). Routes: GET /rfq/{rfqId}, GET /rfq/forjob/{jobId}, POST /rfq/{rfqId}/accept, POST /rfq/{rfqId}/decline, POST /rfq/{rfqId}/cancel, POST /rfq/{rfqId}/acceptwinner, POST /rfq/{rfqId}/comment
- [x] T011 [US1] Add 2 job-scoped RFQ Route definitions and methods to `ab/api/endpoints/jobs.py` — list_rfqs(job_display_id), get_rfq_status(job_display_id, rfq_service_type, company_id). Routes: GET /job/{jobDisplayId}/rfq, GET /job/{jobDisplayId}/rfq/statusof/{rfqServiceType}/forcompany/{companyId}
- [x] T012 [US1] Create runnable example in `examples/rfq.py` — demonstrate list_rfqs, get, accept, decline with staging credentials
- [x] T013 [US1] Add fixture validation tests for QuoteRequestDisplayInfo and QuoteRequestStatus in `tests/models/test_fixtures.py` — skip-marked if fixture not yet captured
- [x] T014 [US1] Update `FIXTURES.md` with 9 RFQ endpoint entries in unified 4D format

**Checkpoint**: `api.rfq.*` and `api.jobs.list_rfqs()` resolve, `pytest` passes, FIXTURES.md updated

---

## Phase 4: User Story 2 — On-Hold Management (Priority: P2)

**Goal**: Enable developers to manage job exceptions — create holds, track follow-ups, add comments, update dates, and resolve holds

**Independent Test**: Call `api.jobs.list_on_hold(job_display_id)`, create a hold, add a comment, then resolve it

### Implementation for User Story 2

- [x] T015 [US2] Create on-hold response models in `ab/api/models/jobs.py` — ExtendedOnHoldInfo, OnHoldDetails, SaveOnHoldResponse, ResolveJobOnHoldResponse, OnHoldUser, OnHoldNoteDetails. Research swagger and ABConnectTools `jobs/onhold.py` for field names.
- [x] T016 [US2] Create on-hold request models in `ab/api/models/jobs.py` — SaveOnHoldRequest (reason, description, follow_up_contact_id, follow_up_date), SaveOnHoldDatesModel (follow_up_date, due_date). Use RequestModel base.
- [x] T017 [US2] Re-export all on-hold models in `ab/api/models/__init__.py` and add to `__all__`
- [x] T018 [US2] Add 10 on-hold Route definitions and methods to `ab/api/endpoints/jobs.py` — list_on_hold, create_on_hold, delete_on_hold, get_on_hold, update_on_hold, get_on_hold_followup_user, list_on_hold_followup_users, add_on_hold_comment, update_on_hold_dates, resolve_on_hold. See contracts/endpoints.md for exact paths.
- [x] T019 [US2] Create runnable example in `examples/onhold.py` — demonstrate list, create, comment, resolve flow
- [x] T020 [US2] Add fixture validation tests for on-hold models in `tests/models/test_fixtures.py` — skip-marked if fixtures not captured
- [x] T021 [US2] Update `FIXTURES.md` with 10 on-hold endpoint entries

**Checkpoint**: `api.jobs.list_on_hold()` through `api.jobs.resolve_on_hold()` resolve, `pytest` passes

---

## Phase 5: User Story 3 — Reports & Analytics (Priority: P3)

**Goal**: Enable developers to generate business reports — insurance, sales forecasts, revenue breakdowns, referrals, and web lead analytics

**Independent Test**: Call `api.reports.sales(**kwargs)` with a date range and verify typed SalesForecastReport response

### Implementation for User Story 3

- [x] T022 [P] [US3] Create report response models in `ab/api/models/reports.py` — InsuranceReport, SalesForecastReport, SalesForecastSummary, RevenueCustomer, ReferredByReport, Web2LeadReport. Research swagger and ABConnectTools `reports.py` for field names.
- [x] T023 [P] [US3] Create report request models in `ab/api/models/reports.py` — InsuranceReportRequest, SalesForecastReportRequest, SalesForecastSummaryRequest, Web2LeadRevenueFilter, ReferredByReportRequest, Web2LeadV2RequestModel. All use RequestModel base.
- [x] T024 [US3] Re-export all report models in `ab/api/models/__init__.py` and add to `__all__`
- [x] T025 [US3] Implement 8 Route definitions and ReportsEndpoint methods in `ab/api/endpoints/reports.py` — insurance, sales, sales_summary, sales_drilldown, top_revenue_customers, top_revenue_sales_reps, referred_by, web2lead. All POST to /reports/... paths with request_model and response_model.
- [x] T026 [US3] Create runnable example in `examples/reports.py` — demonstrate insurance, sales, top_revenue_customers
- [x] T027 [US3] Add fixture validation tests for report models in `tests/models/test_fixtures.py`
- [x] T028 [US3] Update `FIXTURES.md` with 8 report endpoint entries

**Checkpoint**: `api.reports.*` methods resolve, `pytest` passes

---

## Phase 6: User Story 4 — Email & SMS Communication (Priority: P4)

**Goal**: Enable developers to send documents via email, trigger transactional/template emails, send SMS, and manage SMS read status

**Independent Test**: Call `api.jobs.send_email(job_display_id, **kwargs)` and verify the SDK posts successfully

### Implementation for User Story 4

- [x] T029 [US4] Create email/SMS request models in `ab/api/models/jobs.py` — SendDocumentEmailModel (to, cc, bcc, subject, body, document_type), SendSMSModel (phone_number, message, template_id), MarkSmsAsReadModel (sms_ids). Research swagger and ABConnectTools `jobs/email.py`, `jobs/sms.py` for fields.
- [x] T030 [US4] Re-export email/SMS models in `ab/api/models/__init__.py` and add to `__all__`
- [x] T031 [US4] Add 4 email Route definitions and methods to `ab/api/endpoints/jobs.py` — send_email, send_document_email, create_transactional_email, send_template_email. Routes: POST /job/{jobDisplayId}/email, POST .../email/senddocument, POST .../email/createtransactionalemail, POST .../email/{emailTemplateGuid}/send
- [x] T032 [US4] Add 4 SMS Route definitions and methods to `ab/api/endpoints/jobs.py` — list_sms, send_sms, mark_sms_read, get_sms_template. Routes: GET /job/{jobDisplayId}/sms, POST .../sms, POST .../sms/read, GET .../sms/templatebased/{templateId}
- [x] T033 [US4] Create runnable example in `examples/email_sms.py` — demonstrate send_email, send_sms, list_sms
- [x] T034 [US4] Add fixture validation tests for email/SMS models in `tests/models/test_fixtures.py`
- [x] T035 [US4] Update `FIXTURES.md` with 8 email/SMS endpoint entries

**Checkpoint**: `api.jobs.send_email()` through `api.jobs.get_sms_template()` resolve, `pytest` passes

---

## Phase 7: User Story 5 — Extended Lookups & Commodities (Priority: P5)

**Goal**: Enable developers to access extended reference data via generic/named lookup methods and manage commodity records and classification mappings

**Independent Test**: Call `api.lookup.get_by_key("someKey")` and `api.commodities.search(**kwargs)` and verify typed responses

### Implementation for User Story 5

- [x] T036 [P] [US5] Create extended lookup models in `ab/api/models/lookup.py` — LookupValue (id, name, description, value), AccessKey (key, description), ParcelPackageType, DensityClassEntry. Use ResponseModel base. Research swagger and ABConnectTools `lookup.py` for actual field names.
- [x] T037 [P] [US5] Create commodity response models in `ab/api/models/commodities.py` — Commodity (id, description, freight_class, nmfc_code), CommodityMap (id, custom_name, commodity_id). Use ResponseModel base.
- [x] T038 [P] [US5] Create commodity request models in `ab/api/models/commodities.py` — CommodityCreateRequest, CommodityUpdateRequest, CommoditySearchRequest, CommoditySuggestionRequest, CommodityMapCreateRequest, CommodityMapUpdateRequest, CommodityMapSearchRequest. Use RequestModel base.
- [x] T039 [US5] Re-export all lookup and commodity models in `ab/api/models/__init__.py` and add to `__all__`
- [x] T040 [US5] Add 12 extended lookup Route definitions and methods to `ab/api/endpoints/lookup.py` — get_by_key(key), get_by_key_and_id(key, value_id), get_access_keys(), get_access_key(access_key), get_ppc_campaigns(), get_parcel_package_types(), get_document_types(), get_common_insurance(), get_density_class_map(), get_refer_categories(), get_refer_category_hierarchy(), reset_cache()
- [x] T041 [US5] Implement 5 Route definitions and CommoditiesEndpoint methods in `ab/api/endpoints/commodities.py` — get(commodity_id), update(commodity_id, **kwargs), create(**kwargs), search(**kwargs), suggestions(**kwargs)
- [x] T042 [US5] Implement 5 Route definitions and CommodityMapsEndpoint methods in `ab/api/endpoints/commodity_maps.py` — get(map_id), update(map_id, **kwargs), delete(map_id), create(**kwargs), search(**kwargs)
- [x] T043 [P] [US5] Create runnable example in `examples/lookup_extended.py` — demonstrate get_by_key, get_parcel_package_types, get_density_class_map
- [x] T044 [P] [US5] Create runnable example in `examples/commodities.py` — demonstrate create, search, get, update for both commodities and commodity maps
- [x] T045 [US5] Add fixture validation tests for lookup and commodity models in `tests/models/test_fixtures.py`
- [x] T046 [US5] Update `FIXTURES.md` with 22 extended lookup and commodity endpoint entries

**Checkpoint**: `api.lookup.get_by_key()`, `api.commodities.*`, `api.commodity_maps.*` resolve, `pytest` passes

---

## Phase 8: User Story 6 — Dashboard & Views (Priority: P6)

**Goal**: Enable developers to access operational dashboard data and manage saved grid view configurations

**Independent Test**: Call `api.dashboard.get()` and `api.views.list()` and verify typed responses

### Implementation for User Story 6

- [x] T047 [P] [US6] Create dashboard models in `ab/api/models/dashboard.py` — DashboardSummary, GridViewState, GridViewInfo. Use ResponseModel base. Research swagger and ABConnectTools `dashboard.py` for fields.
- [x] T048 [P] [US6] Create views/grids models in `ab/api/models/views.py` — GridViewDetails, GridViewAccess, StoredProcedureColumn, GridViewCreateRequest. Research ABConnectTools `views.py` for fields.
- [x] T049 [US6] Re-export all dashboard and views models in `ab/api/models/__init__.py` and add to `__all__`
- [x] T050 [US6] Implement 9 Route definitions and DashboardEndpoint methods in `ab/api/endpoints/dashboard.py` — get(**params), get_grid_views(), get_grid_view_state(view_id), save_grid_view_state(view_id, **kwargs), inbound(**kwargs), in_house(**kwargs), outbound(**kwargs), local_deliveries(**kwargs), recent_estimates(**kwargs)
- [x] T051 [US6] Implement 8 Route definitions and ViewsEndpoint methods in `ab/api/endpoints/views.py` — list(), get(view_id), create(**kwargs), delete(view_id), get_access_info(view_id), update_access(view_id, **kwargs), get_dataset_sps(), get_dataset_sp(sp_name)
- [x] T052 [P] [US6] Create runnable example in `examples/dashboard.py` — demonstrate get, inbound, get_grid_views
- [x] T053 [P] [US6] Create runnable example in `examples/views.py` — demonstrate list, get, create
- [x] T054 [US6] Add fixture validation tests for dashboard and views models in `tests/models/test_fixtures.py`
- [x] T055 [US6] Update `FIXTURES.md` with 17 dashboard and views endpoint entries

**Checkpoint**: `api.dashboard.*` and `api.views.*` resolve, `pytest` passes

---

## Phase 9: User Story 7 — Extended Companies, Contacts, Freight, Notes & Partners (Priority: P7)

**Goal**: Enable developers to manage extended company data (brands, geo, carriers, packaging), contact history/merge, freight providers, global notes, and partners

**Independent Test**: Call `api.companies.get_brands()`, `api.contacts.get_history_aggregated(contact_id)`, `api.notes.list()`, `api.partners.list()` and verify typed responses

### Implementation for User Story 7

- [x] T056 [P] [US7] Create extended company models in `ab/api/models/companies.py` — CompanyBrand, BrandTree, GeoSettings, GeoSettingsSaveRequest, CarrierAccount, CarrierAccountSaveRequest, PackagingSettings, PackagingLabor, PackagingTariff. Research swagger and ABConnectTools `companies.py` for fields.
- [x] T057 [P] [US7] Create extended contact models in `ab/api/models/contacts.py` — ContactHistory, ContactHistoryAggregated, ContactGraphData, ContactMergePreview. Research ABConnectTools `contacts.py` for fields.
- [x] T058 [P] [US7] Create freight provider models in `ab/api/models/jobs.py` — PricedFreightProvider, ShipmentPlanProvider. Research ABConnectTools `jobs/freightproviders.py` for fields.
- [x] T059 [P] [US7] Create global note models in `ab/api/models/notes.py` — GlobalNote, GlobalNoteCreateRequest, GlobalNoteUpdateRequest, SuggestedUser. Research ABConnectTools `note.py` for fields.
- [x] T060 [P] [US7] Create partner models in `ab/api/models/partners.py` — Partner, PartnerSearchRequest. Research ABConnectTools `partner.py` for fields.
- [x] T061 [US7] Re-export all new models from T056-T060 in `ab/api/models/__init__.py` and add to `__all__`
- [x] T062 [US7] Add 16 extended company Route definitions and methods to `ab/api/endpoints/companies.py` — get_brands(), get_brands_tree(), get_geo_area_companies(**params), get_geo_settings(company_id), save_geo_settings(company_id, **kwargs), get_global_geo_settings(), search_carrier_accounts(**params), suggest_carriers(**params), get_carrier_accounts(company_id), save_carrier_accounts(company_id, **kwargs), get_packaging_settings(company_id), save_packaging_settings(company_id, **kwargs), get_packaging_labor(company_id), save_packaging_labor(company_id, **kwargs), get_inherited_packaging_tariffs(company_id), get_inherited_packaging_labor(company_id). Company-scoped methods MUST use `self._resolve(company_id)` for code→UUID resolution.
- [x] T063 [US7] Add 5 extended contact Route definitions and methods to `ab/api/endpoints/contacts.py` — post_history(contact_id, **kwargs), get_history_aggregated(contact_id), get_history_graph_data(contact_id), merge_preview(merge_to_id, **kwargs), merge(merge_to_id, **kwargs)
- [x] T064 [US7] Add 4 freight provider Route definitions and methods to `ab/api/endpoints/jobs.py` — list_freight_providers(job_display_id, **params), save_freight_providers(job_display_id, **kwargs), get_freight_provider_rate_quote(job_display_id, option_index), add_freight_items(job_display_id, **kwargs)
- [x] T065 [US7] Implement 4 Route definitions and NotesEndpoint methods in `ab/api/endpoints/notes.py` — list(**params) with category/jobId/contactId/companyId query params, create(**kwargs), update(note_id, **kwargs), suggest_users(**params)
- [x] T066 [US7] Implement 3 Route definitions and PartnersEndpoint methods in `ab/api/endpoints/partners.py` — list(), get(partner_id), search(**kwargs)
- [x] T067 [P] [US7] Create runnable example in `examples/companies_extended.py` — demonstrate get_brands, get_geo_settings, get_carrier_accounts, get_packaging_settings
- [x] T068 [P] [US7] Create runnable example in `examples/contacts_extended.py` — demonstrate get_history_aggregated, merge_preview
- [x] T069 [P] [US7] Create runnable example in `examples/notes_global.py` — demonstrate list, create, update
- [x] T070 [P] [US7] Create runnable example in `examples/partners.py` — demonstrate list, search
- [x] T071 [P] [US7] Create runnable example in `examples/freight_providers.py` — demonstrate list_freight_providers, save_freight_providers
- [x] T072 [US7] Add fixture validation tests for all US7 models in `tests/models/test_fixtures.py`
- [x] T073 [US7] Update `FIXTURES.md` with 32 endpoint entries for extended companies, contacts, freight, notes, and partners

**Checkpoint**: All US7 endpoints resolve, `pytest` passes, FIXTURES.md fully updated

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Swagger compliance, documentation, and final validation across all stories

- [x] T074 Update swagger compliance test in `tests/test_swagger_compliance.py` — adjust expected unimplemented endpoint count from ~145 to ~39 to reflect all 106 new endpoints
- [x] T075 Update `tests/test_example_params.py` to cover all new endpoint methods — verify parameter names match swagger specs and transport types (params vs json) are correct per Constitution Principle IX
- [x] T076 [P] Create Sphinx documentation for new endpoint groups — `docs/rfq.rst`, `docs/reports.rst`, `docs/dashboard.rst`, `docs/views.rst`, `docs/commodities.rst`, `docs/commodity_maps.rst`, `docs/notes.rst`, `docs/partners.rst`. Each with endpoint description, code example, and model cross-reference.
- [x] T077 [P] Update Sphinx documentation for extended endpoint groups — `docs/jobs.rst` (on-hold, email, SMS, freight sections), `docs/lookup.rst` (extended methods), `docs/companies.rst` (brands, geo, carriers, packaging), `docs/contacts.rst` (history, merge)
- [x] T078 Create design decisions document at `specs/008-extended-operations/research.md` — document at least one departure from ABConnectTools per new endpoint group (reference D1-D12 from plan)
- [x] T079 Run full test suite (`pytest`) and verify zero regressions — all existing tests pass, all new fixture tests either pass or skip with actionable messages, swagger compliance test passes
- [x] T080 Run `ruff check .` and fix any linting issues across all new and modified files

**Checkpoint**: All 106 endpoints implemented, FIXTURES.md complete, Sphinx docs build without warnings, all tests pass

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **User Stories (Phases 3-9)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5 → P6 → P7)
- **Polish (Phase 10)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (RFQ)**: After Foundational — no other story dependencies. Creates new `rfq.py` endpoint + model files, extends `jobs.py` with 2 methods.
- **US2 (On-Hold)**: After Foundational — no other story dependencies. Extends `jobs.py` with 10 methods.
- **US3 (Reports)**: After Foundational — no other story dependencies. Creates new `reports.py` files.
- **US4 (Email/SMS)**: After Foundational — no other story dependencies. Extends `jobs.py` with 8 methods.
- **US5 (Lookups/Commodities)**: After Foundational — no other story dependencies. Extends `lookup.py`, creates `commodities.py` and `commodity_maps.py`.
- **US6 (Dashboard/Views)**: After Foundational — no other story dependencies. Creates `dashboard.py` and `views.py`.
- **US7 (Companies/Contacts/Freight/Notes/Partners)**: After Foundational — no other story dependencies. Extends `companies.py`, `contacts.py`, `jobs.py`; creates `notes.py`, `partners.py`.

**Note**: US2 and US4 both extend `jobs.py`. If running in parallel, coordinate to avoid merge conflicts in the same file. Sequential execution (P1→P2→P3→P4) avoids this naturally.

### Within Each User Story

1. Models before endpoints (endpoints depend on model names for Route definitions)
2. Model re-exports in `__init__.py` before endpoint implementation
3. Endpoint implementation before examples
4. Examples before fixture tests (tests depend on captured fixtures)
5. FIXTURES.md update after examples run

### Parallel Opportunities

- **Within Phase 2**: T003-T006 can all run in parallel (different files)
- **Within US5**: T036, T037, T038 can run in parallel (different model files)
- **Within US6**: T047, T048 can run in parallel (different model files)
- **Within US7**: T056-T060 can run in parallel (different model files); T067-T071 can run in parallel (different example files)
- **Across stories**: All user stories can start in parallel after Phase 2 (but single-developer sequential is recommended for `jobs.py` coordination)

---

## Parallel Example: User Story 5

```bash
# Launch all model tasks in parallel (different files):
Task: "Create extended lookup models in ab/api/models/lookup.py"        # T036
Task: "Create commodity response models in ab/api/models/commodities.py" # T037
Task: "Create commodity request models in ab/api/models/commodities.py"  # T038

# Then sequentially:
Task: "Re-export models in ab/api/models/__init__.py"  # T039

# Then launch endpoint tasks in parallel (different files):
Task: "Add lookup methods to ab/api/endpoints/lookup.py"            # T040
Task: "Implement CommoditiesEndpoint in ab/api/endpoints/commodities.py"     # T041
Task: "Implement CommodityMapsEndpoint in ab/api/endpoints/commodity_maps.py" # T042

# Then examples in parallel:
Task: "Create examples/lookup_extended.py"  # T043
Task: "Create examples/commodities.py"      # T044
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T006)
3. Complete Phase 3: User Story 1 — RFQ (T007-T014)
4. **STOP and VALIDATE**: Test RFQ endpoints independently
5. Checkpoint commit

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (RFQ) → 9 endpoints → Checkpoint commit
3. Add US2 (On-Hold) → +10 endpoints → Checkpoint commit
4. Add US3 (Reports) → +8 endpoints → Checkpoint commit
5. Add US4 (Email/SMS) → +8 endpoints → Checkpoint commit
6. Add US5 (Lookups/Commodities) → +22 endpoints → Checkpoint commit
7. Add US6 (Dashboard/Views) → +17 endpoints → Checkpoint commit
8. Add US7 (Extended) → +32 endpoints → Checkpoint commit
9. Polish → PR ready

### Per-Story DISCOVER Workflow

Each user story phase maps to DISCOVER:
- **D (Determine)**: Research is done in T002 (upfront) + model task descriptions reference ABConnectTools
- **I (Implement models)**: Model creation tasks (ResponseModel + RequestModel)
- **S (Scaffold endpoints)**: Route definitions + endpoint methods
- **C (Call & Capture)**: Example files → run against staging → fixture capture
- **O (Observe tests)**: Fixture validation tests + FIXTURES.md updates
- **V (Verify & commit)**: Checkpoint commit after each story phase
- **E (Enrich docs)**: Sphinx docs in Phase 10 (batched for efficiency)
- **R (Release)**: PR after all stories complete

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each story phase checkpoint
- All model fields should be `Optional` initially — refined during fixture capture
- `**kwargs: Any` pattern for all endpoint methods per feature 007 methodology
- Request models use `extra="forbid"`, response models use `extra="allow"` with drift logging
- Company-scoped methods MUST use `self._resolve(company_id)` for code→UUID resolution
