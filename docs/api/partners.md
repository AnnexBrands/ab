# Partners

```{eval-rst}
.. autoclass:: ab.api.endpoints.partners.PartnersEndpoint
   :members:
   :undoc-members:
```

## Methods

### list

`GET /partner` — List all partners.

**Returns:** `list[`{class}`~ab.api.models.partners.Partner`]`

```python
partners = api.partners.list()
```

### get

`GET /partner/{id}` — Get a partner by ID.

**Returns:** {class}`~ab.api.models.partners.Partner`

### search

`POST /partner/search` — Search partners.

**Returns:** `list[`{class}`~ab.api.models.partners.Partner`]`

```python
results = api.partners.search(searchText="Navis")
```
