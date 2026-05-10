# Quickstart Guide

## Installation

```bash
pip install -e .
```

## Configuration

Create a `.env.staging` file in your project root:

```ini
ABCONNECT_USERNAME=myuser
ABCONNECT_PASSWORD=mypass
ABCONNECT_CLIENT_ID=myapp
ABCONNECT_CLIENT_SECRET=my-secret-uuid
ABCONNECT_ENVIRONMENT=staging
```

## Basic Usage

```python
from ab import ABConnectAPI

# Initialize — authenticates automatically
api = ABConnectAPI(env="staging")
```

## Common Operations

### Get a Company

```python
company = api.companies.get_by_id("93179b52-3da9-e311-b6f8-000c298b59ee")
print(company.name)  # "Navis Pack & Ship #14004OH"

# Or use a company code
company = api.companies.get_by_id("14004OH")
```

### Get Current User's Contact

```python
me = api.contacts.get_current_user()
print(me.full_name)
```

### Search Companies

```python
results = api.companies.search({"searchText": "Navis"})
for r in results:
    print(r.id, r.name)
```

### List Catalogs

```python
# Basic listing
catalogs = api.catalog.list()

# With filter parameters
catalogs = api.catalog.list(agent="Smith", is_completed=False, page_size=10)
```

### Paginate Through All Results

```python
from ab import ABConnectAPI, paginate

api = ABConnectAPI(env="staging")
for page in paginate(api.catalog.list, page_size=10):
    for item in page.items:
        print(item.title)
```

### Get Lookup Data

```python
countries = api.lookup.get_countries()
statuses = api.lookup.get_job_statuses()
contact_types = api.lookup.get_contact_types()
```

### List Users and Roles

```python
users = api.users.list({"page": 1, "pageSize": 10})
roles = api.users.get_roles()
```

## Django Integration

```python
from ab import ABConnectAPI

def my_view(request):
    api = ABConnectAPI(request=request)
    company = api.companies.get_by_id("14004OH")
    return render(request, "company.html", {"company": company})
```

When using `request=`, tokens are stored in the Django session instead of the filesystem.

For a login view, authenticate explicitly with form credentials:

```python
def login_view(request):
    api = ABConnectAPI(request=request, allow_password_fallback=False)
    api.login(request.POST["username"], request.POST["password"])
```

`allow_password_fallback=False` is recommended for user-session flows so an
expired session token cannot fall back to service-account credentials.

## Error Handling

```python
from ab.exceptions import AuthenticationError, RequestError

try:
    company = api.companies.get_by_id("nonexistent")
except RequestError as e:
    print(f"API error {e.status_code}: {e.message}")
except AuthenticationError:
    print("Invalid credentials")
```
