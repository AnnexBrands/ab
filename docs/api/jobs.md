# Jobs

```{eval-rst}
.. autoclass:: ab.api.endpoints.jobs.JobsEndpoint
   :members:
   :undoc-members:
```

Handles two API surfaces: ACPortal (8 routes) and ABC (1 route).

## Methods

### create

`POST /job` (ACPortal) — Create a new job.

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")
api.jobs.create({"companyId": "...", "contactId": "..."})
```

### save

`PUT /job/save` (ACPortal) — Save/update a job.

```python
api.jobs.save({"id": "...", "status": "Active"})
```

### get

`GET /job/{jobDisplayId}` (ACPortal) — Get job by display ID.

**Returns:** {class}`~ab.api.models.jobs.Job`

```python
job = api.jobs.get(2000001)
```

### search

`GET /job/search` (ACPortal) — Search jobs via query params.

**Returns:** `list[`{class}`~ab.api.models.jobs.JobSearchResult`]`

```python
results = api.jobs.search(status="Active")
```

### search_by_details

`POST /job/searchByDetails` (ACPortal) — Search jobs by detail criteria.

**Returns:** `list[`{class}`~ab.api.models.jobs.JobSearchResult`]`

```python
results = api.jobs.search_by_details({"searchText": "test"})
```

### get_price

`GET /job/{jobDisplayId}/price` (ACPortal) — Get job pricing.

**Returns:** {class}`~ab.api.models.jobs.JobPrice`

```python
price = api.jobs.get_price(2000001)
```

### get_calendar_items

`GET /job/{jobDisplayId}/calendaritems` (ACPortal) — Get job calendar items.

**Returns:** `list[`{class}`~ab.api.models.jobs.CalendarItem`]`

```python
items = api.jobs.get_calendar_items(2000001)
```

### get_update_page_config

`GET /job/{jobDisplayId}/updatePageConfig` (ACPortal) — Get job update page config.

**Returns:** {class}`~ab.api.models.jobs.JobUpdatePageConfig`

```python
config = api.jobs.get_update_page_config(2000001)
```

### update

`POST /job/update` (ABC API) — Update a job via the ABC API surface.

```python
api.jobs.update({"jobId": "...", "status": "Completed"})
```
