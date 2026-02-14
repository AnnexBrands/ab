# AutoPrice

```{eval-rst}
.. autoclass:: ab.api.endpoints.autoprice.AutoPriceEndpoint
   :members:
   :undoc-members:
```

Uses the ABC API surface (requires `access_key` in configuration).

## Methods

### quick_quote

`POST /AutoPrice/QuickQuote` (ABC) — Get a quick price quote.

**Returns:** {class}`~ab.api.models.autoprice.QuickQuoteResponse`

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")
quote = api.autoprice.quick_quote({
    "originZip": "43213",
    "destinationZip": "90210",
    "weight": 150,
})
```

### quote_request

`POST /AutoPrice/QuoteRequest` (ABC) — Submit a full quote request.

**Returns:** {class}`~ab.api.models.autoprice.QuoteRequestResponse`

```python
result = api.autoprice.quote_request({
    "originZip": "43213",
    "destinationZip": "90210",
    "items": [{"weight": 150, "class": "70"}],
})
```
