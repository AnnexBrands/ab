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
| `api.autoprice` | quick_quote, quote_request | ABC |
| `api.web2lead` | get, post | ABC |

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

## Mock Tracking

See [MOCKS.md](MOCKS.md) for fixture provenance — which are live-captured vs fabricated.
