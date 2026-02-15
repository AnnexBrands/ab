# Research: Request Model Methodology

**Feature**: 007-request-model-methodology
**Date**: 2026-02-14

## R1. Endpoint Signature Pattern: `**kwargs` → `model_validate`

**Decision**: Endpoint methods that accept a request body change from `data: dict | Any` to `**kwargs: Any`. The existing `_request()` validation path (`route.request_model` → `model_cls.check(body)`) handles validation. Callers pass snake_case keyword arguments; the model's `check()` method internally calls `model_validate(kwargs)` then `model_dump(by_alias=True)` to produce camelCase JSON.

**Rationale**: This is the minimal change that achieves clean signatures. The `check()` classmethod already does `model_validate` → `model_dump(by_alias=True, exclude_none=True)`, so no new validation plumbing is needed. Callers get IDE autocomplete if type stubs are generated, and `extra="forbid"` on `RequestModel` catches typos at call time.

**Alternatives considered**:
- **Typed model parameter** (`def search(self, request: SearchRequest)`) — forces callers to construct model instances; more verbose than kwargs.
- **Validate in endpoint method** (explicit `Model.model_validate(kwargs)` per method) — duplicates validation logic already centralized in `_request()`.
- **Dual interface** (accept both dict and kwargs) — adds complexity without clear benefit; callers who have a dict can unpack it with `**my_dict`.

**Example — before**:
```python
def search(self, data: dict | Any) -> Any:
    return self._request(_SEARCH, json=data)
# Caller: api.companies.search({"searchText": "test", "pageSize": 25})
```

**Example — after**:
```python
def search(self, **kwargs: Any) -> Any:
    return self._request(_SEARCH, json=kwargs)
# Caller: api.companies.search(search_text="test", page_size=25)
```

The `_request()` method picks up `json=kwargs` and validates through `CompanySearchRequest.check(kwargs)` because `_SEARCH.request_model = "CompanySearchRequest"`.

---

## R2. Query/Path Params Model via Route Extension

**Decision**: Add an optional `params_model: Optional[str]` field to the `Route` dataclass. When present, `_request()` validates the `params=` dict through the resolved model's `check()` method, just like it does for `json=` bodies. Endpoint methods for GET endpoints with complex query params use the same `**kwargs` pattern.

**Rationale**: This keeps validation centralized in `_request()` and follows the same lazy-resolution pattern as `request_model` and `response_model`. GET endpoints with only simple path params (scalar IDs) don't need a params model — they continue using explicit named arguments and `route.bind()`.

**Alternatives considered**:
- **Validate in endpoint method only** — breaks consistency; body validation is centralized but params would be ad-hoc.
- **Merge params into request_model** — conflates body and query params, which are sent via different HTTP mechanisms (`json=` vs `params=`).

**Example**:
```python
_SEARCH = Route("GET", "/job/search", params_model="JobSearchParams", response_model="List[JobSimple]")

def search(self, **kwargs: Any) -> Any:
    return self._request(_SEARCH, params=kwargs)
```

In `_request()`:
```python
if "params" in kwargs and route.params_model:
    model_cls = self._resolve_model(route.params_model)
    kwargs["params"] = model_cls.check(kwargs["params"])
```

---

## R3. ParamsModel Base Class

**Decision**: Reuse `RequestModel` as the base class for params models. No separate `ParamsModel` base class needed.

**Rationale**: Query parameter validation has the same requirements as body validation: `extra="forbid"` catches unknown params, `populate_by_name=True` allows snake_case input, alias generation produces camelCase/PascalCase for the API. The only difference is serialization target (query string vs JSON body), but `check()` returns a dict in both cases — `requests` library handles query string encoding from a dict.

**Alternatives considered**:
- **Dedicated `ParamsModel` base class** — unnecessary abstraction; `RequestModel` already has the right config.
- **Plain dict without model** — no validation, defeats the purpose.

---

## R4. Request Fixture Storage

**Decision**: Store request fixtures in `tests/fixtures/requests/` as a separate subdirectory from response fixtures. Naming convention: `{RequestModelName}.json` (matching the response convention but namespaced by directory).

**Rationale**: Separating request and response fixtures avoids naming collisions (e.g., `CompanyDetails` could be both a request and response model). The `requests/` subdirectory is self-documenting and requires no changes to existing response fixture paths.

**Alternatives considered**:
- **Same directory with prefix** (e.g., `req_CompanyDetails.json`) — clutters the existing fixture directory.
- **Same directory, different names** — relies on models having unique names across request/response; fragile.

---

## R5. FIXTURES.md Format Update

**Decision**: Restructure FIXTURES.md into a single unified tracking table per API surface, with columns covering all four completeness dimensions. Replace the current two-section format (Captured / Needs Request Data) with a per-endpoint row showing:

| Endpoint | Method | Req Model | Req Fixture | Resp Model | Resp Fixture | Status | Notes |

Status values: `complete` (all applicable dimensions done), `partial` (some done), `needs-request-data` (existing meaning preserved).

**Rationale**: A unified table gives a single source of truth for endpoint completeness. The current two-section format splits information about the same endpoint across tables, making it hard to assess overall status. The new format aligns with the four-dimensional completeness entity defined in the spec.

**Alternatives considered**:
- **Add columns to existing tables** — would require merging the two sections anyway.
- **Separate request fixtures table** — splits endpoint info across three places instead of two; worse.

---

## R6. DISCOVER Workflow Updates

**Decision**: Update DISCOVER phases to include request model and fixture steps:

- **Phase D (Determine)**: Research request body schemas and query parameter definitions from swagger + ABConnectTools. Document required fields, types, and realistic test values for requests (not just responses).
- **Phase I (Implement Models)**: Create both request models (`RequestModel` subclasses) and response models. Add skeleton tests for request fixture validation (with `pytest.skip()`).
- **Phase S (Scaffold Endpoints)**: Use `**kwargs` signatures. Set `request_model` and `params_model` on Route definitions.
- **Phase C (Call & Capture)**: Capture request fixtures alongside response fixtures. Save request payloads to `tests/fixtures/requests/`.
- **Phase O (Observe Tests)**: Validate request fixtures against request models. Run `test_example_params.py`.
- **Phase V (Verify)**: Update FIXTURES.md with unified tracking format.

**Rationale**: Request models are a natural extension of each existing phase — no new phases needed, just expanded scope within each.

---

## R7. ExampleRunner Enhancement

**Decision**: Extend `ExampleRunner._save_fixture()` to also save request fixtures. When an example entry has `request_model` set and the call succeeds (200), capture the request payload alongside the response fixture.

**Rationale**: The example runner already tracks `request_model` as metadata on `ExampleEntry`. Extending it to save request fixtures makes capture automatic and consistent with response fixture capture.

**Implementation approach**: After a successful call, if `entry.request_model` is set, serialize the request kwargs (the arguments passed to the endpoint method) as the request fixture. This requires the example lambda to expose its arguments — which means the runner's `add()` method may need a `request_data` parameter for the example payload.

---

## R8. Backward Compatibility

**Decision**: The `**kwargs` pattern is a breaking change for callers who pass `data=dict`. Existing callers must switch from `api.companies.search({"key": "val"})` to `api.companies.search(key="val")` or `api.companies.search(**{"key": "val"})`.

**Rationale**: The spec explicitly requires clean signatures (FR-008: "callers pass keyword arguments directly"). A backward-compatible shim (`data: dict | None = None, **kwargs`) adds complexity and sends mixed signals about the intended API. Since the SDK is pre-1.0 and the feature 007 scope says "newly touched endpoints adopt the new pattern," the break is acceptable for endpoints being converted.

**Migration path**: Endpoints are converted incrementally as they are touched in feature 002+. Unconverted endpoints retain their current `data: dict | Any` signature until touched.

---

## ABConnectTools Departures

| ID | Departure | ABConnectTools Pattern | AB SDK Pattern | Rationale |
|----|-----------|----------------------|----------------|-----------|
| D7 | kwargs signature | `data: dict = None` explicit param | `**kwargs` → model_validate | Cleaner call site; IDE-friendly with type stubs |
| D8 | Params model on Route | No params_model; manual dict assembly in each method | `route.params_model` with centralized validation | Eliminates per-method boilerplate; consistent with body validation |
| D9 | Request fixture tracking | No fixture tracking | Unified FIXTURES.md with 4D completeness | Enables full endpoint status visibility |
| D10 | Request fixture storage | No request fixtures | `tests/fixtures/requests/{Model}.json` | Completes the testing pyramid for both input and output |
