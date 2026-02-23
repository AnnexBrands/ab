# Contract: List Unwrap Behavior

## Context

`BaseEndpoint._request` handles response model casting. When `response_model="List[X]"`, it expects a JSON array. Some API endpoints return a dict wrapper (e.g., `{modifiedDate: ..., parcelItems: [...]}`).

## Contract

### Input
- `response`: The raw deserialized JSON response from the API (dict or list)
- `is_list`: True (parsed from `response_model="List[X]"`)
- `model_name`: The model class name (e.g., `"ParcelItem"`)
- `route.path`: The endpoint path (for logging)

### Behavior

| Response Type | Action | Return |
|---|---|---|
| `list` | Validate each item as `model_name` | `list[Model]` |
| `dict` with exactly 1 list-valued key | Log warning, unwrap, validate each item | `list[Model]` |
| `dict` with multiple list-valued keys | Find best match by model name, log warning, unwrap, validate | `list[Model]` |
| `dict` with 0 list-valued keys | Log error | `response` (raw dict) |
| Other type | Log error | `response` |

### Model Name Matching (for multiple list keys)

When a dict has multiple list-valued keys, prefer the key that matches `model_name`:
1. Exact match (case-insensitive): key `parcelItems` matches model `ParcelItem`
2. Plural match: key `items` matches any model (fallback)
3. If no match: use first list-valued key

### Warning Format

```
WARNING - List[{model_name}] response wrapped in dict; unwrapped from key '{key}'. Route: {path}
```
