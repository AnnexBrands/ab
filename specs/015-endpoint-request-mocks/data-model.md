# Data Model: Endpoint Request Mocks

**Feature**: 015-endpoint-request-mocks
**Date**: 2026-02-22

## Entities

### Request Fixture File

A JSON file on disk representing input data for an API endpoint call.

**Location**: `tests/fixtures/requests/{ModelClassName}.json`
**Format**: JSON object with camelCase keys matching model field aliases
**Lifecycle**: null-populated (generated) → populated (developer fills real values)

| Field | Type | Description |
|---|---|---|
| (varies by model) | null | All model fields set to null initially |

**Identity**: Uniquely identified by model class name (filename)
**Validation**: Parsed by corresponding pydantic model class via `model_validate()`

### Params Model (existing)

Query parameter model for GET endpoints. Inherits from `RequestModel` (`extra="forbid"`).

**Examples**: `AddressValidateParams`, `JobSearchParams`, `DashboardParams`
**Count**: 37 unique models across all Routes
**Fixture naming**: `{ClassName}.json` (e.g., `AddressValidateParams.json`)

### Request Model (existing)

Request body model for POST/PUT endpoints. Inherits from `RequestModel` (`extra="forbid"`).

**Examples**: `CompanySearchRequest`, `JobCreateRequest`, `QuoteRequestModel`
**Count**: ~49 unique models across all Routes
**Fixture naming**: `{ClassName}.json` (e.g., `CompanySearchRequest.json`)

## Relationships

```
Route (1) ──references──> (0..1) params_model ──fixture──> (0..1) Request Fixture File
Route (1) ──references──> (0..1) request_model ──fixture──> (0..1) Request Fixture File
ExampleEntry (1) ──loads──> (0..1) Request Fixture File
Integration Test (1) ──loads──> (0..1) Request Fixture File
```

## Fixture Generation Rules

1. For each Route with `params_model` set: generate `tests/fixtures/requests/{params_model}.json`
2. For each Route with `request_model` set: generate `tests/fixtures/requests/{request_model}.json`
3. Deduplicate by model class name (multiple Routes may reference the same model)
4. Skip if file already exists with non-null content
5. All fields set to `null` using model's `model_json_schema()` for field names

## Model Field Tightening

Models where API-required fields are currently Optional must be updated:

| Model | Fields to Tighten | Rationale |
|---|---|---|
| `AddressValidateParams` | `line1`, `city`, `state`, `zip` | API requires all 4 for validation (already done) |
| (others TBD during implementation) | Per swagger/API investigation | Constitution Principle IX |

## Consumption Patterns

### GET Endpoints (params_model)

```
Fixture JSON → load as dict → unpack as **kwargs → endpoint method signature
→ method builds params dict → BaseEndpoint._request(route, params=dict(...))
→ _request() validates via params_model.check()
```

### POST/PUT Endpoints (request_model)

```
Fixture JSON → load as dict → pass as body → endpoint method
→ method passes to BaseEndpoint._request(route, json=body)
→ _request() validates via request_model.check()
```
