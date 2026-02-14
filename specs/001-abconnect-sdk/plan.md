# Implementation Plan: ABConnect API SDK

**Branch**: `001-abconnect-sdk` | **Date**: 2026-02-13 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-abconnect-sdk/spec.md`

## Summary

Build a clean-room Python SDK (`ab` package) for three ABConnect API
surfaces (ACPortal, Catalog, ABC) with 59 core endpoints. Every
endpoint produces a validated Pydantic model response with
fixture-driven correctness guarantees. The SDK supports dual auth
modes (standalone FileTokenStorage + Django SessionTokenStorage) and
routes requests to the correct API base URL transparently.

Key architectural improvements over ABConnectTools (reference only):
immutable Routes, split Request/Response model configs, instance-level
handler injection, unified HTTP client with connection pooling, typed
configuration via pydantic-settings, and timeouts with retry logic.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pydantic>=2.0, pydantic-settings, requests, python-dotenv
**Storage**: File system (token cache in `~/.cache/ab/`), JSON fixtures in `tests/fixtures/`
**Testing**: pytest with `@pytest.mark.mock` and `@pytest.mark.live` markers
**Target Platform**: Any (Python library/SDK — no platform-specific code)
**Project Type**: Single project (Python package)
**Performance Goals**: SDK overhead < 50ms per call; network latency dominates
**Constraints**: Must coexist with ABConnectTools (independent package). No code copied. Default timeout 30s. Retry transient errors (429, 502, 503) with exponential backoff (max 3 attempts).
**Scale/Scope**: 59 core endpoints across 3 API surfaces. ~35 Pydantic models. ~31 fixture files (one per distinct response model).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|-----------|------|--------|
| I. Pydantic Model Fidelity | All models inherit ABConnectBaseModel; RequestModel (extra="forbid") for strict outbound / ResponseModel (extra="allow" + logger.warning) for resilient inbound with drift visibility; mixin inheritance for shared fields | PASS |
| II. Fixture-Driven Development | Every endpoint gets a fixture in `tests/fixtures/`; mock fixtures tracked in `MOCKS.md` | PASS |
| III. Four-Way Harmony | Implementation + Test/Fixture + Example + Sphinx Docs required per endpoint | PASS |
| IV. Swagger-Informed, Reality-Validated | Swagger specs bundled in `ab/api/schemas/`; models validated against fixtures, deviations documented | PASS |
| V. Mock Tracking | `MOCKS.md` at repo root; pytest markers distinguish mock/live; 35 endpoints need fixtures without swagger schemas | PASS |
| VI. Documentation Completeness | Sphinx + RTD theme + MyST; every endpoint/model gets docs with examples and cross-refs | PASS |

**Post-Phase 1 re-check**: All gates still PASS. No violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/001-abconnect-sdk/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 research decisions
├── data-model.md        # Entity model definitions
├── quickstart.md        # Usage guide
├── contracts/
│   └── endpoints.md     # Core endpoint contracts (59 endpoints)
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
ab/
├── __init__.py              # Public API: ABConnectAPI, models
├── client.py                # ABConnectAPI orchestrator
├── config.py                # pydantic-settings typed config
├── exceptions.py            # ABConnectError, AuthenticationError, RequestError
├── http.py                  # HttpClient (requests.Session wrapper)
├── cache.py                 # CodeResolver (code-to-UUID cache, FR-012)
├── auth/
│   ├── __init__.py          # TokenStorage ABC export
│   ├── base.py              # TokenStorage abstract base
│   ├── file.py              # FileTokenStorage (standalone)
│   └── session.py           # SessionTokenStorage (Django)
├── api/
│   ├── __init__.py          # Endpoint group exports
│   ├── route.py             # Frozen Route dataclass with bind()
│   ├── base.py              # BaseEndpoint (instance-level handler)
│   ├── endpoints/
│   │   ├── __init__.py
│   │   ├── companies.py     # CompaniesEndpoint (8 routes)
│   │   ├── contacts.py      # ContactsEndpoint (7 routes)
│   │   ├── jobs.py          # JobsEndpoint (8 routes)
│   │   ├── documents.py     # DocumentsEndpoint (4 routes)
│   │   ├── address.py       # AddressEndpoint (2 routes)
│   │   ├── lookup.py        # LookupEndpoint (4 routes)
│   │   ├── users.py         # UsersEndpoint (4 routes)
│   │   ├── catalog.py       # CatalogEndpoint (6 routes)
│   │   ├── lots.py          # LotsEndpoint (6 routes)
│   │   ├── sellers.py       # SellersEndpoint (5 routes)
│   │   ├── autoprice.py     # AutoPriceEndpoint (2 routes)
│   │   └── web2lead.py      # Web2LeadEndpoint (2 routes)
│   ├── models/
│   │   ├── __init__.py      # Re-exports all models
│   │   ├── base.py          # ABConnectBaseModel, RequestModel, ResponseModel
│   │   ├── mixins.py        # IdentifiedModel, TimestampedModel, etc.
│   │   ├── shared.py        # ServiceBaseResponse, PaginatedList
│   │   ├── enums.py         # DocumentType, CarrierAPI, etc.
│   │   ├── companies.py
│   │   ├── contacts.py
│   │   ├── jobs.py
│   │   ├── documents.py
│   │   ├── address.py
│   │   ├── lookup.py
│   │   ├── users.py
│   │   ├── catalog.py
│   │   ├── lots.py
│   │   ├── sellers.py
│   │   ├── autoprice.py
│   │   └── web2lead.py
│   └── schemas/
│       ├── acportal.json    # Swagger spec (reference)
│       ├── catalog.json
│       └── abc.json
├── py.typed                 # PEP 561 marker

tests/
├── conftest.py              # Session-scoped API fixture, fixture loader
├── constants.py             # Test IDs (UUIDs, display IDs, codes)
├── fixtures/                # JSON response fixtures ({ModelName}.json)
├── unit/                    # Mocked HTTP tests for client logic
│   ├── test_auth.py
│   ├── test_http.py
│   ├── test_config.py
│   └── test_route.py
├── integration/             # Live API tests (@pytest.mark.live)
│   ├── test_companies.py
│   ├── test_contacts.py
│   ├── test_jobs.py
│   ├── test_documents.py
│   ├── test_catalog.py
│   ├── test_lots.py
│   ├── test_sellers.py
│   ├── test_address.py
│   ├── test_lookup.py
│   ├── test_users.py
│   ├── test_autoprice.py
│   └── test_web2lead.py
├── models/                  # Fixture validation tests
│   ├── test_company_models.py
│   ├── test_contact_models.py
│   ├── test_job_models.py
│   ├── test_catalog_models.py
│   └── ...
└── swagger/                 # Swagger compliance tests
    └── test_coverage.py     # Alert on unimplemented endpoints

examples/
├── companies.py
├── contacts.py
├── jobs.py
├── documents.py
├── catalog.py
├── lots.py
├── sellers.py
├── autoprice.py
└── web2lead.py

docs/
├── conf.py                  # Sphinx config (RTD theme, MyST, autodoc)
├── index.md
├── quickstart.md
├── api/                     # Endpoint reference (auto-generated)
│   ├── companies.md
│   ├── contacts.md
│   ├── jobs.md
│   ├── catalog.md
│   └── ...
├── models/                  # Model reference (autodoc)
│   ├── base.md
│   ├── companies.md
│   └── ...
└── Makefile

pyproject.toml               # Build config, dependencies, pytest config
MOCKS.md                     # Mock fixture tracking
CLAUDE.md                    # Development guidance
README.md                    # Project documentation
```

**Structure Decision**: Single Python package (`ab/`) at the repository
root. Tests, examples, and docs are sibling directories. This matches
the standard Python package layout and is the simplest structure for a
library with no frontend or backend components.

## Complexity Tracking

No constitution violations. No complexity justifications needed.
