# Parameter Correction Contracts

**Feature**: 005-harden-example-params

These contracts define the exact before/after for each endpoint method change, derived from swagger specs.

## Contract 1: address.validate()

**Swagger**: GET `/api/address/isvalid`

```python
# BEFORE (wrong)
def validate(self, *, street: str, city: str, state: str, zip_code: str, country: str) -> AddressIsValidResult:
    params = {}
    if street:    params["street"] = street      # wrong
    if city:      params["city"] = city           # wrong case
    if state:     params["state"] = state         # wrong case
    if zip_code:  params["zipCode"] = zip_code    # wrong
    if country:   params["country"] = country     # fabricated
    return self._request(_IS_VALID, params=params)

# AFTER (correct)
def validate(self, *, line1: str = "", city: str = "", state: str = "", zip: str = "") -> AddressIsValidResult:
    params = {}
    if line1:  params["Line1"] = line1
    if city:   params["City"] = city
    if state:  params["State"] = state
    if zip:    params["Zip"] = zip
    return self._request(_IS_VALID, params=params)
```

## Contract 2: address.get_property_type()

**Swagger**: GET `/api/address/propertytype`

```python
# BEFORE (wrong)
def get_property_type(self, *, street: str, zip_code: str) -> Any:
    return self._request(_PROPERTY_TYPE, params={"street": street, "zipCode": zip_code})

# AFTER (correct)
def get_property_type(self, *, address1: str = "", address2: str = "", city: str = "", state: str = "", zip_code: str = "") -> Any:
    params = {}
    if address1:  params["Address1"] = address1
    if address2:  params["Address2"] = address2
    if city:      params["City"] = city
    if state:     params["State"] = state
    if zip_code:  params["ZipCode"] = zip_code
    return self._request(_PROPERTY_TYPE, params=params)
```

## Contract 3: forms.get_operations()

**Swagger**: GET `/api/job/{jobDisplayId}/form/operations`

```python
# BEFORE (wrong)
if ops_type is not None:
    params["opsType"] = ops_type    # wrong

# AFTER (correct)
if ops_type is not None:
    params["type"] = ops_type       # matches swagger
```

## Contract 4: shipments.request_rate_quotes()

**Swagger**: POST `/api/job/{jobDisplayId}/shipment/ratequotes` with `requestBody`

```python
# BEFORE (wrong — sends query params instead of JSON body)
def request_rate_quotes(self, job_display_id: int, **params: Any) -> Any:
    return self._request(_POST_RATE_QUOTES.bind(jobDisplayId=job_display_id), params=params)

# AFTER (correct — sends JSON request body)
def request_rate_quotes(self, job_display_id: int, data: dict | None = None) -> Any:
    return self._request(_POST_RATE_QUOTES.bind(jobDisplayId=job_display_id), json=data)
```
