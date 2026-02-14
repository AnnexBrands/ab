# Implementation Plan: Harden Example Parameters Against Swagger

**Branch**: `005-harden-example-params` | **Date**: 2026-02-14 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-harden-example-params/spec.md`

## Summary

Fix 4 confirmed parameter mismatches where SDK endpoint methods map Python params to wrong API query-parameter names (address.validate, address.get_property_type, forms.get_operations, shipments.request_rate_quotes). Update corresponding examples. Add an automated validation test that cross-references endpoint param mappings against swagger schemas to prevent future drift.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: N/A
**Testing**: pytest
**Target Platform**: Linux / any Python 3.11+ environment
**Project Type**: Single project (SDK library)
**Performance Goals**: Validation test completes in <10 seconds
**Constraints**: No new dependencies; backward-compatible where possible
**Scale/Scope**: 4 endpoint fixes, 4 example updates, 1 new test module

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | No model changes needed — this feature fixes parameter mappings, not models |
| II. Example-Driven Fixture Capture | **ENFORCED** | This feature directly implements the "research before writing" mandate. Fixes examples that violated the research requirement |
| III. Four-Way Harmony | PASS | Endpoint + example changes maintain harmony. No new endpoints introduced |
| IV. Swagger-Informed, Reality-Validated | **ENFORCED** | Core of this feature — aligning param names with swagger |
| V. Endpoint Status Tracking | PASS | No new endpoints; existing statuses unchanged |
| VI. Documentation Completeness | PASS | Parameter name changes will need docstring updates in endpoint methods |
| VII. Flywheel Evolution | PASS | This feature encodes a lesson (don't guess params) into an automated guard |
| VIII. Phase-Based Context Recovery | PASS | Research → fix → test follows DISCOVER phases |

**Post-Phase 1 re-check**: No violations. All changes align with constitution.

## Project Structure

### Documentation (this feature)

```text
specs/005-harden-example-params/
├── plan.md              # This file
├── research.md          # Phase 0 output — audit findings
├── data-model.md        # Phase 1 output — param mapping reference
├── quickstart.md        # Phase 1 output — verification steps
├── contracts/           # Phase 1 output — correct param contracts
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
ab/api/endpoints/
├── address.py           # Fix validate() + get_property_type() param mappings
├── forms.py             # Fix get_operations() param mapping
└── shipments.py         # Fix request_rate_quotes() params→json

examples/
├── address.py           # Update lambda calls to match new signatures
├── forms.py             # No change needed (Python param name unchanged)
├── shipments.py         # Update if signature changes

tests/
└── test_example_params.py  # New: automated swagger validation guard
```

**Structure Decision**: Edits to existing files in the established project layout. One new test file.
