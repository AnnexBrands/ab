# Quickstart: Scaffold Examples & Fixtures

**Feature**: 004-scaffold-examples-fixtures
**Date**: 2026-02-14

## Running an Example

Run all entries in an example module:

```bash
python -m examples.address
```

Run a specific entry by name:

```bash
python -m examples.address validate
```

Run multiple specific entries:

```bash
python -m examples.address validate get_property_type
```

## Reading an Example File

Each example file follows a consistent structure:

```python
from examples._runner import ExampleRunner

runner = ExampleRunner("Address", env="staging")

# Entry with complete request data (fixture will be captured)
runner.add(
    "validate",
    lambda api: api.address.validate(
        street="5738 Westbourne Ave",
        city="Columbus",
        state="OH",
        zip_code="43213",
    ),
    response_model="AddressIsValidResult",
    fixture_file="AddressIsValidResult.json",
)

# Entry with incomplete request data (annotated with TODO)
runner.add(
    "get_property_type",
    lambda api: api.address.get_property_type(
        # TODO: capture fixture — needs valid street + zipCode for real address
        street="",
        zip_code="",
    ),
    response_model="PropertyType",
    fixture_file="PropertyType.json",
)

if __name__ == "__main__":
    runner.run()
```

## What Each Entry Declares

| Field | Purpose | Example |
|-------|---------|---------|
| Name | CLI selection key | `"validate"` |
| Call | The actual API call with parameters | `lambda api: api.address.validate(...)` |
| response_model | Response Pydantic model name | `"AddressIsValidResult"` |
| request_model | Request Pydantic model name (POST/PUT bodies) | `"QuickQuoteRequest"` |
| fixture_file | Where to save the captured response | `"AddressIsValidResult.json"` |

## Fixture Capture Flow

When you run an entry with complete request data:

1. Runner initializes `ABConnectAPI(env="staging")`
2. Calls the endpoint method with declared parameters
3. Response is already cast to the Pydantic model by `_request()`
4. Model serialized to JSON: `model.model_dump(by_alias=True, mode="json")`
5. JSON written to `tests/fixtures/{fixture_file}`
6. Console confirms: `Fixture saved: tests/fixtures/AddressIsValidResult.json`

## Filling in Missing Request Data

1. Find the TODO comment in the entry
2. Research the correct parameters:
   - Check ABConnectTools: `/usr/src/pkgs/ABConnectTools/ABConnect/api/endpoints/`
   - Check swagger specs: `ab/api/schemas/{acportal,catalog,abc}.json`
   - Check FIXTURES.md for known blockers
3. Replace placeholder values with real data
4. Remove the `# TODO` comment
5. Run the example to capture the fixture
6. Commit the fixture file and updated example

## Prerequisites

- Valid staging credentials in `.env.staging` or environment variables
- Python environment with `ab` package installed (`pip install -e .`)
