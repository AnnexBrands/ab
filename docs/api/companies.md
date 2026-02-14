# Companies

```{eval-rst}
.. autoclass:: ab.api.endpoints.companies.CompaniesEndpoint
   :members:
   :undoc-members:
```

## Methods

### get_by_id

`GET /companies/{id}` — Retrieve a company by UUID or company code.

**Returns:** {class}`~ab.api.models.companies.CompanySimple`

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")
company = api.companies.get_by_id("93179b52-3da9-e311-b6f8-000c298b59ee")
print(company.name)

# Also accepts company codes (resolved via CodeResolver)
company = api.companies.get_by_id("14004OH")
```

### get_details

`GET /companies/{companyId}/details` — Company detail summary.

**Returns:** {class}`~ab.api.models.companies.CompanyDetails`

```python
details = api.companies.get_details("93179b52-...")
print(details.details)
```

### get_fulldetails

`GET /companies/{companyId}/fulldetails` — Full editable company details.

**Returns:** {class}`~ab.api.models.companies.CompanyDetails`

```python
full = api.companies.get_fulldetails("93179b52-...")
```

### update_fulldetails

`PUT /companies/{companyId}/fulldetails` — Update company details.

**Returns:** {class}`~ab.api.models.companies.CompanyDetails`

```python
api.companies.update_fulldetails("93179b52-...", {"name": "Updated Name"})
```

### create

`POST /companies/fulldetails` — Create a new company.

**Returns:** New company ID string.

```python
new_id = api.companies.create({"name": "New Co", "code": "NEWCO"})
```

### search

`POST /companies/search/v2` — Search companies.

**Returns:** `list[`{class}`~ab.api.models.companies.SearchCompanyResponse`]`

```python
results = api.companies.search({"searchText": "Navis"})
```

### list

`POST /companies/list` — Paginated company list.

**Returns:** `list[`{class}`~ab.api.models.companies.CompanySimple`]`

```python
companies = api.companies.list({"page": 1, "pageSize": 25})
```

### available_by_current_user

`GET /companies/availableByCurrentUser` — Companies accessible to the current user.

**Returns:** `list[`{class}`~ab.api.models.companies.CompanySimple`]`

```python
my_companies = api.companies.available_by_current_user()
```
