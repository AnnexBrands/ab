# Research: CLI Gate Sweep

## Decision 1: CLI Listing Format

**Decision**: Remove route paths from `_list_methods()`, keep them only in `--help`
**Rationale**: Route paths are developer implementation detail. Method listings should be scannable by name. The route is still accessible via `ab payments get --help` for debugging.
**Alternatives considered**:
- Show abbreviated route (e.g., just the path without HTTP method) — still clutters listing
- Add a `--verbose` flag to toggle route display — over-engineering for this use case

## Decision 2: Constant Naming Convention

**Decision**: Use `path_param_to_constant()` deterministic convention: camelCase → TEST_SCREAMING_SNAKE
**Rationale**: Already implemented in `ab/cli/route_resolver.py:68-79`. Ensures consistency across all constants.
**Examples**:
- `jobDisplayId` → `TEST_JOB_DISPLAY_ID` (exists)
- `historyAmount` → `TEST_HISTORY_AMOUNT` (needs adding, default: 3)
- `rfqId` → `TEST_RFQ_ID` (needs chain discovery)
- `contactId` → `TEST_CONTACT_ID` (exists: 30760)
- `taskCode` → `TEST_TASK_CODE` (needs research)
- `timelineTaskIdentifier` → `TEST_TIMELINE_TASK_IDENTIFIER` (needs chain discovery)
- `templateId` → `TEST_TEMPLATE_ID` (needs research)
- `shipmentPlanId` → `TEST_SHIPMENT_PLAN_ID` (needs chain discovery)

## Decision 3: Chain Discovery Pattern

**Decision**: For missing IDs, call parent listing endpoints with known constants, extract IDs from response
**Rationale**: Some IDs (rfqId, timelineTaskIdentifier) only exist in the context of a parent resource. Hardcoding staging-specific IDs is fragile. Listing the parent and extracting is self-documenting.
**Pattern**:
```python
# In examples/jobs.py, discover rfqId by listing RFQs for our test job
rfqs = api.jobs.get_rfqs(TEST_JOB_DISPLAY_ID)
if rfqs:
    rfq_id = rfqs[0].id  # Use first available
    runner.add("get_rfq_details", lambda api: api.jobs.get_rfq(rfq_id), ...)
```
**Fallback**: If listing returns empty, skip the dependent example with a clear message.

## Decision 4: "Received Extras" Handling

**Decision**: Follow constitution principle I — ResponseModel uses `extra="allow"`, extras are logged via `model_post_init`. Fix models by adding missing fields from swagger/fixtures.
**Rationale**: The constitution explicitly states response models MUST use `extra="allow"` so new API fields don't break deserialization. But we should still add known fields for completeness.
**Process**:
1. Run example, observe logged extras
2. Check swagger for field definitions
3. Add fields to model with correct types and optionality
4. Re-run to confirm no more extras logged

## Decision 5: Gate Evaluation Scope

**Decision**: Focus on gates G1 (Model Fidelity), G2 (Fixture Status), G3 (Test Quality), and G5 (Param Routing). G4 (Doc Accuracy) and G6 (Request Quality) are lower priority.
**Rationale**: G1-G3 directly measure whether an endpoint has a working model, fixture, and test. G5 measures parameter correctness. G4/G6 are documentation/typing concerns better addressed in a dedicated docs sweep.

## Current Gate Status (Baseline)

| Gate | Passing | Total | Rate |
|------|---------|-------|------|
| G1 Model Fidelity | 2 | 231 | 0.9% |
| G2 Fixture Status | 2 | 231 | 0.9% |
| G3 Test Quality | 6 | 231 | 2.6% |
| G4 Doc Accuracy | 5 | 231 | 2.2% |
| G5 Param Routing | 216 | 231 | 93.5% |
| G6 Request Quality | 21 | 231 | 9.1% |
| All Gates | 0 | 231 | 0% |

## G5 Failures (10 endpoints)

1. `/Catalog` — Seller, Catalog, Web2Lead module inference issue
2. `/Seller` — same
3. `/Web2Lead/get` — same
4. `/job/{jobDisplayId}/form/bill-of-lading` — missing params_model
5. `/job/{jobDisplayId}/form/invoice` — missing params_model
6. `/job/{jobDisplayId}/form/operations` — missing params_model
7. `/job/{jobDisplayId}/form/packaging-labels` — missing params_model
8. `/job/{jobDisplayId}/form/usar` — missing params_model
9. `/job/{jobDisplayId}/payment` — missing params_model for jobSubKey
10. `/job/{jobDisplayId}/shipment/ratequotes` — missing params_model (RateQuotesParams exists but not wired)
