# Implementation Plan: Endpoint Request Mocks

**Branch**: `015-endpoint-request-mocks` | **Date**: 2026-02-22 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/015-endpoint-request-mocks/spec.md`

## Summary

Generate null-populated JSON request fixture files for all ~82 unique params_model and request_model classes referenced by Route definitions. Wire `ExampleRunner` and integration tests to load request data from these fixtures instead of hardcoded values. Tighten models where API-required fields are incorrectly Optional. The result is a fail-first workflow where `pytest` failures surface which fixtures need real data.

## Technical Context

**Language/Version**: Python 3.11+ (existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: Filesystem (fixture JSON files in `tests/fixtures/requests/`)
**Testing**: pytest (existing — 232 passing tests)
**Target Platform**: Developer workstation (CLI + test runner)
**Project Type**: Single project (SDK)
**Performance Goals**: N/A (one-time generation + test-time loading)
**Constraints**: Must not break existing 232 passing tests. Must not overwrite existing `CompanySearchRequest.json`.
**Scale/Scope**: ~82 fixture files to generate, ~36 examples to update, ~11 integration test files to update

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|---|---|---|
| I. Pydantic Model Fidelity | PASS | Request models use `RequestModel` (extra="forbid"). Tightening Optional→required aligns with principle. |
| II. Example-Driven Fixture Capture | PASS | Fixtures are populated from real API calls via examples, not fabricated. Null fixtures are scaffolding, not fabricated data. |
| III. Four-Way Harmony | PASS | Feature touches examples, tests, and fixtures (3 of 4 artifacts). Docs updated via FIXTURES.md. |
| IV. Swagger-Informed, Reality-Validated | PASS | Model tightening uses swagger required fields as input, validated against API behavior. |
| V. Endpoint Status Tracking | PASS | FIXTURES.md updated with new request fixture entries. |
| VI. Documentation Completeness | PASS | FIXTURES.md documents all new fixtures. |
| VII. Flywheel Evolution | N/A | No new guidelines produced by this feature. |
| VIII. Phase-Based Context Recovery | PASS | Work organized in discrete phases with checkpoint commits. |
| IX. Endpoint Input Validation | PASS | Core alignment — fixtures drive validation, model tightening enforces required fields. |

No violations. No complexity tracking needed.

## Project Structure

### Documentation (this feature)

```text
specs/015-endpoint-request-mocks/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── fixture-generation.md
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
ab/api/models/address.py          # Model tightening (AddressValidateParams → required fields)
examples/_runner.py                # ExampleRunner fixture loading wiring
examples/address.py                # Updated to use request_fixture_file
examples/*.py                      # Other examples updated
tests/conftest.py                  # Request fixture loading support
tests/fixtures/requests/*.json     # ~82 generated fixture files
tests/integration/test_address.py  # Updated to load from fixtures
tests/integration/test_*.py        # Other integration tests updated
docs/FIXTURES.md                   # Updated with request fixture tracking
```

**Structure Decision**: Single project, existing directory layout. New files only in `tests/fixtures/requests/`. All other changes are modifications to existing files.
