# AB SDK

Python SDK for the ABConnect API ecosystem — ACPortal, Catalog, and ABC APIs.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

# Get a company
company = api.companies.get_by_id("93179b52-3da9-e311-b6f8-000c298b59ee")
print(company.name)

# List catalogs
catalogs = api.catalog.list()

# Get current user's contact info
me = api.contacts.get_current_user()
print(me.full_name)
```

## Configuration

Set credentials via environment variables with the `ABCONNECT_` prefix:

```bash
export ABCONNECT_USERNAME=myuser
export ABCONNECT_PASSWORD=mypass
export ABCONNECT_CLIENT_ID=myapp
export ABCONNECT_CLIENT_SECRET=my-secret-uuid
export ABCONNECT_ENVIRONMENT=staging
```

Or use a `.env.staging` / `.env.production` file.

## API Reference

```{toctree}
:maxdepth: 2

api/companies
api/contacts
api/jobs
api/documents
api/address
api/lookup
api/users
api/catalog
api/lots
api/sellers
api/autoprice
api/web2lead
```

## Model Reference

```{toctree}
:maxdepth: 2

models/base
models/common
models/companies
models/contacts
models/jobs
models/documents
models/address
models/lookup
models/users
models/catalog
models/lots
models/sellers
models/autoprice
models/web2lead
```

## Guides

```{toctree}
:maxdepth: 1

quickstart
```

See also: [Mock Tracking (MOCKS.md)](https://github.com/AnnexBrands/ABConnnect/blob/main/MOCKS.md)
