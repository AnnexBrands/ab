# Implementation Plan: Request Model Methodology

**Branch**: `007-request-model-methodology` | **Date**: 2026-02-14 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/007-request-model-methodology/spec.md`

## Summary

Update the SDK's endpoint methodology to use Pydantic request models for both body payloads and query parameters. Endpoint methods change from `data: dict | Any` to `**kwargs: Any`, validated through `RequestModel.check()` (which calls `model_validate` internally). Extend the Route dataclass with `params_model` for GET query param validation. Update FIXTURES.md to a unified tracking format covering four completeness dimensions (request model, request fixture, response model, response fixture). Update the DISCOVER workflow to include request model and fixture steps in each phase.

## Technical Context

**Language/Version**: Python 3.11+ (existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: Filesystem (fixture JSON files in `tests/fixtures/` and `tests/fixtures/requests/`)
**Testing**: pytest (existing)
**Target Platform**: Python SDK (cross-platform)
**Project Type**: Single project
**Performance Goals**: N/A — methodology/process feature, not runtime
**Constraints**: Must be backward-compatible at the `_request()` level; breaking change is only at endpoint method signatures for converted endpoints
**Scale/Scope**: Affects ~13 endpoint files, ~17 model files, FIXTURES.md, DISCOVER.md, progress reporting. Does not require converting all 59 existing endpoints — only establishes the pattern and converts a reference endpoint as proof.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | **PASS** | Feature extends model usage to request bodies and params. `RequestModel` with `extra="forbid"` already exists. |
| II. Example-Driven Fixture Capture | **PASS** | Feature adds request fixture capture alongside response fixtures. Examples remain the primary capture mechanism. |
| III. Four-Way Harmony | **PASS** | Feature extends harmony to include request models and request fixtures — strengthens the principle. |
| IV. Swagger-Informed, Reality-Validated | **PASS** | FR-010 requires checking both swagger and ABConnectTools for request model fields. |
| V. Endpoint Status Tracking | **PASS** | FIXTURES.md restructured to unified 4D format. Status values preserved (`captured`, `needs-request-data`). |
| VI. Documentation Completeness | **PASS** | Quickstart.md documents the new pattern. Sphinx docs updated when endpoints are converted. |
| VII. Flywheel Evolution | **PASS** | Methodology codified in DISCOVER workflow → feeds into CLAUDE.md guidance. |
| VIII. Phase-Based Context Recovery | **PASS** | DISCOVER phases updated with explicit request model steps and checkpoint artifacts. |
| IX. Endpoint Input Validation | **PASS** | Feature directly implements this principle. `**kwargs` → `model_validate` ensures validation before HTTP call. `extra="forbid"` catches unknown fields. |

**Gate result**: All 9 principles pass. No violations to justify.

### Post-Phase 1 Re-check

Design decisions in research.md align with all principles:
- R1 (kwargs pattern) → directly implements Principle IX
- R2 (params_model on Route) → extends Principle I to query params
- R4 (request fixture storage) → supports Principle II and V
- R5 (FIXTURES.md format) → implements Principle V with 4D tracking
- R6 (DISCOVER updates) → implements Principle VIII
- R8 (breaking change) → acceptable for pre-1.0 SDK; migration is incremental

**Post-design gate result**: All principles still pass.

## Project Structure

### Documentation (this feature)

```text
specs/007-request-model-methodology/
├── spec.md
├── plan.md              # This file
├── research.md          # Phase 0: design decisions (R1-R8)
├── data-model.md        # Phase 1: entity definitions
├── quickstart.md        # Phase 1: implementation guide
├── contracts/           # Phase 1: pattern contracts
│   └── endpoint-pattern.md
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
ab/
├── api/
│   ├── base.py              # MODIFY: add params_model validation in _request()
│   ├── route.py             # MODIFY: add params_model field to Route
│   ├── endpoints/           # MODIFY: convert signatures to **kwargs (per endpoint)
│   │   ├── companies.py     # Reference conversion (proof of pattern)
│   │   └── *.py             # Future conversions in feature 002+
│   └── models/              # ADD: new request models as needed
│       └── *.py
├── client.py                # NO CHANGE (endpoint registration unchanged)
└── auth/                    # NO CHANGE

tests/
├── fixtures/
│   ├── *.json               # Response fixtures (unchanged)
│   └── requests/            # NEW: request fixture directory
│       └── *.json           # Request fixtures
├── models/                  # MODIFY: add request fixture validation tests
└── test_example_params.py   # NO CHANGE (already validates params)

examples/
├── _runner.py               # MODIFY: add request fixture capture support
└── *.py                     # MODIFY: add request_fixture_file to entries

.claude/
└── workflows/
    └── DISCOVER.md          # MODIFY: add request model steps to phases

FIXTURES.md                  # MODIFY: restructure to unified 4D format
CLAUDE.md                    # AUTO-UPDATED by update-agent-context.sh
```

**Structure Decision**: Single project. All changes are modifications to existing files plus one new directory (`tests/fixtures/requests/`). No new packages or modules.

## Complexity Tracking

> No constitution violations. No complexity justifications needed.
