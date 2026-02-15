# Data Model: Verify Artifact Integrity

## Entities

### Endpoint Claim

An assertion about an endpoint's status in a tracking document.

| Field | Type | Description |
|-------|------|-------------|
| endpoint_path | string | API path (e.g., `/address/isvalid`) |
| http_method | string | GET, POST, PUT, DELETE |
| claimed_status | enum | `captured`, `needs-request-data`, `done`, `pending` |
| source_document | string | File where claim appears (FIXTURES.md, api-surface.md) |
| model_name | string | Pydantic model name (e.g., `AddressIsValidResult`) |
| fixture_file | string | Expected fixture filename (e.g., `AddressIsValidResult.json`) |

### Audit Finding

A discrepancy between a claim and ground truth.

| Field | Type | Description |
|-------|------|-------------|
| endpoint_path | string | API path of the discrepancy |
| claimed_status | string | What the document says |
| actual_status | string | What reality shows |
| failure_reason | string | Why the claim is wrong |
| source_document | string | Which document has the wrong claim |
| action | string | What correction is needed |

### Status Transitions

```
captured ──(fixture missing)──→ needs-request-data
captured ──(example errors)──→ needs-request-data
done ──(no example exists)──→ pending
done ──(example errors)────→ pending
```

No transitions in the other direction — this audit only
downgrades, never promotes.
