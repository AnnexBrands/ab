# Implementation Plan: Extended Operations Endpoints

**Branch**: `008-extended-operations` | **Date**: 2026-02-14 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/008-extended-operations/spec.md`

## Summary

Extend the ABConnect SDK with ~106 MEDIUM-priority ACPortal endpoints covering operational workflows: RFQ lifecycle, job on-hold management, reports, email/SMS communication, extended lookups, commodities, dashboard, views, extended company/contact operations, global notes, partners, and freight providers. All endpoints follow the established Route/BaseEndpoint/Pydantic model architecture from features 001, 002, and 007.

## Technical Context

**Language/Version**: Python 3.11+ (unchanged from 001)
**Primary Dependencies**: pydantic>=2.0, pydantic-settings, requests, python-dotenv (unchanged from 001)
**Storage**: N/A (SDK — no local storage)
**Testing**: pytest + ruff
**Target Platform**: Python SDK (pip install ab)
**Project Type**: single (Python package)
**Performance Goals**: N/A (SDK wraps HTTP calls — performance governed by API latency)
**Constraints**: Follow established patterns from features 001/002/007 — Route, BaseEndpoint, RequestModel/ResponseModel, `**kwargs` signatures, DISCOVER workflow
**Scale/Scope**: ~106 new endpoints across 14 functional groups, 8 new endpoint classes, 6 extended endpoint classes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | ✅ PASS | All new models inherit RequestModel/ResponseModel. snake_case fields, camelCase aliases, extra="forbid"/"allow". |
| II. Example-Driven Fixture Capture | ✅ PASS | Every endpoint gets a runnable example. Fixtures captured from staging, not fabricated. |
| III. Four-Way Harmony | ✅ PASS | Each endpoint: implementation + example + fixture/test + Sphinx docs. |
| IV. Swagger-Informed, Reality-Validated | ✅ PASS | Models from swagger, validated by fixtures. Swagger compliance tests updated. |
| V. Endpoint Status Tracking | ✅ PASS | FIXTURES.md updated with unified 4D format for all new endpoints. |
| VI. Documentation Completeness | ✅ PASS | Sphinx docs with code examples, model cross-references for all new groups. |
| VII. Flywheel Evolution | ✅ PASS | Feature driven by gap analysis, extends SDK coverage per stakeholder priorities. |
| VIII. Phase-Based Context Recovery | ✅ PASS | DISCOVER workflow with committed checkpoints per phase. |
| IX. Endpoint Input Validation | ✅ PASS | RequestModel extra="forbid" validates outbound bodies. params_model on Routes for query param validation. |

**No violations. No complexity tracking needed.**

## Project Structure

### Documentation (this feature)

```text
specs/008-extended-operations/
├── plan.md              # This file
├── research.md          # Phase 0 — design decisions vs ABConnectTools
├── data-model.md        # Phase 1 — entity catalog with fields
├── quickstart.md        # Phase 1 — developer quick-reference
├── contracts/           # Phase 1 — SDK interface contracts
│   └── endpoints.md     # Method signatures for all 106 endpoints
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 (/speckit.tasks output)
```

### Source Code (repository root)

```text
ab/
├── api/
│   ├── endpoints/
│   │   ├── __init__.py          # UPDATED — register 8 new endpoint classes
│   │   ├── commodities.py       # NEW — 5 commodity CRUD + search
│   │   ├── commodity_maps.py    # NEW — 5 commodity map CRUD + search
│   │   ├── companies.py         # EXTENDED — 16 methods (brands, geo, carriers, packaging)
│   │   ├── contacts.py          # EXTENDED — 5 methods (history, merge)
│   │   ├── dashboard.py         # NEW — 9 dashboard + grid view state
│   │   ├── jobs.py              # EXTENDED — 22 methods (on-hold, email, SMS, freight)
│   │   ├── lookup.py            # EXTENDED — 12 methods (generic + named conveniences)
│   │   ├── notes.py             # NEW — 4 global note operations
│   │   ├── partners.py          # NEW — 3 partner operations
│   │   ├── reports.py           # NEW — 8 report generation
│   │   ├── rfq.py               # NEW — 7 standalone RFQ lifecycle (+ 2 job-scoped in jobs.py)
│   │   └── views.py             # NEW — 8 saved view management
│   ├── models/
│   │   ├── __init__.py          # UPDATED — re-export all new models
│   │   ├── commodities.py       # NEW — Commodity, CommodityMap, request models
│   │   ├── companies.py         # EXTENDED — brand, geo, carrier, packaging models
│   │   ├── contacts.py          # EXTENDED — history, merge models
│   │   ├── dashboard.py         # NEW — dashboard summary, grid view models
│   │   ├── jobs.py              # EXTENDED — on-hold, email, SMS, freight models
│   │   ├── lookup.py            # EXTENDED — generic lookup value, convenience types
│   │   ├── notes.py             # NEW — global note models
│   │   ├── partners.py          # NEW — partner models
│   │   ├── reports.py           # NEW — report request/response models
│   │   ├── rfq.py               # NEW — RFQ display, status, accept models
│   │   └── views.py             # NEW — view config, access models
│   └── schemas/
│       └── acportal.json        # Reference (read-only)
├── client.py                    # UPDATED — register 8 new endpoint attributes

tests/
├── fixtures/                    # NEW fixture JSON files
│   └── requests/                # NEW request fixture JSON files
├── models/
│   ├── test_fixtures.py         # EXTENDED — new fixture validation tests
│   └── test_request_fixtures.py # EXTENDED — new request fixture tests
├── test_example_params.py       # EXTENDED — swagger param validation
└── test_swagger_compliance.py   # EXTENDED — updated endpoint count

examples/                        # NEW example files per endpoint group
docs/                            # NEW Sphinx RST files per endpoint group
```

**Structure Decision**: Single Python package (`ab/`). New endpoint groups get their own files (`rfq.py`, `reports.py`, etc.). Extensions to existing groups add methods to existing files. This is consistent with the project's established pattern. No new packages or directories needed beyond the existing structure.

## Implementation Strategy

### Batching Plan (DISCOVER workflow)

Work is organized into 7 batches following the user story priority order. Each batch completes all DISCOVER phases before the next begins:

| Batch | Group | New Endpoints | Files Modified/Created |
|-------|-------|---------------|----------------------|
| 1 | RFQ Lifecycle | 9 | `rfq.py`, `jobs.py` (2 job-scoped) |
| 2 | On-Hold Management | 10 | `jobs.py` (10 new methods) |
| 3 | Reports & Analytics | 8 | `reports.py` |
| 4 | Email & SMS | 8 | `jobs.py` (8 new methods) |
| 5 | Extended Lookups + Commodities | 22 | `lookup.py`, `commodities.py`, `commodity_maps.py` |
| 6 | Dashboard + Views | 17 | `dashboard.py`, `views.py` |
| 7 | Companies + Contacts + Freight + Notes + Partners | 32 | `companies.py`, `contacts.py`, `jobs.py` (4), `notes.py`, `partners.py` |

### Per-Batch DISCOVER Phases

1. **D (Determine)** — Research swagger + ABConnectTools for request bodies, params, test values
2. **I (Implement models)** — Pydantic models (ResponseModel + RequestModel) with skip-marked tests
3. **S (Scaffold endpoints)** — Route definitions + endpoint methods + client registration
4. **C (Call & Capture)** — Examples → staging → fixtures
5. **O (Observe tests)** — pytest + test_example_params.py + FIXTURES.md update
6. **V (Verify & commit)** — Checkpoint commit
7. **E (Enrich docs)** — Sphinx RST pages
8. **R (Release)** — PR ready

### Client Registration

New endpoint groups registered in `ab/client.py`:

```python
# New ACPortal endpoint groups
self.rfq = RFQEndpoint(self._acportal)
self.reports = ReportsEndpoint(self._acportal)
self.dashboard = DashboardEndpoint(self._acportal)
self.views = ViewsEndpoint(self._acportal)
self.commodities = CommoditiesEndpoint(self._acportal)
self.commodity_maps = CommodityMapsEndpoint(self._acportal)
self.notes = NotesEndpoint(self._acportal)
self.partners = PartnersEndpoint(self._acportal)
```

Extended endpoint groups (companies, contacts, jobs, lookup) already registered — methods added in-place.
