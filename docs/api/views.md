# Views

```{eval-rst}
.. autoclass:: ab.api.endpoints.views.ViewsEndpoint
   :members:
   :undoc-members:
```

## Methods

### list

`GET /views/all` — List all saved views.

**Returns:** `list[`{class}`~ab.api.models.views.GridViewDetails`]`

```python
views = api.views.list()
```

### get / create / delete

Standard CRUD operations for saved views.

### get_access_info / update_access

`GET/PUT /views/{viewId}/accessinfo` — View access control.

**Returns:** {class}`~ab.api.models.views.GridViewAccess`

### get_dataset_sps / get_dataset_sp

`GET /views/datasetsps` — List or retrieve dataset stored procedures.

**Returns:** `list[`{class}`~ab.api.models.views.StoredProcedureColumn`]`
