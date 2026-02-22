# Data Model: Progress Report

**Feature**: 003-progress-report
**Date**: 2026-02-14

These are internal dataclasses used by the generator script, not SDK API models. They do not inherit from `ABConnectBaseModel`.

## Entities

### Endpoint

Represents a single API route extracted from `specs/api-surface.md`.

| Field | Type | Description |
|-------|------|-------------|
| group_name | str | Endpoint group name (e.g., "Companies", "Job — Timeline") |
| api_surface | str | API surface: "ACPortal", "Catalog", or "ABC" |
| index | int | Row number within the group table |
| route_key | str | Route identifier (e.g., "GET_FULLDETAILS") |
| method | str | HTTP method (GET, POST, PUT, DELETE, PATCH) |
| path | str | API endpoint path (e.g., "/companies/{companyId}/fulldetails") |
| response_model | str | Expected response model name (e.g., "CompanyDetails") |
| ab_status | str | Implementation status: "done", "pending", or "not_started" (from `—` in source) |
| ref_status | str | ABConnectTools reference: "JSON", "PDF", or "none" (from `—` in source) |

### EndpointGroup

Aggregates endpoints by group with summary metadata.

| Field | Type | Description |
|-------|------|-------------|
| name | str | Group name (e.g., "Companies") |
| api_surface | str | API surface |
| endpoints | list[Endpoint] | All endpoints in this group |
| total | int | Total endpoint count |
| done | int | Count with ab_status == "done" |
| pending | int | Count with ab_status == "pending" |
| not_started | int | Count with ab_status == "not_started" |
| ab_file | str or None | Path to AB endpoint file (e.g., "endpoints/companies.py") |
| ref_file | str or None | ABConnectTools file reference |
| priority | str or None | Priority label (e.g., "Low", "Medium") |

### Fixture

Represents a fixture entry from `FIXTURES.md`.

| Field | Type | Description |
|-------|------|-------------|
| endpoint_path | str | API endpoint path |
| method | str | HTTP method |
| model_name | str | Pydantic model name / fixture filename stem |
| status | str | "captured" or "pending" |
| capture_date | str or None | Date captured (captured only) |
| source | str or None | "staging", "production", or "legacy-validated" (captured only) |
| capture_instructions | str or None | SDK method call (pending only) |
| blocker | str or None | Reason fixture can't be captured yet (pending only) |
| ref | str or None | ABConnectTools fixture reference |

### Constant

Represents a test constant from `tests/constants.py`.

| Field | Type | Description |
|-------|------|-------------|
| name | str | Constant name (e.g., "TEST_COMPANY_UUID") |
| value | str | String representation of the value |
| value_type | str | Inferred type: "uuid", "int", "str" |

### ActionItem

Enriched view of an unimplemented endpoint, ready for rendering.

| Field | Type | Description |
|-------|------|-------------|
| endpoint | Endpoint | The endpoint record |
| tier | int | 1 = scaffolded (needs fixture), 2 = not started (needs implementation) |
| fixture | Fixture or None | Matching fixture record from FIXTURES.md |
| fixture_exists | bool | Whether the fixture file exists on disk |
| blocker_type | str | "capture", "constant_needed", "env_blocked", "not_implemented" |
| instructions | list[str] | Ordered step-by-step instructions for the reviewer |
| required_constants | list[str] | Constants needed (may already exist) |
| missing_constants | list[str] | Constants needed that don't exist in constants.py |

## Relationships

```text
EndpointGroup 1──* Endpoint
Endpoint 1──0..1 Fixture       (matched by endpoint_path + method)
Endpoint 1──0..1 ActionItem    (created for non-done endpoints only)
ActionItem *──* Constant       (path parameters determine required constants)
```

## Status Classification Logic

An endpoint's `blocker_type` is determined by:

1. `ab_status == "not_started"` AND no fixture record → `"not_implemented"`
2. `ab_status == "pending"` AND fixture has blocker containing "no * data in staging" → `"env_blocked"`
3. `ab_status == "pending"` AND path has unresolved `{param}` AND required constant missing → `"constant_needed"`
4. `ab_status == "pending"` AND fixture file missing → `"capture"`
