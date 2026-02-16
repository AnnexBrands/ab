# Tasks: Remaining API Endpoints (009)

**Input**: Design documents from `/specs/009-remaining-endpoints/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Fixture validation tests are INCLUDED per Constitution Principle III (Four-Way Harmony) — every endpoint requires a skip-marked test.

**Organization**: Tasks grouped by user story. Each story maps to a DISCOVER workflow batch. Stories can be implemented independently after Phase 2 (Foundational).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Verify baseline and confirm patterns before adding new endpoints

- [x] T001 Run existing test suite to confirm baseline passes — `pytest tests/ --tb=line`
- [x] T002 Verify swagger specs are current — read `ab/api/schemas/acportal.json` and `ab/api/schemas/abc.json` to confirm remaining endpoints match research.md gap analysis

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No new infrastructure needed — the SDK core, auth, HTTP client, Route system, and DISCOVER workflow are all established from Features 001/007/008. This phase confirms readiness.

- [x] T003 Review existing endpoint patterns in `ab/api/endpoints/companies.py` and `ab/api/models/companies.py` to confirm Route definition, model inheritance, and `__init__.py` registration conventions
- [x] T004 Review `ab/client.py` to identify where new endpoint classes will be registered and confirm the registration pattern

**Checkpoint**: Foundation confirmed — user story implementation can begin in parallel

---

## Phase 3: User Story 1 — Admin Configuration Access (Priority: P1)

**Goal**: Expose 18 company setup endpoints (Calendar, External Accounts, Document Templates, Settings, Container Thickness, Planner) as typed SDK methods in a new `company_setup.py` file

**Independent Test**: Call any company setup endpoint with a valid companyId and verify the SDK returns a properly typed response or skip-marked test exists

### Implementation for User Story 1

- [x] T005 [US1] Create Pydantic response models (CalendarDay, CalendarBaseInfo, CalendarTimeInfo, StripeConnectUrl, StripeConnection, DocumentTemplate, GridSettings, CompanySetupData, ContainerThickness, PlannerEntry) in `ab/api/models/company_setup.py` — derive fields from swagger `components/schemas`, use `ResponseModel` base with camelCase aliases
- [x] T006 [P] [US1] Create Pydantic request models (StripeCompleteRequest, DocumentTemplateRequest, GridSettingsRequest, ContainerThicknessRequest) in `ab/api/models/company_setup.py` — use `RequestModel` base with `extra="forbid"`
- [x] T007 [US1] Create `CompanySetupEndpoint` class with 18 Route definitions and endpoint methods in `ab/api/endpoints/company_setup.py` — Calendar(4), ExtAccounts(3), DocTemplates(4), Settings(3), ContainerThickness(3), Planner(1). Follow `**kwargs` signature pattern, use correct transport (`params=` for GET, `json=` for POST/PUT)
- [x] T008 [US1] Register `CompanySetupEndpoint` in `ab/client.py` and update `ab/api/endpoints/__init__.py`
- [x] T009 [US1] Register new models in `ab/api/models/__init__.py`
- [x] T010 [P] [US1] Create fixture validation tests (18 test functions with `pytest.skip`) in `tests/models/test_company_setup_fixtures.py`
- [x] T011 [P] [US1] Create example script demonstrating Calendar, DocTemplates, and Settings calls in `examples/company_setup.py`
- [x] T012 [US1] Add 18 company setup endpoints to `FIXTURES.md` in unified 4D format
- [x] T013 [P] [US1] Create Sphinx documentation page in `docs/company_setup.rst`
- [x] T014 [US1] Run `pytest tests/ --tb=line` to verify no regressions and all new tests skip gracefully

**Checkpoint**: Company setup endpoints (18) callable via SDK. Fixture tests skip. No regressions.

---

## Phase 4: User Story 2 — Admin Settings Management (Priority: P1)

**Goal**: Expose 13 admin endpoints (AdvancedSettings, CarrierErrorMessage, GlobalSettings, LogBuffer) as typed SDK methods in a new `admin.py` file

**Independent Test**: Call admin settings GET endpoints and verify typed responses or skip-marked tests exist

### Implementation for User Story 2

- [x] T015 [US2] Create Pydantic response models (AdvancedSetting, CarrierErrorMessage, CompanyHierarchy, InsuranceException, IntacctSettings) in `ab/api/models/admin.py`
- [x] T016 [P] [US2] Create Pydantic request models (AdvancedSettingRequest, CarrierErrorMessageRequest, InsuranceExceptionFilter, IntacctSettingsRequest, LogFlushRequest) in `ab/api/models/admin.py`
- [x] T017 [US2] Create `AdminEndpoint` class with 13 Route definitions and endpoint methods in `ab/api/endpoints/admin.py` — AdvancedSettings(4), CarrierErrorMessage(2), GlobalSettings(5), LogBuffer(2). Note: `approveinsuranceexception` uses `JobId` query param on POST
- [x] T018 [US2] Register `AdminEndpoint` in `ab/client.py` and update `ab/api/endpoints/__init__.py` and `ab/api/models/__init__.py`
- [x] T019 [P] [US2] Create fixture validation tests (13 test functions with `pytest.skip`) in `tests/models/test_admin_fixtures.py`
- [x] T020 [P] [US2] Create example script demonstrating AdvancedSettings and GlobalSettings calls in `examples/admin.py`
- [x] T021 [US2] Add 13 admin endpoints to `FIXTURES.md` in unified 4D format
- [x] T022 [P] [US2] Create Sphinx documentation page in `docs/admin.rst`
- [x] T023 [US2] Run `pytest tests/ --tb=line` to verify no regressions

**Checkpoint**: Admin endpoints (13) callable via SDK. Combined with US1 = 31 endpoints added. No regressions.

---

## Phase 5: User Story 3 — Account and Authentication Operations (Priority: P2)

**Goal**: Expose 10 account endpoints (register, confirm, forgot, reset password, set password, profile, payment source) as typed SDK methods in a new `account.py` file

**Independent Test**: Call `GET /account/profile` and verify typed `UserProfile` response or skip-marked test exists

### Implementation for User Story 3

- [x] T024 [US3] Create Pydantic response models (AccountResponse, TokenVerification, UserProfile, PaymentSource) in `ab/api/models/account.py`
- [x] T025 [P] [US3] Create Pydantic request models (RegisterRequest, SendConfirmationRequest, ConfirmRequest, ForgotRequest, ResetPasswordRequest, SetPasswordRequest, PaymentSourceRequest) in `ab/api/models/account.py`
- [x] T026 [US3] Create `AccountEndpoint` class with 10 Route definitions and endpoint methods in `ab/api/endpoints/account.py` — Note: `verifyresettoken` uses `username` and `token` query params; `paymentsource/{sourceId}` uses URL path param
- [x] T027 [US3] Register `AccountEndpoint` in `ab/client.py` and update `__init__.py` files
- [x] T028 [P] [US3] Create fixture validation tests (10 test functions with `pytest.skip`) in `tests/models/test_account_fixtures.py`
- [x] T029 [P] [US3] Create example script demonstrating profile and verifyresettoken calls in `examples/account.py`
- [x] T030 [US3] Add 10 account endpoints to `FIXTURES.md` in unified 4D format
- [x] T031 [P] [US3] Create Sphinx documentation page in `docs/account.rst`
- [x] T032 [US3] Run `pytest tests/ --tb=line` to verify no regressions

**Checkpoint**: Account endpoints (10) callable via SDK. Combined total = 41 endpoints added. No regressions.

---

## Phase 6: User Story 4 — Miscellaneous Job Operations (Priority: P2)

**Goal**: Extend `jobs.py` with 12 remaining job endpoints (misc, booking, tracking shipment, tracking v2, email labelrequest) to complete full job lifecycle coverage

**Independent Test**: Call `GET /job/documentConfig` and verify typed response or skip-marked test exists

### Implementation for User Story 4

- [x] T033 [US4] Add new Pydantic response models for job extensions (DocumentConfig, JobFeedback, JobAccessLevel, SubManagementStatus, TrackingShipment, BookingResult) to `ab/api/models/jobs.py` or a suitable existing model file
- [x] T034 [P] [US4] Add new Pydantic request models for job extensions (FeedbackRequest, TransferRequest, ChangeAgentRequest, BookRequest, LabelRequest) to the same model file
- [x] T035 [US4] Add 12 Route definitions and endpoint methods to `ab/api/endpoints/jobs.py` — Job misc(8), JobBooking(1), JobTracking shipment(1), JobTrackingV2(1), Email labelrequest(1). Note: v2 tracking path is `/v2/job/{jobDisplayId}/tracking/{historyAmount}`; email labelrequest path is `/email/{jobDisplayId}/labelrequest`
- [x] T036 [US4] Update model `__init__.py` if new model file created
- [x] T037 [P] [US4] Add 12 fixture validation test functions (with `pytest.skip`) to existing `tests/models/test_job_fixtures.py` or new test file
- [x] T038 [P] [US4] Extend `examples/jobs.py` with new endpoint calls (documentConfig, feedback, transfer, book)
- [x] T039 [US4] Add 12 job extension endpoints to `FIXTURES.md` in unified 4D format
- [x] T040 [P] [US4] Update Sphinx documentation in `docs/jobs.rst` with new endpoints
- [x] T041 [US4] Run `pytest tests/ --tb=line` to verify no regressions

**Checkpoint**: Job lifecycle 100% covered. Combined total = 53 endpoints added. No regressions.

---

## Phase 7: User Story 5 — Physical Resource Management (Priority: P3)

**Goal**: Add 8 Material/Truck endpoints to `company_setup.py` (created in US1) for logistics resource management

**Dependencies**: US1 must be complete (creates `company_setup.py`)

### Implementation for User Story 5

- [x] T042 [US5] Add Material and Truck response models (Material, Truck) and request models (MaterialRequest, TruckRequest) to `ab/api/models/company_setup.py`
- [x] T043 [US5] Add 8 Route definitions and endpoint methods to `ab/api/endpoints/company_setup.py` — Material CRUD(4), Truck CRUD(4). Note: Truck GET accepts `onlyOwnTrucks` query param; ContainerThickness DELETE uses `containerId` query param
- [x] T044 [P] [US5] Add 8 fixture validation test functions (with `pytest.skip`) to `tests/models/test_company_setup_fixtures.py`
- [x] T045 [P] [US5] Extend `examples/company_setup.py` with Material and Truck demonstration calls
- [x] T046 [US5] Add 8 material/truck endpoints to `FIXTURES.md` in unified 4D format
- [x] T047 [P] [US5] Update Sphinx documentation in `docs/company_setup.rst` with Material and Truck sections
- [x] T048 [US5] Run `pytest tests/ --tb=line` to verify no regressions

**Checkpoint**: Physical resource endpoints (8) callable via SDK. company_setup.py now has all 26 routes. Combined total = 61 endpoints added.

---

## Phase 8: User Story 6 — Integration and Communication Endpoints (Priority: P3)

**Goal**: Expose 28 endpoints across Intacct (5), E-Sign (2), Webhooks (6), SMS Templates (5), Notifications (1), Values (1), Users ext (1), and ABC gaps (7) — each in their own new file

**Independent Test**: Call any integration endpoint and verify typed response or skip-marked test exists

### Implementation for User Story 6

#### Intacct (5 endpoints)
- [x] T049 [P] [US6] Create Pydantic models (JobIntacctData, JobIntacctRequest, JobIntacctDraftRequest, ApplyRebateRequest) in `ab/api/models/intacct.py`
- [x] T050 [P] [US6] Create `IntacctEndpoint` class with 5 Routes in `ab/api/endpoints/intacct.py` — GET, POST, draft, applyRebate, DELETE by jobDisplayId/franchiseeId

#### E-Sign (2 endpoints)
- [x] T051 [P] [US6] Create Pydantic models (ESignResult, ESignData) in `ab/api/models/esign.py`
- [x] T052 [P] [US6] Create `ESignEndpoint` class with 2 Routes in `ab/api/endpoints/esign.py` — result(GET, query: envelope, event), e-sign by jobDisplayId/bookingKey(GET)

#### Webhooks (6 endpoints)
- [x] T053 [P] [US6] Create `WebhooksEndpoint` class with 6 Routes in `ab/api/endpoints/webhooks.py` — Stripe(3), Twilio(3). Note: these are server-side callback receivers; document accordingly

#### SMS Templates (5 endpoints)
- [x] T054 [P] [US6] Create Pydantic models (SmsTemplate, NotificationTokens, SmsTemplateRequest) in `ab/api/models/sms_templates.py`
- [x] T055 [P] [US6] Create `SmsTemplateEndpoint` class with 5 Routes in `ab/api/endpoints/sms_templates.py` — list(GET, query: companyId), notificationTokens(GET), save(POST), get/delete by templateId

#### Notifications + Values + Users ext (3 endpoints)
- [x] T056 [P] [US6] Create `NotificationsEndpoint` with 1 Route in `ab/api/endpoints/notifications.py` and Notification model in `ab/api/models/notifications.py`
- [x] T057 [P] [US6] Create `ValuesEndpoint` with 1 Route in `ab/api/endpoints/values.py` (health check, returns List[str])
- [x] T058 [P] [US6] Add 1 Route (_GET_POC_USERS) and method to `ab/api/endpoints/users.py`

#### ABC Gaps (7 endpoints)
- [x] T059 [P] [US6] Create `ABCTestEndpoint` with 3 Routes in `ab/api/endpoints/abc_test.py` — contact(GET, query: crmContactId), recentestimates(GET), renderedtemplate(GET). Use `api_surface="abc"`
- [x] T060 [P] [US6] Create `ABCReportsEndpoint` with 1 Route in `ab/api/endpoints/abc_reports.py` — webrevenue(GET, query: accessKey, startDate, endDate). Use `api_surface="abc"`. Also add ABC logbuffer flush (1 Route)
- [x] T061 [P] [US6] Add 1 Route (_POST_V2) to `ab/api/endpoints/web2lead.py` and Web2LeadV2Request model. Use `api_surface="abc"`
- [x] T062 [P] [US6] Add 1 Route (_QUOTE_REQUEST_V1) to `ab/api/endpoints/autoprice.py`. Use `api_surface="abc"`

#### Registration and Tests
- [x] T063 [US6] Register all new endpoint classes (IntacctEndpoint, ESignEndpoint, WebhooksEndpoint, SmsTemplateEndpoint, NotificationsEndpoint, ValuesEndpoint, ABCTestEndpoint, ABCReportsEndpoint) in `ab/client.py` and update all `__init__.py` files
- [x] T064 [P] [US6] Create fixture validation tests for Intacct, E-Sign, SMS Templates in `tests/models/test_intacct_fixtures.py`, `tests/models/test_esign_fixtures.py`, `tests/models/test_sms_template_fixtures.py`
- [x] T065 [P] [US6] Create example scripts: `examples/intacct.py`, `examples/esign.py`, `examples/webhooks.py`, `examples/sms_templates.py`, `examples/notifications.py`, `examples/abc_test.py`, `examples/abc_reports.py`
- [x] T066 [US6] Add 28 integration/communication endpoints to `FIXTURES.md` in unified 4D format
- [x] T067 [P] [US6] Create Sphinx documentation pages: `docs/intacct.rst`, `docs/esign.rst`, `docs/webhooks.rst`, `docs/sms_templates.rst`
- [x] T068 [US6] Run `pytest tests/ --tb=line` to verify no regressions

**Checkpoint**: All integration/communication endpoints (28) callable via SDK. Combined total = 89 endpoints added.

---

## Phase 9: User Story 7 — Extended CRUD Operations (Priority: P3)

**Goal**: Extend 5 existing endpoint files with 13 remaining ACPortal CRUD operations (Companies +7, Contacts +2, Address +2, Documents +2) to achieve 100% coverage

**Independent Test**: Call any extended CRUD endpoint and verify typed response consistent with existing entity models

### Implementation for User Story 7

- [x] T069 [P] [US7] Add 7 Routes and methods to `ab/api/endpoints/companies.py` — filteredCustomers(POST), infoFromKey(GET), search(GET), simplelist(POST), capabilities GET/POST, franchiseeAddresses(GET). Add any new response/request models to `ab/api/models/companies.py`
- [x] T070 [P] [US7] Add 2 Routes and methods to `ab/api/endpoints/contacts.py` — customers(POST), search(POST). Add any new models to `ab/api/models/contacts.py`
- [x] T071 [P] [US7] Add 2 Routes and methods to `ab/api/endpoints/address.py` — avoidValidation(POST), validated(POST). Add any new models to `ab/api/models/address.py`
- [x] T072 [P] [US7] Add 2 Routes and methods to `ab/api/endpoints/documents.py` — get/thumbnail/{docPath}(GET), hide/{docId}(PUT). Add any new models to `ab/api/models/documents.py`
- [x] T073 [P] [US7] Add fixture validation test functions for new endpoints to existing test files: `tests/models/test_company_fixtures.py`, `tests/models/test_contact_fixtures.py`, `tests/models/test_address_fixtures.py`, `tests/models/test_document_fixtures.py`
- [x] T074 [P] [US7] Extend existing example scripts (`examples/companies.py`, `examples/contacts.py`, `examples/address.py`, `examples/documents.py`) with new endpoint calls
- [x] T075 [US7] Add 13 extended CRUD endpoints to `FIXTURES.md` in unified 4D format
- [x] T076 [P] [US7] Update existing Sphinx documentation pages with new endpoint sections
- [x] T077 [US7] Run `pytest tests/ --tb=line` to verify no regressions

**Checkpoint**: All extended CRUD endpoints (13) callable via SDK. Combined total = 102 endpoints added. **100% API coverage achieved.**

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, tracking updates, and cross-story consistency checks

- [x] T078 Run full test suite including `pytest tests/test_example_params.py` to verify all param names match swagger (Principle IX)
- [x] T079 Run swagger compliance tests to confirm no unimplemented endpoints remain
- [x] T080 Verify `FIXTURES.md` has exactly 328 total entries (226 existing + 102 new) in correct 4D format
- [x] T081 Verify all new endpoint classes are importable via `from ab import ABClient` and accessible as client properties
- [x] T082 [P] Review all Sphinx docs build without warnings — `make html` in `docs/`
- [x] T083 Update `specs/009-remaining-endpoints/spec.md` status from Draft to Complete
- [x] T084 Final checkpoint commit with all 102 endpoints implemented

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Phase 2 — creates `company_setup.py`
- **US2 (Phase 4)**: Depends on Phase 2 — independent of US1
- **US3 (Phase 5)**: Depends on Phase 2 — independent of US1/US2
- **US4 (Phase 6)**: Depends on Phase 2 — independent of US1/US2/US3
- **US5 (Phase 7)**: Depends on **US1** (company_setup.py must exist)
- **US6 (Phase 8)**: Depends on Phase 2 — independent of other stories
- **US7 (Phase 9)**: Depends on Phase 2 — extends existing files only
- **Polish (Phase 10)**: Depends on ALL user stories being complete

### User Story Dependencies

```
Phase 2 (Foundational)
├── US1 (P1) ──→ US5 (P3) [file dependency: company_setup.py]
├── US2 (P1) ──→ (independent)
├── US3 (P2) ──→ (independent)
├── US4 (P2) ──→ (independent)
├── US6 (P3) ──→ (independent)
└── US7 (P3) ──→ (independent)
         └──────→ Phase 10 (Polish)
```

### Within Each User Story (DISCOVER order)

1. Models (I phase) — response models, then request models
2. Endpoints (S phase) — Route definitions and methods
3. Registration (S phase) — client.py and __init__.py
4. Tests (S phase) — fixture validation with skip
5. Examples (C phase) — runnable scripts
6. FIXTURES.md (O phase) — tracking update
7. Documentation (E phase) — Sphinx pages
8. Verify (V phase) — run pytest

### Parallel Opportunities

**Within US6** (largest story — 28 endpoints across 8+ files):
All T049–T062 are marked [P] and can execute simultaneously since they create independent files.

**Across stories** (after Phase 2):
US1, US2, US3, US4, US6, US7 can all start in parallel. Only US5 must wait for US1.

**PR delivery alignment**:
- PR 1: US1 + US2 + US5 = 39 endpoints (Plan Phase 1)
- PR 2: US3 + US4 = 22 endpoints (Plan Phase 2)
- PR 3: US6 = 21 endpoints (Plan Phase 3, minus ABC)
- PR 4: US7 + US6-ABC = 20 endpoints (Plan Phase 4)

---

## Parallel Example: User Story 6

```bash
# Launch all independent endpoint files simultaneously:
Task: "Create IntacctEndpoint in ab/api/endpoints/intacct.py"        # T050
Task: "Create ESignEndpoint in ab/api/endpoints/esign.py"            # T052
Task: "Create WebhooksEndpoint in ab/api/endpoints/webhooks.py"      # T053
Task: "Create SmsTemplateEndpoint in ab/api/endpoints/sms_templates.py"  # T055
Task: "Create NotificationsEndpoint in ab/api/endpoints/notifications.py" # T056
Task: "Create ValuesEndpoint in ab/api/endpoints/values.py"          # T057
Task: "Create ABCTestEndpoint in ab/api/endpoints/abc_test.py"       # T059
Task: "Create ABCReportsEndpoint in ab/api/endpoints/abc_reports.py" # T060

# After all files created, register together:
Task: "Register all new endpoints in ab/client.py"                    # T063
```

---

## Implementation Strategy

### MVP First (US1 + US2 = 31 endpoints)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US1 — Company Setup (18 endpoints)
4. Complete Phase 4: US2 — Admin Settings (13 endpoints)
5. **STOP and VALIDATE**: Run full test suite, verify 31 new endpoints
6. Create PR 1 with 31 endpoints

### Incremental Delivery (4 PRs)

1. **PR 1** (US1 + US2 + US5): 39 endpoints → Company Setup + Admin + Materials/Trucks
2. **PR 2** (US3 + US4): 22 endpoints → Account + Extended Jobs
3. **PR 3** (US6 minus ABC): 21 endpoints → Intacct, E-Sign, Webhooks, SMS, Notifications, Values
4. **PR 4** (US7 + US6-ABC): 20 endpoints → Extended entities + ABC gaps
5. Each PR independently testable; existing tests never break

### Parallel Agent Strategy

With multiple agents:
1. All agents complete Phase 2 review
2. Once confirmed:
   - Agent A: US1 + US5 (company_setup.py — 26 endpoints)
   - Agent B: US2 (admin.py — 13 endpoints)
   - Agent C: US3 (account.py — 10 endpoints)
   - Agent D: US4 (jobs.py extend — 12 endpoints)
3. Then:
   - Agent A: US6 part 1 (intacct, esign, webhooks — 13 endpoints)
   - Agent B: US6 part 2 (sms, notifications, values, ABC — 15 endpoints)
   - Agent C: US7 (extended entities — 13 endpoints)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story independently completable and testable
- DISCOVER workflow order within each story: Models → Endpoints → Register → Tests → Examples → FIXTURES.md → Docs → Verify
- Commit after each story phase completes (Principle VIII)
- company_setup.py is the largest new file (26 routes) — consider US1+US5 as one implementation batch
- jobs.py grows to 67 routes (D2 flat-file decision from Feature 008)
- Webhook endpoints are server-side callbacks — document as testing-only in SDK context
