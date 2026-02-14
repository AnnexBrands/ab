# Web2Lead

```{eval-rst}
.. autoclass:: ab.api.endpoints.web2lead.Web2LeadEndpoint
   :members:
   :undoc-members:
```

Uses the ABC API surface (requires `access_key` in configuration).

## Methods

### get

`GET /Web2Lead` (ABC) — Get Web2Lead configuration.

**Returns:** {class}`~ab.api.models.web2lead.Web2LeadResponse`

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")
config = api.web2lead.get()
```

### post

`POST /Web2Lead` (ABC) — Submit a Web2Lead form.

```python
api.web2lead.post({
    "companyCode": "14004OH",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
})
```
