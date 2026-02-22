# Contract: Fixture Generation

## generate_request_fixtures()

**Purpose**: Enumerate all Route definitions, resolve model classes, and write null-populated JSON fixture files.

**Input**: None (discovers Routes by introspecting endpoint modules)

**Output**: JSON files in `tests/fixtures/requests/`

**Algorithm**:
1. Import all endpoint classes from `ab.api.endpoints`
2. For each endpoint class, find all `Route` class attributes
3. For each Route with `params_model` or `request_model`:
   - Resolve model class from `ab.api.models`
   - Get field names from `model_fields` (use alias if set)
   - Write `{ModelName}.json` with all fields → `null`
4. Skip files that already exist

**Invariants**:
- File count = count of unique model names across all params_model + request_model
- All JSON files are valid JSON objects
- All JSON keys are camelCase aliases
- Existing files are never overwritten

## load_request_fixture(model_name: str) -> dict

**Purpose**: Load a request fixture by model name.

**Input**: `model_name` — the model class name (e.g., `"AddressValidateParams"`)

**Output**: Dict with fixture data

**Resolution order**:
1. `tests/fixtures/requests/{model_name}.json`
2. FileNotFoundError if not found

## ExampleRunner._run_entry() (modified)

**Current behavior**: Executes `entry.call(api)` directly.

**New behavior**:
1. If `entry.request_fixture_file` is set:
   - Load fixture from `tests/fixtures/requests/{request_fixture_file}`
   - Execute endpoint method with fixture data as kwargs (params_model) or body (request_model)
2. Else: Execute `entry.call(api)` as before (backward compatible)
