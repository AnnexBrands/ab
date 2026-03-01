# Implementation Plan: Timeline Operations

**Branch**: `024-timeline-operations` | **Date**: 2026-02-28 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/024-timeline-operations/spec.md`

## Summary

Correct the timeline response models, capture fixtures for all task codes, and build timeline helpers that provide idempotent status transitions with get-then-set collision prevention. The GET /timeline route currently declares `List[TimelineTask]` but the API returns a `TimelineResponse` wrapper object. The `TimelineTask` model is a flat, simplified view that doesn't match the task-code-discriminated models in the C# source (PU/PK/ST/CP each have different fields). This plan rewrites the models from ground truth, captures live fixtures, and ports the `TimelineHelpers` class from ABConnectTools.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: Filesystem (fixture JSON files in `tests/fixtures/`)
**Testing**: pytest with `@pytest.mark.live` for integration tests
**Target Platform**: Linux (SDK library)
**Project Type**: Single project (Python package)
**Performance Goals**: N/A — SDK wrapper
**Constraints**: Must match C# ABConnectTools ground truth behavior
**Scale/Scope**: 8 existing timeline routes + 1 new helper module

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | Models will use ResponseModel (extra=allow) with snake_case + camelCase aliases |
| II. Example-Driven Fixture Capture | PASS | Fixtures captured from live staging, not fabricated |
| III. Four-Way Harmony | PASS | Implementation + example + fixture/test + docs all updated |
| IV. Swagger-Informed, Reality-Validated | PASS | C# server source (Tier 1) + live fixtures (Tier 2) are primary; swagger is reference only |
| V. Endpoint Status Tracking | PASS | FIXTURES.md updated after fixture capture |
| VI. Documentation Completeness | DEFERRED | Sphinx docs updated in Enrich phase |
| VII. Flywheel Evolution | PASS | Timeline helpers are a stakeholder-driven priority |
| VIII. Phase-Based Context Recovery | PASS | Checkpoint commits per phase |
| IX. Endpoint Input Validation | PASS | RequestModel with extra=forbid for outbound bodies |

## Project Structure

### Documentation (this feature)

```text
specs/024-timeline-operations/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
ab/api/
├── endpoints/
│   └── jobs.py                    # Timeline routes + methods (MODIFY)
├── models/
│   └── jobs.py                    # TimelineTask, TimelineResponse, TimelineSaveResponse + sub-models (MODIFY)
├── helpers/
│   └── timeline.py                # NEW: TimelineHelpers class

tests/
├── fixtures/
│   ├── TimelineTask.json          # NEW: captured PU task fixture
│   ├── TimelineAgent.json         # NEW: captured agent fixture
│   └── TimelineResponse.json      # NEW: full timeline response fixture
├── integration/
│   └── test_jobs.py               # Timeline integration tests (MODIFY)
└── models/
    └── test_timeline_models.py    # Timeline model tests (MODIFY)

examples/
└── timeline.py                    # Timeline examples (MODIFY)
```

**Structure Decision**: Single project layout matching existing SDK structure. New `ab/api/helpers/` directory for the timeline helpers module, following ABConnectTools' `endpoints/jobs/timeline_helpers.py` pattern.
