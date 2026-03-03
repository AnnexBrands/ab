# AB SDK

Python SDK for the ABConnect API ecosystem.

## API Surfaces

| Surface | Base URL | Auth |
|---------|----------|------|
| ACPortal | `portal.{env}.abconnect.co/api/api/` | Bearer JWT |
| Catalog | `catalog-api.{env}.abconnect.co/api/` | Bearer JWT |
| ABC | `api.{env}.abconnect.co/api/` | Bearer JWT + accessKey |

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

# Get a company
company = api.companies.get_by_id("14004OH")
print(company.name)

# Get current user contact
me = api.contacts.get_current_user()
print(me.full_name)

# List lookup data
countries = api.lookup.get_countries()
roles = api.users.get_roles()
```

## Configuration

Set environment variables with `ABCONNECT_` prefix:

```bash
export ABCONNECT_USERNAME=myuser
export ABCONNECT_PASSWORD=mypass
export ABCONNECT_CLIENT_ID=myapp
export ABCONNECT_CLIENT_SECRET=my-secret
export ABCONNECT_ENVIRONMENT=staging
```

Or use `.env.staging` / `.env.production` files.

## Endpoint Groups

| Group | Methods | API Surface |
|-------|---------|-------------|
| `api.companies` | get_by_id, get_details, get_fulldetails, search, list, create, update_fulldetails, available_by_current_user | ACPortal |
| `api.contacts` | get, get_details, get_primary_details, get_current_user, search, create, update_details | ACPortal |
| `api.jobs` | get, search, search_by_details, get_price, get_calendar_items, get_update_page_config, create, save, update | ACPortal + ABC |
| `api.documents` | list, get, upload, update | ACPortal |
| `api.address` | validate, get_property_type | ACPortal |
| `api.lookup` | get_contact_types, get_countries, get_job_statuses, get_items | ACPortal |
| `api.users` | list, get_roles, create, update | ACPortal |
| `api.catalog` | list, get, create, update, delete, bulk_insert | Catalog |
| `api.lots` | list, get, create, update, delete, get_overrides | Catalog |
| `api.sellers` | list, get, create, update, delete | Catalog |
| `api.jobs.agent` | oa, da, change | ACPortal |
| `api.jobs.timeline` | schedule, received, pack_start, pack_finish, storage_begin, storage_end, carrier_schedule, carrier_pickup, carrier_delivery, delete, delete_all | ACPortal |
| `api.autoprice` | quick_quote, quote_request | ABC |
| `api.web2lead` | get, post | ABC |

## Agent Assignment Helpers

Change origin or delivery agents by friendly company code:

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

# Change origin agent (pick-and-pack) using a company code
result = api.jobs.agent.oa(12345, "3P-5153")

# Change delivery agent with price recalculation
result = api.jobs.agent.da(12345, "9999AZ", recalculate_price=True)

# Generic change with explicit service type
from ab.api.models.enums import ServiceType
result = api.jobs.agent.change(12345, "9999AZ", service_type=ServiceType.PICK)

# UUIDs work too — resolver detects them and skips cache lookup
result = api.jobs.agent.oa(12345, "ed282b80-54fe-4f42-bf1b-69103ce1f76c")
```

## Running Examples

The SDK ships with runnable examples for every endpoint group. Use the `ex` console script or `python -m examples`:

```bash
# List all available example modules
ex --list

# Run all examples for a module
ex contacts

# Run a single entry (dot syntax)
ex contacts.get_details

# Prefix matching and aliases work too
ex co.get_d          # matches companies.get_details
ex addr.val          # matches address.validate
```

Each example authenticates against the configured environment, calls the endpoint, displays the result, and saves response fixtures to `tests/fixtures/`.

## Documentation

Build Sphinx docs:

```bash
cd docs && make html
```

## Testing

```bash
# Unit + fixture validation tests (no network)
pytest tests/ --ignore=tests/integration -v

# Live integration tests (requires staging credentials)
pytest tests/integration/ -m live -v
```

## UAT Guide

Step-by-step validation for the SDK after any change.

### 1. Run the full test suite

```bash
cd src && pytest --tb=line -q
```

**Expected**: All tests pass or skip. Zero failures. Output shows a summary like:

```
535 passed, 88 skipped, 3 xfailed
```

Any `FAILED` line means a regression — investigate before proceeding.

### 2. Run quality gate regression

```bash
pytest tests/test_gate_regression.py -v
```

**Expected**: Single test passes. This verifies no endpoint lost gates compared to the committed baseline.

### 3. Update the gate baseline

```bash
python scripts/update_gate_baseline.py
```

**Expected**: Script prints the new gate counts and writes `tests/gate_baseline.json`. If new endpoints were added, you'll see the count increase. Verify no gates were lost from existing endpoints.

### 4. Regenerate FIXTURES.md

```bash
python scripts/generate_progress.py --fixtures
```

**Expected**: `FIXTURES.md` is regenerated with the current endpoint status. New endpoints appear in the table. Verify their gate columns match expectations.

### 5. Run mock coverage check

```bash
pytest tests/test_mock_coverage.py -v
```

**Expected**: Passes. This verifies every example-registered endpoint has a matching mock fixture or documented skip reason.

### Troubleshooting

**Gate regression failure** (`test_gate_regression.py` fails):
A gate that previously passed now fails. Check `git diff tests/gate_baseline.json` to see which endpoint lost a gate. Common causes: model field removed, response_model annotation dropped, or route definition changed. Fix the root cause, then re-run step 3 to update the baseline.

**Fixture missing** (test skips with "Fixture needed"):
Run the corresponding example to capture the fixture from staging:
```bash
ex <module>.<entry>    # e.g., ex timeline.get_timeline
```
If staging credentials are unavailable, the test will remain skipped until a live capture is performed.

**Model mismatch** (extra fields warning in test output):
The API returned fields not declared in the Pydantic model. Run the example to capture a fresh fixture, inspect the new fields, and add them to the model with `Optional[...]` types and `Field(description=...)`.

**FIXTURES.md drift** (table doesn't match current state):
Regenerate with `python scripts/generate_progress.py --fixtures` and verify the diff. Commit the updated file.

## Mock Tracking

See [MOCKS.md](MOCKS.md) for fixture provenance — which are live-captured vs fabricated.
