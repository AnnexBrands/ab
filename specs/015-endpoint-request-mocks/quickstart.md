# Quickstart: Endpoint Request Mocks

## What This Feature Does

Generates null-populated JSON fixture files for every API endpoint that accepts input parameters or a request body. These fixtures replace hardcoded test/example values and create a fail-first workflow: endpoints with required fields fail validation until the fixture is populated with real data.

## After Implementation

### View all request fixtures
```bash
ls tests/fixtures/requests/
# AddressValidateParams.json
# AddressPropertyTypeParams.json
# CompanySearchRequest.json
# JobSearchParams.json
# ... (~82 files total)
```

### See which fixtures need real data
```bash
# Run tests — failures indicate fixtures needing real values
pytest tests/integration/test_address.py -v
# FAILED: ValidationError - line1 field required (value was null)
```

### Fill in a fixture with real data
```bash
# Edit the fixture file with valid values
cat tests/fixtures/requests/AddressValidateParams.json
# Before: {"Line1": null, "City": null, "State": null, "Zip": null}

# After editing:
# {"Line1": "12742 E Caley Av", "City": "Centennial", "State": "CO", "Zip": "80111"}
```

### Run the example using fixture data
```bash
python -m examples address
# Loads params from AddressValidateParams.json instead of hardcoded values
```

### Check fixture coverage
```bash
# All fixtures tracked in FIXTURES.md
cat docs/FIXTURES.md | grep "requests/"
```

## Key Patterns

### For examples
```python
# Before (hardcoded):
runner.add("validate",
    lambda api: api.address.validate(line1="123 Main", city="Denver", ...),
    response_model="AddressIsValidResult",
)

# After (fixture-driven):
runner.add("validate",
    lambda api: api.address.validate,  # method reference
    request_fixture_file="AddressValidateParams.json",
    response_model="AddressIsValidResult",
)
```

### For tests
```python
# Before (hardcoded):
result = api.address.validate(line1="123 Main", city="Denver", ...)

# After (fixture-driven):
params = require_fixture("AddressValidateParams", required=True)
result = api.address.validate(**params)
```

## Fail-First Workflow

1. Generate all fixtures with null values
2. Run `pytest` — tests with required fields FAIL
3. Fill in real values for priority endpoints
4. Tests pass as fixtures are populated
5. Remaining failures = visible backlog
