# E-Sign

```{eval-rst}
.. autoclass:: ab.api.endpoints.esign.ESignEndpoint
   :members:
   :undoc-members:
```

## Methods

### get_result

`GET /e-sign/result` — Get e-sign result by envelope and event.

**Returns:** {class}`~ab.api.models.esign.ESignResult`

```python
result = api.esign.get_result(envelope="env-id", event="completed")
```

### get_esign_data

`GET /e-sign/{jobDisplayId}/{bookingKey}` — Get e-sign data for a booking.

**Returns:** {class}`~ab.api.models.esign.ESignData`
