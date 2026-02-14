# Quickstart: ABConnect SDK (`ab`)

## Installation

```bash
pip install ab
```

## Configuration

Create a `.env.staging` file:

```env
ABCONNECT_USERNAME=your_username
ABCONNECT_PASSWORD=your_password
ABC_CLIENT_ID=your_client_id
ABC_CLIENT_SECRET=your_client_secret
ABC_ENVIRONMENT=staging
```

Or set environment variables directly.

## Basic Usage

### Initialize the Client

```python
from ab import ABConnectAPI

# Standalone usage (FileTokenStorage)
api = ABConnectAPI(env="staging")

# Django usage (SessionTokenStorage)
api = ABConnectAPI(request=django_request)
```

### Companies

```python
# Get a company by ID
company = api.companies.get_by_id("company-uuid")
print(company.name)
print(company.code)

# Get a company by code (auto-resolves via cache)
company = api.companies.get_by_id("9999AZ")

# Search companies
results = api.companies.search(search_text="Acme")
for company in results:
    print(f"{company.code}: {company.name}")

# Get full details
details = api.companies.get_fulldetails("company-uuid")
print(details.addresses)
```

### Contacts

```python
# Get contact details
contact = api.contacts.get_details("contact-uuid")
print(f"{contact.first_name} {contact.last_name}")

# Search contacts
results = api.contacts.search(search_text="John")
for contact in results:
    print(f"{contact.name} ({contact.email})")
```

### Jobs

```python
# Get a job by display ID
job = api.jobs.get(2000000)
print(job.status)
print(job.customer)

# Search jobs
results = api.jobs.search(query="pending")

# Get job pricing
price = api.jobs.get_price(2000000)
```

### Catalog API

```python
# List catalogs
catalogs = api.catalog.list(page=1, page_size=10)
for catalog in catalogs.items:
    print(f"{catalog.title} ({catalog.id})")
print(f"Page {catalogs.page_number} of {catalogs.total_pages}")

# Get a specific catalog
catalog = api.catalog.get(catalog_id=1)

# Create a catalog
from ab.api.models import AddCatalogRequest
new_catalog = api.catalog.create(AddCatalogRequest(
    title="Fall 2026 Auction",
    agent_id="agent-uuid",
    seller_ids=[1, 2, 3]
))
```

### Lots

```python
# List lots
lots = api.lots.list(page=1)
for lot in lots.items:
    print(f"Lot {lot.lot_number}: {lot.data.description}")

# Get lot overrides
overrides = api.lots.get_overrides(
    customer_item_ids=["ITEM-001", "ITEM-002"]
)
```

### Quoting (ABC API)

```python
from ab.api.models import QuoteRequestModel

# Quick quote
quote = api.autoprice.quick_quote(QuoteRequestModel(
    job_info={"origin_zip": "90210", "dest_zip": "10001"},
    items=[{"description": "Sofa", "weight": 150}]
))
print(quote.quotes)

# Full quote request
result = api.autoprice.quote_request(QuoteRequestModel(...))
print(result.status)
```

### Documents

```python
# List documents for a job
docs = api.documents.list(job_id="job-uuid")
for doc in docs:
    print(f"{doc.file_name} ({doc.doc_type})")

# Download a document
content = api.documents.get("path/to/document")

# Upload a document
api.documents.upload(
    job_id="job-uuid",
    file_path="/path/to/file.pdf",
    document_type=6
)
```

### Address Validation

```python
result = api.address.validate(
    street="123 Main St",
    city="Los Angeles",
    state="CA",
    zip_code="90210"
)
if result.is_valid:
    print("Address is valid")
else:
    print("Suggestions:", result.suggestions)
```

## Environment Switching

```python
# Staging (default for development)
api = ABConnectAPI(env="staging")

# Production
api = ABConnectAPI(env="production")

# Custom environment
api = ABConnectAPI(env_file="/path/to/.env.custom")
```

## Error Handling

```python
from ab.exceptions import (
    ABConnectError,
    AuthenticationError,
    RequestError
)

try:
    company = api.companies.get_by_id("invalid-id")
except AuthenticationError:
    print("Login failed — check credentials")
except RequestError as e:
    print(f"API error {e.status_code}: {e.message}")
except ABConnectError as e:
    print(f"SDK error: {e}")
```

## Model Inspection

All responses are Pydantic models with full type information:

```python
company = api.companies.get_by_id("company-uuid")

# Access typed fields
print(type(company))          # <class 'ab.api.models.CompanySimple'>
print(company.model_fields)   # See all fields and types

# Serialize to dict (camelCase keys for API compatibility)
data = company.model_dump(by_alias=True, exclude_none=True)

# Validate request data
from ab.api.models import CompanySearchRequest
request = CompanySearchRequest(search_text="Acme", page=1)
request.check()  # Returns validated, serialized dict
```
