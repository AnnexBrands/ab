# Contract: Model Typing Rules

## Typing Rules for New Nested Models

1. **All new models inherit from `ResponseModel`** (which sets `extra="allow"` per Constitution Principle I)
2. **All fields are `Optional`** — the API may omit any field depending on context
3. **Field aliases must match exact JSON keys from fixture** — camelCase
4. **C# `Guid` maps to `Optional[str]`** — UUIDs are strings in JSON
5. **C# `decimal` maps to `Optional[float]`** — Python float handles JSON number
6. **C# `DateTime` maps to `Optional[str]`** — ISO 8601 strings in JSON
7. **C# `bool?` maps to `Optional[bool]`**

## Fixture Validation Contract

After model changes, the existing `CompanyDetails.json` fixture MUST pass validation:

```python
from ab.api.models.companies import CompanyDetails
import json

data = json.load(open("tests/fixtures/CompanyDetails.json"))
obj = CompanyDetails.model_validate(data)

# These must work (typed access):
assert obj.company_info.company_id is not None
assert obj.address_data.company is not None
assert obj.overridable_address_data.company.value is not None

# No extra_fields warnings on nested models
```

## Backward Compatibility Contract

- `CompanyDetails` field names unchanged
- `CompanyDetails` field aliases unchanged
- `extra="allow"` on all response models ensures unknown fields don't break deserialization
- Code that previously accessed `obj.company_info` as a dict will break (intentional — users must update to attribute access)
