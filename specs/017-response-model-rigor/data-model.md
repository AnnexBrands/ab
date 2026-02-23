# Data Model: Response Model Rigor

This feature primarily modifies existing code rather than introducing new entities. The key entities are already defined; this documents the relationships relevant to this feature.

## Existing Entities (Modified)

### BaseEndpoint._request (ab/api/base.py)

The core dispatch method. Currently at lines 46-99.

**Current behavior** (line 94-97):
```
if is_list:
    if isinstance(response, list):
        return [model_cls.model_validate(item) for item in response]
    return response  # ← BUG: silently returns raw dict
```

**New behavior**:
```
if is_list:
    if isinstance(response, list):
        return [model_cls.model_validate(item) for item in response]
    if isinstance(response, dict):
        items = _unwrap_list_from_dict(response, model_name, route.path)
        return [model_cls.model_validate(item) for item in items]
    return response  # non-dict, non-list — log and return
```

### ExampleEntry (examples/_runner.py)

Dataclass with fields: `name`, `call`, `response_model`, `request_model`, `fixture_file`, `request_fixture_file`.

**Invariant being enforced**: If `response_model` is set, `fixture_file` MUST also be set (unless response is `bytes` or the call is expected to fail).

### Fixture Files (tests/fixtures/)

JSON files named `{ModelName}.json`. Can contain either:
- A single JSON object (for single-model responses)
- A JSON array (for list responses — each element is a model instance)

## Relationships

```
Route.response_model ──→ determines ──→ BaseEndpoint._request behavior
                                              │
                                              ▼
                                    API Response (list or dict-wrapper)
                                              │
                                              ▼
                                    Validated list[Model] or Model
                                              │
                                              ▼
ExampleEntry.fixture_file ──→ _save_fixture ──→ tests/fixtures/{ModelName}.json
                                              │
                                              ▼
                              Fixture validation test ──→ model_validate()
```
