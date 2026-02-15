# Tasks: Request Model Methodology

**Input**: Design documents from `/specs/007-request-model-methodology/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create directory structure for request fixtures

- [x] T001 Create `tests/fixtures/requests/` directory with `.gitkeep` file

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Extend Route and BaseEndpoint to support the new params_model pattern. MUST complete before any user story work begins.

- [x] T002 [P] Add `params_model: Optional[str] = None` field to Route dataclass in `ab/api/route.py` — insert after `request_model` field, default `None`, preserve frozen dataclass behavior
- [x] T003 [P] Add `params_model` validation to `BaseEndpoint._request()` in `ab/api/base.py` — when `"params"` is in kwargs and `route.params_model` is set, resolve the model via `_resolve_model()` and call `model_cls.check(kwargs["params"])` to validate and serialize query params, mirroring the existing `json`/`request_model` validation block

**Checkpoint**: Route supports `params_model` and `_request()` validates both body and query params. Existing tests pass (no regressions — new field defaults to `None`).

---

## Phase 3: User Story 1 — Clean Endpoint Signatures with Request Models (Priority: P1) 🎯 MVP

**Goal**: Prove the `**kwargs` → `model_validate` pattern by converting reference endpoints in the companies service. Callers pass snake_case keyword arguments instead of raw dicts.

**Independent Test**: Call `api.companies.search(search_text="test", page_size=10)` and confirm (a) Pydantic validation occurs, (b) HTTP request sends camelCase JSON, (c) invalid kwargs raise `ValidationError`.

### Implementation for User Story 1

- [x] T004 [US1] Convert `companies.search` method signature from `data: dict | Any` to `**kwargs: Any` in `ab/api/endpoints/companies.py` — change `self._request(_SEARCH, json=data)` to `self._request(_SEARCH, json=kwargs)`. Ensure `_SEARCH` Route already has `request_model="CompanySearchRequest"` set.
- [x] T005 [US1] Convert `companies.update_fulldetails` method signature from `data: dict | Any` to `**kwargs: Any` in `ab/api/endpoints/companies.py` — keep `company_id: str` as first positional arg, add `**kwargs` for the body. Pattern: `self._request(_UPDATE_FULLDETAILS.bind(companyId=...), json=kwargs)`
- [x] T006 [US1] Convert all remaining `data: dict | Any` method signatures in `ab/api/endpoints/companies.py` to `**kwargs: Any` — scan for any other methods that accept a raw dict body parameter and convert them to the kwargs pattern
- [x] T007 [US1] Update `examples/companies.py` to use kwargs call pattern — replace dict arguments like `{}` or `{"key": "val"}` with snake_case keyword arguments (e.g., `search_text="test"`, `page_size=25`). Update `runner.add()` entries to reflect the new calling convention.
- [x] T008 [US1] Run existing test suite (`pytest`) to verify companies endpoint conversion causes no regressions — all existing tests must pass. Fix any failures caused by the signature change.

**Checkpoint**: `companies` endpoint proves the pattern. Callers use kwargs, validation works, tests pass.

---

## Phase 4: User Story 2 — Request Fixture Tracking (Priority: P1)

**Goal**: Track request fixtures alongside response fixtures. FIXTURES.md uses a unified 4D format. Request fixtures are captured and validated.

**Independent Test**: Open `FIXTURES.md` and verify each endpoint row shows request model, request fixture, response model, and response fixture status. Load a request fixture file and validate it against its Pydantic model.

### Implementation for User Story 2

- [x] T009 [P] [US2] Add `request_fixture_file: Optional[str] = None` field to `ExampleEntry` dataclass and add request fixture save logic to `ExampleRunner._save_fixture()` in `examples/_runner.py` — when `entry.request_fixture_file` is set, serialize the request data (the kwargs dict passed to the endpoint) as JSON and save to `tests/fixtures/{request_fixture_file}`. The `runner.add()` method already accepts arbitrary kwargs; add the new field.
- [x] T010 [P] [US2] Research CompanySearchRequest fields from swagger spec (`ab/api/schemas/acportal.json`) and ABConnectTools (`/usr/src/pkgs/ABConnectTools/ABConnect/api/endpoints/company.py` + examples) — create a valid request fixture at `tests/fixtures/requests/CompanySearchRequest.json` with realistic field values in camelCase
- [x] T011 [US2] Restructure `FIXTURES.md` to unified 4D tracking format — replace the current two-section layout (Captured / Needs Request Data) with a single table per API surface using columns: `Endpoint Path | Method | Req Model | Req Fixture | Resp Model | Resp Fixture | Status | Notes`. Migrate all existing entries to the new format. Preserve all existing data and status information. Follow the format defined in `data-model.md`.
- [x] T012 [US2] Add request fixture validation test in `tests/models/test_request_fixtures.py` — for each JSON file in `tests/fixtures/requests/`, load it, resolve the corresponding `RequestModel` subclass by filename, and call `model.model_validate(data)`. Test must pass for all present fixtures and skip with actionable messages for models without fixtures yet.

**Checkpoint**: FIXTURES.md shows 4D status. At least one request fixture exists and validates. ExampleRunner can save request fixtures.

---

## Phase 5: User Story 3 — Updated Progress and API Surface Tracking (Priority: P2)

**Goal**: Progress reports and API surface documents reflect request model completeness alongside response model completeness.

**Independent Test**: Run the progress report generator and verify the output includes request model and request fixture columns for each endpoint. Check that endpoints with missing request models are flagged as partial.

### Implementation for User Story 3

- [x] T013 [US3] Update the progress report HTML generator in `specs/003-progress-report/` to include request model and request fixture columns — add "Req Model" and "Req Fixture" columns to the endpoint status table. Parse the new FIXTURES.md 4D format to populate these columns. Endpoints with `—` in request dimensions (GET with no body) should show as N/A, not as missing.
- [x] T014 [US3] Update or create `api-surface.md` at the repository root to include request model presence and fixture status — for each implemented endpoint, show whether a request model is defined and whether a request fixture is captured. Use the same status vocabulary as FIXTURES.md (`captured`, `needs-data`, `—`).

**Checkpoint**: Progress report shows 4D completeness. API surface doc reflects request model status.

---

## Phase 6: User Story 4 — Methodology Documentation (Priority: P2)

**Goal**: DISCOVER workflow and methodology docs prescribe request model creation and fixture capture in every phase.

**Independent Test**: Read the updated DISCOVER.md and follow it to implement a hypothetical new endpoint — every phase should mention request model/fixture steps.

### Implementation for User Story 4

- [x] T015 [P] [US4] Update Phase D (Determine) in `.claude/workflows/DISCOVER.md` — add explicit steps to research request body schemas and query parameter definitions from swagger + ABConnectTools. Document required fields, types, and realistic test values for request payloads alongside response research.
- [x] T016 [P] [US4] Update Phases I and S in `.claude/workflows/DISCOVER.md` — Phase I: add step to create `RequestModel` subclasses alongside response models, add skeleton request fixture tests with `pytest.skip()`. Phase S: prescribe `**kwargs` signatures, require `request_model` and/or `params_model` on Route definitions. Reference the endpoint-pattern contract (`specs/007-request-model-methodology/contracts/endpoint-pattern.md`).
- [x] T017 [P] [US4] Update Phases C, O, and V in `.claude/workflows/DISCOVER.md` — Phase C: capture request fixtures to `tests/fixtures/requests/` alongside response fixtures, add `request_fixture_file` to example runner entries. Phase O: validate request fixtures against models, run `test_request_fixtures.py`. Phase V: update FIXTURES.md with unified 4D format entries. Update the Four-Way Harmony checklist to include request model and request fixture dimensions.
- [x] T018 [US4] Update DISCOVER.md anti-patterns section — add anti-patterns for: (1) using `data: dict | Any` instead of `**kwargs`, (2) omitting `request_model` on POST/PUT/PATCH Route definitions, (3) not tracking request fixtures in FIXTURES.md, (4) fabricating request fixtures instead of deriving from swagger/ABConnectTools/staging.

**Checkpoint**: DISCOVER.md prescribes request model and fixture steps in all phases. A developer following the workflow produces complete endpoints.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [x] T019 Run full test suite (`pytest`) to verify all changes across all phases — zero failures, zero errors
- [x] T020 Run linter (`ruff check .`) to verify code quality — zero violations
- [x] T021 Validate quickstart.md accuracy — verify the companies reference endpoint follows every step documented in `specs/007-request-model-methodology/quickstart.md`. Confirm the endpoint completeness checklist at the bottom of quickstart.md is satisfied for the converted companies endpoints.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational (Phase 2) — needs `params_model` on Route and `_request()` validation
- **US2 (Phase 4)**: Depends on Foundational (Phase 2) — needs fixture directory and Route changes
- **US3 (Phase 5)**: Depends on US2 (Phase 4) — needs FIXTURES.md 4D format to parse
- **US4 (Phase 6)**: Depends on Foundational (Phase 2) — needs understanding of new Route field, but can run in parallel with US1/US2
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Depends only on Phase 2. Can start immediately after Foundational.
- **US2 (P1)**: Depends only on Phase 2. Can run in parallel with US1.
- **US3 (P2)**: Depends on US2 (needs 4D FIXTURES.md format). Must wait for US2 completion.
- **US4 (P2)**: Depends only on Phase 2. Can run in parallel with US1 and US2.

### Within Each User Story

- Tasks marked [P] within a phase can run in parallel
- Sequential tasks depend on prior tasks in the same phase
- Each phase checkpoint must be verified before moving on

### Parallel Opportunities

```
Phase 2:  T002 ─┐
          T003 ─┤ (parallel — different files)
                │
Phase 3:  T004 ─┤──▶ US1 (sequential within)
          ...   │
Phase 4:  T009 ─┤──▶ US2 (T009, T010 parallel; T011, T012 sequential)
          T010 ─┤
Phase 6:  T015 ─┤──▶ US4 (T015, T016, T017 parallel)
          T016 ─┤
          T017 ─┘
                │
Phase 5:  T013 ─┤──▶ US3 (after US2 complete)
          T014 ─┘
```

---

## Parallel Example: After Foundational Phase

```bash
# Launch US1, US2, and US4 in parallel (different file sets):

# US1 track (ab/api/endpoints/companies.py, examples/companies.py):
Task: "T004 Convert companies.search to **kwargs in ab/api/endpoints/companies.py"

# US2 track (examples/_runner.py, tests/fixtures/requests/, FIXTURES.md):
Task: "T009 Add request_fixture_file to ExampleRunner in examples/_runner.py"
Task: "T010 Create CompanySearchRequest fixture in tests/fixtures/requests/"

# US4 track (.claude/workflows/DISCOVER.md):
Task: "T015 Update Phase D in .claude/workflows/DISCOVER.md"
Task: "T016 Update Phases I and S in .claude/workflows/DISCOVER.md"
Task: "T017 Update Phases C, O, V in .claude/workflows/DISCOVER.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational (T002, T003)
3. Complete Phase 3: US1 (T004–T008)
4. **STOP and VALIDATE**: `api.companies.search(search_text="test")` works, validation fires, tests pass
5. The kwargs-to-model pattern is proven and ready for adoption

### Incremental Delivery

1. Setup + Foundational → Infrastructure ready
2. US1 → Pattern proven with reference endpoint (MVP)
3. US2 → Fixture tracking in place, FIXTURES.md restructured
4. US4 → DISCOVER workflow updated (can run parallel with US2)
5. US3 → Progress reports show 4D completeness (after US2)
6. Polish → Full validation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- No new dependencies added — all changes use existing pydantic and pytest
- Feature 002+ will be the primary consumer of this methodology — 007 establishes the pattern
- Existing 59 endpoints are NOT retroactively converted; only newly touched endpoints adopt the pattern
- The reference conversion (companies) serves as proof and documentation
