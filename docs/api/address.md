# Address

```{eval-rst}
.. autoclass:: ab.api.endpoints.address.AddressEndpoint
   :members:
   :undoc-members:
```

## Methods

### validate

`GET /address/isvalid` — Validate an address.

**Returns:** {class}`~ab.api.models.address.AddressIsValidResult`

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")
result = api.address.validate(
    street="5738 Westbourne Ave",
    city="Columbus",
    state="OH",
    zip_code="43213",
    country="US",
)
if result and result.is_valid:
    print("Address is valid")
```

### get_property_type

`GET /address/propertytype` — Get property type for an address.

**Returns:** {class}`~ab.api.models.address.PropertyType`

```python
prop = api.address.get_property_type(street="5738 Westbourne Ave", zip_code="43213")
```
