# Dashboard

```{eval-rst}
.. autoclass:: ab.api.endpoints.dashboard.DashboardEndpoint
   :members:
   :undoc-members:
```

## Methods

### get

`GET /dashboard` — Aggregated dashboard summary.

**Returns:** {class}`~ab.api.models.dashboard.DashboardSummary`

```python
summary = api.dashboard.get()
print(summary.inbound_count, summary.outbound_count)
```

### get_grid_views

`GET /dashboard/gridviews` — List available grid views.

**Returns:** `list[`{class}`~ab.api.models.dashboard.GridViewInfo`]`

### get_grid_view_state / save_grid_view_state

`GET/POST /dashboard/gridviewstate/{id}` — Read/save grid view state.

**Returns:** {class}`~ab.api.models.dashboard.GridViewState`

### inbound / in_house / outbound / local_deliveries / recent_estimates

`POST /dashboard/{panel}` — Operational panel data.

```python
data = api.dashboard.inbound()
```
