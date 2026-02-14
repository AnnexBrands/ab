# Implementation Plan: Extended API Endpoints

**Branch**: `002-extended-endpoints` | **Date**: 2026-02-13 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-extended-endpoints/spec.md`

## Summary

Extend the `ab` SDK with ~62 new ACPortal endpoints covering job lifecycle management (timeline/status), shipments (rate quotes, booking, accessorials), payments (ACH, Stripe sources), form generation (15 document types), tracking (v3), notes, and parcel items. All new endpoints follow the patterns established in feature 001 — frozen Route dataclasses, typed Pydantic models, fixture-driven validation, Four-Way Harmony, and Sphinx documentation. Three new endpoint classes are introduced (FormsEndpoint, ShipmentsEndpoint, PaymentsEndpoint) while timeline, notes, tracking, and parcel operations extend the existing JobsEndpoint.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pydantic>=2.0, pydantic-settings, requests, python-dotenv (unchanged from 001)
**Storage**: N/A (SDK — no local storage)
**Testing**: pytest with markers `@pytest.mark.live` / `@pytest.mark.mock`
**Target Platform**: Linux/macOS/Windows (Python package)
**Project Type**: Single package (`ab`)
**Performance Goals**: Same as 001 — 30s default timeout, exponential backoff retry on 429/502/503
**Constraints**: Zero regressions in feature 001 tests
**Scale/Scope**: ~62 new endpoints, ~25 new models, 3 new endpoint classes, extensions to 1 existing class

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | All new endpoints get typed models (RequestModel/ResponseModel). Forms return raw bytes (no model needed). |
| II. Fixture-Driven Development | PASS | Every JSON-returning endpoint gets a fixture. Binary form endpoints get content-type validation tests instead. |
| III. Four-Way Harmony | PASS | Each endpoint group gets implementation + fixture/test + example + Sphinx docs. |
| IV. Swagger-Informed, Reality-Validated | PASS | Models built from swagger + fixture validation. ACPortal swagger unreliable — fixtures are source of truth. |
| V. Mock Tracking & Transparency | PASS | All mock fixtures tracked in MOCKS.md with reason and status. |
| VI. Documentation Completeness | PASS | Sphinx docs with examples and model cross-references for every new endpoint. |
| VII. Flywheel Evolution | PASS | Feature driven by integration needs identified in stakeholder discussions. |

No violations. No complexity tracking needed.

## Project Structure

### Documentation (this feature)

```text
specs/002-extended-endpoints/
├── plan.md              # This file
├── research.md          # Phase 0: Design decisions referencing ABConnectTools
├── data-model.md        # Phase 1: Entity definitions for new models
├── quickstart.md        # Phase 1: Usage examples for new endpoint groups
├── contracts/
│   └── endpoints.md     # Phase 1: Full endpoint contract table
└── tasks.md             # Phase 2: Task breakdown (created by /speckit.tasks)
```

### Source Code (repository root)

```text
ab/
├── client.py                          # UPDATE: Register 3 new endpoint groups
├── api/
│   ├── endpoints/
│   │   ├── jobs.py                    # UPDATE: Add timeline, notes, tracking, parcel methods
│   │   ├── forms.py                   # NEW: 15 form generation methods
│   │   ├── shipments.py               # NEW: 14 shipment methods (job-scoped + global)
│   │   └── payments.py                # NEW: 10 payment methods
│   ├── models/
│   │   ├── __init__.py                # UPDATE: Re-export new models
│   │   ├── jobs.py                    # UPDATE: Add timeline, note, tracking, parcel models
│   │   ├── forms.py                   # NEW: FormsShipmentPlan model (only JSON-returning form)
│   │   ├── shipments.py               # NEW: RateQuote, Accessorial, ShipmentOriginDestination, etc.
│   │   └── payments.py                # NEW: PaymentInfo, PaymentSource, ACH models
│   └── endpoints/
│       └── __init__.py                # UPDATE: Export new endpoint classes

tests/
├── fixtures/                          # NEW: ~25 new fixture JSON files
├── models/                            # NEW: Fixture validation tests for new models
└── unit/                              # NEW: Mocked HTTP tests for new endpoints

examples/
├── forms.py                           # NEW: Form generation examples
├── shipments.py                       # NEW: Shipment workflow examples
├── payments.py                        # NEW: Payment processing examples
├── timeline.py                        # NEW: Job lifecycle examples
├── tracking.py                        # NEW: Shipment tracking examples
├── notes.py                           # NEW: Job notes examples
└── parcels.py                         # NEW: Parcel item examples

docs/
├── api/
│   ├── forms.md                       # NEW: Forms endpoint reference
│   ├── shipments.md                   # NEW: Shipments endpoint reference
│   ├── payments.md                    # NEW: Payments endpoint reference
│   └── jobs.md                        # UPDATE: Add timeline/notes/tracking/parcel sections
└── models/
    ├── forms.md                       # NEW: Form models reference
    ├── shipments.md                   # NEW: Shipment models reference
    └── payments.md                    # NEW: Payment models reference
```

**Structure Decision**: Follows the established flat layout from feature 001. New endpoint groups get their own files under `endpoints/` and `models/`. Operations that are conceptually "job sub-resources" (timeline, notes, tracking, parcels) extend the existing `JobsEndpoint` rather than creating separate classes, since they share the same `job_display_id` parameter pattern and are accessed through `api.jobs.*`.

## Endpoint Group Organization

| Group | Class | File | Methods | Rationale |
|-------|-------|------|---------|-----------|
| Timeline/Status | JobsEndpoint (extended) | jobs.py | 9 | Job sub-resource, shares job_display_id pattern |
| Shipments | ShipmentsEndpoint (new) | shipments.py | 14 | Large enough for own class; includes global non-job endpoints |
| Payments | PaymentsEndpoint (new) | payments.py | 10 | Financial operations warrant isolation for clarity |
| Forms | FormsEndpoint (new) | forms.py | 15 | 15 methods is too many to add to JobsEndpoint |
| Notes | JobsEndpoint (extended) | jobs.py | 4 | Small CRUD, natural job sub-resource |
| Tracking | JobsEndpoint (extended) | jobs.py | 2 | Only 2 methods (v1 + v3), job sub-resource |
| Items/Parcels | JobsEndpoint (extended) | jobs.py | 7 | Job sub-resource, shares job_display_id pattern |

## Implementation Order

Phase by user story priority, within each phase following the batch workflow (models → endpoints → fixtures → tests → docs → harmony check):

1. **P1: Timeline/Status** (9 endpoints) — JobsEndpoint extensions + new timeline models
2. **P2: Shipments + Tracking** (16 endpoints) — New ShipmentsEndpoint + tracking methods on JobsEndpoint
3. **P3: Payments** (10 endpoints) — New PaymentsEndpoint + payment models
4. **P4: Forms** (15 endpoints) — New FormsEndpoint + binary response handling
5. **P5: Notes + Items/Parcels** (12 endpoints) — JobsEndpoint extensions + note/parcel models
6. **Cross-cutting**: Client registration, MOCKS.md updates, swagger compliance test updates, example files, Sphinx docs
