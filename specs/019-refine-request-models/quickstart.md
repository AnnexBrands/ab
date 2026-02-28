# Quickstart: Refine Request Models

**Feature**: 019-refine-request-models
**Date**: 2026-02-27

## What This Feature Does

Transforms SDK endpoint methods from opaque `**kwargs` signatures into fully-typed, IDE-discoverable method calls. After this feature, every endpoint parameter has a name, type, description, and correct required/optional designation — visible directly in IDE autocomplete tooltips.

## Before & After

### Before: No IDE Hints

```python
# Developer must read source code to know what parameters exist
result = api.companies.search(**kwargs)  # What goes in kwargs?
result = api.companies.update_fulldetails(company_id, **kwargs)  # ???
```

### After: Full IDE Discoverability

```python
# IDE shows: search_text, page, page_size, filters, sort_by
result = api.companies.search(
    search_text="acme",
    page=1,
    page_size=25,
)

# IDE shows: data (CompanyDetails | dict)
result = api.companies.update_fulldetails(
    company_id="14004OH",
    data={"name": "Acme Corp", "taxId": "12-345"},
)
```

## How to Refine an Endpoint (Developer Guide)

### Step 1: Find the C# Source

Look up the endpoint's controller and DTO in `/src/ABConnect/`:

```
ACPortal controllers: ACPortal/ABC.ACPortal.WebAPI/Controllers/
ACPortal DTOs:        ACPortal/ABC.ACPortal.WebAPI/Models/
ABC controllers:      ABC.WebAPI/Controllers/
Catalog controllers:  Catalog.WebAPI/Controllers/
```

### Step 2: Determine Required vs Optional

For each property in the C# DTO:
- **Non-nullable** (`string Name`) → Required: `name: str = Field(..., description="...")`
- **Nullable** (`string? Name`) → Optional: `name: Optional[str] = Field(None, description="...")`
- **Has default** (`int PageSize = 25`) → Default: `page_size: int = Field(25, description="...")`

### Step 3: Add Descriptions

Every field needs a `description` in `Field()`:

```python
# BAD — no description
company_id: str = Field(..., alias="companyId")

# GOOD — has description
company_id: str = Field(..., alias="companyId", description="Target company UUID")
```

### Step 4: Use Mixins for Common Patterns

```python
from ab.api.models.mixins import PaginatedRequestMixin, SearchableRequestMixin

class MySearchRequest(PaginatedRequestMixin, SearchableRequestMixin):
    """Body for POST /my-domain/search."""
    # pagination (page, page_size) and search (search_text) come from mixins
    custom_filter: Optional[str] = Field(None, description="Domain-specific filter")
```

### Step 5: Update the Endpoint Method

Replace `**kwargs: Any` with typed parameters following the contract patterns:

```python
# For ≤8 fields: inline keyword arguments
def search(self, *, search_text=None, page=1, page_size=25):
    body = dict(search_text=search_text, page=page, page_size=page_size)
    return self._request(_SEARCH, json=body)

# For >8 fields: data parameter
def create(self, *, data: MyCreateRequest | dict):
    return self._request(_CREATE, json=data)
```

### Step 6: Add Docstring

```python
def search(self, *, search_text=None, page=1, page_size=25):
    """POST /my-domain/search.

    Args:
        search_text: Free-text search query.
        page: Page number (1-based).
        page_size: Items per page.

    Request model: :class:`MySearchRequest`
    """
```

### Step 7: Verify

```bash
# Run request fixture validation — must pass
pytest tests/models/test_request_fixtures.py -v

# Run field description check
pytest tests/models/test_request_descriptions.py -v

# Regenerate progress report to see G6 status
python scripts/generate_progress.py
```

## Checking Progress

After refining any endpoint, regenerate `progress.html`:

```bash
python scripts/generate_progress.py
open progress.html
```

The G6 column shows request model quality:
- **PASS**: Typed signature + descriptions + verified optionality
- **FAIL**: Still uses `**kwargs`, missing descriptions, or unverified optionality

## Common Patterns

### Pagination
```python
class PaginatedRequestMixin(RequestModel):
    page: int = Field(1, description="Page number (1-based)")
    page_size: int = Field(25, alias="pageSize", description="Items per page")
```

### Search
```python
class SearchableRequestMixin(RequestModel):
    search_text: Optional[str] = Field(None, alias="searchText", description="Free-text search query")
```

### Date Range
```python
class DateRangeRequestMixin(RequestModel):
    start_date: Optional[str] = Field(None, alias="startDate", description="Range start (ISO 8601)")
    end_date: Optional[str] = Field(None, alias="endDate", description="Range end (ISO 8601)")
```
