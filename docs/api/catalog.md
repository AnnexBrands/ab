# Catalog

```{eval-rst}
.. autoclass:: ab.api.endpoints.catalog.CatalogEndpoint
   :members:
   :undoc-members:
```

## Methods

### create

`POST /Catalog` — Create a new catalog.

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")
result = api.catalog.create({"name": "New Catalog"})
```

### list

`GET /Catalog` — List catalogs (paginated).

**Returns:** `list[`{class}`~ab.api.models.catalog.CatalogWithSellersDto`]`

```python
catalogs = api.catalog.list(page=1, page_size=25)
```

### get

`GET /Catalog/{id}` — Get a catalog by ID.

**Returns:** {class}`~ab.api.models.catalog.CatalogExpandedDto`

```python
catalog = api.catalog.get(1)
print(catalog.name)
```

### update

`PUT /Catalog/{id}` — Update a catalog.

```python
api.catalog.update(1, {"name": "Updated Catalog"})
```

### delete

`DELETE /Catalog/{id}` — Delete a catalog.

```python
api.catalog.delete(1)
```

### bulk_insert

`POST /Catalog/bulkInsert` — Bulk insert catalog items.

```python
api.catalog.bulk_insert({"items": [...]})
```
