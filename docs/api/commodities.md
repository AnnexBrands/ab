# Commodities

```{eval-rst}
.. autoclass:: ab.api.endpoints.commodities.CommoditiesEndpoint
   :members:
   :undoc-members:
```

## Methods

### search / suggestions

`POST /commodity/search` and `POST /commodity/suggestions` — Search and suggest commodities.

**Returns:** `list[`{class}`~ab.api.models.commodities.Commodity`]`

```python
results = api.commodities.search(searchText="furniture")
suggestions = api.commodities.suggestions(searchText="chair")
```

### get / create / update

Standard CRUD operations on commodity records.

**Returns:** {class}`~ab.api.models.commodities.Commodity`

# Commodity Maps

```{eval-rst}
.. autoclass:: ab.api.endpoints.commodity_maps.CommodityMapsEndpoint
   :members:
   :undoc-members:
```

## Methods

### search / get / create / update / delete

Standard CRUD operations on commodity mapping records.

**Returns:** {class}`~ab.api.models.commodities.CommodityMap`

```python
maps = api.commodity_maps.search(searchText="test")
```
