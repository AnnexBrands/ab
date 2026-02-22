# Quickstart: Fix Parameter Routing

**Feature**: 012-fix-param-routing
**Date**: 2026-02-21

## What Changed

The SDK now uses Pydantic models to validate and route query parameters, just like it already does for request bodies. This eliminates manual dict construction in endpoint methods and catches invalid parameter names before the HTTP call is made.

## Before (Manual Dict)

```python
# Old pattern — error-prone, verbose
def validate(self, *, line1=None, city=None, state=None, zip=None):
    params: dict[str, str] = {}
    if line1:
        params["Line1"] = line1
    if city:
        params["City"] = city
    if state:
        params["State"] = state
    if zip:
        params["Zip"] = zip
    return self._request(_IS_VALID, params=params)
```

## After (Params Model)

```python
# Route declares params_model
_IS_VALID = Route(
    "GET", "/address/isvalid",
    params_model="AddressValidateParams",
    response_model="AddressIsValidResult",
)

# Endpoint method passes kwargs directly
def validate(self, **kwargs) -> AddressIsValidResult:
    return self._request(_IS_VALID, params=kwargs)
```

```python
# Params model validates and aliases
class AddressValidateParams(RequestModel):
    line1: Optional[str] = Field(None, alias="Line1")
    city: Optional[str] = Field(None, alias="City")
    state: Optional[str] = Field(None, alias="State")
    zip: Optional[str] = Field(None, alias="Zip")
```

## How It Works

1. Caller provides snake_case kwargs: `api.address.validate(line1="123 Main St")`
2. `_request()` sees `params_model="AddressValidateParams"` on the Route
3. Calls `AddressValidateParams.check({"line1": "123 Main St"})` which:
   - Validates the input (rejects unknown field names)
   - Converts to aliased dict: `{"Line1": "123 Main St"}`
   - Excludes None and unset values
4. Passes aliased dict as `params=` to `HttpClient.request()`
5. `requests` library URL-encodes: `GET /address/isvalid?Line1=123+Main+St`

## Three Transport Mechanisms

| Transport | Trigger | Model | Example |
| --------- | ------- | ----- | ------- |
| Path substitution | `Route.bind(paramName=value)` | None (explicit) | `/companies/{companyId}` → `/companies/abc-123` |
| Query string | `params=kwargs` + `route.params_model` | ParamsModel (RequestModel subclass) | `?Line1=123+Main+St&City=Columbus` |
| JSON body | `json=kwargs` + `route.request_model` | RequestModel subclass | `{"searchText": "john", "pageSize": 50}` |

## Quality Gate G5

A new quality gate evaluates parameter routing correctness:
- Endpoints with swagger query params MUST have `params_model` on their Route
- Endpoints with swagger request bodies MUST have `request_model` on their Route
- G5 appears alongside G1-G4 in the progress HTML report

## Adding a New Endpoint with Query Params

1. Check swagger spec for parameter definitions (`"in": "query"`)
2. Create a params model with fields matching swagger names:
   ```python
   class MyEndpointParams(RequestModel):
       my_field: Optional[str] = Field(None, alias="myField")
   ```
3. Add `params_model="MyEndpointParams"` to the Route definition
4. Export the model from `ab/api/models/__init__.py`
5. Endpoint method accepts `**kwargs` and passes as `params=kwargs`
