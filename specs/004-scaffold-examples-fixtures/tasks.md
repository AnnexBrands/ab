# Tasks: Scaffold Examples & Fixtures

**Input**: Design documents from `/specs/004-scaffold-examples-fixtures/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Not requested — no test tasks included.

**Organization**: Tasks grouped by user story. Each story is independently testable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Exact file paths included in descriptions

## Phase 1: Setup

**Purpose**: Convert examples/ to a Python package

- [x] T001 Create package marker at examples/__init__.py (empty file enabling `python -m examples.*` execution)

---

## Phase 2: Foundational (Runner Infrastructure)

**Purpose**: Build the shared runner module that ALL example files depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 Implement ExampleRunner and ExampleEntry in examples/_runner.py — ExampleEntry dataclass (name, call, response_model, request_model, fixture_file), ExampleRunner class (lazy ABConnectAPI init, add() registration, run() with sys.argv CLI parsing, --list mode showing entry metadata), and _save_fixture() logic (BaseModel → model_dump(by_alias=True, mode="json"), list handling, None/bytes skip, write to tests/fixtures/{fixture_file} as indented JSON). See data-model.md for entity fields, research.md Decision 1-2 for design rationale, quickstart.md for target UX.

**Checkpoint**: `python -c "from examples._runner import ExampleRunner"` succeeds

---

## Phase 3: User Story 1 — Run an Example to Capture a Fixture (Priority: P1) MVP

**Goal**: Prove the runner captures fixtures end-to-end: call API → cast to model → serialize JSON → save fixture file

**Independent Test**: Run `python -m examples.contacts get_current_user` with staging credentials → fixture file appears at tests/fixtures/ContactSimple.json with valid camelCase JSON

- [x] T003 [US1] Migrate examples/contacts.py to runner pattern as proof-of-concept — read ab/api/endpoints/contacts.py for all public methods, cross-reference FIXTURES.md for fixture status (captured: ContactSimple, ContactDetailedInfo, ContactPrimaryDetails, SearchContactEntityResult), populate captured entries with known working params, annotate pending entries with `# TODO: capture fixture — <reason>`, wrap all in runner.add() calls with response_model, request_model, fixture_file metadata
- [x] T004 [US1] Validate runner end-to-end by verifying: (1) `python -m examples.contacts --list` shows all entries with metadata, (2) examples/contacts.py follows the quickstart.md structure pattern, (3) runner handles error entries gracefully without aborting

**Checkpoint**: Runner proven — contacts example captures fixtures. Pattern established for all subsequent migrations.

---

## Phase 4: User Story 2 — Discover All SDK Methods via Structured Examples (Priority: P2)

**Goal**: Every public method of every endpoint module appears as a structured runner entry with request/response metadata, TODO annotations for pending fixtures, and populated params for captured fixtures

**Independent Test**: Compare public methods of each endpoint class against runner.add() entries in its example file — every method appears exactly once

### ABC API Examples

- [x] T005 [P] [US2] Migrate examples/autoprice.py to runner pattern — read ab/api/endpoints/autoprice.py for public methods (quick_quote, quote_request), cross-reference FIXTURES.md (captured: QuickQuoteResponse; needs-request-data: QuoteRequest), add response_model/request_model/fixture_file metadata per entry
- [x] T006 [P] [US2] Migrate examples/web2lead.py to runner pattern — read ab/api/endpoints/web2lead.py for public methods (get, post), cross-reference FIXTURES.md (captured: Web2LeadResponse), add metadata per entry

### Catalog API Examples

- [x] T007 [P] [US2] Migrate examples/catalog.py to runner pattern — read ab/api/endpoints/catalog.py for all public methods, cross-reference FIXTURES.md for fixture status, add metadata per entry
- [x] T008 [P] [US2] Migrate and expand examples/lots.py (currently truncated at 1 method) — read ab/api/endpoints/lots.py for all public methods (list, get, overrides), cross-reference FIXTURES.md (all 3 need request data), add all methods as runner entries with TODO annotations
- [x] T009 [P] [US2] Migrate examples/sellers.py to runner pattern — read ab/api/endpoints/sellers.py for all public methods, cross-reference FIXTURES.md (captured: SellerDto, SellerExpandedDto), add metadata per entry

### ACPortal Simple Examples

- [x] T010 [P] [US2] Migrate examples/companies.py to runner pattern — read ab/api/endpoints/companies.py for all 8 public methods (get_by_id, get_details, get_fulldetails, update_fulldetails, create, search, list, available_by_current_user), cross-reference FIXTURES.md (captured: CompanySimple, CompanyDetails, SearchCompanyResponse), add metadata per entry
- [x] T011 [P] [US2] Migrate examples/documents.py to runner pattern — read ab/api/endpoints/documents.py for all public methods, cross-reference FIXTURES.md (captured: Document), add metadata per entry
- [x] T012 [P] [US2] Migrate examples/payments.py to runner pattern — read ab/api/endpoints/payments.py for all public methods (get, get_sources, pay_by_source, create_ach_session), cross-reference FIXTURES.md (all 3 job payment endpoints need request data), add metadata per entry
- [x] T013 [P] [US2] Migrate examples/notes.py to runner pattern — read ab/api/endpoints/jobs.py for note-related public methods (list_notes, create_note), cross-reference FIXTURES.md (needs-request-data: /job/{id}/note), add metadata per entry
- [x] T014 [P] [US2] Migrate examples/tracking.py to runner pattern — read ab/api/endpoints/jobs.py for tracking-related public methods (get_tracking, get_tracking_v3), cross-reference FIXTURES.md (both need shipped job ID), add metadata per entry
- [x] T015 [P] [US2] Migrate examples/timeline.py to runner pattern — read ab/api/endpoints/jobs.py for timeline-related public methods (get_timeline, create_timeline_task, get_timeline_agent, increment_status), cross-reference FIXTURES.md (needs job ID with active timeline), add metadata per entry

### ACPortal Complex Examples

- [x] T016 [P] [US2] Migrate and expand examples/jobs.py (currently 2 methods → 28+ methods) — read ab/api/endpoints/jobs.py for ALL public methods across job CRUD (get, create, save, search, search_by_details), pricing (get_price), status (get_status, increment_status), config (get_update_page_config), calendar (get_calendar_items), and ABC update; cross-reference FIXTURES.md for each (captured: Job, JobPrice, JobSearchResult, JobUpdatePageConfig, CalendarItem); populate captured entries, TODO-annotate pending entries
- [x] T017 [P] [US2] Migrate examples/shipments.py to runner pattern — read ab/api/endpoints/shipments.py for all 14 public methods, verify all are represented in current example, cross-reference FIXTURES.md (needs-request-data: rate quotes, origin/destination, accessorials, rates state), add runner wrapper with metadata
- [x] T018 [P] [US2] Migrate examples/forms.py to runner pattern — read ab/api/endpoints/forms.py for all 15 public methods (invoices, BOLs, packing slips, labels, shipment plans, etc.), verify all are represented, cross-reference FIXTURES.md (needs-request-data: /job/{id}/form/shipments), add runner wrapper with metadata
- [x] T019 [P] [US2] Migrate examples/parcels.py to runner pattern — read ab/api/endpoints/jobs.py for parcel-related public methods (list_parcel_items, create_parcel_item, get_parcel_items_with_materials, get_packaging_containers), cross-reference FIXTURES.md (all need job ID with parcel data), add runner wrapper with metadata

**Checkpoint**: All 16 existing example files migrated. Every public method has a runner.add() entry. Jobs expanded from 2 to 28+ methods, lots from 1 to all methods.

---

## Phase 5: User Story 3 — Create Missing Example Files (Priority: P3)

**Goal**: Every endpoint module in ab/api/endpoints/ has a corresponding example file in examples/

**Independent Test**: List endpoint modules and example files — verify 1:1 mapping (15 modules, 15+ example files)

- [x] T020 [P] [US3] Create examples/address.py — read ab/api/endpoints/address.py for public methods (validate, get_property_type), read ab/api/models/address.py for response model names (AddressIsValidResult, PropertyType), cross-reference FIXTURES.md (both need request data: valid street/city/state/zipCode), create runner-wrapped file with TODO-annotated entries per quickstart.md pattern
- [x] T021 [P] [US3] Create examples/lookup.py — read ab/api/endpoints/lookup.py for public methods (get_contact_types, get_countries, get_job_statuses, get_items), cross-reference FIXTURES.md (captured: ContactTypeEntity, CountryCodeDto, JobStatus; needs-request-data: /lookup/items returns 204), create runner-wrapped file with metadata per entry
- [x] T022 [P] [US3] Create examples/users.py — read ab/api/endpoints/users.py for public methods (list, get_roles, create, update), cross-reference FIXTURES.md (captured: User, UserRole; create/update have no response_model), create runner-wrapped file with metadata per entry

**Checkpoint**: 15 endpoint modules → 15+ example files. 100% module coverage achieved.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate completeness and consistency across all example files

- [x] T023 Verify 1:1 mapping: every .py file in ab/api/endpoints/ (excluding __init__.py, base.py) has a corresponding .py in examples/ (excluding __init__.py, _runner.py)
- [x] T024 Verify full method coverage: for each endpoint class, every public method (not underscore-prefixed) appears as a runner.add() entry in the corresponding example file
- [x] T025 [P] Run ruff check on all files in examples/ and fix any lint issues
- [x] T026 [P] Run existing test suite (`pytest tests/`) to verify no fixture loading or model validation breakage from example changes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Phase 2 — proves the runner pattern works
- **US2 (Phase 4)**: Depends on Phase 3 — uses proven pattern for bulk migration
- **US3 (Phase 5)**: Depends on Phase 2 — can run in parallel with Phase 4
- **Polish (Phase 6)**: Depends on Phases 4 and 5 complete

### User Story Dependencies

- **US1 (P1)**: Requires only foundational runner — no dependency on other stories
- **US2 (P2)**: Requires US1 pattern as template — then all migrations are independent
- **US3 (P3)**: Requires only foundational runner — can run in parallel with US2

### Within Each Phase

- Phase 4 (US2): All tasks T005–T019 are [P] — they modify different files with no cross-dependencies
- Phase 5 (US3): All tasks T020–T022 are [P] — they create different new files
- Phase 6 (Polish): T025 and T026 are [P] — independent validation checks

### Parallel Opportunities

After Phase 3 (US1 MVP) completes:

```
Phase 4 (US2) ──────────────────────────── Phase 6
  T005 autoprice.py ─┐                        ↑
  T006 web2lead.py ──┤                        │
  T007 catalog.py ───┤                        │
  T008 lots.py ──────┤  All [P]               │
  T009 sellers.py ───┤                        │
  T010 companies.py ─┤                        │
  T011 documents.py ─┤                        │
  T012 payments.py ──┤                  (waits for both)
  T013 notes.py ─────┤                        │
  T014 tracking.py ──┤                        │
  T015 timeline.py ──┤                        │
  T016 jobs.py ──────┤                        │
  T017 shipments.py ─┤                        │
  T018 forms.py ─────┤                        │
  T019 parcels.py ───┘                        │
                                              │
Phase 5 (US3) ────────────────────────────────┘
  T020 address.py ───┐
  T021 lookup.py ────┤  All [P], parallel with Phase 4
  T022 users.py ─────┘
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational — runner module (T002)
3. Complete Phase 3: US1 — migrate contacts.py, validate end-to-end (T003–T004)
4. **STOP and VALIDATE**: `python -m examples.contacts --list` works, fixture capture proven
5. Pattern established — ready for bulk migration

### Incremental Delivery

1. Setup + Foundational → Runner infrastructure ready
2. US1 (contacts proof-of-concept) → Pattern validated → Checkpoint commit
3. US2 (all 16 migrations) + US3 (3 new files) → Full coverage → Checkpoint commit
4. Polish (validation + lint) → Feature complete → PR ready

### Parallel Execution (Multiple Agents)

After Phase 3 completes:
- **Agent A**: Migrate ABC + Catalog examples (T005–T009)
- **Agent B**: Migrate ACPortal simple examples (T010–T015)
- **Agent C**: Migrate ACPortal complex examples (T016–T019)
- **Agent D**: Create missing example files (T020–T022)
- All agents work simultaneously — no file conflicts

---

## Notes

- [P] tasks = different files, no dependencies — safe for parallel execution
- [Story] label maps task to user story for traceability
- Every migration task follows the same pattern: read endpoint → cross-reference FIXTURES.md → wrap in runner → annotate TODOs
- T016 (jobs.py expansion) is the largest single task: 2 → 28+ methods
- Commit after each phase completion (Phase-Based Context Recovery, Constitution VIII)
- Constitution Principle II alignment: examples become the fixture-capture mechanism
