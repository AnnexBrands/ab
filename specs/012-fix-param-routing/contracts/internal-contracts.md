# Internal Contracts: Fix Parameter Routing

**Feature**: 012-fix-param-routing
**Date**: 2026-02-21

This feature modifies internal SDK contracts — no new external APIs are created. The contracts below describe the internal interfaces between SDK components.

## Contract 1: Route → BaseEndpoint Parameter Dispatch

**Current behavior**: `_request()` validates params only when `route.params_model` is set (currently never set).

**New contract**: Every Route with query parameters MUST declare `params_model`. The `_request()` method dispatch logic is:

```
IF route has params_model AND params provided:
    validated_params = ParamsModel.check(raw_params)  # → aliased dict
    send validated_params as query string

IF route has request_model AND json body provided:
    validated_body = RequestModel.check(raw_body)  # → aliased dict
    send validated_body as JSON body

IF route has _path_params:
    path params MUST be bound via Route.bind() before _request() is called
```

## Contract 2: ParamsModel Validation Interface

**Interface**: Same as existing RequestModel — extends `ABConnectBaseModel` with `extra="forbid"`.

```
Input:  dict[str, Any]  (snake_case or alias keys)
Output: dict[str, Any]  (aliased keys, None excluded, unset excluded)
Error:  ValidationError  (raised before HTTP call for unknown/invalid fields)
```

**Example flow**:
```
Input:   {"line1": "123 Main St", "city": "Columbus"}
Model:   AddressValidateParams.check(input)
Output:  {"Line1": "123 Main St", "City": "Columbus"}
HTTP:    GET /address/isvalid?Line1=123+Main+St&City=Columbus
```

## Contract 3: G5 Gate Evaluation Interface

**Input**: endpoint_path (str), method (str), swagger spec reference

**Output**: GateResult with:
- `gate = "G5"`
- `passed = True` if all applicable param routing checks pass
- `reason` describing what's missing if failed

**Evaluation rules**:
1. Swagger has `"in": "query"` params → Route MUST have `params_model`
2. Swagger has `requestBody` → Route MUST have `request_model`
3. Swagger has `"in": "path"` params → Route MUST have matching `_path_params`
4. No swagger params → auto-pass (no routing needed)

## Contract 4: Progress Report Column Addition

**Current columns**: Method | Endpoint Path | Resp Model | G1 | G2 | G3 | G4 | Status | Notes

**New columns**: Method | Endpoint Path | Req Model | Resp Model | G1 | G2 | G3 | G4 | G5 | Status | Notes

**Summary addition**: G5 pass rate displayed alongside G1-G4 summary cards.
