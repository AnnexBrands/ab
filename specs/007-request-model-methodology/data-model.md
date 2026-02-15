# Data Model: Request Model Methodology

**Feature**: 007-request-model-methodology
**Date**: 2026-02-14

## Entities

### Route (Extended)

The existing `Route` dataclass gains one new field: `params_model`.

| Field | Type | Description |
|-------|------|-------------|
| method | str | HTTP method (GET, POST, PUT, DELETE, PATCH) |
| path | str | URL path template with `{param}` placeholders |
| request_model | Optional[str] | Name of Pydantic RequestModel for body validation |
| **params_model** | **Optional[str]** | **Name of Pydantic RequestModel for query param validation (NEW)** |
| response_model | Optional[str] | Name of Pydantic model (or `List[Model]`) for response casting |
| api_surface | str | Target API: `acportal`, `catalog`, or `abc` |
| _path_params | frozenset[str] | Extracted path parameter names (computed) |

**Relationships**: Route references model names as strings; models are resolved lazily via `_resolve_model()` in `BaseEndpoint`.

### RequestModel (Unchanged)

Base class for outbound request bodies and params models. No structural changes.

| Field | Type | Description |
|-------|------|-------------|
| (varies per subclass) | typed | Snake_case fields with camelCase aliases |

**Config**: `extra="forbid"`, `populate_by_name=True`, `alias_generator=_to_camel`

**Key method**: `check(data)` → validates via `model_validate()`, returns dict via `model_dump(by_alias=True, exclude_none=True, mode="json")`

### Request Fixture File

A JSON file representing a valid request payload for an endpoint.

| Attribute | Value |
|-----------|-------|
| Location | `tests/fixtures/requests/{RequestModelName}.json` |
| Format | JSON object with camelCase keys (matching API contract) |
| Naming | Matches the Pydantic model name exactly |
| Validation | Must pass `RequestModelName.model_validate(data)` |

### FIXTURES.md Tracking Entry

Each row in the unified tracking table represents one endpoint.

| Column | Type | Description |
|--------|------|-------------|
| Endpoint Path | str | API path (e.g., `/companies/search/v2`) |
| Method | str | HTTP method |
| Req Model | str or `—` | Request model name, or `—` if no body |
| Req Fixture | status | `captured`, `needs-data`, or `—` |
| Resp Model | str or `—` | Response model name |
| Resp Fixture | status | `captured`, `needs-data`, or `—` |
| Status | enum | `complete`, `partial`, `needs-request-data` |
| Notes | str | What's missing (actionable, per Principle V) |

**Status rules**:
- `complete`: All applicable dimensions have captured fixtures and defined models.
- `partial`: Some dimensions done, others in progress.
- `needs-request-data`: Example fails; notes specify what request data is missing.
- Dimensions that don't apply (e.g., no request body for a GET) show `—` and don't affect completeness.

## Relationships

```
Route ──references──▶ RequestModel (body, via request_model string)
Route ──references──▶ RequestModel (params, via params_model string)
Route ──references──▶ ResponseModel (via response_model string)

ExampleEntry ──captures──▶ Request Fixture (tests/fixtures/requests/)
ExampleEntry ──captures──▶ Response Fixture (tests/fixtures/)

FIXTURES.md ──tracks──▶ Route + all associated models and fixtures
```

## Validation Rules

1. `RequestModel` with `extra="forbid"` rejects unknown fields at construction.
2. `populate_by_name=True` allows both snake_case field names and camelCase aliases as input.
3. `check()` returns camelCase-keyed dict ready for HTTP transport.
4. Request fixture files must round-trip: `Model.model_validate(json.loads(fixture))` must succeed.
5. Params model validation follows the same path as body validation (via `check()`), but the result is passed as `params=` instead of `json=`.
