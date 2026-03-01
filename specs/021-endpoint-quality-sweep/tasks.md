# Tasks: Endpoint Quality Sweep

**Input**: Design documents from `/specs/021-endpoint-quality-sweep/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/endpoint-checklist.md, quickstart.md

**Tests**: Tests are part of the quality gate requirements (G3). Test updates are included inline.

**Organization**: Tasks are grouped by user story. US1 is the core implementation (fix ContactDetailedInfo). US2 is the checklist artifact (already delivered in plan phase). US3 is the priority ordering workflow.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: No project setup needed — existing SDK project with all infrastructure in place.

_(No tasks — all tooling, dependencies, and project structure already exist.)_

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create typed sub-models that ContactDetailedInfo depends on. These must exist before the main model can reference them.

- [x] T001 [P] Create `EmailDetails` sub-model in `ab/api/models/contacts.py` with fields: id (Optional[int]), email (Optional[str]), invalid (Optional[bool]), dont_spam (Optional[bool], alias="dontSpam") — all with Field(description=...)
- [x] T002 [P] Create `PhoneDetails` sub-model in `ab/api/models/contacts.py` with fields: id (Optional[int]), phone (Optional[str]) — all with Field(description=...)
- [x] T003 [P] Create `ContactEmailEntry` sub-model in `ab/api/models/contacts.py` with fields from data-model.md: id, is_active (alias="isActive"), deactivated_reason (alias="deactivatedReason"), meta_data (alias="metaData"), editable, email (Optional[EmailDetails]) — all with Field(description=...)
- [x] T004 [P] Create `ContactPhoneEntry` sub-model in `ab/api/models/contacts.py` with fields from data-model.md: id, is_active, deactivated_reason, meta_data, editable, phone (Optional[PhoneDetails]) — all with Field(description=...)
- [x] T005 [P] Create `ContactAddressEntry` sub-model in `ab/api/models/contacts.py` with fields from data-model.md: id, is_active, deactivated_reason, meta_data, editable, address (Optional[CompanyAddress]) — reuse existing CompanyAddress from `ab/api/models/common.py`

**Checkpoint**: All 5 sub-models exist and can be imported. No tests needed yet — they will be validated through ContactDetailedInfo fixture in Phase 3.

---

## Phase 3: User Story 1 — Fix ContactDetailedInfo to pass all 6 gates (Priority: P1)

**Goal**: Make `GET /contacts/{contactId}/editdetails` (ContactDetailedInfo) pass G1-G6 by adding all 31 undeclared fields, updating tests, and updating docs.

**Independent Test**: Run `python scripts/generate_progress.py --fixtures` and confirm the endpoint shows all PASS. Run `pytest tests/ -x -q -m "not live"` with zero failures.

### G1 — Model Fidelity

- [x] T006 [US1] Add all missing fields from C# `ContactBaseDetails` to `ContactDetailedInfo` in `ab/api/models/contacts.py`: contact_display_id, full_name, contact_type_id, care_of, bol_notes, tax_id, is_business, is_payer, is_prefered, is_private, is_primary, company_id, root_contact_id, owner_franchisee_id, company, legacy_guid, assistant, department, web_site, birth_date, job_title_id, job_title — all with correct types, aliases, and Field(description=...)
- [x] T007 [US1] Add fields from C# `ContactExtendedDetails` to `ContactDetailedInfo` in `ab/api/models/contacts.py`: emails_list (Optional[List[ContactEmailEntry]], alias="emailsList"), phones_list (Optional[List[ContactPhoneEntry]], alias="phonesList"), addresses_list (Optional[List[ContactAddressEntry]], alias="addressesList"), fax, primary_phone (alias="primaryPhone"), primary_email (alias="primaryEmail")
- [x] T008 [US1] Add fields from C# `ContactEditDetails` and fixture-only fields to `ContactDetailedInfo` in `ab/api/models/contacts.py`: editable, contact_details_company_info (Optional[dict], alias="contactDetailsCompanyInfo"), full_name_update_required (Optional[bool], alias="fullNameUpdateRequired"), is_empty (Optional[bool], alias="isEmpty")
- [x] T009 [US1] Remove or update stale fields on `ContactDetailedInfo` in `ab/api/models/contacts.py`: remove `addresses`, `phones`, `emails` (List[dict]) since they are replaced by typed `addresses_list`, `phones_list`, `emails_list`; keep `company_info` as-is
- [x] T010 [US1] Validate G1 by running: `python -c "from ab.api.models.contacts import ContactDetailedInfo; import json; d = json.load(open('tests/fixtures/ContactDetailedInfo.json')); m = ContactDetailedInfo.model_validate(d); print(len(m.__pydantic_extra__ or {}), 'extra fields')"` — must print `0 extra fields`

### G3 — Test Quality

- [x] T011 [US1] Uncomment `assert_no_extra_fields(model)` on line 28 of `tests/models/test_contact_models.py` in `test_contact_detailed_info`
- [x] T012 [US1] Run `pytest tests/models/test_contact_models.py::TestContactModels::test_contact_detailed_info -x -q -m "not live"` — must pass
- [x] T013 [US1] Run `pytest tests/ -x -q -m "not live"` — must pass with zero regressions

### G4 — Documentation

- [x] T014 [US1] Update `docs/api/contacts.md` get_details section: update example code to reference typed fields (e.g., `details.emails_list`, `details.addresses_list`, `details.full_name`) instead of `details.emails`

### G1-G6 — Full Verification

- [x] T015 [US1] Run `python scripts/generate_progress.py --fixtures` and confirm GET /contacts/{contactId}/editdetails shows G1=PASS, G2=PASS, G3=PASS, G4=PASS, G5=PASS (or auto-pass), G6=PASS (or auto-pass)

**Checkpoint**: ContactDetailedInfo endpoint is "complete" — all 6 gates pass, tests green, docs updated.

---

## Phase 4: User Story 2 — Per-Endpoint Quality Checklist (Priority: P1)

**Goal**: Ensure the per-endpoint checklist (quickstart.md) is complete, actionable, and validated against the ContactDetailedInfo exemplar.

**Independent Test**: Walk through each checklist item against the ContactDetailedInfo endpoint and confirm every item is satisfied.

- [x] T016 [US2] Validate `specs/021-endpoint-quality-sweep/quickstart.md` checklist against the completed ContactDetailedInfo endpoint — confirm every item passes
- [x] T017 [US2] Validate `specs/021-endpoint-quality-sweep/contracts/endpoint-checklist.md` gate definitions match `ab/progress/gates.py` logic — confirm no discrepancies

**Checkpoint**: Checklist artifacts are validated and ready for use on subsequent endpoints.

---

## Phase 5: User Story 3 — Priority Ordering Workflow (Priority: P2)

**Goal**: Generate updated progress report showing the sweep results and establish the priority ordering for the next endpoints to fix.

**Independent Test**: Run `python scripts/generate_progress.py` and confirm the HTML report reflects the ContactDetailedInfo fix and provides correct gate counts.

- [x] T018 [US3] Run `python scripts/generate_progress.py --fixtures` to regenerate FIXTURES.md with updated gate statuses
- [x] T019 [US3] Run `python scripts/generate_progress.py` to regenerate progress.html
- [x] T020 [US3] Spot-check FIXTURES.md: confirm GET /contacts/{contactId}/editdetails status = "complete"

**Checkpoint**: Progress report updated, ContactDetailedInfo confirmed complete, priority list visible for next sweep targets.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [x] T021 Run full test suite: `pytest tests/ -x -q -m "not live"` — zero failures, zero regressions
- [x] T022 Verify no new `# TODO: verify optionality` markers were introduced in `ab/api/models/contacts.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: N/A — no setup needed
- **Foundational (Phase 2)**: No dependencies — can start immediately. BLOCKS Phase 3 (sub-models must exist before ContactDetailedInfo can reference them)
- **US1 (Phase 3)**: Depends on Phase 2 completion. T006-T009 depend on T001-T005. T010 depends on T006-T009. T011-T013 depend on T010. T014 depends on T006-T009. T015 depends on all prior US1 tasks.
- **US2 (Phase 4)**: Depends on US1 completion (needs the exemplar endpoint to validate checklist against)
- **US3 (Phase 5)**: Depends on US1 completion (needs the fix applied before regenerating reports)
- **Polish (Phase 6)**: Depends on all prior phases

### Within Phase 2 (Foundational)

All 5 sub-model tasks (T001-T005) are independent and can run in parallel — they create separate classes in the same file but don't reference each other.

### Within Phase 3 (US1)

```
T006 ─┐
T007 ─┼─→ T009 → T010 → T011 → T012 → T013
T008 ─┘                    │
                           └──→ T014
                                  │
                           T015 ←─┘
```

- T006, T007, T008 can run in parallel (adding fields to different sections)
- T009 depends on T007 (must add typed lists before removing untyped ones)
- T010 depends on T006-T009 (validates all fields present)
- T011-T013 depend on T010 (tests will fail without model fixes)
- T014 depends on T006-T009 (docs reference new fields)
- T015 depends on T013 and T014 (full gate verification)

### Parallel Opportunities

```bash
# Phase 2: Launch all sub-models in parallel
T001: Create EmailDetails
T002: Create PhoneDetails
T003: Create ContactEmailEntry
T004: Create ContactPhoneEntry
T005: Create ContactAddressEntry

# Phase 3: Launch field additions in parallel
T006: Add ContactBaseDetails fields
T007: Add ContactExtendedDetails fields
T008: Add ContactEditDetails fields
```

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Phase 2: Create 5 sub-models (T001-T005)
2. Complete Phase 3: Fix ContactDetailedInfo (T006-T015)
3. **STOP and VALIDATE**: All 6 gates pass, tests green
4. This is the primary deliverable — a fully compliant endpoint

### Incremental Delivery

1. Phase 2 → Sub-models ready
2. Phase 3 (US1) → ContactDetailedInfo complete → **MVP delivered**
3. Phase 4 (US2) → Checklist validated → Workflow documented
4. Phase 5 (US3) → Progress report updated → Next targets identified
5. Phase 6 → Final cleanup

---

## Notes

- [P] tasks = different files or independent class definitions, no dependencies
- [Story] label maps task to specific user story for traceability
- The `addresses`, `phones`, `emails` fields (List[dict]) on ContactDetailedInfo are REMOVED — replaced by typed `addresses_list`, `phones_list`, `emails_list` with proper sub-models
- CompanyAddress is reused from `ab/api/models/common.py` — no duplication
- G5 (param routing) and G6 (request quality) auto-pass for this GET endpoint (no request body, no query params needing a params_model)
- The per-endpoint checklist (quickstart.md) and gate contract (endpoint-checklist.md) were already created during the plan phase
