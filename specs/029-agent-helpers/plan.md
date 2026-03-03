# Implementation Plan: Agent Assignment Helpers

**Branch**: `029-agent-helpers` | **Date**: 2026-03-03 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/029-agent-helpers/spec.md`

## Summary

Add a POST `/job/{jobDisplayId}/changeAgent` route with `ChangeJobAgentRequest` model and `AgentHelpers` class providing `oa()`, `da()`, and `change()` convenience methods with code-to-UUID resolution. Update README.md with agent endpoint documentation and a comprehensive UAT guide covering test execution, progress scripts, and troubleshooting.

## Technical Context

**Language/Version**: Python 3.11+ (existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: Filesystem (fixture JSON files in `tests/fixtures/`)
**Testing**: pytest (existing test infrastructure, gate regression ratchet from 028)
**Target Platform**: Python SDK (pip installable)
**Project Type**: Single project — SDK package
**Performance Goals**: N/A (SDK wrapping HTTP API — latency is API-bound)
**Constraints**: Must follow existing patterns (Route, RequestModel, helpers, ExampleRunner)
**Scale/Scope**: 1 new endpoint, 1 new model, 1 new enum, 1 new helper class, README update

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | `ChangeJobAgentRequest` extends `RequestModel` (extra="forbid"); `ServiceBaseResponse` already exists as `ResponseModel` (extra="allow"). All fields snake_case with camelCase aliases. |
| II. Example-Driven Fixture Capture | PASS | `examples/agent.py` will be created with `ExampleRunner`. ABConnectTools reference used for request data. Fixtures captured from staging, not fabricated. |
| III. Four-Way Harmony | PASS | All 4 artifacts planned: implementation (route + model + helper), example, fixture + test, documentation (README). |
| IV. Swagger-Informed, Reality-Validated | PASS | Model fields match swagger schema + ABConnectTools C# DTO. Will be validated against live fixture on capture. |
| V. Endpoint Status Tracking | PASS | FIXTURES.md will be updated with the new endpoint's status after implementation. |
| VI. Documentation Completeness | PASS | README updated with endpoint group and UAT guide. Sphinx docs via existing autodoc. |
| VII. Flywheel Evolution | PASS | UAT guide in README encodes operational knowledge into permanent guidance (stage 4: Agents.md equivalent). |
| VIII. Phase-Based Context Recovery | PASS | Tasks use checkbox format. Each phase produces committed artifacts. |
| IX. Endpoint Input Validation | PASS | `ChangeJobAgentRequest` uses `RequestModel` (extra="forbid") to validate request body. |

**No violations. No complexity tracking needed.**

## Project Structure

### Documentation (this feature)

```text
specs/029-agent-helpers/
├── spec.md
├── plan.md              # This file
├── research.md          # Design decisions D1-D7
├── data-model.md        # Entity definitions
├── quickstart.md        # Usage scenarios
├── contracts/
│   └── api-endpoints.md # Endpoint contract
├── checklists/
│   └── requirements.md  # Quality checklist
└── tasks.md             # Task breakdown (via /speckit.tasks)
```

### Source Code (repository root)

```text
ab/
├── api/
│   ├── endpoints/
│   │   └── jobs.py          # Add _POST_CHANGE_AGENT route + change_agent() method
│   ├── models/
│   │   ├── jobs.py          # Add ChangeJobAgentRequest
│   │   └── enums.py         # Add ServiceType enum
│   └── helpers/
│       ├── timeline.py      # Existing (reference pattern)
│       └── agent.py         # NEW — AgentHelpers class (oa, da, change)

examples/
└── agent.py                 # NEW — ExampleRunner for agent operations

tests/
├── fixtures/
│   ├── requests/
│   │   └── ChangeJobAgentRequest.json  # Request fixture
│   └── mocks/
│       └── (response fixture if staging unavailable)
├── models/
│   └── (test_generated_stubs.py may gain an entry)
└── gate_baseline.json       # Updated baseline

README.md                    # Updated with agent group + UAT guide
FIXTURES.md                  # Regenerated with new endpoint
```

**Structure Decision**: Follows established single-project SDK layout. New helper file mirrors existing `ab/api/helpers/timeline.py` pattern. No structural changes — only additions within existing directory hierarchy.

## Design Decisions Summary

| ID | Decision | Rationale |
|----|----------|-----------|
| D1 | `AgentHelpers` class in `ab/api/helpers/agent.py` | Follows `TimelineHelpers` pattern — separates business logic from route plumbing |
| D2 | Route + method in existing `jobs.py` | All 55 jobs routes live in one file; helper consumes the route |
| D3 | `ChangeJobAgentRequest` with `int` service_type (not enum) | Forward-compatible with new API service types |
| D4 | `ServiceType(int, Enum)` in `enums.py` | Type safety for helper callers; not used in request model |
| D5 | Use existing `CodeResolver` for agent codes | Same cache service, same pattern as `companies.transfer()` |
| D6 | Separate `examples/agent.py` with ExampleRunner | Agent is a distinct sub-group; clean discoverability |
| D7 | UAT guide in README.md (not separate file) | User explicitly requested README coverage |

## Story Dependency Graph

```text
US1 (OA) ──────────────────────────────────────────┐
   │                                                 │
   ├── Route + model + enum + helper (foundation)    │
   │                                                 │
US2 (DA) ── trivial after US1 (same endpoint)        ├── US4 (README/UAT)
   │                                                 │
US3 (change) ── trivial after US1 (same method)   ──┘
```

All code work (US1-US3) is essentially a single implementation phase. US4 (README) can proceed after US1 is working.

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Staging API rejects change-agent request | Medium | Low | Use mock fixtures; document as needs-staging in FIXTURES.md |
| Agent code cache lookup fails | Low | Low | CodeResolver already has fallback (pass raw code) |
| ServiceBaseResponse has different fields for this endpoint | Low | Low | extra="allow" handles new fields; log warnings |
