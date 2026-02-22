# Research: Fix Parameter Routing

**Feature**: 012-fix-param-routing
**Date**: 2026-02-21

## R1: Current Parameter Routing Patterns

**Decision**: Adopt a single params_model-based pattern for query parameters, keeping the existing request_model pattern for bodies and Route.bind() for paths.

**Rationale**: The codebase has 263 endpoint methods using 6 different patterns. The manual-dict pattern (5 methods in address.py, documents.py, forms.py) is the source of the reported bug. The kwargs-params pattern (12 methods) lacks validation. The infrastructure for params_model already exists in Route and BaseEndpoint._request() but has zero usage.

**Current pattern distribution**:

| Pattern | Count | Issue |
| ------- | ----- | ----- |
| explicit-bind (path only) | 136 | Clean, no change needed |
| kwargs-json (body) | 63 | Works but 48 lack request_model validation |
| explicit-json (body) | 45 | Works but some lack request_model |
| kwargs-params (query) | 12 | No validation, no params_model |
| manual-dict (query) | 5 | Verbose, error-prone — the reported bug |
| mixed | 2 | Conditional body handling |

**Alternatives considered**:
1. **Single-model dispatch**: One Pydantic model per endpoint containing all params (path + query + body) with metadata to route each field. Rejected — over-engineered, path params are better handled explicitly via Route.bind().
2. **Auto-detect transport from HTTP method**: GET → params, POST → json. Rejected — too implicit, some GETs have no params and some POSTs need query params alongside body.

## R2: Pydantic Alias Handling for Query Parameter Names

**Decision**: Use explicit `Field(alias=...)` for query parameter names that don't follow standard camelCase convention (e.g., `Line1`, `City`, `Address1`, `ZipCode`).

**Rationale**: The `_to_camel` alias generator converts `line1` → `line1` (no underscore, no transformation). But the API expects `Line1` (PascalCase). The existing codebase already uses explicit aliases extensively (e.g., `alias="isValid"`, `alias="countryId"`). This is the established pattern for non-standard naming.

**Key swagger parameter naming patterns**:
- Address: PascalCase — `Line1`, `City`, `State`, `Zip`, `Address1`, `ZipCode`
- Pagination: camelCase — `pageNumber`, `pageSize`
- Forms: camelCase — `shipmentPlanId`, `providerOptionIndex`, `type`
- Documents: camelCase — `jobDisplayId`

**Alternatives considered**:
1. **PascalCase alias generator**: Add a `_to_pascal` generator for params models. Rejected — inconsistent with the rest of the codebase and would require a separate model base.
2. **No aliases, use camelCase field names**: e.g., `Line1: Optional[str]`. Rejected — violates Python naming conventions.

## R3: Quality Gate Extension Strategy

**Decision**: Add a new G5 gate ("Parameter Routing") to the existing gate system. G5 evaluates whether endpoints with query parameters have a `params_model` on their Route and whether endpoints with request bodies have a `request_model`.

**Rationale**: Gates G1-G4 focus exclusively on response models and fixtures. An endpoint can pass all four gates but send parameters via the wrong transport. G5 closes this gap by verifying that param routing is defined, not just that the response is correct.

**G5 evaluation logic**:
1. Load swagger spec for the endpoint
2. If swagger defines `"in": "query"` parameters → check that Route has `params_model` set
3. If swagger defines `requestBody` → check that Route has `request_model` set
4. If swagger defines `"in": "path"` parameters → check that Route's `_path_params` match
5. Pass only if all applicable checks pass

**Alternatives considered**:
1. **Expand G3 (Test Quality)**: Add param routing checks to the test quality gate. Rejected — G3 measures test assertions, not code correctness. Mixing concerns.
2. **No new gate, rely on test_example_params.py**: Rejected — the test validates parameter names but not whether models exist for validation.

## R4: Unified Dispatch Design

**Decision**: The unified pattern uses three transport mechanisms, already built into the infrastructure:

1. **Path params**: Explicit in method signature → `Route.bind()` (unchanged)
2. **Query params**: Method accepts `**kwargs` → passed as `params=kwargs` → validated via `route.params_model` → `.check()` returns aliased dict
3. **Body params**: Method accepts `**kwargs` → passed as `json=kwargs` → validated via `route.request_model` → `.check()` returns aliased dict

No new `_dispatch` method needed. The existing `_request` method already validates params and json when models are declared on the Route. The work is:
- Define params models for endpoints with query params
- Add `params_model=` to Route definitions
- Simplify endpoint methods to pass kwargs instead of manual dicts

**Rationale**: The `BaseEndpoint._request()` method (base.py:69-74) already has the validation hook for params_model — it just has zero usage. Activating it requires only model definitions and Route declarations. No framework changes needed.

**Alternatives considered**:
1. **New `_call()` helper method**: Auto-separates path/query/body from a single kwargs dict. Rejected — adds indirection and loses explicit control over which transport receives which params. Method signatures would lose IDE type hints.
2. **Decorator-based approach**: `@routed(params=..., body=...)` decorator on endpoint methods. Rejected — adds a layer of magic, harder to debug, doesn't play well with IDE autocomplete.

## R5: Impact on `exclude_unset` Behavior

**Decision**: Use `exclude_unset=True` (the default in `.check()`) for params models. This means only explicitly provided kwargs are sent as query parameters.

**Rationale**: The manual dict pattern uses `if line1:` guards which exclude None, empty strings, zero, and False. The Pydantic pattern with `exclude_none=True, exclude_unset=True` excludes None and unset fields but correctly includes empty strings, zero, and False if explicitly provided. This is more correct behavior — a caller explicitly passing `zip=""` presumably means something different from not passing it at all.

**Behavior change**: Empty string `""`, `0`, and `False` will now be sent when explicitly provided. Previously `if value:` guards would silently drop them. This is the correct behavior for an SDK.

## R6: Scope of Endpoint Refactoring

**Decision**: Refactor in three tiers:
1. **Tier 1 (P1)**: 5 manual-dict methods → params_model pattern (address.py, forms.py, documents.py)
2. **Tier 2 (P1)**: 12 kwargs-params methods → add params_model to Route for validation
3. **Tier 3 (P2)**: 62 kwargs-json methods lacking request_model → add request_model where swagger defines a requestBody

Path-only endpoints (136 methods) and endpoints already using request_model correctly need no changes.

**Rationale**: Tier 1 fixes the reported bug and the most error-prone pattern. Tier 2 adds validation to currently-unvalidated query params. Tier 3 completes body validation coverage. Each tier is independently shippable.
