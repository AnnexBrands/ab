# Shipments

```{note}
``api.shipments`` retains three non-job-scoped methods as canonical:
``get_shipment`` (``GET /shipment``), ``get_global_accessorials``
(``GET /shipment/accessorials``), and ``get_shipment_document``
(``GET /shipment/document/{docId}``).

The 11 job-scoped methods (``get_rate_quotes``, ``book``, accessorials,
etc.) are **deprecation shims** that forward to
{class}`ab.api.endpoints.jobs.shipment.JobShipmentEndpoint` (``api.jobs.shipment``).
```

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
