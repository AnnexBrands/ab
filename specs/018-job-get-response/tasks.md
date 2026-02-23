# Tasks: Complete Job Get Response Model

**Input**: Design documents from `/specs/018-job-get-response/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Test updates are included as they are explicitly required by the spec (US3) and are integral to verifying model correctness.

**Organization**: Tasks are grouped by user story. US1 (scalar fields) can be completed and verified independently before US2 (deep sub-models) begins.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: No setup needed — this feature modifies an existing codebase with no new dependencies or project structure changes.

(No tasks in this phase.)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Verify fixture data and understand current model state before making changes.

- [x] T001 Verify Job.json fixture is current by running `python -m examples jobs get 2000000` and confirming fixture is captured at tests/fixtures/Job.json
- [x] T002 Run existing test suite `pytest tests/models/test_job_models.py tests/integration/test_jobs.py -v` to confirm baseline (tests pass with skipped assertions)

**Checkpoint**: Baseline confirmed — fixture is current, existing tests pass.

---

## Phase 3: User Story 1 — Cast Job API Response Without Extra-Field Warnings (Priority: P1) MVP

**Goal**: Add all 27 missing top-level fields to the `Job` model so that `Job.model_validate(fixture_data)` produces zero extra-field warnings. Fields that reference nested objects use `Optional[dict]` or `Optional[List[dict]]` as placeholders (deep typing comes in US2).

**Independent Test**: Load `Job.json` fixture, call `Job.model_validate(data)`, assert `model_extra` is empty.

### Implementation for User Story 1

- [x] T003 [US1] Add 12 scalar fields to Job model in ab/api/models/jobs.py: `booked_date`, `owner_company_id`, `total_sell_price`, `write_access`, `access_level`, `status_id`, `job_mgmt_sub_id`, `is_cancelled`, `expected_pickup_date`, `expected_delivery_date`, `label_request_sent_date`, `job_type` — all `Optional` with proper camelCase aliases
- [x] T004 [US1] Add 15 nested/list fields to Job model as dict placeholders in ab/api/models/jobs.py: `customer_contact` (Optional[dict]), `pickup_contact` (Optional[dict]), `delivery_contact` (Optional[dict]), `freight_items` (Optional[List[dict]]), `job_summary_snapshot` (Optional[dict]), `notes` (Optional[List[dict]]), `active_on_hold_info` (Optional[dict]), `freight_info` (Optional[dict]), `freight_providers` (Optional[List[dict]]), `timeline_tasks` (Optional[List[dict]]), `documents` (Optional[List[dict]]), `payment_info` (Optional[dict]), `agent_payment_info` (Optional[dict]), `sla_info` (Optional[dict]), `prices` (Optional[List[dict]])
- [x] T005 [US1] Verify zero extra-field warnings by running `python -m examples jobs get 2000000` and confirming no "unexpected field" lines in output

**Checkpoint**: `Job.model_validate(fixture_data)` has empty `model_extra`. Zero warnings from example runner. US1 is independently verifiable.

---

## Phase 4: User Story 2 — Deep Typing for Nested Job Structures (Priority: P2)

**Goal**: Replace `dict` placeholders from US1 with strongly-typed pydantic sub-models for all nested structures that have data in the fixture. Follow the deep-model pattern from feature 016 (CompanyDetails).

**Independent Test**: Load `Job.json` fixture, validate against Job model, assert nested fields are instances of typed sub-models (not dict).

### Implementation for User Story 2

Leaf models first (no dependencies), then composites, then update Job field types.

- [x] T006 [P] [US2] Create `JobContactEmail` sub-model (4 fields) in ab/api/models/jobs.py — id, email, invalid, dont_spam
- [x] T007 [P] [US2] Create `JobContactPhone` sub-model (2 fields) in ab/api/models/jobs.py — id, phone
- [x] T008 [P] [US2] Create `ContactDetails` sub-model (33 fields) in ab/api/models/jobs.py — full contact person with company as dict, emails_list/phones_list/addresses_list as List[dict]
- [x] T009 [P] [US2] Create `JobItemMaterial` sub-model (34 fields) in ab/api/models/jobs.py — per data-model.md field table, preserve API typo `mateialMasterID`
- [x] T010 [P] [US2] Create `JobSummarySnapshot` sub-model (24 fields) in ab/api/models/jobs.py — per data-model.md field table
- [x] T011 [P] [US2] Create `ActiveOnHoldInfo` sub-model (8 fields) in ab/api/models/jobs.py — id, responsible_party_type_id, reason_id, responsible_party, reason, comment, start_date, created_by
- [x] T012 [P] [US2] Create `JobDocument` sub-model (10 fields) in ab/api/models/jobs.py — id, path, thumbnail_path, description, type_name, type_id, file_name, shared, tags, job_items
- [x] T013 [P] [US2] Create `JobSlaInfo` sub-model (5 fields) in ab/api/models/jobs.py — days, expedited, start_date, finish_date, total_on_hold_days
- [x] T014 [P] [US2] Create `JobFreightInfo` sub-model (5 fields) in ab/api/models/jobs.py — per data-model.md, typed from server source (null in fixture)
- [x] T015 [P] [US2] Create `JobPaymentInfo` sub-model (5 fields) in ab/api/models/jobs.py — per data-model.md, typed from server source (null in fixture)
- [x] T016 [P] [US2] Create `JobAgentPaymentInfo` sub-model (2 fields) in ab/api/models/jobs.py — amount, paid_date
- [x] T017 [P] [US2] Create `JobFreightItem` sub-model (11 fields) in ab/api/models/jobs.py — per data-model.md, typed from server source (empty list in fixture)
- [x] T018 [US2] Create `JobContactDetails` composite sub-model (13 fields) in ab/api/models/jobs.py — imports CompanyAddress from common.py, uses ContactDetails, JobContactEmail, JobContactPhone (depends on T006–T008)
- [x] T019 [US2] Create `JobItem` sub-model (~75 fields) in ab/api/models/jobs.py — per data-model.md field table, materials field typed as List[JobItemMaterial] (depends on T009)
- [x] T020 [US2] Update Job model field types in ab/api/models/jobs.py — change dict placeholders to typed sub-models: customer_contact→JobContactDetails, pickup_contact→JobContactDetails, delivery_contact→JobContactDetails, items→List[JobItem], freight_items→List[JobFreightItem], job_summary_snapshot→JobSummarySnapshot, active_on_hold_info→ActiveOnHoldInfo, documents→List[JobDocument], freight_info→JobFreightInfo, payment_info→JobPaymentInfo, agent_payment_info→JobAgentPaymentInfo, sla_info→JobSlaInfo (depends on T006–T019)
- [x] T021 [US2] Verify deep typing by running `python -m examples jobs get 2000000` — confirm zero warnings and that nested fields are typed model instances, not dicts

**Checkpoint**: All nested structures are strongly typed. `job.customer_contact.address.city` works. `job.items[0].materials[0].material_name` works. US2 verifiable with fixture validation.

---

## Phase 5: User Story 3 — Adequate Test Coverage for Job Model Casting (Priority: P3)

**Goal**: Enable all previously disabled `assert_no_extra_fields` assertions in job-related tests. Add recursive sub-model validation.

**Independent Test**: `pytest tests/models/test_job_models.py tests/integration/test_jobs.py -v` passes with all assertions enabled, no commented-out checks.

### Implementation for User Story 3

- [x] T022 [US3] Enable `assert_no_extra_fields(model)` in tests/models/test_job_models.py::TestJobModels::test_job — uncomment the assertion and remove the "not yet fully typed" comment
- [x] T023 [US3] Add recursive sub-model extra-field checks to tests/models/test_job_models.py::test_job — assert_no_extra_fields on customer_contact, customer_contact.contact, customer_contact.email, customer_contact.phone, customer_contact.address, items[0], items[0].materials[0], job_summary_snapshot, active_on_hold_info, documents[0], sla_info
- [x] T024 [US3] Enable `assert_no_extra_fields(result)` in tests/integration/test_jobs.py::TestJobsIntegration::test_get_job — remove "Job not yet fully typed" comment and add the assertion
- [x] T025 [US3] Run full test suite `pytest tests/models/test_job_models.py tests/integration/test_jobs.py -v` and verify all assertions pass with zero failures

**Checkpoint**: All job tests pass with full extra-field validation enabled. No commented-out assertions remain.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup.

- [x] T026 Run `python -m examples jobs get 2000000` end-to-end — confirm zero warnings in output
- [x] T027 Run full pytest suite `pytest` — confirm no regressions across entire test suite
- [x] T028 Verify model file organization in ab/api/models/jobs.py — sub-models should be grouped with section comment headers (e.g., `# ---- Contact sub-models ----`) following existing convention

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Skipped — no setup needed
- **Foundational (Phase 2)**: T001–T002 baseline verification
- **US1 (Phase 3)**: Depends on Phase 2. T003–T004 can be done in one edit. T005 validates.
- **US2 (Phase 4)**: Depends on US1 (T003–T004 must be done first so scalar fields exist). T006–T017 are all parallel leaf models. T018–T019 are composites. T020 wires everything together.
- **US3 (Phase 5)**: Depends on US2 (models must be complete for assertions to pass). T022–T024 are all parallel (different test files/methods). T025 validates.
- **Polish (Phase 6)**: Depends on US3 completion.

### User Story Dependencies

- **US1 (P1)**: Can start after Phase 2 — **MVP, delivers zero-warning Job model**
- **US2 (P2)**: Depends on US1 — dict placeholders must exist before being replaced with typed models
- **US3 (P3)**: Depends on US2 — test assertions require fully typed models to pass

### Within User Story 2

- T006–T017 (12 leaf sub-models): ALL parallelizable — different classes, no inter-dependencies
- T018–T019 (composite models): Depend on leaf models they reference
- T020 (update Job types): Depends on all sub-models being defined
- T021 (verify): Depends on T020

### Parallel Opportunities

```bash
# Phase 4 — launch all 12 leaf sub-models in parallel:
T006: JobContactEmail
T007: JobContactPhone
T008: ContactDetails
T009: JobItemMaterial
T010: JobSummarySnapshot
T011: ActiveOnHoldInfo
T012: JobDocument
T013: JobSlaInfo
T014: JobFreightInfo
T015: JobPaymentInfo
T016: JobAgentPaymentInfo
T017: JobFreightItem

# Phase 5 — launch all 3 test updates in parallel:
T022: test_job_models.py::test_job assertion
T023: test_job_models.py recursive checks
T024: test_jobs.py::test_get_job assertion
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Verify baseline (T001–T002)
2. Complete Phase 3: Add 27 fields as scalar/dict placeholders (T003–T005)
3. **STOP and VALIDATE**: `python -m examples jobs get 2000000` shows zero warnings
4. This alone eliminates all 27 warning log lines — immediate value

### Incremental Delivery

1. US1 → Zero warnings, all fields accessible (as dict for nested) → **MVP**
2. US2 → Deep typing, IDE autocompletion for nested structures → **Full model**
3. US3 → Test assertions enabled, regression protection → **Quality gate**

### Single-Developer Sequential

Since all changes are in one file (`ab/api/models/jobs.py`), the most efficient path is:
1. T001–T002 (verify baseline)
2. T003–T005 (US1 — add all fields, verify)
3. T006–T021 (US2 — add sub-models bottom-up, update types, verify)
4. T022–T025 (US3 — enable tests, verify)
5. T026–T028 (polish)

---

## Notes

- All sub-models go in `ab/api/models/jobs.py` (single file, following existing convention where all job models live)
- Reuse `CompanyAddress` and `Coordinates` from `ab/api/models/common.py` — do not duplicate
- Preserve API typos in aliases: `mateialMasterID`, `isPrefered`, `ModifiyDate` (per Constitution I)
- All fields `Optional` — response shape varies by `JobAccessLevel` (Owner vs Agent vs Customer)
- List fields that are empty in fixture (`notes`, `freight_providers`, `timeline_tasks`, `prices`) stay as `List[dict]` — cannot validate sub-model shapes without data
- [P] tasks in Phase 4 are technically parallelizable but since they all target the same file, a sequential bottom-up approach in a single editing session is more practical
