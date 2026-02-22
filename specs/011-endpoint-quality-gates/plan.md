# Implementation Plan: Endpoint Quality Gates

**Branch**: `011-endpoint-quality-gates` | **Date**: 2026-02-21 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/011-endpoint-quality-gates/spec.md`

## Summary

Enforce multi-dimensional quality gates (Model Fidelity, Fixture Status, Test Quality, Documentation Accuracy) for every SDK endpoint. Update 15 response models with ~30 fully-typed sub-models to eliminate all `__pydantic_extra__` warnings. Rewrite all tests with substantive assertions. Fix all `-> Any` return type annotations. Generate FIXTURES.md and progress.html from source artifacts with per-gate pass/fail columns.

## Technical Context

**Language/Version**: Python 3.11+ (existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests, sphinx, sphinx-rtd-theme, myst-parser (all existing)
**Storage**: Filesystem (fixture JSON files in `tests/fixtures/`, generated Markdown/HTML)
**Testing**: pytest with `@pytest.mark.live` for integration tests, model validation tests for fixtures
**Target Platform**: Developer workstation / CI pipeline
**Project Type**: Single SDK project
**Performance Goals**: N/A — tooling, not runtime
**Constraints**: All models must follow ResponseModel conventions (extra="allow", camelCase aliases, Field descriptions)
**Scale/Scope**: 156 tracked endpoints, 15 models to update, ~30 new sub-model classes, 12 integration test files, 30 model test files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | **ENFORCED** | This feature directly enforces Principle I by requiring zero `__pydantic_extra__` for all captured fixtures |
| II. Example-Driven Fixture Capture | **ALIGNED** | Gate G2 checks fixture existence. No fabricated fixtures created |
| III. Four-Way Harmony | **ENFORCED** | The four gates (G1-G4) map directly to the four harmony artifacts: model, fixture/test, example, docs |
| IV. Swagger-Informed, Reality-Validated | **ALIGNED** | Model field types derived from captured fixtures (Tier 2), not swagger (Tier 3) |
| V. Endpoint Status Tracking | **ENHANCED** | FIXTURES.md upgraded from single-status to per-gate multi-dimensional tracking |
| VI. Documentation Completeness | **ENFORCED** | Gate G4 checks return types and autodoc pages |
| VII. Flywheel Evolution | **ALIGNED** | Quality gates become permanent engineering pattern |
| VIII. Phase-Based Context Recovery | **ALIGNED** | Phases produce committed artifacts at each step |
| IX. Endpoint Input Validation | **NO IMPACT** | Feature focuses on response models, not request validation |

**Gate result**: PASS — no violations.

## Project Structure

### Documentation (this feature)

```text
specs/011-endpoint-quality-gates/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 research findings
├── data-model.md        # Sub-model catalog and field mappings
├── quickstart.md        # Implementation quickstart guide
├── contracts/           # Gate evaluation contracts
│   └── gate-evaluation.md
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
ab/api/models/
├── common.py            # NEW — shared sub-models (Coordinates, CompanyAddress)
├── companies.py         # MODIFIED — add 7 fields + ~20 sub-models
├── contacts.py          # MODIFIED — add missing fields
├── shipments.py         # MODIFIED — add 12+ fields + Weight sub-model
├── jobs.py              # MODIFIED — add notedConditions
├── lookup.py            # MODIFIED — add value, id, iataCode
├── users.py             # MODIFIED — add 18+ fields
├── forms.py             # MODIFIED — add 11 fields
├── sellers.py           # MODIFIED — add 2 fields
├── web2lead.py          # MODIFIED — add POST variant alias
├── address.py           # MODIFIED — add 6 fields
└── __init__.py          # MODIFIED — register all new models

ab/api/endpoints/
├── companies.py         # MODIFIED — return type annotations
├── contacts.py          # MODIFIED — return type annotations
├── jobs.py              # MODIFIED — return type annotations
├── users.py             # MODIFIED — return type annotations
├── address.py           # MODIFIED — return type annotations
├── documents.py         # MODIFIED — return type annotations
├── lookup.py            # MODIFIED — return type annotations
├── sellers.py           # MODIFIED — return type annotations
├── catalog.py           # MODIFIED — return type annotations
├── lots.py              # MODIFIED — return type annotations
├── autoprice.py         # MODIFIED — return type annotations
├── web2lead.py          # MODIFIED — return type annotations
└── [all other endpoints] # MODIFIED — return type annotations

ab/progress/
├── gates.py             # NEW — gate evaluation functions
├── models.py            # MODIFIED — add gate dimensions
├── parsers.py           # MODIFIED — parse new FIXTURES.md format
├── renderer.py          # MODIFIED — per-gate columns in HTML
└── fixtures_generator.py # NEW — FIXTURES.md generation from source

tests/
├── conftest.py          # MODIFIED — add assertion helpers
├── integration/
│   └── [all files]      # MODIFIED — substantive assertions
└── models/
    └── [all files]      # MODIFIED — __pydantic_extra__ assertions

scripts/
└── generate_progress.py # MODIFIED — gate evaluation + FIXTURES.md generation

docs/
├── api/[all].md         # VERIFIED — return types correct
└── models/
    ├── companies.md     # VERIFIED — includes new sub-models via automodule
    └── common.md        # NEW — shared sub-models doc page

FIXTURES.md              # REGENERATED — per-gate columns
```

**Structure Decision**: Extends existing single-project structure. New files are `ab/api/models/common.py` (shared sub-models), `ab/progress/gates.py` (gate evaluation), `ab/progress/fixtures_generator.py` (FIXTURES.md generation), and `docs/models/common.md` (shared model docs).

## Complexity Tracking

No violations requiring justification. All changes follow existing patterns:
- Sub-models use existing `ResponseModel` base class
- Gate evaluation extends existing `ab.progress` module
- Tests follow existing `require_fixture()` + assertion patterns
- Docs follow existing `automodule` directive patterns
