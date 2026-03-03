# Tasks: Agent Assignment Helpers

**Input**: Design documents from `/specs/029-agent-helpers/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/api-endpoints.md, quickstart.md

**Tests**: Not explicitly requested. Quality gate regression and mock coverage are enforced by existing infrastructure (028).

**Organization**: Tasks grouped by user story. US1-US3 share foundational infrastructure (Phase 2), then each story adds its specific helper method. US4 (README) is independent documentation work.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Branch verification and project structure confirmation

- [x] T001 Verify branch `029-agent-helpers` is checked out and clean
- [x] T002 Confirm `ab/api/helpers/` directory exists (already present from timeline.py)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared models, enum, route, and endpoint method that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 [P] Add `ServiceType(int, Enum)` to `ab/api/models/enums.py` with values UNDEFINED=0, PICK=1, PACK=2, PICKANDPACK=3, DELIVERY=4
- [x] T004 [P] Add `ChangeJobAgentRequest(RequestModel)` to `ab/api/models/jobs.py` with fields: service_type (Optional[int], alias serviceType), agent_id (Optional[str], alias agentId), recalculate_price (Optional[bool], alias recalculatePrice), apply_rebate (Optional[bool], alias applyRebate)
- [x] T005 [P] Create request fixture `tests/fixtures/requests/ChangeJobAgentRequest.json` with sample payload matching contracts/api-endpoints.md
- [x] T006 Add `_POST_CHANGE_AGENT` Route and `change_agent()` method to `ab/api/endpoints/jobs.py` — route: POST `/job/{jobDisplayId}/changeAgent`, request_model=ChangeJobAgentRequest, response_model=ServiceBaseResponse
- [x] T007 Add TYPE_CHECKING import for `ChangeJobAgentRequest` in `ab/api/endpoints/jobs.py` and return type annotation `ServiceBaseResponse` on `change_agent()`

**Checkpoint**: Route + model + enum ready. The raw `api.jobs.change_agent(jobDisplayId=..., **kwargs)` call works.

---

## Phase 3: User Story 1 — Change Origin Agent via Code (Priority: P1)

**Goal**: Enable `api.jobs.agent.oa(job, "3P-5153")` to change the origin agent using a friendly code

**Independent Test**: `api.jobs.agent.oa(12345, "3P-5153")` resolves code to UUID, sends POST with serviceType=3, returns ServiceBaseResponse

### Implementation for User Story 1

- [x] T008 [US1] Create `ab/api/helpers/agent.py` with `AgentHelpers` class — `__init__(self, jobs, resolver)` stores references to JobsEndpoint and CodeResolver, following TimelineHelpers pattern
- [x] T009 [US1] Implement `AgentHelpers.change()` method in `ab/api/helpers/agent.py` — resolves agent code via `self._resolver.resolve(agent)`, builds ChangeJobAgentRequest, calls `self._jobs.change_agent()`, returns ServiceBaseResponse
- [x] T010 [US1] Implement `AgentHelpers.oa()` method in `ab/api/helpers/agent.py` — calls `self.change()` with service_type=ServiceType.PICKANDPACK (3)
- [x] T011 [US1] Wire `AgentHelpers` into `JobsEndpoint.__init__` in `ab/api/endpoints/jobs.py` — `self.agent = AgentHelpers(self, self._resolver)`, add import

**Checkpoint**: `api.jobs.agent.oa(job, code)` works end-to-end. US1 acceptance scenarios pass.

---

## Phase 4: User Story 2 — Change Delivery Agent via Code (Priority: P2)

**Goal**: Enable `api.jobs.agent.da(job, "9999AZ")` to change the delivery agent

**Independent Test**: `api.jobs.agent.da(12345, "9999AZ", recalculate_price=True)` sends POST with serviceType=4

### Implementation for User Story 2

- [x] T012 [US2] Implement `AgentHelpers.da()` method in `ab/api/helpers/agent.py` — calls `self.change()` with service_type=ServiceType.DELIVERY (4)

**Checkpoint**: `api.jobs.agent.da(job, code)` works. US2 acceptance scenarios pass.

---

## Phase 5: User Story 3 — Generic Agent Change with Service Type (Priority: P3)

**Goal**: Enable `api.jobs.agent.change(job, code, service_type=1)` for any service type

**Independent Test**: `api.jobs.agent.change(12345, "9999AZ", service_type=ServiceType.PICK)` sends POST with serviceType=1

### Implementation for User Story 3

- [x] T013 [US3] Verify `AgentHelpers.change()` accepts both `ServiceType` enum and raw `int` for service_type parameter in `ab/api/helpers/agent.py` — add `int(service_type)` coercion if enum passed

**Checkpoint**: `api.jobs.agent.change()` accepts enum or int. US3 acceptance scenarios pass.

---

## Phase 6: User Story 4 — README with Agent Group & UAT Guide (Priority: P4)

**Goal**: Update README.md with agent endpoint documentation and comprehensive UAT guide

**Independent Test**: README contains agent endpoint row, UAT steps, expected outputs, failure patterns, and remediation

### Implementation for User Story 4

- [x] T014 [US4] Add `api.jobs.agent` row to the endpoint groups table in `README.md` with methods oa, da, change
- [x] T015 [US4] Add "Agent Assignment Helpers" section to `README.md` with usage examples from quickstart.md
- [x] T016 [US4] Add "UAT Guide" section to `README.md` covering: (1) run full test suite `cd src && pytest --tb=line -q`, (2) expected output (pass/skip/xfail counts, zero failures), (3) run gate regression `pytest tests/test_gate_regression.py -v`, (4) update gate baseline `python scripts/update_gate_baseline.py`, (5) regenerate FIXTURES.md `python scripts/generate_progress.py --fixtures`
- [x] T017 [US4] Add "Troubleshooting" subsection to README.md UAT guide covering: gate regression (meaning + fix + when to update baseline), fixture missing (capture via examples), model mismatch (extra fields investigation), FIXTURES.md drift (regenerate + verify)

**Checkpoint**: README is complete with agent docs + UAT guide. US4 acceptance scenarios pass.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Example file, fixtures, quality gate updates, final validation

- [x] T018 [P] Create `examples/agent.py` with ExampleRunner entries for `oa` and `da` operations, following pattern from existing example files
- [x] T019 Run full test suite `cd src && pytest --tb=line -q` — verify zero failures, no regressions
- [x] T020 Run gate baseline update `python scripts/update_gate_baseline.py` — verify new endpoint gates added, no regressions
- [x] T021 Regenerate FIXTURES.md via `python scripts/generate_progress.py --fixtures` — verify new endpoint appears with correct status
- [x] T022 Run gate regression test `pytest tests/test_gate_regression.py -v` — verify pass
- [x] T023 Run mock coverage test `pytest tests/test_mock_coverage.py -v` — verify pass

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Phase 2 — creates AgentHelpers class and oa()
- **US2 (Phase 4)**: Depends on Phase 3 (uses AgentHelpers class created in US1)
- **US3 (Phase 5)**: Depends on Phase 3 (verifies change() from US1)
- **US4 (Phase 6)**: Can start after Phase 2 (documentation only, no code deps) — but best after Phase 5 to document final API
- **Polish (Phase 7)**: Depends on Phases 3-6 completion

### Within Each User Story

- Models/enum before route (Phase 2)
- Route before helpers (Phase 2 → Phase 3)
- Helper class before wiring into endpoint (T008 → T011)
- oa() before da() (same class, da is trivial addition)
- All code before README documentation

### Parallel Opportunities

- T003, T004, T005 can run in parallel (different files, no deps)
- T018 (example file) can run in parallel with T014-T017 (README)
- US4 (README) can run in parallel with US2/US3 if needed

---

## Parallel Example: Phase 2 (Foundational)

```bash
# Launch parallel foundational tasks (different files):
Task T003: "Add ServiceType enum in ab/api/models/enums.py"
Task T004: "Add ChangeJobAgentRequest in ab/api/models/jobs.py"
Task T005: "Create request fixture in tests/fixtures/requests/ChangeJobAgentRequest.json"

# Then sequential (same file):
Task T006: "Add route + method in ab/api/endpoints/jobs.py"
Task T007: "Add imports in ab/api/endpoints/jobs.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (model + enum + route)
3. Complete Phase 3: US1 (AgentHelpers + oa())
4. **STOP and VALIDATE**: Test `api.jobs.agent.oa(job, code)` independently
5. Proceed to US2-US4 and Polish

### Incremental Delivery

1. Phase 2 → Foundation ready (raw `change_agent()` works)
2. Add US1 → `oa()` works → Core MVP
3. Add US2 → `da()` works → Full convenience API
4. Add US3 → `change()` validated → Full API surface
5. Add US4 → README complete → Discoverable
6. Polish → Gates, fixtures, examples → Ship-ready

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- US1-US3 are tightly coupled (same endpoint, same helper class) — sequential execution recommended
- US4 (README) is independent documentation and can be written at any point after Phase 2
- Total: 23 tasks across 7 phases
- Parallel opportunities: 3 foundational tasks, 2 polish tasks
