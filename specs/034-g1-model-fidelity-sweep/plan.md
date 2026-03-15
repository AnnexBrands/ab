# Implementation Plan: G1 Model Fidelity Sweep

**Branch**: `034-g1-model-fidelity-sweep` | **Date**: 2026-03-15 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/034-g1-model-fidelity-sweep/spec.md`

## Summary

All 21 endpoints that pass G2 but fail G1 share a single response model: `ServiceBaseResponse` in `ab/api/models/shared.py`. The model declares 3 fields but the captured fixture contains 16. Expanding this one model to declare the 13 missing fields (using existing `ShipmentWeight` for the nested `weight` object) will bring all 21 endpoints to G1 parity in a single change. Secondary work: add a fixture-validation test, verify examples cover all 21 endpoints, verify Sphinx docs completeness, update gate baseline.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: N/A — SDK, no local storage
**Testing**: pytest
**Target Platform**: Linux / cross-platform (Python library)
**Project Type**: Library (SDK)
**Performance Goals**: N/A — model expansion, no runtime impact
**Constraints**: No new dependencies; all fields Optional per convention
**Scale/Scope**: 1 model expansion (ServiceBaseResponse), 13 new fields, 1 nested model reuse (ShipmentWeight)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | Core of this feature — expanding models to match fixtures |
| II. Example-Driven Fixture Capture | PASS | Fixture already captured; examples already exist for all 21 endpoints |
| III. Four-Way Harmony | CHECK | Must verify all 4 artifacts updated: model, example, test, docs |
| IV. Swagger-Informed, Reality-Validated | PASS | Using fixture as source of truth (Tier 2), swagger as reference |
| V. Endpoint Status Tracking | CHECK | FIXTURES.md may need update if status changes |
| VI. Documentation Completeness | CHECK | Missing API docs for payments.md, shipments.md; missing model docs for payments.md, commodities.md, views.md |
| VIII. Phase-Based Context Recovery | PASS | Single-phase atomic change |
| IX. Endpoint Input Validation | N/A | No request model changes |

**Verdict**: No violations. CHECK items are verification tasks included in scope.

## Project Structure

### Documentation (this feature)

```text
specs/034-g1-model-fidelity-sweep/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
ab/api/models/
├── shared.py            # ServiceBaseResponse expansion (13 new fields)
└── __init__.py          # No changes needed (ServiceBaseResponse already exported)

tests/
├── fixtures/
│   └── ServiceBaseResponse.json   # Already exists (16 fields)
├── models/
│   └── test_shared_models.py      # New: fixture-validation test for ServiceBaseResponse
└── gate_baseline.json             # Update: add G1 to all 21 endpoint entries

docs/
├── api/
│   ├── payments.md                # New: API docs for payments endpoint
│   └── shipments.md               # New: API docs for shipments endpoint
└── models/
    ├── payments.md                # New: model docs for payment models
    ├── commodities.md             # New: model docs for commodity models
    └── views.md                   # New: model docs for views models
```

**Structure Decision**: Single model file change (`shared.py`) plus test, docs, and baseline updates. No new source directories needed.

## Complexity Tracking

> No constitution violations. This section intentionally left empty.
