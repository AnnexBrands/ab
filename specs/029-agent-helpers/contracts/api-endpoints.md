# API Contracts: 029 — Agent Assignment Helpers

## POST /job/{jobDisplayId}/changeAgent

**Surface**: ACPortal
**Route name**: `_POST_CHANGE_AGENT`
**Python method**: `JobsEndpoint.change_agent()`
**Request model**: `ChangeJobAgentRequest`
**Response model**: `ServiceBaseResponse`

### Request

```json
POST /api/api/job/12345/changeAgent
Content-Type: application/json
Authorization: Bearer {token}

{
  "serviceType": 3,
  "agentId": "ed282b80-54fe-4f42-bf1b-69103ce1f76c",
  "recalculatePrice": false,
  "applyRebate": false
}
```

### Response (Success)

```json
HTTP/1.1 200 OK

{
  "success": true,
  "errorMessage": null
}
```

### Response (Error)

```json
HTTP/1.1 200 OK

{
  "success": false,
  "errorMessage": "Agent not found or not valid for this job"
}
```

### Parameters

| Parameter | In | Type | Required | Description |
|-----------|-----|------|----------|-------------|
| jobDisplayId | path | string | Yes | Job display ID (e.g., "12345") |

### Request Body Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| serviceType | integer | No | 0=undefined, 1=pick, 2=pack, 3=pickandpack, 4=delivery |
| agentId | string (UUID) | No | Agent company UUID |
| recalculatePrice | boolean | No | Recalculate job price after change |
| applyRebate | boolean | No | Apply rebate after change |

---

## Helper Methods (AgentHelpers)

### api.jobs.agent.oa(job, agent, ...)

**Maps to**: POST /job/{job}/changeAgent with serviceType=3 (PICKANDPACK)

```python
api.jobs.agent.oa(
    job=12345,                    # Job display ID (int or str)
    agent="3P-5153",              # Agent code or UUID
    recalculate_price=False,      # Optional
    apply_rebate=False,           # Optional
) -> ServiceBaseResponse
```

### api.jobs.agent.da(job, agent, ...)

**Maps to**: POST /job/{job}/changeAgent with serviceType=4 (DELIVERY)

```python
api.jobs.agent.da(
    job=12345,
    agent="9999AZ",
    recalculate_price=False,
    apply_rebate=False,
) -> ServiceBaseResponse
```

### api.jobs.agent.change(job, agent, service_type, ...)

**Maps to**: POST /job/{job}/changeAgent with caller-specified serviceType

```python
api.jobs.agent.change(
    job=12345,
    agent="9999AZ",
    service_type=ServiceType.PICK,   # Or raw int
    recalculate_price=False,
    apply_rebate=False,
) -> ServiceBaseResponse
```
