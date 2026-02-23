# Implementation Plan: Complete Job Get Response Model

**Branch**: `018-job-get-response` | **Date**: 2026-02-23 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/018-job-get-response/spec.md`

## Summary

The `Job` response model currently defines only 6 domain fields, leaving 27 API response fields unmodeled. Running `python -m examples jobs get 2000000` produces 27 "unexpected field" warnings. This feature completes the Job model with all missing fields and ~15 new sub-models for nested structures (contacts, items, documents, snapshot, SLA, payments, on-hold), following the deep-typing pattern established by feature 016 (CompanyDetails). Tests that currently skip extra-field validation will be enabled.

## Technical Context

**Language/Version**: Python 3.11+ (existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: N/A — SDK, no local storage
**Testing**: pytest with `require_fixture()` and `assert_no_extra_fields()` pattern
**Target Platform**: Python SDK library (cross-platform)
**Project Type**: single
**Performance Goals**: N/A — pydantic model definition, no runtime performance concern
**Constraints**: All fields Optional (response varies by user access level). Aliases must match exact API camelCase keys.
**Scale/Scope**: ~15 new sub-model classes, ~200 new field definitions across all models. 3 files modified.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | All models inherit ResponseModel, use snake_case with camelCase aliases, Optional for nullable, Field descriptions. API typos preserved with comments. |
| II. Example-Driven Fixture Capture | PASS | Fixture already captured (`Job.json`). Server source (Tier 1) researched for field types. No fabricated data. |
| III. Four-Way Harmony | PASS | Endpoint exists, example exists, fixture captured, test exists (will be strengthened). Docs update tracked as follow-up. |
| IV. Swagger-Informed, Reality-Validated | PASS | Models match fixture (Tier 2) and server source (Tier 1). Swagger not needed (higher-tier sources available). |
| V. Endpoint Status Tracking | PASS | `GET /job/{jobDisplayId}` already tracked as captured in FIXTURES.md. |
| VI. Documentation Completeness | DEFERRED | Sphinx docs for new sub-models to be added in documentation phase. Not blocking model completion. |
| VII. Flywheel Evolution | PASS | Follows pattern established by feature 016 (deep company models). |
| VIII. Phase-Based Context Recovery | PASS | Plan artifacts committed. Tasks will use checkbox format. |
| IX. Endpoint Input Validation | N/A | This is a response model change — no endpoint input changes. |

**Post-Phase 1 Re-check**: All gates still pass. No new API contracts introduced. Model design follows established patterns.

## Project Structure

### Documentation (this feature)

```text
specs/018-job-get-response/
├── plan.md              # This file
├── research.md          # Phase 0 output — server source findings, design decisions
├── data-model.md        # Phase 1 output — all entity definitions with field tables
├── quickstart.md        # Phase 1 output — implementation steps and verification
├── contracts/           # Phase 1 output — N/A (no new API contracts)
│   └── README.md
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
ab/api/models/
└── jobs.py              # MODIFY: extend Job, add ~15 sub-model classes

tests/
├── models/
│   └── test_job_models.py    # MODIFY: enable assert_no_extra_fields
└── integration/
    └── test_jobs.py          # MODIFY: enable assert_no_extra_fields
```

**Structure Decision**: Single-project SDK layout. All model changes in one file (`jobs.py`). Reuse `CompanyAddress` and `Coordinates` from `ab/api/models/common.py`.
