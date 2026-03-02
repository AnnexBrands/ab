# Implementation Plan: Reports & Lookups Quality Gates

**Branch**: `027-reports-lookups-gates` | **Date**: 2026-03-01 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/027-reports-lookups-gates/spec.md`

## Summary

Rewrite all report response models and extended lookup models to match C# ground truth (Tier 1) and swagger schemas (Tier 3). Current models use placeholder dict-based fields that don't match actual API responses. Capture response fixtures from staging API to pass G1 (Model Fidelity) and G2 (Fixture Status) gates. Target: 50 → 65+ endpoints passing all gates.

## Technical Context

**Language/Version**: Python 3.11+ (existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: Filesystem (fixture JSON files in `tests/fixtures/`)
**Testing**: pytest (existing test suite)
**Target Platform**: Linux (SDK library)
**Project Type**: Single project (SDK)
**Performance Goals**: N/A (model correctness, not performance)
**Constraints**: No new dependencies; backward-compatible model changes
**Scale/Scope**: 8 report endpoints + 12 extended lookup endpoints = 20 endpoints to fix

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | FIX NEEDED | Report models use placeholder dict fields; must match C# DTOs |
| II. Example-Driven Fixture Capture | FIX NEEDED | Report fixtures don't exist; must capture via examples |
| III. Four-Way Harmony | FIX NEEDED | Models, examples, fixtures, tests out of sync for 20 endpoints |
| IV. Swagger-Informed, Reality-Validated | COMPLIANT | Will use C# (Tier 1) > fixtures (Tier 2) > swagger (Tier 3) |
| V. Endpoint Status Tracking | FIX NEEDED | FIXTURES.md shows FAIL for these endpoints |
| VI. Documentation Completeness | DEFERRED | Docs out of scope for this PR |
| VII. Flywheel Evolution | COMPLIANT | Fixing identified gaps from gate sweep |
| VIII. Phase-Based Context Recovery | COMPLIANT | Using speckit workflow |
| IX. Endpoint Input Validation | COMPLIANT | Request models already exist with correct transport |

No violations requiring justification — all FIX NEEDED items are the purpose of this feature.

## Project Structure

### Documentation (this feature)

```text
specs/027-reports-lookups-gates/
├── plan.md              # This file
├── research.md          # C# ground truth findings
├── data-model.md        # Corrected entity definitions
├── quickstart.md        # Verification scenarios
└── tasks.md             # Task breakdown (via /speckit.tasks)
```

### Source Code (repository root)

```text
ab/api/models/
├── reports.py           # MODIFY — rewrite 6 response models from C# DTOs
└── lookup.py            # MODIFY — fix LookupValue, AccessKey, add new models

ab/api/endpoints/
├── reports.py           # VERIFY — response_model references may need updates
└── lookup.py            # VERIFY — response_model for accessKey/{key} needs new model

examples/
├── reports.py           # MODIFY — add date range params for fixture capture
└── lookup.py            # MODIFY — add examples for uncaptured endpoints

tests/
├── fixtures/            # NEW fixtures captured from staging
├── models/
│   ├── test_report_models.py         # MODIFY — update for new model shapes
│   └── test_extended_lookup_models.py # MODIFY — update for new model shapes
└── integration/
    └── test_lookup.py   # VERIFY — existing tests still pass
```

**Structure Decision**: Single project, modifying existing files only. No new architectural patterns.
