# Quickstart: Implementing an Endpoint with Request Models

**Feature**: 007-request-model-methodology
**Date**: 2026-02-14

## The New Pattern at a Glance

### Before (old pattern)

```python
# Endpoint method — accepts raw dict
def search(self, data: dict | Any) -> Any:
    """POST /companies/search/v2"""
    return self._request(_SEARCH, json=data)

# Caller — must construct dict with camelCase keys
result = api.companies.search({"searchText": "acme", "pageSize": 10})
```

### After (new pattern)

```python
# Endpoint method — accepts **kwargs
def search(self, **kwargs: Any) -> Any:
    """POST /companies/search/v2"""
    return self._request(_SEARCH, json=kwargs)

# Caller — passes snake_case keyword arguments
result = api.companies.search(search_text="acme", page_size=10)
```

Validation happens automatically in `_request()` via `CompanySearchRequest.check(kwargs)`.

## Step-by-Step: New Endpoint Implementation

### 1. Research (DISCOVER Phase D)

Check two sources for the endpoint's request contract:

- **Swagger spec** (`ab/api/schemas/{surface}.json`): parameter names, required fields, types, request body schema.
- **ABConnectTools** (`/usr/src/pkgs/ABConnectTools/ABConnect/api/endpoints/`): realistic parameter values, transport type (json vs params).

### 2. Define Request Model (DISCOVER Phase I)

```python
# ab/api/models/myservice.py
class MyEndpointRequest(RequestModel):
    """Body for POST /myservice/action."""
    required_field: str = Field(..., description="A required field")
    optional_field: Optional[int] = Field(None, description="An optional field")
    nested_data: Optional[dict] = Field(None, description="Nested structure")
```

For GET endpoints with complex query params, define a params model the same way:

```python
class MySearchParams(RequestModel):
    """Query params for GET /myservice/search."""
    query: str = Field(..., description="Search query")
    page: int = Field(1, description="Page number")
    page_size: int = Field(25, description="Results per page")
```

### 3. Define Route (DISCOVER Phase S)

```python
# ab/api/endpoints/myservice.py
_ACTION = Route(
    "POST", "/myservice/action",
    request_model="MyEndpointRequest",
    response_model="MyEndpointResponse",
)

_SEARCH = Route(
    "GET", "/myservice/search",
    params_model="MySearchParams",
    response_model="List[MySearchResult]",
)
```

### 4. Write Endpoint Method (DISCOVER Phase S)

```python
class MyServiceEndpoint(BaseEndpoint):
    def action(self, **kwargs: Any) -> Any:
        """POST /myservice/action"""
        return self._request(_ACTION, json=kwargs)

    def search(self, **kwargs: Any) -> Any:
        """GET /myservice/search"""
        return self._request(_SEARCH, params=kwargs)
```

For endpoints with path params + body:

```python
def update(self, item_id: str, **kwargs: Any) -> Any:
    """PUT /myservice/{itemId}"""
    return self._request(_UPDATE.bind(itemId=item_id), json=kwargs)
```

### 5. Write Example & Capture Fixtures (DISCOVER Phase C)

```python
# examples/myservice.py
runner.add(
    "action",
    lambda api: api.myservice.action(
        required_field="test value",
        optional_field=42,
    ),
    request_model="MyEndpointRequest",
    response_model="MyEndpointResponse",
    fixture_file="MyEndpointResponse.json",
    request_fixture_file="requests/MyEndpointRequest.json",
)
```

### 6. Track in FIXTURES.md (DISCOVER Phase V)

Add a row to the unified tracking table:

```markdown
| /myservice/action | POST | MyEndpointRequest | captured | MyEndpointResponse | captured | complete | — |
```

## Caller Usage

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

# POST with body — snake_case kwargs
result = api.myservice.action(required_field="value", optional_field=5)

# GET with query params — same pattern
results = api.myservice.search(query="test", page=1, page_size=10)

# PUT with path param + body
updated = api.myservice.update("item-123", required_field="new value")

# Existing dict? Unpack it
my_data = {"required_field": "value", "optional_field": 5}
result = api.myservice.action(**my_data)
```

## Checklist: Is My Endpoint Complete?

- [ ] Request model defined (if POST/PUT/PATCH with body)
- [ ] Params model defined (if GET with complex query params)
- [ ] Response model defined
- [ ] Route has `request_model` / `params_model` / `response_model` set
- [ ] Endpoint method uses `**kwargs` (not `data: dict`)
- [ ] Example written with realistic parameters
- [ ] Request fixture captured in `tests/fixtures/requests/`
- [ ] Response fixture captured in `tests/fixtures/`
- [ ] FIXTURES.md updated with all dimensions
- [ ] Tests validate both request and response fixtures against models
