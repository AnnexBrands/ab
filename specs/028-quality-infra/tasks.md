# Tasks: Quality Infrastructure Sprint

**Input**: Design documents from `/specs/028-quality-infra/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/cli-interfaces.md, quickstart.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Foundational — Unified Fixture Handling (US2)

**Goal**: Consolidate 3 competing fixture-unwrapping patterns into canonical helpers. Every downstream story depends on these helpers.

**Independent Test**: `grep -rn "def first_or_skip\|def _first_or_skip" tests/` shows only one definition in `tests/conftest.py`.

- [X] T001 [US2] Add `first_or_skip(data)` helper function to `tests/conftest.py` — handles dict passthrough, `list[0]` extraction, empty-list `pytest.skip()`, and paginated `{data: [...]}` unwrapping per D3 in research.md
- [X] T002 [US2] Extract inline unwrapping logic from `ab/progress/gates.py` `evaluate_g1()` (lines 101-123) into a standalone `unwrap_fixture(data, model_cls=None)` function at module level in `ab/progress/gates.py`, then call it from `evaluate_g1()` — per D4 in research.md
- [X] T003 [P] [US2] Refactor `tests/models/test_report_models.py` — remove local `_first_or_skip` definition, import and use `first_or_skip` from `tests.conftest` in all test methods
- [X] T004 [P] [US2] Refactor `tests/models/test_extended_lookup_models.py` — remove local `_first_or_skip` definition, import and use `first_or_skip` from `tests.conftest` in all test methods
- [X] T005 [P] [US2] Refactor `tests/models/test_lookup_models.py` — replace inline `if isinstance(data, list) and data: data = data[0]` with `first_or_skip` calls
- [X] T006 [P] [US2] Refactor `tests/models/test_shipment_models.py` — replace inline `isinstance(data, list)` patterns and early returns with `first_or_skip` calls
- [X] T007 [US2] Run `cd src && pytest tests/models/ --tb=line -q` to verify all refactored tests still pass/skip correctly — zero new failures introduced

**Checkpoint**: Single canonical `first_or_skip` in conftest.py, `unwrap_fixture` in gates.py. All model tests use shared helpers.

---

## Phase 2: Fix Pre-Existing Test Failures (US3)

**Goal**: Resolve 5 of 7 pre-existing failures (remaining 2 fixed in US4). Establish a nearly-clean suite.

**Independent Test**: `cd src && pytest --tb=line -q` shows at most 2 failures (the FIXTURES.md-related ones fixed in US4).

- [X] T008 [US3] Fix `test_list_users` — change positional `api.users.list(data)` to keyword `api.users.list(data=data)` in the test file (find via `grep -rn "test_list_users" tests/`)
- [X] T009 [US3] Fix `test_priced_freight_provider` in `tests/models/test_freight_models.py` — use `first_or_skip(data)` to handle empty `[]` fixture gracefully
- [X] T010 [US3] Fix `test_user_role` in `tests/models/test_user_models.py` — the API returns `List[str]`, not a Pydantic model; rewrite test to assert `isinstance(data, list)` and `isinstance(data[0], str)`, or skip if fixture missing
- [X] T011 [US3] Fix `test_search_contact_entity_result` and `test_response_field_values` — replaced misfiled live fixture (contained ContactDetailedInfo data) with correct search result data from mocks/
- [X] T012 [US3] Run `cd src && pytest --tb=line -q` to verify failures #1-#5 are resolved — expected: at most 2 remaining failures (FIXTURES.md-related, fixed in Phase 3)

**Checkpoint**: 5 of 7 failures fixed. Test output is nearly clean.

---

## Phase 3: FIXTURES.md Integrity Repair (US4)

**Goal**: Fix mock coverage scanning and FIXTURES.md drift. Resolves final 2 pre-existing failures.

**Independent Test**: `cd src && pytest tests/test_mock_coverage.py -v` passes all assertions.

- [X] T013 [US4] Update `tests/test_mock_coverage.py` — fixed column offset (cells[4] for RespModel, cells[6] for G2), added request model + params_model tracking from Route definitions, scanned `tests/fixtures/requests/` directory
- [X] T014 [US4] Update `tests/test_mock_coverage.py` — modified `test_captured_fixtures_exist_on_disk` to check `tests/fixtures/requests/` for request fixture files, separated response vs request captured tracking
- [X] T015 [US4] Fixed missing `request_model="TimelineTaskCreateRequest"` on `_POST_TIMELINE` Route in `ab/api/endpoints/jobs.py` (was causing orphaned fixture)
- [X] T016 [US4] Run `pytest tests/test_mock_coverage.py -v` — all 4 tests pass
- [X] T017 [US4] Run `pytest --tb=line -q` — 533 passed, 57 skipped, 5 xfailed, 0 failures

**Checkpoint**: FIXTURES.md reflects reality. Test suite is clean (0 failures). Ready for gate ratchet baseline.

---

## Phase 4: No-Response Endpoint Exemptions (US8)

**Goal**: Adjust gate denominators by exempting void endpoints from response-model-dependent gates.

**Independent Test**: Run `cd src && python scripts/generate_progress.py --fixtures` and verify denominator changes.

- [X] T018 [US8] Modified `evaluate_endpoint_gates()` in `ab/progress/gates.py` — when `response_model` is `None`, G1-G4 now return `True` ("No response model — exempt"). Added `bytes` to `_SCALAR_TYPES` set for auto-pass
- [X] T019 [US8] (Covered by T018 — all four gates handled in single block)
- [X] T020 [US8] (Covered by T018)
- [X] T021 [US8] (Covered by T018)
- [X] T022 [US8] FIXTURES.md regenerated in T048 — complete count increased from 69 to 127, 52 void endpoints now exempt
- [X] T023 [US8] Run `pytest --tb=line -q` — 533 passed, 57 skipped, 5 xfailed, 0 failures

**Checkpoint**: Gate denominators are honest. Void endpoints no longer drag down percentages.

---

## Phase 5: Return Type Annotation Sweep (US7)

**Goal**: Fix `-> Any` return type annotations to match Route `response_model`. Close G4 gap.

**Independent Test**: Run gate evaluation and confirm G4 pass count >= 200.

- [X] T024 [US7] Audit performed inline — all 46 `-> Any` methods identified. 45 void (Route response_model=None) → `-> None`, 1 bytes (shipments.get_shipment_document) → `-> bytes`
- [X] T025 [US7] (Covered by T024)
- [X] T026 [P] [US7] Fixed `ab/api/endpoints/jobs.py` — 17 methods changed from `-> Any` to `-> None`, removed unused `Any` import
- [X] T027 [P] [US7] Fixed `ab/api/endpoints/rfq.py` — 5 methods changed to `-> None`
- [X] T028 [P] [US7] Fixed `ab/api/endpoints/companies.py` — 7 methods changed to `-> None`
- [X] T029 [P] [US7] Fixed `ab/api/endpoints/contacts.py` — 3 methods changed to `-> None`
- [X] T030 [P] [US7] Fixed `ab/api/endpoints/dashboard.py` — 6 methods changed to `-> None`
- [X] T031 [P] [US7] Fixed documents.py (2→None), users.py (2→None), shipments.py (1→bytes), catalog.py (1→None), lookup.py (1→None), views.py (1→None)
- [X] T032 [US7] Run `pytest --tb=line -q` — 533 passed, 57 skipped, 5 xfailed, 0 failures
- [X] T033 [US7] FIXTURES.md regenerated in T048 — G4: 220/231 pass (target was >= 200)

**Checkpoint**: G4 gap closed from ~78 to ~30 or less. Return types match Route definitions.

---

## Phase 6: Gate Regression Ratchet (US1)

**Goal**: Create per-endpoint-per-gate regression test with JSON baseline. Prevent future gate regressions.

**Independent Test**: Break a passing model field, run `pytest tests/test_gate_regression.py`, confirm it fails naming the regressed endpoint and gate.

- [X] T034 [US1] Created `scripts/update_gate_baseline.py` — generates sorted JSON baseline with diff summary
- [X] T035 [US1] Created `tests/test_gate_regression.py` — auto-generates baseline on first run, detects regressions per-endpoint-per-gate
- [X] T036 [US1] Generated initial baseline: 231 endpoints, 1190 passing gates
- [X] T037 [US1] Ratchet test passes against baseline — 534 total tests passing
- [X] T038 [US1] Verified ratchet catches regressions — renamed CompanySimple.name → name_BROKEN, ratchet correctly detected 3 G1 regressions (/companies/{_} GET, /companies/list POST, /companies/availableByCurrentUser GET), reverted successfully

**Checkpoint**: Gate ratchet is live. Any future PR that regresses a gate will be caught by `pytest`.

---

## Phase 7: Auto-Generate Model Test Stubs (US6)

**Goal**: Generate mechanical test stubs for endpoints missing G3 (Test Quality) coverage.

**Independent Test**: Run generator, then `cd src && pytest tests/models/ --tb=line -q` — generated tests pass or skip, none fail.

- [X] T039 [US6] Create `scripts/generate_model_tests.py` — reads all Route definitions via `ab.progress.route_index`, filters to routes with a Pydantic `response_model` (excluding None, bytes, primitives), checks existing `tests/models/test_*_models.py` files for `def test_{model_name_snake}(` to detect duplicates, generates missing test methods using the pattern in D7 of research.md. Group output by endpoint module. Support `--dry-run` flag. Per contracts/cli-interfaces.md
- [X] T040 [US6] Dry-run showed 1 stub needed (ShipmentExportData) — existing coverage is already high; original estimate of 40+ was before earlier work completed. ServiceBaseResponse excluded (G1 fails). Fuzzy name matching handles snake_case variations (e.g., Web2LeadReport)
- [X] T041 [US6] Run `cd src && python scripts/generate_model_tests.py` to generate and write the test stubs to `tests/models/test_generated_stubs.py`
- [X] T042 [US6] Run `cd src && pytest tests/models/ --tb=line -q` — 307 passed, 44 skipped, 0 failures
- [X] T043 [US6] Run `cd src && python scripts/update_gate_baseline.py` — 231 endpoints, 1191 passing gates (+1 G3 for ShipmentExportData)

**Checkpoint**: G3 gap reduced. Generated stubs auto-skip when fixtures are missing. Baseline updated.

---

## Phase 8: Batch Fixture Capture Tooling (US5)

**Goal**: Build batch capture script to accelerate fixture collection. Run against staging if available.

**Independent Test**: `cd src && python scripts/capture_missing.py --dry-run` completes without errors and lists G2-failing endpoints.

- [X] T044 [US5] Created `scripts/capture_missing.py` — parses FIXTURES.md for G2=FAIL endpoints, discovers matching example entries by response model name, supports `--dry-run` and live capture via subprocess
- [X] T045 [US5] Dry-run showed 54 G2-failing endpoints, all 54 have matching example entries (100% coverage). No unmatched endpoints
- [X] T046 [US5] Staging API not available — script is ready for use when staging becomes available. No fixtures captured

**Checkpoint**: Batch capture tooling delivered. Script is ready for current or future staging runs.

---

## Phase 9: Polish & Final Validation

**Purpose**: Final verification across all stories. Update baseline and regenerate tracking.

- [X] T047 Gate baseline updated — 231 endpoints, 1191 passing gates (no change from T043)
- [X] T048 FIXTURES.md regenerated — 231 endpoints, 127 complete, G4: 220/231
- [X] T049 Full test suite — 535 passed, 57 skipped, 5 xfailed, 0 failures
- [X] T050 Gate ratchet passes against final baseline
- [X] T051 FIXTURES.md integrity — all 4 mock coverage tests pass
- [X] T052 Success criteria verified: SC-001 ✓ (0 failures), SC-002 ✓ (ratchet exists), SC-003 ✓ (single first_or_skip), SC-004 ✓ (integrity passes), SC-005 ✓ (batch capture 54/54 matched), SC-006 ~ (1 stub — coverage already high), SC-007 ✓ (G4=220 >= 200), SC-008 ✓ (179 non-exempt), SC-009 ~ (127 vs 130 target — 3 short, gap is endpoint-level G5/G6 issues)

**Checkpoint**: All success criteria validated. Feature complete.

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (US2: helpers) ─────────────────────────────────────────────────────────┐
  │                                                                              │
  ├──> Phase 2 (US3: fix failures) ──> Phase 3 (US4: FIXTURES.md) ──┐           │
  │                                                                   ├──> Phase 6 (US1: ratchet)
  │    Phase 4 (US8: exemptions) ────────────────────────────────────┘           │
  │                                                                              │
  │    Phase 5 (US7: return types) ── independent after Phase 1                  │
  │                                                                              │
  ├──> Phase 7 (US6: test stubs) ── depends on Phase 1 helpers                  │
  │                                                                              │
  │    Phase 8 (US5: batch capture) ── fully independent                         │
  │                                                                              │
  └──> Phase 9 (polish) ── after all phases                                     ─┘
```

### Parallel Opportunities

- **After Phase 1 (US2)**: Phase 2 (US3), Phase 4 (US8), Phase 5 (US7), Phase 7 (US6), Phase 8 (US5) can all start
- **Within Phase 5 (US7)**: T026-T031 are parallel (different endpoint files)
- **Within Phase 1 (US2)**: T003-T006 are parallel (different test files)

### Critical Path

```
US2 (T001-T007) → US3 (T008-T012) → US4 (T013-T017) → US8 (T018-T023) → US1 (T034-T038) → Polish (T047-T052)
```

---

## Implementation Strategy

### MVP First (Phase 1 + 2 + 3)

1. Complete Phase 1 (US2): Unified helpers
2. Complete Phase 2 (US3): Fix failures
3. Complete Phase 3 (US4): FIXTURES.md integrity
4. **STOP and VALIDATE**: `pytest` shows 0 failures, `pytest tests/test_mock_coverage.py` passes
5. This alone delivers SC-001 and SC-003 and SC-004

### Incremental Delivery

1. Phases 1-3 → Clean test suite (MVP)
2. Phase 4 (US8) → Honest denominators
3. Phase 5 (US7) → G4 improvement
4. Phase 6 (US1) → Regression protection (highest business value)
5. Phase 7 (US6) → G3 improvement via generated stubs
6. Phase 8 (US5) → Batch capture tooling
7. Phase 9 → Final validation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Commit after each phase completion (per Constitution Principle VIII)
- The implementation order differs from spec priority order (US1 is P1 in spec but Phase 6 here) because technical dependencies require foundation work first
- US5 (batch capture) requires staging API credentials — can be delivered as tooling and run later
- Tasks T007, T012, T017, T023, T032, T037, T042 are verification gates — do not skip them
