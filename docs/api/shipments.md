# Shipments

```{eval-rst}
.. autoclass:: ab.api.endpoints.shipments.ShipmentsEndpoint
   :members:
   :undoc-members:
```

## Methods

### get_rate_quotes

`GET /job/{jobDisplayId}/shipment/ratequotes` — Get rate quotes for a job shipment.

**Returns:** `list[`{class}`~ab.api.models.shipments.RateQuote`]`

```python
quotes = api.shipments.get_rate_quotes(job_display_id)
```

### book

`POST /job/{jobDisplayId}/shipment/book` — Book a shipment.

**Returns:** {class}`~ab.api.models.shared.ServiceBaseResponse`

### delete_shipment

`DELETE /job/{jobDisplayId}/shipment` — Delete a shipment.

**Returns:** {class}`~ab.api.models.shared.ServiceBaseResponse`

### add_accessorial / remove_accessorial

`POST /job/{jobDisplayId}/shipment/accessorial` and `DELETE .../accessorial/{addOnId}` — Manage accessorial charges.

**Returns:** {class}`~ab.api.models.shared.ServiceBaseResponse`

### get_export_data / post_export_data

`GET/POST /job/{jobDisplayId}/shipment/exportdata` — Shipment export data operations.

**Returns:** {class}`~ab.api.models.shipments.ShipmentExportData`
