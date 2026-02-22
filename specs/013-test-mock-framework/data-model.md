# Data Model: Unified Test Mock Framework

**Feature**: 013-test-mock-framework
**Date**: 2026-02-21

## Entities

### TestConstants (Expanded)

**Location**: `tests/constants.py`
**Purpose**: Single source of truth for all test entity identifiers.

| Field | Type | Value | Source | Description |
|-------|------|-------|--------|-------------|
| TEST_COMPANY_UUID | str | `"93179b52-3da9-e311-b6f8-000c298b59ee"` | Staging | Existing — company with populated details |
| TEST_CONTACT_ID | int | `30760` | Staging | Existing — contact with detailed info |
| TEST_USER_CONTACT_ID | int | `1271` | Staging | Existing — contact linked to test user |
| TEST_JOB_DISPLAY_ID | int | `2000000` | Staging | Existing — job with shipments, documents, timeline |
| TEST_SELLER_ID | int | `1` | Staging | Existing — seller with expanded details |
| TEST_CATALOG_ID | int | `1` | Staging | Existing — catalog with lots |
| TEST_COMPANY_CODE | str | `"14004OH"` | Staging | Existing — company code for lookup |

**Rules**:
- All consumers (tests, examples, docs) MUST import from this module
- No duplicate definitions allowed outside this file
- New constants added with a docstring comment indicating source

### Fixture Directory Structure

**Location**: `tests/fixtures/`

```
tests/fixtures/
├── *.json               # Live-captured fixtures (Tier 2 source of truth)
├── requests/            # Request model fixtures
│   └── *.json
└── mocks/               # Manually-authored mock fixtures (Tier 3)
    └── *.json           # Same ModelName.json naming convention
```

**Precedence Rules**:
1. `tests/fixtures/{Model}.json` (live) — always wins
2. `tests/fixtures/mocks/{Model}.json` (mock) — fallback when no live fixture
3. Neither exists — test skips with actionable message

**Naming Convention**: `{ModelClassName}.json` (PascalCase, matching Pydantic model class name)
**Variant Convention**: `{ModelClassName}_{variant}.json` (e.g., `SellerExpandedDto_detail.json`)

### Models Requiring Fixes

#### Missing Fields (add to existing models)

| Model | File | Missing Fields Count | Source for Field Definitions |
|-------|------|---------------------|------------------------------|
| CompanyDetails | `ab/api/models/companies.py` | 97 | Live fixture + server source |
| ContactSimple | `ab/api/models/contacts.py` | 30 | Live fixture + server source |
| CatalogExpandedDto | `ab/api/models/catalog.py` | 6 | Live fixture: agent, customerCatalogId, endDate, isCompleted, lots, startDate |
| LotDto | `ab/api/models/lots.py` | 4 | Live fixture: catalogs, imageLinks, initialData, overridenData |
| CompanySimple | `ab/api/models/companies.py` | 2 | Live fixture: companyName, typeId |

#### Type Mismatches (redesign model)

| Model | File | Current Shape | Actual API Shape | Fix |
|-------|------|---------------|------------------|-----|
| PropertyType | `ab/api/models/address.py` | `{propertyType: str, confidence: float}` | `int` (raw integer) | Change endpoint return type or wrap int |
| UserRole | `ab/api/models/users.py` | `{id: str, name: str}` | `str` (plain string) | Change to `List[str]` response or add string validator |

#### HTTP 404 Failures (endpoint path issues)

| Endpoint | File | Error | Resolution |
|----------|------|-------|------------|
| documents.list | `ab/api/endpoints/documents.py` | HTTP 404 | Verify path against server source; provide mock fixture |
| jobs.search | `ab/api/endpoints/jobs.py` | HTTP 404 | Verify path against server source; provide mock fixture |
| jobs.search_by_details | `ab/api/endpoints/jobs.py` | HTTP 404 | Verify path against server source; provide mock fixture |

### Params Models Needed (32 xfail resolutions)

Routes needing `params_model` classes, grouped by endpoint file:

| Endpoint File | Routes Needing params_model | Count |
|---------------|----------------------------|-------|
| `catalog.py` | _LIST | 1 |
| `companies.py` | _GET_GLOBAL_GEO_SETTINGS, _GET_INHERITED_PACKAGING_TARIFFS, _GET_INHERITED_PACKAGING_LABOR | 3 |
| `contacts.py` | _UPDATE_DETAILS, _CREATE, _GET_HISTORY_AGGREGATED, _GET_HISTORY_GRAPH_DATA | 4 |
| `dashboard.py` | _GET_GRID_VIEWS, _INBOUND, _IN_HOUSE, _OUTBOUND, _LOCAL_DELIVERIES, _RECENT_ESTIMATES | 6 |
| `forms.py` | _GET_INVOICE, _GET_PACKAGING_LABELS, _GET_USAR | 3 |
| `jobs.py` | _POST_TIMELINE, _GET_TRACKING_V3, _GET_NOTES, _LIST_RFQS | 4 |
| `lookup.py` | _ITEMS, _DOCUMENT_TYPES, _DENSITY_CLASS_MAP | 3 |
| `lots.py` | _LIST | 1 |
| `partners.py` | _LIST | 1 |
| `payments.py` | _GET_PAYMENT | 1 |
| `rfq.py` | _GET_FOR_JOB, _ACCEPT_WINNER | 2 |
| `sellers.py` | _LIST | 1 |
| `shipments.py` | _GET_RATE_QUOTES, _GET_SHIPMENT_DOCUMENT | 2 |
| **Total** | | **32** |

## Relationships

```
TestConstants ──imports──> tests/models/*.py
TestConstants ──imports──> tests/integration/*.py
TestConstants ──imports──> examples/*.py

load_fixture() ──reads──> tests/fixtures/{Model}.json (primary)
load_fixture() ──reads──> tests/fixtures/mocks/{Model}.json (fallback)

G2 gate ──checks──> tests/fixtures/{Model}.json (primary)
G2 gate ──checks──> tests/fixtures/mocks/{Model}.json (fallback)

test_mock_coverage.py ──validates──> FIXTURES.md ↔ tests/fixtures/ + tests/fixtures/mocks/
```
