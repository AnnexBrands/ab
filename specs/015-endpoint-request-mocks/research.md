# Research: Endpoint Request Mocks

**Feature**: 015-endpoint-request-mocks
**Date**: 2026-02-22

## Decision 1: Fixture Generation Method

**Decision**: One-time script that introspects all Route definitions, resolves model classes, and writes null-populated JSON files.

**Rationale**: The SDK already has `ab.api.models` with all request/params models exported. Each model's `model_json_schema()` provides field names and aliases. A script can iterate all endpoint files, extract Route definitions, resolve model classes, and write `{ModelName}.json` with all fields set to `null`. This is deterministic and repeatable.

**Alternatives considered**:
- Manual creation: Error-prone with 82 models. Rejected.
- pytest fixture factory: Would run at test time. Rejected — we want files on disk for developer visibility.
- Pydantic `model_construct()` with None defaults: Generates Python objects, not JSON files. Would need serialization. More complex than direct schema-based generation.

## Decision 2: Fixture JSON Key Format

**Decision**: Use model field aliases (camelCase) as JSON keys, matching the API wire format.

**Rationale**: Existing fixtures (`CompanySearchRequest.json`) use camelCase keys (`searchText`, `pageSize`). The `BaseEndpoint._request()` method calls `model_cls.check(body)` which handles both camelCase and snake_case via `populate_by_name=True`. Using camelCase maintains consistency with response fixtures and the API.

**Alternatives considered**:
- snake_case keys: Would work via `populate_by_name`, but inconsistent with existing request fixture and all response fixtures. Rejected.
- Both formats: Redundant. Rejected.

## Decision 3: How Examples Consume Request Fixtures

**Decision**: Modify `ExampleRunner._run_entry()` to load request fixture and pass values as kwargs when `request_fixture_file` is set. The lambda call pattern changes from `lambda api: api.addr.validate(line1="X")` to a fixture-driven call.

**Rationale**: `ExampleEntry` already has `request_fixture_file` field (defined but never used). The fixture loading infrastructure (`load_fixture()`) exists. The only missing piece is wiring `_run_entry()` to load the fixture and inject it into the endpoint call. For params_model fixtures (GET endpoints), the values become `**kwargs`. For request_model fixtures (POST endpoints), the values become the `data` or `json` body.

**Alternatives considered**:
- Global fixture registry: Over-engineered for this use case. Rejected.
- New ExampleRunner subclass: Unnecessary complexity. Rejected.

## Decision 4: How Tests Consume Request Fixtures

**Decision**: Use existing `require_fixture()` from conftest to load request fixtures by model name from `tests/fixtures/requests/`. Integration tests call `require_fixture("AddressValidateParams", required=True)` and use the returned dict as kwargs.

**Rationale**: The fixture loading infrastructure already supports custom paths via `_resolve_fixture_path()`. Adding the `requests/` subdirectory to the resolution chain is minimal work. `require_fixture(required=True)` will fail loudly if the fixture is missing, which aligns with the fail-first pattern.

**Alternatives considered**:
- Separate `load_request_fixture()` function: Creates API surface bloat. `load_fixture()` with path awareness is sufficient. Rejected.
- Parametrized test fixtures: Good for future but out of scope for this feature. Deferred.

## Decision 5: Scope of Model Tightening

**Decision**: Tighten models where API-required fields are incorrectly marked Optional. Start with `AddressValidateParams` (already done in clarification), then apply the same pattern to other models where swagger or API behavior clearly indicates required fields.

**Rationale**: Constitution Principle IX mandates that required swagger query parameters SHOULD be required Python arguments. The fail-first pattern only works when models accurately reflect API requirements. Models with all-Optional fields will pass validation with null fixtures, defeating the purpose.

**Alternatives considered**:
- Tighten all models in one pass: Risk of regressions. Start conservative with address, expand incrementally. Rejected as initial approach.
- Leave models Optional and validate at API level: Defeats the offline validation purpose. Rejected.

## Decision 6: Fixture Count and Scope

**Decision**: Generate fixtures for all 82 unique request/params models referenced by Routes. Preserve the 1 existing fixture (`CompanySearchRequest.json`).

**Findings**:
- 37 unique params_model names (GET query params)
- ~49 unique request_model names (POST/PUT bodies)
- Some overlap where models are shared (e.g., `DashboardCompanyParams` used by 5 routes)
- 1 existing fixture to preserve
- ~81 new fixtures to generate

## Decision 7: Existing Infrastructure Reuse

**Decision**: Maximize reuse of existing infrastructure — no new frameworks or patterns needed.

**Available infrastructure**:
| Component | Location | Reuse |
|---|---|---|
| `load_fixture()` | `tests/conftest.py` | Load request fixtures |
| `require_fixture()` | `tests/conftest.py` | Test fixture loading with skip/fail |
| `_resolve_fixture_path()` | `tests/conftest.py` | Needs `requests/` subdir support |
| `test_request_fixtures.py` | `tests/models/` | Already auto-discovers and validates request fixtures |
| `ExampleEntry.request_fixture_file` | `examples/_runner.py` | Already defined, needs wiring |
| `BaseEndpoint._request()` validation | `ab/api/base.py` | Already validates via `model_cls.check()` |
| `RequestModel.check()` | `ab/api/models/base.py` | Handles camelCase/snake_case conversion |
