# PR Analysis: 012 — Fix Parameter Routing

## Code Quality Grade: **A-**

### What Works Well

**1. Zero new abstractions — pure activation of existing infrastructure.**
The entire feature activates `params_model` that was already built into `Route` and `BaseEndpoint._request()` but never used. This is the right call. No new dispatch layers, no new base classes, no middleware. The validation hook at `base.py:69-74` is untouched — all work happened at the configuration layer (Route definitions) and the model layer (RequestModel subclasses). Minimal blast radius.

**2. Swagger-driven alias correctness.**
Every params model was researched against the actual swagger spec, not guessed. PascalCase endpoints (`Line1`, `City`, `Address1`) get explicit `Field(alias=...)` because the SDK's `_to_camel` generator only handles camelCase. This was the root cause of `address.validate()` failing — the aliases were silently wrong. Correct diagnosis, correct fix.

**3. Typed signatures preserved for IDE autocomplete.**
The refactored methods keep explicit keyword arguments (`line1=`, `city=`, `state=`, `zip=`) rather than collapsing to `**kwargs`. The params_model validates at the dispatch layer. This gives callers both IDE autocomplete AND runtime validation — the right trade-off per the spec's clarification session.

**4. G5 gate is well-scoped.**
The gate auto-passes for endpoints with no swagger query params (134/161 pass). It checks the _code_ (scanning Route definitions for `params_model=`) against the _spec_ (swagger `"in": "query"` params). The `lru_cache` on swagger loading prevents redundant I/O. The normalized path matching handles param name mismatches between our Routes and swagger.

**5. Test enforcement is forward-looking.**
`test_query_param_routes_have_params_model` catches all 32 unconverted Tier 3 endpoints as `xfail`. Any future PR that adds `params_model` to one of these endpoints automatically converts the xfail to a pass. Any PR that _adds_ a new Route with swagger query params but forgets `params_model` will fail the test. This is the right ratchet.

### Issues Worth Calling Out

**1. `PropertyType` response model is wrong (pre-existing).**
The integration test `test_get_property_type` fails because the API returns a raw integer `3` but the model expects `{"propertyType": ..., "confidence": ...}`. This is a pre-existing bug — it existed before this PR. The model needs to be `int` or a wrapper that handles raw ints. Not blocking this PR, but worth fixing.

**2. Web2Lead's 29-param `**params` pattern is defensible but inconsistent.**
`web2lead.get()` keeps `**params` while every other endpoint got typed signatures. The rationale (29 params is too many for a signature) is reasonable, but it means one endpoint method has a different call pattern from all others. Consider a builder pattern or a typed `Web2LeadGetParams` object as the method's input in a future pass.

**3. `notes_global.py` example required a signature fix.**
The example called `suggest_users()` without `search_key` — a now-required param. This was caught and fixed, but it shows that signature changes have a ripple effect on examples. No examples were _run_ against the live API to confirm they still produce 200s (only parsed for syntax and import compatibility).

**4. Complete count dropped from 25 to 24.**
Adding G5 caused one previously-complete endpoint to become incomplete (because it now needs `params_model` to pass G5). This is correct behavior — the bar was raised — but stakeholders should understand the regression is definitional, not functional.

**5. G5 regex matching could be fragile.**
The `_route_has_params_model` function uses regex to find Route definitions containing a specific path string and then checks for `params_model` within that match. This works for the current code style (module-level Route constants), but could break if Routes were defined differently (e.g., inside functions, dynamically constructed). Low risk given the codebase's consistency.

## Constitution Coherence: **Strong**

All nine principles are addressed:
- **I (Pydantic Model Fidelity)**: 15 new RequestModel subclasses with `extra="forbid"`, explicit aliases, Field descriptions.
- **IV (Swagger-Informed)**: Every alias researched from swagger specs, not guessed.
- **V (Endpoint Status Tracking)**: FIXTURES.md gains G5 column, summary updated.
- **VIII (Phase-Based Context Recovery)**: tasks.md uses checkbox tasks, all 43 marked complete.
- **IX (Endpoint Input Validation)**: This PR is the direct implementation of Principle IX. The `test_example_params.py` enforcement is exactly what IX prescribes.

The constitution is coherent. The plan correctly identified that the infrastructure already existed (Principle IX was written _for_ this feature in a prior cycle). No principle conflicts.

## User Story Effectiveness: **Good**

| Story | Priority | Delivered? | Assessment |
|-------|----------|------------|------------|
| US1: Correct parameter routing | P1 | Yes | 5/5 manual-dict endpoints refactored. SC-006 verified. |
| US2: Unified pattern | P1 | Yes | 12 kwargs-params endpoints unified. 17 total with params_model. |
| US3: Quality gates | P2 | Yes | G5 in HTML + FIXTURES.md. 134/161 pass. |

The three-tier rollout (Tier 1 manual-dict, Tier 2 kwargs-params, Tier 3 deferred) was a pragmatic scoping choice. Tier 3 (62 endpoints with `json=` body but no `request_model`) is correctly deferred — it's a different problem (body validation, not query param routing).

## High-Level Project Progress

The SDK is maturing from "scaffolded endpoints" toward "production-grade endpoint correctness":
- **291 endpoints tracked**, 68 done (23%), 9 pending, 214 not started
- **Quality gates**: 24/161 pass all 5 gates (15%)
- **G5 specifically**: 134/161 pass (83%) — most endpoints auto-pass because they have no query params
- **27 endpoints** now have G5 FAIL — these are the next conversion targets

The bottleneck is no longer model scaffolding (G3/G4 pass rates are high). It's **fixture capture** (G1: 30/161 pass, G2: 35/161 pass). The next high-impact work is running examples against staging to capture fixtures for the 126 endpoints that pass G3+G4+G5 but fail G1+G2.

## Suggested Next Steps

1. **Capture fixtures for G5-passing endpoints.** 100+ endpoints now pass G3+G4+G5 but fail G1+G2 solely because they lack captured fixture data. A batch fixture capture sprint against staging would move the overall "complete" count from 24 to 50+.
2. **Fix `PropertyType` response model.** The API returns a raw integer, not a dict. Quick fix: change `response_model="PropertyType"` to `response_model="int"` on the Route and update the integration test.
3. **Tier 3 params_model conversion.** The 32 xfail tests in `test_example_params.py` are a ready-made backlog. Prioritize endpoints that have swagger query params AND existing fixtures (easiest to validate).
4. **Run examples against staging.** The `notes_global.py` fix shows that signature changes can break examples silently. A CI step that imports all examples (without executing) would prevent future regressions.
