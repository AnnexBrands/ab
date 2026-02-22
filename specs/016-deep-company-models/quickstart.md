# Quickstart: Deep Pydantic Models for Company Response

## Before (dict access — the problem)

```python
from ab import ABConnectAPI

api = ABConnectAPI()
company = api.companies.get_details("ELABEL")

# Forced to use dict bracket access — no autocomplete, no type safety
company_id = company.company_info["companyId"]  # KeyError risk
address = company.address_data["addressLine1"]   # No IDE help
override = company.overridable_address_data["company"]["value"]  # Nested dict hell
```

## After (typed attribute access — the fix)

```python
from ab import ABConnectAPI

api = ABConnectAPI()
company = api.companies.get_details("ELABEL")

# Full attribute access with autocomplete and type checking
company_id = company.company_info.company_id        # str
address = company.address_data.address_line1         # str
override = company.overridable_address_data.company.value  # str

# Nested models are properly typed
main_addr = company.company_info.main_address        # CompanyAddress
lat = main_addr.latitude                              # float

# Override pattern fields
field = company.overridable_address_data.company
print(field.default_value)    # "Navis Pack & Ship #14004OH"
print(field.override_value)   # None
print(field.force_empty)      # False
print(field.value)            # "Navis Pack & Ship #14004OH"
```

## Validation Test

```python
# Load fixture and verify typed access works
import json
from ab.api.models.companies import CompanyDetails

data = json.load(open("tests/fixtures/CompanyDetails.json"))
obj = CompanyDetails.model_validate(data)

# All nested objects are pydantic models, not dicts
assert hasattr(obj.company_info, "company_id")
assert hasattr(obj.address_data, "address_line1")
assert hasattr(obj.overridable_address_data.company, "value")
```
