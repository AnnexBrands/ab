# Lookup

```{eval-rst}
.. autoclass:: ab.api.endpoints.lookup.LookupEndpoint
   :members:
   :undoc-members:
```

## Methods

### get_contact_types

`GET /lookup/contacttypes` — List all contact types.

**Returns:** `list[`{class}`~ab.api.models.lookup.ContactTypeEntity`]`

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")
types = api.lookup.get_contact_types()
for t in types:
    print(t.name)
```

### get_countries

`GET /lookup/countries` — List all countries.

**Returns:** `list[`{class}`~ab.api.models.lookup.CountryCodeDto`]`

```python
countries = api.lookup.get_countries()
```

### get_job_statuses

`GET /lookup/jobstatuses` — List all job statuses.

**Returns:** `list[`{class}`~ab.api.models.lookup.JobStatus`]`

```python
statuses = api.lookup.get_job_statuses()
```

### get_items

`GET /lookup/items` — List lookup items.

**Returns:** `list[`{class}`~ab.api.models.lookup.LookupItem`]`

```python
items = api.lookup.get_items()
```
