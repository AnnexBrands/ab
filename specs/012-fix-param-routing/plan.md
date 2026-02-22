# Implementation Plan: Fix Parameter Routing

**Branch**: `012-fix-param-routing` | **Date**: 2026-02-21 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/012-fix-param-routing/spec.md`

## Summary

The SDK routes caller arguments to the wrong HTTP transport for some endpoints (query params sent incorrectly, no validation on query param names). This feature activates the existing but unused `params_model` infrastructure on `Route` to validate and alias query parameters through Pydantic models — the same pattern already used for request bodies. Additionally, a new G5 quality gate tracks parameter routing completeness in the progress HTML report.

**Core approach** (from research): No new framework needed. The `BaseEndpoint._request()` method already validates `params_model` when declared on a Route (base.py:69-74). The work is: (1) define params models, (2) add `params_model=` to Routes, (3) simplify endpoint methods, (4) add G5 gate.

## Technical Context

**Language/Version**: Python 3.11+ (existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: Filesystem (fixture JSON files in `tests/fixtures/`, generated Markdown/HTML)
**Testing**: pytest (existing `tests/test_example_params.py` extended, model tests added)
**Target Platform**: Python SDK library (pip-installable package)
**Project Type**: Single project (SDK library)
**Performance Goals**: N/A — validation adds microseconds per call, negligible vs network latency
**Constraints**: Must not break existing caller code; `**kwargs` interface is backward-compatible
**Scale/Scope**: 263 endpoint methods across 23 files; 5 manual-dict methods to refactor (Tier 1), 12 kwargs-params methods to add models (Tier 2), 62 kwargs-json without request_model (Tier 3)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
| --------- | ------ | ----- |
| I. Pydantic Model Fidelity | PASS | New params models inherit RequestModel (extra="forbid"), use snake_case fields with explicit aliases |
| II. Example-Driven Fixture Capture | PASS | No new examples needed — params models don't change response fixtures |
| III. Four-Way Harmony | PASS | Implementation + models change; existing examples/tests/docs updated accordingly |
| IV. Swagger-Informed, Reality-Validated | PASS | Params models derived from swagger param definitions; aliases match swagger names |
| V. Endpoint Status Tracking | PASS | FIXTURES.md gains G5 column tracking param routing completeness |
| VI. Documentation Completeness | PASS | Sphinx docs updated for new params model classes |
| VII. Flywheel Evolution | PASS | Addresses stakeholder-reported bug (address.validate failure) |
| VIII. Phase-Based Context Recovery | PASS | Three tiers provide natural checkpoints; each tier independently committable |
| IX. Endpoint Input Validation | PASS | **Primary alignment** — this feature directly implements Principle IX by adding params_model validation to endpoints that currently lack it |

**Post-Phase 1 re-check**: Design aligns. The params_model pattern is the same pattern prescribed by Principle IX and already built into the Route/BaseEndpoint infrastructure.

## Project Structure

### Documentation (this feature)

```text
specs/012-fix-param-routing/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0: pattern audit, alias strategy, gate design
├── data-model.md        # Phase 1: params model definitions, gate status extension
├── quickstart.md        # Phase 1: before/after examples, transport reference
├── contracts/           # Phase 1: internal SDK contracts
│   └── internal-contracts.md
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (via /speckit.tasks)
```

### Source Code (repository root)

```text
ab/
├── api/
│   ├── base.py              # No changes needed (_request already supports params_model)
│   ├── route.py             # No changes needed (params_model field already exists)
│   ├── endpoints/
│   │   ├── address.py       # Tier 1: refactor manual-dict → params= **kwargs
│   │   ├── forms.py         # Tier 1: refactor manual-dict → params= **kwargs
│   │   ├── documents.py     # Tier 1: refactor manual-dict → params= **kwargs
│   │   ├── companies.py     # Tier 2: add params_model to Routes for 3 query endpoints
│   │   ├── dashboard.py     # Tier 2: add params_model to Route for get()
│   │   ├── jobs.py          # Tier 2: add params_model to Routes for 3 query endpoints
│   │   ├── notes.py         # Tier 2: add params_model to Routes for 2 query endpoints
│   │   ├── shipments.py     # Tier 2: add params_model to Route for get_shipment()
│   │   └── web2lead.py      # Tier 2: add params_model to Route for get()
│   └── models/
│       ├── __init__.py      # Export new params models
│       ├── address.py       # Add AddressValidateParams, AddressPropertyTypeParams
│       ├── forms.py         # Add BillOfLadingParams, OperationsFormParams
│       ├── documents.py     # Add DocumentListParams
│       ├── companies.py     # Add params models for geo/carrier/suggest endpoints
│       ├── dashboard.py     # Add DashboardParams
│       ├── jobs.py          # Add params models for search/notes/freight endpoints
│       ├── notes.py         # Add NotesListParams, NotesSuggestUsersParams
│       ├── shipments.py     # Add ShipmentParams
│       └── web2lead.py      # Add Web2LeadGetParams
└── progress/
    ├── gates.py             # Add evaluate_g5() function
    ├── models.py            # Add g5_param_routing to EndpointGateStatus
    ├── renderer.py          # Add G5 column to HTML report
    └── fixtures_generator.py # Add G5 column to FIXTURES.md output

tests/
├── models/
│   └── test_params_models.py  # Unit tests for new params models
└── test_example_params.py     # Extended to verify params_model presence on Routes
```

**Structure Decision**: Existing single-project layout. All changes are within the established `ab/` and `tests/` directories. No new top-level directories.

## Complexity Tracking

No constitution violations. The design uses existing infrastructure (RequestModel base, Route.params_model field, BaseEndpoint._request validation hook) with zero new abstractions.
