# Implementation Plan: Unified Test Mock Framework

**Branch**: `013-test-mock-framework` | **Date**: 2026-02-21 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/013-test-mock-framework/spec.md`

## Summary

Resolve 13 failing tests and 32 xfailed tests by fixing model-API mismatches, adding missing `params_model` classes, and introducing a mock fixture fallback layer (`tests/fixtures/mocks/`). Consolidate duplicated test constants across 15 example files into the existing `tests/constants.py` module. Enhance the fixture loader and G2 quality gate to support mock fixtures with live-fixture precedence.

## Technical Context

**Language/Version**: Python 3.11+ (existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: Filesystem (fixture JSON files in `tests/fixtures/` and `tests/fixtures/mocks/`)
**Testing**: pytest>=7.0 with existing conftest.py fixture infrastructure
**Target Platform**: Developer workstation / CI pipeline (offline-capable)
**Project Type**: Single project (SDK + tests)
**Performance Goals**: N/A — test infrastructure, not runtime
**Constraints**: Must work fully offline (no staging credentials required for model tests)
**Scale/Scope**: 161 endpoints, 13 failures to fix, 32 xfails to resolve, 66 skipped model tests to enable, 15 files with duplicated constants

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | Feature fixes model mismatches to match actual API responses |
| II. Example-Driven Fixture Capture | DEVIATION | Mock fixtures in `tests/fixtures/mocks/` deviate from "fabricated fixtures prohibited" — see Complexity Tracking |
| III. Four-Way Harmony | PASS | Feature strengthens all four artifacts (implementation, example, fixture/test, docs) |
| IV. Swagger-Informed, Reality-Validated | PASS | Models validated against live fixtures where available; swagger used as Tier 3 reference for params models |
| V. Endpoint Status Tracking | DEVIATION | FIXTURES.md and G2 gate updated to reflect mock fixture availability. Mock-backed tests execute instead of skipping — see Complexity Tracking |
| VI. Documentation Completeness | PASS | Mock fixtures enable Sphinx builds without staging credentials |
| VII. Flywheel Evolution | N/A | Not applicable to this feature |
| VIII. Phase-Based Context Recovery | PASS | Work organized into discrete phases with checkpoint commits |
| IX. Endpoint Input Validation | PASS | 32 xfails resolved by adding params_model classes for query parameter validation |

### Post-Phase 1 Re-check

| Principle | Status | Notes |
|-----------|--------|-------|
| II. Example-Driven Fixture Capture | JUSTIFIED DEVIATION | Mock fixtures are (a) stored separately in `mocks/` subdirectory, (b) live fixtures always take precedence, (c) provenance is machine-readable by file location. Spirit of Principle II is preserved. |

## Project Structure

### Documentation (this feature)

```text
specs/013-test-mock-framework/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 research decisions
├── data-model.md        # Phase 1 data model
├── quickstart.md        # Phase 1 quickstart guide
├── contracts/           # Phase 1 internal contracts
│   └── fixture-loader.md
├── checklists/
│   └── requirements.md  # Specification quality checklist
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
ab/
├── api/
│   ├── endpoints/       # Endpoint classes — params_model additions (32 routes)
│   │   ├── catalog.py
│   │   ├── companies.py
│   │   ├── contacts.py
│   │   ├── dashboard.py
│   │   ├── forms.py
│   │   ├── jobs.py
│   │   ├── lookup.py
│   │   ├── lots.py
│   │   ├── partners.py
│   │   ├── payments.py
│   │   ├── rfq.py
│   │   ├── sellers.py
│   │   └── shipments.py
│   └── models/          # Pydantic models — field additions and type fixes
│       ├── address.py   # PropertyType fix
│       ├── catalog.py   # CatalogExpandedDto: +6 fields
│       ├── companies.py # CompanyDetails: +97 fields, CompanySimple: +2 fields
│       ├── contacts.py  # ContactSimple: +30 fields
│       ├── lots.py      # LotDto: +4 fields
│       └── users.py     # UserRole type fix
├── progress/
│   └── gates.py         # G2 gate enhancement for mock fallback

tests/
├── constants.py         # Expanded constants (single source of truth)
├── conftest.py          # Fixture loader with mock fallback
├── fixtures/
│   ├── *.json           # Live-captured fixtures (unchanged)
│   ├── requests/        # Request fixtures (unchanged)
│   └── mocks/           # NEW — manually-authored mock fixtures
│       └── *.json
├── integration/         # Integration tests — fix assertions
├── models/              # Model tests — now run against mocks when no live fixture
└── test_mock_coverage.py # Updated to track mocks/ subdirectory

examples/
├── *.py                 # 15 files — replace hardcoded constants with imports
└── _runner.py           # Unchanged
```

**Structure Decision**: Single project structure. This feature modifies existing files across `ab/`, `tests/`, and `examples/` directories. No new top-level directories. The only new directory is `tests/fixtures/mocks/`.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Principle II: Mock fixtures in `tests/fixtures/mocks/` | 126 endpoints lack live fixtures; 66 model tests permanently skip; Sphinx docs require staging credentials | Strict compliance means no offline testing, no CI without staging access, no docs without live API. Mock fixtures are clearly separated and subordinate to live fixtures. |
| Principle V: Mock-backed tests do not skip | Principle V says endpoints without captured fixtures MUST skip. Mock fixtures enable tests to execute instead of skipping. | Perpetual skips provide no regression signal. Mock fixtures are clearly labeled (separate directory) and live fixtures replace them when captured. The skip obligation applies to fabricated-as-live data, not to explicitly separated mock scaffolding. |
