# Contracts: 018-job-get-response

No new API contracts for this feature. This is a model-completion task — the existing `GET /job/{jobDisplayId}` endpoint is unchanged. The work is entirely in the response model layer (adding fields and sub-models to match the existing API response).

The API contract is defined by:
- **Tier 1**: Server source at `/src/ABConnect/AB.ABCEntities/JobEntities/JobPortalInfo.cs`
- **Tier 2**: Captured fixture at `tests/fixtures/Job.json`
