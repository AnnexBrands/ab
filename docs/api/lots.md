# Lots

```{eval-rst}
.. autoclass:: ab.api.endpoints.lots.LotsEndpoint
   :members:
   :undoc-members:
```

## Methods

### create

`POST /Lot` — Create a new lot.

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")
api.lots.create({"catalogId": 1, "name": "New Lot"})
```

### list

`GET /Lot` — List lots (paginated).

**Returns:** `list[`{class}`~ab.api.models.lots.LotDto`]`

```python
lots = api.lots.list(page=1, page_size=25)
```

### get

`GET /Lot/{id}` — Get a lot by ID.

**Returns:** {class}`~ab.api.models.lots.LotDto`

```python
lot = api.lots.get(100)
```

### update

`PUT /Lot/{id}` — Update a lot.

```python
api.lots.update(100, {"name": "Updated Lot"})
```

### delete

`DELETE /Lot/{id}` — Delete a lot.

```python
api.lots.delete(100)
```

### get_overrides

`POST /Lot/overrides` — Get lot overrides for customer items.

**Returns:** `list[`{class}`~ab.api.models.lots.LotOverrideDto`]`

```python
overrides = api.lots.get_overrides(["item-id-1", "item-id-2"])
```
