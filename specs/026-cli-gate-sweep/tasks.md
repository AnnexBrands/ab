# Tasks: CLI Gate Sweep

**Input**: Design documents from `/specs/026-cli-gate-sweep/`
**Prerequisites**: plan.md, spec.md, research.md, quickstart.md

**Organization**: Tasks are grouped by user story. US2 is subdivided by endpoint group for manageability.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to

---

## Phase 1: Setup

**Purpose**: Capture baseline gate status and understand current failures

- [x] T001 Run `python scripts/generate_progress.py` and record baseline gate counts in a comment at the top of tests/constants.py
- [x] T002 Run `python scripts/generate_progress.py --fixtures` to ensure FIXTURES.md is current

**Checkpoint**: Baseline gate status captured

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: CLI listing fix and constants infrastructure — must complete before endpoint sweep

- [x] T003 [US1] Remove route paths from `_list_methods()` API Methods section in ab/cli/__main__.py — format API methods same as Helpers: `{name:<30} {params}{ret_str}`, sort by method name instead of route path
- [x] T004 [US1] Verify `print_method_help()` in ab/cli/parser.py still shows Route line (no changes needed, just confirm)
- [x] T005 [US1] Smoke test: run `ab jobs` via CLI entry point and confirm no route paths in output, then run `ab jobs get --help` and confirm route IS shown
- [x] T006 Add `TEST_HISTORY_AMOUNT = 3` to tests/constants.py (for tracking v3 `historyAmount` parameter)
- [x] T007 Review all path parameters across GET Route definitions in ab/api/endpoints/*.py and identify any missing constants not yet in tests/constants.py — add educated defaults for each

**Checkpoint**: CLI listing is clean, constants are populated for all known path parameters

---

## Phase 3: User Story 2 — Jobs GET Endpoints (Priority: P1) 🎯 MVP

**Goal**: Fix all Jobs GET endpoints so they pass quality gates using auto-resolved constants

**Independent Test**: Run `ex jobs` and verify all GET examples execute without manual input. Run progress report and confirm jobs gates improve.

### Jobs: Tracking

- [x] T008 [US2] Run `ex jobs get_tracking` (uses TEST_JOB_DISPLAY_ID). Inspect output for errors. If "received extras" → note extra fields. If HTTP error → diagnose request. Fix model in ab/api/models/jobs.py if needed.
- [x] T009 [US2] Run `ex jobs get_tracking_v3` (uses TEST_JOB_DISPLAY_ID + TEST_HISTORY_AMOUNT). Inspect output. Fix model in ab/api/models/jobs.py if needed.

### Jobs: Core

- [x] T010 [US2] Run `ex jobs get` (uses TEST_JOB_DISPLAY_ID). Inspect output. Fix Job model in ab/api/models/jobs.py if "received extras".
- [x] T011 [US2] Run `ex jobs get_price` (uses TEST_JOB_DISPLAY_ID). Inspect output. Fix JobPrice model if needed.
- [x] T012 [US2] Run `ex jobs get_calendar_items` (uses TEST_JOB_DISPLAY_ID). Inspect output. Fix CalendarItem model if needed.
- [x] T013 [US2] Run `ex jobs search` (ensure example exists with default params). Inspect output. Fix JobSearchResult model if needed.

### Jobs: Parcel & Packaging

- [x] T014 [P] [US2] Run `ex jobs get_parcel_items` (uses TEST_JOB_DISPLAY_ID). Inspect output. Fix ParcelItem model if needed.
- [x] T015 [P] [US2] Run `ex jobs get_parcel_items_with_materials` (uses TEST_JOB_DISPLAY_ID). Inspect output. Fix ParcelItemWithMaterials model if needed.
- [x] T016 [P] [US2] Run `ex jobs get_packaging_containers` (uses TEST_JOB_DISPLAY_ID). Inspect output. Fix PackagingContainer model if needed.

### Jobs: Notes

- [x] T017 [US2] Run `ex jobs get_notes` (uses TEST_JOB_DISPLAY_ID). Inspect output. Fix JobNote model if needed.

### Jobs: On-Hold

- [x] T018 [US2] Run `ex jobs get_on_hold` (uses TEST_JOB_DISPLAY_ID). Inspect output. Fix OnHoldDetails model if needed.

### Jobs: Payment

- [x] T019 [US2] Run `ex jobs get_payment` (uses TEST_JOB_DISPLAY_ID). Inspect output. Fix PaymentInfo/JobPayment model if needed.
- [x] T020 [US2] Run `ex jobs get_payment_sources` (uses TEST_JOB_DISPLAY_ID). Inspect output. Fix PaymentSources model if needed.

### Jobs: Checkpoint

- [x] T021 [US2] Run `python scripts/generate_progress.py` and compare Jobs gate counts against baseline from T001

**Checkpoint**: All Jobs GET endpoints pass gates or have documented skip reasons

---

## Phase 4: User Story 2 — Companies & Contacts GET Endpoints (Priority: P1)

**Goal**: Fix Companies and Contacts GET endpoints

### Companies

- [x] T022 [P] [US2] Run `ex companies get` (uses TEST_COMPANY_UUID). Inspect output. Fix Company model in ab/api/models/companies.py if needed.
- [x] T023 [P] [US2] Run `ex companies get_by_code` (uses TEST_COMPANY_CODE). Inspect output. Fix model if needed.

### Contacts

- [x] T024 [P] [US2] Run `ex contacts get` (uses TEST_CONTACT_ID). Inspect output. Fix Contact model in ab/api/models/contacts.py if needed.
- [x] T025 [P] [US2] Run `ex contacts search` (ensure example with default params). Inspect output. Fix model if needed.

**Checkpoint**: Companies and Contacts GET endpoints pass gates

---

## Phase 5: User Story 2 — Shipments & Remaining GET Endpoints (Priority: P1)

**Goal**: Fix Shipments, Address, Catalog, and other GET endpoints

### Shipments

- [x] T026 [US2] Run `ex shipments get_accessorials` (uses TEST_JOB_DISPLAY_ID). Inspect output. Fix Accessorial model if needed.
- [x] T027 [US2] Run `ex shipments get_origin_destination` (uses TEST_JOB_DISPLAY_ID). Inspect output. Fix OriginDestination model if needed.
- [x] T028 [US2] Run `ex shipments get_rates_state` (uses TEST_JOB_DISPLAY_ID). Inspect output. Fix RatesState model if needed.

### Address

- [x] T029 [P] [US2] Run any address GET examples (e.g., `ex address validate`). Inspect output. Fix models in ab/api/models/address.py if needed.

### Lookup

- [x] T030 [P] [US2] Run `ex lookup get_items` (uses TEST_LOOKUP_KEY_SUB_MGMT). Inspect output. Fix LookupItem model if needed.

### Catalog / Sellers

- [x] T031 [P] [US2] Run `ex catalog get` and `ex sellers get` (use TEST_CATALOG_ID, TEST_SELLER_ID). Inspect output. Fix models if needed.

**Checkpoint**: All simple GET endpoints (single known constant) pass gates

---

## Phase 6: User Story 3 — Chain Discovery Endpoints (Priority: P2)

**Goal**: Fix GET endpoints that require IDs obtainable only through parent listing calls

### RFQ Chain

- [x] T032 [US3] In examples/jobs.py, implement chain discovery: call `api.jobs.get_rfqs(TEST_JOB_DISPLAY_ID)` to obtain rfqId, then register `get_rfq` example using discovered ID. Skip if listing returns empty.

### Timeline Chain

- [x] T033 [US3] In examples/jobs.py, implement chain discovery: call `api.jobs.get_timeline(TEST_JOB_DISPLAY_ID)` to obtain timelineTaskIdentifier and taskCode, then register `get_timeline_task` and `get_timeline_agent` examples. Skip if listing returns empty.

### On-Hold Detail Chain

- [x] T034 [US3] In examples/jobs.py, implement chain discovery: call `api.jobs.get_on_hold(TEST_JOB_DISPLAY_ID)` to obtain on-hold record ID, then register `get_on_hold_detail` example. Skip if listing returns empty.

### SMS Template Chain

- [x] T035 [US3] In examples/jobs.py, implement chain discovery for SMS template endpoints — obtain templateId from parent listing. Skip if not available.

### Shipment Plan Chain

- [x] T036 [US3] In examples/jobs.py or examples/shipments.py, implement chain discovery for endpoints needing shipmentPlanId (bill-of-lading, packaging-labels forms). Skip if not available.

### Run and Validate

- [x] T037 [US3] Run all chain discovery examples. Inspect output for each. Add discovered IDs as constants to tests/constants.py if they are stable staging values.

**Checkpoint**: Chain discovery endpoints either pass gates or have documented skip reasons

---

## Phase 7: User Story 4 — Model Mismatch Fixes (Priority: P2)

**Goal**: Fix all "received extras" warnings identified during the sweep

- [x] T038 [US4] Collect all "received extras" warnings from T008-T037 runs. For each, check swagger definition in specs/*.json for field types and optionality.
- [x] T039 [US4] Update response models in ab/api/models/*.py to add missing fields with correct types, Optional markers, and Field descriptions
- [x] T040 [US4] Re-run all examples that previously showed "received extras". Confirm warnings are resolved.
- [x] T041 [US4] Run `pytest tests/ -q` to verify no regressions from model changes

**Checkpoint**: Zero "received extras" warnings from fixed endpoints

---

## Phase 8: Polish & Validation

**Purpose**: Final verification and progress report update

- [x] T042 Run `python scripts/generate_progress.py` and compare final gate counts against baseline from T001 — target SC-003 (at least 10 more GET endpoints passing all gates)
- [x] T043 Run `python scripts/generate_progress.py --fixtures` to update FIXTURES.md with current gate status
- [x] T044 Run quickstart.md scenarios 1-7 from specs/026-cli-gate-sweep/quickstart.md and verify all pass
- [x] T045 Run `pytest tests/ -q` to confirm no regressions (512+ passing, same or fewer failures)
- [x] T046 Run `ruff check ab/ tests/ examples/` on modified files to ensure no lint errors

**Checkpoint**: All success criteria met, progress report updated

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — CLI fix + constants must be done first
- **US2 Phases (3-5)**: Depend on Phase 2 — constants must exist before running examples
  - Phase 3 (Jobs) → Phase 4 (Companies/Contacts) → Phase 5 (Shipments/Other) — sequential by priority
- **US3 (Phase 6)**: Depends on Phase 3-5 — chain discovery builds on simple constant endpoints
- **US4 (Phase 7)**: Depends on Phases 3-6 — model fixes are collected during the sweep
- **Polish (Phase 8)**: Depends on all previous phases

### User Story Dependencies

- **US1 (CLI Listing)**: Independent — can be done in Phase 2
- **US2 (Gate Fixes)**: Depends on US1 completion (constants must be in place)
- **US3 (Chain Discovery)**: Depends on US2 base endpoints working
- **US4 (Model Fixes)**: Depends on US2/US3 identifying the mismatches

### Parallel Opportunities

- T014, T015, T016 (parcel/packaging) can run in parallel
- T022, T023 (companies) can run in parallel
- T024, T025 (contacts) can run in parallel
- T029, T030, T031 (address, lookup, catalog) can run in parallel

---

## Implementation Strategy

### MVP First (US1 + US2 Jobs Only)

1. Complete Phase 1: Baseline capture
2. Complete Phase 2: CLI fix + constants
3. Complete Phase 3: Jobs GET endpoints
4. **STOP and VALIDATE**: Run progress report, confirm improvement
5. Continue to remaining phases if time permits

### Iterative Sweep Pattern

For each endpoint in US2:
1. Run the example (`ex {endpoint} {method}`)
2. Inspect the output — look for HTTP errors or "received extras"
3. If HTTP error → diagnose request (wrong params, missing constant)
4. If "received extras" → note fields, check swagger, fix model
5. If success → verify fixture captured, move to next endpoint
6. If constant missing → add to tests/constants.py with educated default

### "Received Extras" Fix Pattern

1. Run example, observe extra field names in warning log
2. Check swagger spec for field definition (type, nullable, description)
3. If swagger disagrees with fixture → trust fixture (constitution principle IV)
4. Add field to model with `Optional[type]` and `Field(description="...")`
5. Re-run example to confirm warning resolved
