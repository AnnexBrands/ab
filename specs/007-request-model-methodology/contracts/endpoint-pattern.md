# Contract: Endpoint Method Pattern

**Feature**: 007-request-model-methodology
**Date**: 2026-02-14

This document defines the canonical patterns for endpoint method signatures in the AB SDK after feature 007.

## Pattern 1: POST/PUT/PATCH with Request Body

**Route definition**:
```python
_ACTION = Route(
    "POST", "/service/action",
    request_model="ActionRequest",
    response_model="ActionResponse",
)
```

**Endpoint method**:
```python
def action(self, **kwargs: Any) -> Any:
    """POST /service/action"""
    return self._request(_ACTION, json=kwargs)
```

**With path params**:
```python
_UPDATE = Route(
    "PUT", "/service/{itemId}",
    request_model="UpdateRequest",
    response_model="UpdateResponse",
)

def update(self, item_id: str, **kwargs: Any) -> Any:
    """PUT /service/{itemId}"""
    return self._request(_UPDATE.bind(itemId=item_id), json=kwargs)
```

**Validation flow**: `_request()` detects `json=kwargs` + `route.request_model` → resolves `ActionRequest` → calls `ActionRequest.check(kwargs)` → `model_validate(kwargs)` + `model_dump(by_alias=True)` → sends camelCase JSON.

## Pattern 2: GET with Complex Query Params

**Route definition**:
```python
_SEARCH = Route(
    "GET", "/service/search",
    params_model="SearchParams",
    response_model="List[SearchResult]",
)
```

**Endpoint method**:
```python
def search(self, **kwargs: Any) -> Any:
    """GET /service/search"""
    return self._request(_SEARCH, params=kwargs)
```

**Validation flow**: `_request()` detects `params=kwargs` + `route.params_model` → resolves `SearchParams` → calls `SearchParams.check(kwargs)` → `model_validate(kwargs)` + `model_dump(by_alias=True)` → sends validated query params.

## Pattern 3: GET with Simple Path Params Only

**Route definition**:
```python
_GET = Route("GET", "/service/{id}", response_model="ServiceItem")
```

**Endpoint method** (unchanged from current pattern):
```python
def get_by_id(self, item_id: str) -> Any:
    """GET /service/{id}"""
    return self._request(_GET.bind(id=item_id))
```

**No request model or params model needed** — simple scalar path params are explicit named arguments.

## Pattern 4: POST with Body + Path Params + Query Params

**Route definition**:
```python
_COMPLEX = Route(
    "POST", "/service/{parentId}/items",
    request_model="CreateItemRequest",
    params_model="CreateItemParams",
    response_model="ItemResponse",
)
```

**Endpoint method**:
```python
def create_item(self, parent_id: str, *, params: dict | None = None, **kwargs: Any) -> Any:
    """POST /service/{parentId}/items"""
    kw: dict[str, Any] = {"json": kwargs}
    if params:
        kw["params"] = params
    return self._request(_COMPLEX.bind(parentId=parent_id), **kw)
```

**Note**: This pattern is rare. Most endpoints have either a body OR query params, not both.

## Anti-Patterns (DO NOT USE)

```python
# BAD: Raw dict parameter
def action(self, data: dict | Any) -> Any:
    return self._request(_ACTION, json=data)

# BAD: Manual dict assembly from named params
def action(self, field1: str, field2: int = 0) -> Any:
    body = {"field1": field1, "field2": field2}
    return self._request(_ACTION, json=body)

# BAD: No request_model on Route for POST endpoint
_ACTION = Route("POST", "/service/action", response_model="ActionResponse")
```

## Request Model Contract

Every request model MUST:
1. Inherit from `RequestModel` (which provides `extra="forbid"`, `populate_by_name=True`, camelCase alias generation)
2. Define all fields from the swagger `requestBody` schema
3. Mark required swagger fields as required Python fields (no `Optional`, no default)
4. Mark optional swagger fields as `Optional[T] = Field(None, ...)`
5. Include `Field(description=...)` for all fields
6. Use snake_case field names with auto-generated camelCase aliases

## Request Fixture Contract

Every request fixture MUST:
1. Live in `tests/fixtures/requests/{ModelName}.json`
2. Contain a valid JSON object with camelCase keys (matching the API contract)
3. Pass `ModelName.model_validate(json.loads(fixture_content))`
4. Represent a realistic request payload (sourced from swagger examples, ABConnectTools, or staging)
5. NOT be fabricated — must be derived from a known-working request
