# Data Model: 029 — Agent Assignment Helpers

## Entities

### ChangeJobAgentRequest (New — RequestModel)

Outbound request body for POST `/job/{jobDisplayId}/changeAgent`.

| Field | Type | Alias | Required | Description |
|-------|------|-------|----------|-------------|
| service_type | Optional[int] | serviceType | No | Agent service type (0=undefined, 1=pick, 2=pack, 3=pickandpack, 4=delivery) |
| agent_id | Optional[str] | agentId | No | Agent company UUID (resolved from code before sending) |
| recalculate_price | Optional[bool] | recalculatePrice | No | Whether to recalculate job price after agent change |
| apply_rebate | Optional[bool] | applyRebate | No | Whether to apply rebate after agent change |

**Validation**: `extra="forbid"` (RequestModel base). Catches typos in field names at construction time.

**Source**: ABConnectTools `ChangeJobAgentRequest` (C# DTO), confirmed by swagger schema.

---

### ServiceType (New — IntEnum)

Enumeration of agent service types used by the change-agent endpoint.

| Value | Name | Used By |
|-------|------|---------|
| 0 | UNDEFINED | — |
| 1 | PICK | Pick-only operations |
| 2 | PACK | Pack-only operations |
| 3 | PICKANDPACK | Origin Agent (OA) — `oa()` method |
| 4 | DELIVERY | Delivery Agent (DA) — `da()` method |

**Source**: ABConnectTools `ServiceType` enum, confirmed by swagger.

---

### ServiceBaseResponse (Existing — ResponseModel)

Standard success/error wrapper. Already defined in `ab/api/models/shared.py`.

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| success | Optional[bool] | — | Whether the operation succeeded |
| error_message | Optional[str] | errorMessage | Error detail when success is False |
| job_sub_management_status | Optional[dict] | jobSubManagementStatus | Current job sub-management status |

**No changes needed.**

---

## Relationships

```
AgentHelpers ──uses──> CodeResolver (resolve agent code → UUID)
AgentHelpers ──calls──> JobsEndpoint.change_agent() (the route method)
JobsEndpoint.change_agent() ──sends──> ChangeJobAgentRequest (request body)
JobsEndpoint.change_agent() ──receives──> ServiceBaseResponse (response)
```

## File Placement

| Entity | File |
|--------|------|
| ChangeJobAgentRequest | `ab/api/models/jobs.py` (append to existing) |
| ServiceType | `ab/api/models/enums.py` (append to existing) |
| AgentHelpers | `ab/api/helpers/agent.py` (new file) |
| Route + method | `ab/api/endpoints/jobs.py` (add to existing) |
