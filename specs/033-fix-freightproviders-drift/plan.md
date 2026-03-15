# Implementation Plan: Fix FreightProviders Drift

**Branch**: `033-fix-freightproviders-drift` | **Date**: 2026-03-15 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/033-fix-freightproviders-drift/spec.md`

## Summary

The `PricedFreightProvider` response model has 3 stub fields but the live API returns 15+ fields (including nested `CarrierAccountInfo`), causing "extra fields not in model" warnings. The response fixture is an empty list `[]`, so tests skip trivially and quality gates pass falsely. Meanwhile `api-surface.md` says "AB done: 0 of 3" contradicting FIXTURES.md which says "complete". This feature expands all freight models to match swagger/live shapes, captures real fixtures, and reconciles all progress artifacts.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: Filesystem (fixture JSON files in `tests/fixtures/` and `tests/fixtures/requests/`)
**Testing**: pytest
**Target Platform**: Linux / cross-platform Python
**Project Type**: Library (SDK)
**Performance Goals**: N/A — model correctness, not throughput
**Constraints**: Models must match live API response shape; no fabricated fixtures (Constitution II)
**Scale/Scope**: 4 endpoints (3 freightproviders + 1 freightitems), 4 models to expand, 3 progress artifacts to reconcile

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | VIOLATION (to fix) | `PricedFreightProvider` has 3 stub fields vs 15+ real fields; request models have 1 stub field each |
| II. Example-Driven Fixture Capture | VIOLATION (to fix) | Fixture is `[]` — no real data captured; request fixtures all null |
| III. Four-Way Harmony | VIOLATION (to fix) | Model incomplete, fixture empty, tests skip, docs show stub fields |
| IV. Swagger-Informed, Reality-Validated | VIOLATION (to fix) | Swagger defines 15 response fields + 22 request fields; models ignore them |
| V. Endpoint Status Tracking | VIOLATION (to fix) | FIXTURES.md says "complete" but gates pass trivially; api-surface.md says 0/3 done |
| VI. Documentation Completeness | VIOLATION (to fix) | Sphinx docs reflect only stub fields |
| VII. Flywheel Evolution | PASS | This feature is a direct result of runtime observation |
| VIII. Phase-Based Context Recovery | PASS | Will follow DISCOVER workflow |
| IX. Endpoint Input Validation | VIOLATION (to fix) | `ShipmentPlanProvider` uses `dict` instead of typed fields; `extra="forbid"` can't catch bad fields |

**Gate result**: 6 violations — all are the *target* of this feature. No violations are introduced; all are being resolved.

## Project Structure

### Documentation (this feature)

```text
specs/033-fix-freightproviders-drift/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
ab/api/models/jobs.py            # PricedFreightProvider, ShipmentPlanProvider, RateQuoteRequest, FreightItemsRequest, CarrierAccountInfo, CarrierAPI
ab/api/endpoints/jobs.py         # list_freight_providers, save_freight_providers, get_freight_provider_rate_quote, add_freight_items
tests/fixtures/PricedFreightProvider.json   # Response fixture (currently [])
tests/fixtures/requests/ShipmentPlanProvider.json  # Request fixture
tests/fixtures/requests/RateQuoteRequest.json      # Request fixture (currently missing)
tests/fixtures/requests/FreightProvidersParams.json # Query params fixture
tests/fixtures/requests/FreightItemsRequest.json    # Request fixture
tests/models/test_freight_models.py  # Model validation tests
examples/freight_providers.py        # Runnable example
specs/api-surface.md                 # "AB done" counter
FIXTURES.md                          # Gate tracking
html/progress.html                   # Generated report
docs/                                # Sphinx docs
```

**Structure Decision**: Existing SDK structure — all changes are modifications to existing files, no new directories needed.

## Complexity Tracking

No violations to justify — this feature reduces complexity by replacing `dict` stubs with typed models.
