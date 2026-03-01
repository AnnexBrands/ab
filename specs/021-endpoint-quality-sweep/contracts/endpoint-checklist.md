# Contract: Per-Endpoint Quality Gate Requirements

## Gate Pass Criteria

Each gate has binary pass/fail logic evaluated by `ab/progress/gates.py`.

### G1 — Model Fidelity
```
PASS when: model_validate(fixture_data).__pydantic_extra__ == {} or None
FAIL when: any keys land in __pydantic_extra__
AUTO-PASS when: response_model is scalar (str, int, bool, float, bytes)
```

### G2 — Fixture Status
```
PASS when: tests/fixtures/{ModelName}.json exists (live or mock)
FAIL when: no fixture file on disk
```

### G3 — Test Quality
```
PASS when: test file contains BOTH:
  1. isinstance(result, ModelName) assertion
  2. __pydantic_extra__ / assert_no_extra_fields / model_extra reference
FAIL when: either pattern is missing or commented out
```

### G4 — Documentation Accuracy
```
PASS when: endpoint method has -> ModelName return type (not Any)
FAIL when: return type is Any or missing
```

### G5 — Parameter Routing
```
PASS when: swagger has 0 query params OR Route has params_model set
FAIL when: swagger defines query params but Route lacks params_model
```

### G6 — Request Quality (3 sub-checks, all must pass)
```
G6a: endpoint method does NOT use **kwargs or data: Any
G6b: all request/params model fields have Field(description="...")
G6c: no "# TODO: verify optionality" in model source
AUTO-PASS when: no request_model and no params_model
```

## Overall Status
```
"complete" = G1 AND G2 AND G3 AND G4 AND G5 AND G6 all PASS
"incomplete" = any gate FAIL
```
