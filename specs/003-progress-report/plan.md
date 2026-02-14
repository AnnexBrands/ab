# Implementation Plan: Progress Report

**Branch**: `003-progress-report` | **Date**: 2026-02-14 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-progress-report/spec.md`

## Summary

Generate a self-contained `progress.html` that visualizes SDK implementation coverage across all ABConnect API surfaces. A Python script parses `specs/api-surface.md`, `FIXTURES.md`, `tests/fixtures/`, and `tests/constants.py` to produce a static HTML report with a coverage summary and an "Action Required" section containing step-by-step instructions for every unimplemented endpoint.

## Technical Context

**Language/Version**: Python 3.11+ (same as SDK)
**Primary Dependencies**: None beyond stdlib (`re`, `pathlib`, `html`, `json`, `datetime`)
**Storage**: N/A — reads existing files, writes a single HTML file
**Testing**: pytest — unit tests for markdown parsers and HTML generation
**Target Platform**: Any OS with Python 3.11+; output viewable in any modern browser
**Project Type**: Single script with supporting modules
**Performance Goals**: Sub-second generation for ~300 endpoints
**Constraints**: No external dependencies; self-contained HTML (inline CSS, no JS frameworks)
**Scale/Scope**: ~300 endpoints, ~50 fixtures, ~10 constants

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Applies? | Status | Notes |
|-----------|----------|--------|-------|
| I. Pydantic Model Fidelity | No | N/A | No new API models |
| II. Fixture-Driven Development | No | N/A | No new endpoints; script reads existing fixtures |
| III. Four-Way Harmony | No | N/A | Developer tool, not an API endpoint |
| IV. Swagger-Informed | No | N/A | Does not interact with swagger |
| V. Pending Fixture Tracking | Yes | Aligned | Report visualizes FIXTURES.md data |
| VI. Documentation Completeness | Partial | Aligned | Script docstrings + quickstart sufficient for internal tooling |
| VII. Flywheel Evolution | Yes | Aligned | Tool makes progress visible for stakeholder showcases |
| VIII. Phase-Based Context Recovery | Yes | Aligned | Script produces a checkpoint artifact (HTML report) |

**Gate result**: PASS — no violations.

## Project Structure

### Documentation (this feature)

```text
specs/003-progress-report/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
scripts/
└── generate_progress.py   # Entry point — single command

ab/progress/
├── __init__.py
├── parsers.py             # Markdown parsers for api-surface.md and FIXTURES.md
├── scanner.py             # Filesystem scanner (fixtures dir, constants file)
├── models.py              # Internal dataclasses (Endpoint, Fixture, etc.)
├── renderer.py            # HTML generation with inline CSS
└── instructions.py        # Step-by-step instruction builder

tests/
├── unit/
│   └── test_progress/
│       ├── test_parsers.py
│       ├── test_scanner.py
│       ├── test_renderer.py
│       └── test_instructions.py
└── fixtures/
    └── (existing — read-only by this feature)
```

**Structure Decision**: The generator lives in `ab/progress/` as a subpackage of the SDK, keeping it co-located with the data it reads. The entry point `scripts/generate_progress.py` is a thin wrapper. Tests follow the existing `tests/unit/` convention.

## Complexity Tracking

No constitution violations — section not applicable.
