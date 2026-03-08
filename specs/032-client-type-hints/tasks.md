# Tasks: Client Endpoint Type Hints for IDE Discoverability

**Input**: Design documents from `/specs/032-client-type-hints/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, quickstart.md

**Tests**: Not explicitly requested — verification tasks use existing test suite and tooling.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Baselines)

**Purpose**: Capture baseline outputs before any code changes, for diff-based verification later.

- [x] T001 Capture baseline CLI output by running `ab --list` and saving to a temp file for later diff
- [x] T002 [P] Capture baseline Sphinx build output by running `sphinx-build docs/ html/` and noting warning count
- [x] T003 [P] Run `pytest` and confirm all existing tests pass (baseline green)

**Checkpoint**: Baselines captured — ready to implement.

---

## Phase 2: User Story 1 — IDE Autocompletion on Endpoint Methods (Priority: P1) — MVP

**Goal**: Add type annotations to all 22 endpoint attributes and 2 aliases on `ABConnectAPI` so IDEs resolve types and offer method completions.

**Independent Test**: Type `api.dashboard.` in VS Code with Pylance or PyCharm and confirm method suggestions appear with signatures and return types.

### Implementation for User Story 1

- [x] T004 [US1] Add `: <EndpointType>` annotation to all 22 endpoint attribute assignments in `ab/client.py` `_init_endpoints()` method (lines 93–119) — e.g., `self.dashboard: DashboardEndpoint = DashboardEndpoint(self._acportal)`
- [x] T005 [US1] Add `: DocumentsEndpoint` annotation to the `self.docs` alias and `: CommodityMapsEndpoint` annotation to the `self.cmaps` alias in `ab/client.py` (lines 123–124)
- [x] T006 [US1] Run `pytest` and confirm all existing tests still pass after the annotation changes in `ab/client.py`

**Checkpoint**: User Story 1 complete — IDE autocompletion works for all endpoints.

---

## Phase 3: User Story 2 — Request Model Discoverability (Priority: P2)

**Goal**: Verify that the type annotations enable IDE go-to-definition and hover on request/response model types used in endpoint method signatures.

**Independent Test**: Hover over or go-to-definition on the `data` parameter in `api.dashboard.inbound(data=...)` and confirm the IDE resolves to `DashboardCompanyRequest` with all fields visible.

### Implementation for User Story 2

- [x] T007 [US2] Verify that endpoint method signatures in `ab/api/endpoints/dashboard.py` (and a sample of other endpoint files) use concrete model types in their `data:` and return annotations, not string literals — if any use string-only forward references behind `TYPE_CHECKING`, convert them to runtime imports so IDEs can resolve the full chain
- [x] T008 [US2] Spot-check 3–5 endpoint files (`ab/api/endpoints/companies.py`, `ab/api/endpoints/contacts.py`, `ab/api/endpoints/jobs.py`, `ab/api/endpoints/shipments.py`, `ab/api/endpoints/catalog.py`) for `TYPE_CHECKING`-guarded model imports that block IDE resolution — convert to runtime imports if safe (no circular import risk)

**Checkpoint**: User Story 2 complete — full model discoverability chain works from client through endpoint to request model.

---

## Phase 4: User Story 3 — Documentation and CLI Remain Accurate (Priority: P2)

**Goal**: Confirm that Sphinx docs, CLI discovery, and examples are unaffected by the changes.

**Independent Test**: Diff CLI output against baseline; build Sphinx docs with zero new warnings; confirm examples list.

### Verification for User Story 3

- [x] T009 [US3] Run `ab --list` and diff against baseline captured in T001 — output must be identical
- [x] T010 [P] [US3] Run `sphinx-build docs/ html/` and confirm zero new warnings compared to baseline from T002
- [x] T011 [P] [US3] Run `ex --list` and confirm all example modules are listed without errors

**Checkpoint**: User Story 3 complete — no regressions in docs, CLI, or examples.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation across all stories.

- [x] T012 Run `ruff check .` to confirm no linting issues introduced in `ab/client.py`
- [x] T013 Run full `pytest` suite one final time to confirm green across all tests

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **User Story 1 (Phase 2)**: Depends on baselines from Phase 1
- **User Story 2 (Phase 3)**: Can start after T004–T005 (needs annotations in place)
- **User Story 3 (Phase 4)**: Can start after T004–T005 (needs annotations in place)
- **Polish (Phase 5)**: Depends on all user stories complete

### User Story Dependencies

- **US1 (P1)**: Independent — core implementation
- **US2 (P2)**: Depends on US1 (annotations must exist before verifying model resolution chain)
- **US3 (P2)**: Depends on US1 (annotations must exist before verifying no regressions)

### Parallel Opportunities

- T001, T002, T003 can all run in parallel (baseline captures)
- T004 and T005 are sequential (same file) but fast
- T007 and T008 can run in parallel (different endpoint files)
- T009, T010, T011 can all run in parallel (different tools)
- T012 and T013 can run in parallel (different tools)

---

## Parallel Example: Baseline Capture

```bash
# Launch all baseline captures together:
Task: "Capture CLI baseline — ab --list"
Task: "Capture Sphinx baseline — sphinx-build docs/ html/"
Task: "Run pytest baseline"
```

## Parallel Example: Regression Verification

```bash
# Launch all verification tasks together:
Task: "Diff CLI output — ab --list"
Task: "Build Sphinx docs — sphinx-build docs/ html/"
Task: "List examples — ex --list"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Capture baselines
2. Complete Phase 2: Add all type annotations to `ab/client.py`
3. **STOP and VALIDATE**: Run pytest, check IDE completions
4. This alone delivers the core value

### Incremental Delivery

1. Baselines → captured
2. Add type annotations → IDE completions work (MVP!)
3. Verify model chain → full discoverability confirmed
4. Verify docs/CLI/examples → no regressions confirmed
5. Polish → clean

---

## Notes

- Only 1 file is modified: `ab/client.py`
- All other tasks are verification/spot-checks
- The `from __future__ import annotations` at the top of `client.py` makes all annotations strings at runtime — this is fine because the types are also used as runtime assignments, and type checkers evaluate annotations statically
- If any `TYPE_CHECKING`-guarded imports in endpoint files block IDE resolution (US2), the fix is to move those specific imports out of the guard — but only if they don't cause circular imports
