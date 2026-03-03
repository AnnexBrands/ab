# Implementation Plan: Quality Infrastructure Sprint

**Branch**: `028-quality-infra` | **Date**: 2026-03-02 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/028-quality-infra/spec.md`

## Summary

This feature builds quality infrastructure to prevent gate regressions, unify fixture handling, fix 7 pre-existing test failures, repair FIXTURES.md integrity, and provide tooling for batch fixture capture, test stub generation, and return type cleanup. The work is derived from the 027 PR analysis recommendations R1-R9. The approach leverages the existing gate evaluation system (`ab/progress/gates.py`) and test infrastructure (`tests/conftest.py`) without introducing new external dependencies.

## Technical Context

**Language/Version**: Python 3.11+ (existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: Filesystem (JSON baseline file in `tests/`, generated test stubs in `tests/models/`)
**Testing**: pytest (existing test suite)
**Target Platform**: Developer workstation / CI
**Project Type**: Single project (Python SDK)
**Performance Goals**: Gate evaluation completes in <30s for 231 endpoints; batch capture bounded by API response times
**Constraints**: No new external dependencies; must preserve all existing passing tests
**Scale/Scope**: 231 endpoints, 7 test failures to fix, ~46 return type mismatches, ~48 endpoints to exempt

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | US3 expands SearchContactEntityResult model fields from fixture (Tier 2 source) |
| II. Example-Driven Fixture Capture | PASS | US5 batch capture uses existing ExampleRunner, never fabricates fixtures |
| III. Four-Way Harmony | PASS | US1 ratchet enforces harmony by detecting regression across all 4 artifacts |
| IV. Swagger-Informed, Reality-Validated | PASS | Model fixes (US3) prioritize fixture data over swagger per constitution hierarchy |
| V. Endpoint Status Tracking | PASS | US4 directly repairs FIXTURES.md integrity per this principle |
| VI. Documentation Completeness | PASS | US7 return type sweep improves documentation accuracy (G4) |
| VII. Flywheel Evolution | PASS | This feature IS a flywheel rotation: 027 showcase → guidelines → agent context update |
| VIII. Phase-Based Context Recovery | PASS | Stories have clear dependencies and checkpoint artifacts (baseline.json, fixed tests, regenerated FIXTURES.md) |
| IX. Endpoint Input Validation | N/A | No new endpoints or request models introduced |

**Post-design re-check**: All principles pass. D5 (exemption via `response_model=None`) avoids modifying the Route dataclass, preserving existing contracts.

## Project Structure

### Documentation (this feature)

```text
specs/028-quality-infra/
├── plan.md              # This file
├── research.md          # Phase 0: 8 design decisions (D1-D8)
├── data-model.md        # Phase 1: Gate Baseline, Route, Batch Capture Summary
├── quickstart.md        # Phase 1: Implementation order, verification commands
├── contracts/
│   └── cli-interfaces.md  # Phase 1: 5 script CLIs
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
# Modified files
ab/progress/gates.py           # US2: extract unwrap_fixture; US8: exemption logic
ab/api/models/contacts.py      # US3: expand SearchContactEntityResult
ab/api/endpoints/*.py           # US7: return type annotations (11 files)
tests/conftest.py               # US2: add first_or_skip helper
tests/models/test_report_models.py         # US2: use canonical helper
tests/models/test_extended_lookup_models.py # US2: use canonical helper
tests/models/test_lookup_models.py         # US2: use canonical helper
tests/models/test_shipment_models.py       # US2: use canonical helper
tests/models/test_freight_models.py        # US3: fix empty-list test
tests/models/test_user_models.py           # US3: fix UserRole test
tests/test_mock_coverage.py                # US4: scan requests/ subdir
FIXTURES.md                                # US4: regenerated

# New files
tests/test_gate_regression.py    # US1: ratchet test
tests/gate_baseline.json         # US1: baseline data (auto-generated)
scripts/update_gate_baseline.py  # US1: baseline updater
scripts/capture_missing.py       # US5: batch fixture capture
scripts/generate_model_tests.py  # US6: test stub generator
scripts/audit_return_types.py    # US7: return type mismatch reporter
tests/models/test_*_models.py    # US6: generated test stubs (varies)
```

**Structure Decision**: Follows existing project layout. New scripts go in `scripts/`, new tests go in `tests/`. No structural changes.

## Design Decisions Summary

| ID | Decision | Rationale |
|----|----------|-----------|
| D1 | JSON baseline keyed by `"{path} {METHOD}"` → `["G1", ...]` | Human-readable, diff-friendly, matches route_index normalization |
| D2 | Standalone update script (not pytest flag) | Clear intent separation: running tests vs updating baseline |
| D3 | `first_or_skip()` in conftest.py handles list + empty + dict passthrough | Consolidates 3 competing patterns; mirrors `assert_no_extra_fields` placement |
| D4 | Extract `unwrap_fixture()` from gates.py inline code | Reusable by regression test; includes `items` field disambiguation |
| D5 | Use `response_model=None` as exemption signal (no Route changes) | Avoids modifying frozen dataclass; information already encoded |
| D6 | `scripts/capture_missing.py` orchestrates ExampleRunner | Leverages existing fixture-saving infrastructure |
| D7 | `scripts/generate_model_tests.py` appends to existing test files | Avoids duplicates; follows existing test module organization |
| D8 | Audit script reports mismatches; developer applies fixes | Safer than auto-fixer for edge cases (bytes, None, bypassed routes) |

See [research.md](research.md) for full decision rationale and alternatives considered.

## Story Dependency Graph

```
US2 (unified helpers) ───┐
                         ├──> US3 (fix failures) ──> US4 (FIXTURES.md) ──> US1 (ratchet)
US7 (return types) ──────┘
US8 (exemptions) ─────────────────────────────────────────────────────────────────────>
US5 (batch capture) ── independent (needs staging API)
US6 (test stubs) ── depends on US2 (uses first_or_skip)
```

## Implementation Phases

### Phase A: Foundation (US2 + US3 + US4)

**Goal**: Clean test suite with unified fixture handling.

1. **US2**: Add `first_or_skip()` to `tests/conftest.py`. Extract `unwrap_fixture()` in `ab/progress/gates.py`. Refactor all model test files to use canonical helper. Remove all `_first_or_skip` definitions from individual files.

2. **US3**: Fix 5 easy failures (test_list_users kwarg, test_priced_freight_provider empty list, test_user_role string list, SearchContactEntityResult 31 fields × 2 tests). Fix 2 FIXTURES.md failures via US4.

3. **US4**: Update `test_mock_coverage.py` to scan `tests/fixtures/requests/`. Regenerate FIXTURES.md via `python scripts/generate_progress.py --fixtures`.

**Exit gate**: `pytest` passes with 0 failures. `pytest tests/test_mock_coverage.py` passes.

### Phase B: Tooling (US1 + US7 + US8)

**Goal**: Regression protection, return type accuracy, honest denominators.

4. **US8**: Modify gate evaluation in `ab/progress/gates.py` to skip G1-G4 for endpoints with `response_model=None`. Auto-pass G1 for `bytes` and primitive types. Regenerate FIXTURES.md to reflect new denominators.

5. **US7**: Create `scripts/audit_return_types.py`. Run audit to identify 46 mismatches. Manually fix return type annotations in 11 endpoint files.

6. **US1**: Create `scripts/update_gate_baseline.py`. Create `tests/test_gate_regression.py`. Run baseline updater to generate initial `tests/gate_baseline.json`. Verify ratchet catches intentional regression.

**Exit gate**: `pytest tests/test_gate_regression.py` passes. G4 count >= 200. Denominators adjusted.

### Phase C: Automation (US6 + US5)

**Goal**: Tooling for accelerating future gate progress.

7. **US6**: Create `scripts/generate_model_tests.py`. Run generator. Verify generated stubs pass or skip. Commit generated test files.

8. **US5**: Create `scripts/capture_missing.py`. Verify with `--dry-run`. Run batch capture against staging (if available). Report results.

**Exit gate**: Generator produces 40+ stubs. Batch capture script runs without errors.

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Staging API unavailable for batch capture (US5) | US5 incomplete | US5 is lowest priority; script can be delivered and run later when staging is available |
| SearchContactEntityResult fixture has different fields than documented | US3 fix may differ | Read actual fixture file to determine real field gap (research agent found 22 matching fields — verify live) |
| Test stub generator creates tests that fail immediately | Noise in test output | Generated tests use `require_fixture()` with skip-on-missing — they skip, not fail |
| Return type fixes break existing type checking | Tests fail | Run pytest after each endpoint file change; revert if needed |
| Gate evaluation performance with 231 endpoints | Slow ratchet test | Gate evaluation already runs in <10s; regression test adds only baseline comparison overhead |
