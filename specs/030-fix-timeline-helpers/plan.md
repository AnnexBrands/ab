# Implementation Plan: Fix Timeline Helpers

**Branch**: `030-fix-timeline-helpers` | **Date**: 2026-03-03 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/030-fix-timeline-helpers/spec.md`

## Summary

Replace the broken `TimelineTaskCreateRequest` (4 generic fields) with three per-type request models matching the C# server's polymorphic deserialization: `InTheFieldTaskRequest` (PU/DE), `SimpleTaskRequest` (PK/ST), and `CarrierTaskRequest` (CP). Rewrite `TimelineHelpers` to construct proper Pydantic model instances instead of raw dicts. Add type annotations to `JobsEndpoint.__init__` for IDE discoverability. Include the `ChangeJobAgentRequest` export fix from the previous session.

## Technical Context

**Language/Version**: Python 3.11+ (existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: Filesystem (fixture JSON files in `tests/fixtures/`)
**Testing**: pytest (existing test infrastructure, gate regression ratchet from 028)
**Target Platform**: Python SDK (pip installable)
**Project Type**: Single project — SDK package
**Performance Goals**: N/A (SDK wrapping HTTP API — latency is API-bound)
**Constraints**: Must follow existing patterns (Route, RequestModel, helpers). Must match C# ground truth DTOs.
**Scale/Scope**: 3 new request models + 6 nested models (replacing 1 broken model), helper rewrite, type annotations, 3 request fixtures

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | Three per-type request models with `extra="forbid"`, nested models for TimeLog/WorkTimeLog/etc. Field names match C# DTOs exactly. |
| II. Example-Driven Fixture Capture | PASS | Existing `examples/timeline.py` unchanged. Request fixtures created from C# ground truth and ABConnectTools patterns. |
| III. Four-Way Harmony | PASS | Endpoint method (existing), examples (existing), fixtures (updated), tests (existing + new request fixtures). |
| IV. Swagger-Informed, Reality-Validated | PASS | Models derived from C# server source (Tier 1), cross-referenced with ABConnectTools and swagger. |
| V. Endpoint Status Tracking | PASS | FIXTURES.md updated after implementation. Gate baseline updated. |
| VI. Documentation Completeness | PASS | Sphinx autodoc covers models automatically. Helper method docstrings preserved. |
| VII. Flywheel Evolution | PASS | Bug fix feedback loop — runtime crash discovered in consumer usage drives model correction. |
| VIII. Phase-Based Context Recovery | PASS | Tasks use checkbox format, each phase produces committed artifacts. |
| IX. Endpoint Input Validation | PASS | Per-type request models enforce correct fields per task code. `extra="forbid"` catches invalid fields at construction time. This is the primary fix. |

**No violations. No complexity tracking needed.**

## Project Structure

### Documentation (this feature)

```text
specs/030-fix-timeline-helpers/
├── spec.md
├── plan.md              # This file
├── research.md          # Design decisions D1-D7
├── data-model.md        # Request model definitions
├── quickstart.md        # Usage scenarios
├── contracts/
│   └── api-endpoints.md # Endpoint contract with polymorphic examples
├── checklists/
│   └── requirements.md  # Quality checklist
└── tasks.md             # Task breakdown (via /speckit.tasks)
```

### Source Code (repository root)

```text
ab/
├── api/
│   ├── endpoints/
│   │   └── jobs.py           # MODIFY — type annotations, remove request_model from Route
│   ├── models/
│   │   ├── __init__.py       # MODIFY — export new models, remove old export
│   │   └── jobs.py           # MODIFY — replace TimelineTaskCreateRequest with 3 models + nested
│   └── helpers/
│       └── timeline.py       # REWRITE — model construction instead of raw dicts

tests/
├── fixtures/
│   └── requests/
│       ├── InTheFieldTaskRequest.json    # NEW
│       ├── SimpleTaskRequest.json        # NEW
│       ├── CarrierTaskRequest.json       # NEW
│       └── TimelineTaskCreateRequest.json # REMOVE
├── gate_baseline.json                     # UPDATE
└── models/
    └── (auto-discovered by test_request_fixtures.py)

FIXTURES.md                                # REGENERATE
```

**Structure Decision**: Follows established single-project SDK layout. No new files beyond models and fixtures — the helper file and endpoint file are modified in place.

## Design Decisions Summary

| ID | Decision | Rationale |
|----|----------|-----------|
| D1 | Three per-type request models (InTheField/Simple/Carrier) replacing one broken model | Matches C# `TaskModelDataBinder` polymorphic deserialization |
| D2 | Nested request models for TimeLog, WorkTimeLog, InitialNote, etc. | `extra="forbid"` requires typed nested structures, not dicts |
| D3 | Remove `request_model` from `_POST_TIMELINE` Route; validate in helper layer | Avoids framework-level polymorphic dispatch; same pattern as AgentHelpers |
| D4 | Type annotations via `TYPE_CHECKING` imports | IDEs need annotations; runtime imports stay in `__init__` to avoid circular imports |
| D5 | Model instantiation in helpers, no raw dict templates | Pydantic-first architecture; catches typos at construction time |
| D6 | Keep unified `TimelineTask` response model | `extra="allow"` handles all task types; no benefit to splitting |
| D7 | One request fixture per task type | Each type has different fields; one fixture can't represent all three |

## Story Dependency Graph

```text
US1 (Per-type models) ─────────────────────────────┐
   │                                                 │
   ├── Nested models (TimeLog, etc.)                 │
   ├── Per-type request models (3)                   │
   ├── Remove old TimelineTaskCreateRequest          │
   ├── Remove request_model from Route               │
   │                                                 │
US2 (IDE discoverability) ── type annotations        ├── US3 (Helper rewrite)
   │                                                 │
   └── TYPE_CHECKING imports in jobs.py              │
                                                     │
US3 (Model construction) ──────────────────────────┘
   │
   ├── Rewrite all helper methods to construct models
   ├── Remove _NEW_*_TASK dict templates
   └── Request fixtures per task type
```

US1 (models) must complete first. US2 (type annotations) is independent. US3 (helper rewrite) depends on US1. US4 (response models) is deferred — existing models work.

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Existing tests break from model replacement | Medium | Medium | Run full suite after model changes; gate ratchet catches regressions |
| Helper rewrite introduces behavioral changes | Low | High | Preserve exact same field names and values; test against staging |
| `ChangeJobAgentRequest` export fix conflicts with main | Low | Low | Include in this branch's first commit |
| Nested model construction adds verbosity to helpers | Low | Low | Helper methods hide the complexity; consumer API unchanged |
