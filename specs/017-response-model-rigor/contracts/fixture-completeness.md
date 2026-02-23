# Contract: Fixture Completeness Gate

## Context

Every `ExampleEntry` with a `response_model` must also have a `fixture_file`, ensuring that successful API calls capture fixtures for validation testing.

## Contract

### Invariant

For every `runner.add()` call across all `examples/*.py` files:

```
IF response_model IS SET
AND response_model != "bytes"
AND the entry is expected to produce a 200 response
THEN fixture_file MUST BE SET
```

### Naming Convention

| response_model | fixture_file |
|---|---|
| `"SomeModel"` | `"SomeModel.json"` |
| `"List[SomeModel]"` | `"SomeModel.json"` |
| `"PaginatedList[SomeModel]"` | `"SomeModel.json"` |
| `"bytes"` | (none — binary, not JSON-serializable) |
| `"ServiceBaseResponse"` | `"ServiceBaseResponse.json"` (shared) |

### Exemptions

- Entries with `response_model="bytes"` — binary responses cannot be JSON-serialized.
- Entries that are expected to fail (e.g., placeholder IDs like `"PARCEL_ITEM_ID"`) — these won't produce a 200, so no fixture can be captured.

### Enforcement

A test MUST exist that:
1. Imports all example modules
2. Iterates over all `ExampleEntry` instances
3. Asserts that if `response_model` is set (and not `bytes`), `fixture_file` is also set
4. Reports all violating entries with file name, entry name, and response_model
