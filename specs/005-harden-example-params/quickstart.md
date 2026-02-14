# Quickstart: Verifying Parameter Fixes

**Feature**: 005-harden-example-params

## After Implementation

### 1. Run the corrected examples against staging

```bash
# Address — should return valid result without 400 errors
python -m examples address.validate
python -m examples address.get_property_type

# Forms — operations endpoint
python -m examples forms.get_operations

# Shipments — rate quotes (needs valid request body to succeed)
python -m examples ship.request_rate_quotes
```

### 2. Run the automated validation test

```bash
# Should pass — all params match swagger
pytest tests/test_example_params.py -v

# Confirm it catches bad params (manually introduce one to test, then revert)
```

### 3. Run full test suite

```bash
pytest
```

### 4. Lint check

```bash
ruff check ab/api/endpoints/address.py ab/api/endpoints/forms.py ab/api/endpoints/shipments.py examples/address.py tests/test_example_params.py
```
