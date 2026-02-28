# Implementation Plan: Refine Request Models

**Branch**: `019-refine-request-models` | **Date**: 2026-02-27 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/019-refine-request-models/spec.md`

## Summary

Replace opaque `**kwargs: Any` and `data: dict | Any` patterns in endpoint methods with explicit, typed keyword arguments backed by validated Pydantic `RequestModel` subclasses. Correct required vs optional field designations using the C# server source as ground truth (Tier 1), add `description` to every field, extract common patterns (pagination, sorting) into shared mixins, and add a G6 quality gate to `progress.html` for incremental tracking.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pydantic>=2.0, pydantic-settings, requests, python-dotenv
**Storage**: N/A (SDK — no persistence)
**Testing**: pytest (unit, contract, integration); `tests/models/test_request_fixtures.py` validates request fixtures
**Target Platform**: PyPI package consumed by Python developers in IDE environments (VSCode, PyCharm)
**Project Type**: Single package (`ab/`)
**Performance Goals**: N/A (SDK correctness, not throughput)
**Constraints**: Backwards compatibility — existing callers passing dicts must continue to work
**Scale/Scope**: ~95 existing request models across 27 model files; ~120 request fixture files; 161 tracked endpoints

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | Core focus of this feature — all request models gain correct fields, descriptions, mixins |
| II. Example-Driven Fixture Capture | PASS | Existing request fixtures must continue to validate (FR-006); no new fabricated fixtures |
| III. Four-Way Harmony | PASS | Endpoint methods, models, fixtures, and docs updated in concert |
| IV. Swagger-Informed, Reality-Validated | PASS | C# source (Tier 1) takes precedence over swagger for required/optional (FR-003) |
| V. Endpoint Status Tracking | PASS | G6 gate added to FIXTURES.md and progress.html (FR-010) |
| VI. Documentation Completeness | PASS | Docstrings on all updated endpoint methods (FR-008); Field descriptions (FR-002) |
| VII. Flywheel Evolution | PASS | Incremental rollout with progress tracking enables flywheel visibility |
| VIII. Phase-Based Context Recovery | PASS | Tasks organized in phases; progress tracked via progress.html and checkbox tasks |
| IX. Endpoint Input Validation | PASS | Core focus — all updated endpoints cast through request models (FR-009) |

No constitution violations. All nine principles are served by this feature.

## Project Structure

### Documentation (this feature)

```text
specs/019-refine-request-models/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── endpoint-method-contract.md
└── tasks.md             # Phase 2 output (NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
ab/
├── api/
│   ├── models/
│   │   ├── base.py           # RequestModel base (unchanged)
│   │   ├── mixins.py         # Add request-specific mixins (PaginationMixin, SortMixin, DateRangeMixin, SearchMixin)
│   │   ├── shared.py         # ListRequest refactored to use PaginationMixin
│   │   ├── jobs.py           # Refine ~20 request models: correct optionality, add descriptions
│   │   ├── companies.py      # Refine ~10 request/params models
│   │   ├── contacts.py       # Refine ~4 request models
│   │   ├── shipments.py      # Refine params/request models
│   │   ├── commodities.py    # Refine ~7 request models
│   │   └── [other domain].py # Each domain module refined incrementally
│   └── endpoints/
│       ├── companies.py      # Replace **kwargs with typed signatures
│       ├── jobs.py           # Replace **kwargs/data with typed signatures
│       ├── contacts.py       # Replace **kwargs with typed signatures
│       └── [other].py        # Each endpoint refined incrementally
└── progress/
    └── gates.py              # Add G6 gate: request model quality

tests/
├── models/
│   ├── test_request_fixtures.py  # Existing — must pass (FR-006)
│   └── test_request_descriptions.py  # New — validates all fields have descriptions
├── fixtures/
│   └── requests/             # Existing request fixture JSON files
└── unit/
    └── test_request_mixins.py  # New — validates mixin composition
```

**Structure Decision**: Single project. All changes within existing `ab/` package and `tests/` directory. No new top-level directories needed.

## Complexity Tracking

No constitution violations to justify.
