# Quickstart: G1 Model Fidelity Sweep

**Feature**: 034-g1-model-fidelity-sweep
**Branch**: `034-g1-model-fidelity-sweep`

## What This Feature Does

Expands `ServiceBaseResponse` from 3 fields to 16 fields to match the captured fixture, closing the G1 (Model Fidelity) gap for all 21 endpoints that use this shared response model.

## Implementation Steps

### 1. Expand ServiceBaseResponse (core change)

Edit `ab/api/models/shared.py`:

1. Import `ShipmentWeight` from `ab.api.models.shipments`
2. Add 13 new `Optional` fields to `ServiceBaseResponse` matching the fixture keys
3. Use `ShipmentWeight` for the nested `weight` field

### 2. Add fixture-validation test

Create `tests/models/test_shared_models.py`:

1. Load `ServiceBaseResponse.json` fixture
2. Validate with `ServiceBaseResponse.model_validate(data)`
3. Assert `assert_no_extra_fields(model)`
4. Assert key fields populated (success, documents, weight)

### 3. Update gate baseline

Run gate evaluation and update `tests/gate_baseline.json`:

1. Add `"G1"` to all 21 endpoint entries
2. Run `pytest tests/test_gate_regression.py` to confirm no regressions

### 4. Create missing Sphinx doc stubs

Create minimal automodule/autoclass stubs for:
- `docs/api/payments.md`
- `docs/api/shipments.md`
- `docs/models/payments.md`
- `docs/models/commodities.md`
- `docs/models/views.md`

### 5. Verify

```bash
# Run all tests
pytest

# Run gate regression specifically
pytest tests/test_gate_regression.py -v

# Run freight + shared model tests
pytest tests/models/test_shared_models.py tests/models/test_freight_models.py -v

# Build Sphinx docs
cd docs && make html
```

## Key Files

| File | Action |
|------|--------|
| `ab/api/models/shared.py` | Expand ServiceBaseResponse (13 new fields) |
| `tests/models/test_shared_models.py` | New fixture-validation test |
| `tests/gate_baseline.json` | Add G1 to 21 endpoint entries |
| `docs/api/payments.md` | New Sphinx stub |
| `docs/api/shipments.md` | New Sphinx stub |
| `docs/models/payments.md` | New Sphinx stub |
| `docs/models/commodities.md` | New Sphinx stub |
| `docs/models/views.md` | New Sphinx stub |

## Estimated Scope

- 1 model file changed
- 1 test file created
- 1 baseline file updated
- 5 doc stubs created
- ~50 lines of model code, ~20 lines of test code, ~50 lines of doc stubs
