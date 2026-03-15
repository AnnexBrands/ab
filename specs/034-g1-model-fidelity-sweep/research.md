# Research: G1 Model Fidelity Sweep

**Feature**: 034-g1-model-fidelity-sweep
**Date**: 2026-03-15

## Key Finding: Single Model Root Cause

### Decision: Expand `ServiceBaseResponse` only
**Rationale**: All 21 G1-failing endpoints share a single response model (`ServiceBaseResponse` in `ab/api/models/shared.py`). The model declares 3 fields; the fixture contains 16. Expanding this one model fixes all 21 endpoints.
**Alternatives considered**:
- Create per-endpoint response subclasses (rejected: all 21 endpoints return the same shape; subclasses would add complexity without value)
- Use `model_config = ConfigDict(extra="ignore")` to suppress warnings (rejected: violates Principle I — drift becomes invisible)

## Field Gap Analysis

### Current Model (3 fields)

| Field | Type | Alias |
|-------|------|-------|
| `success` | `Optional[bool]` | — |
| `error_message` | `Optional[str]` | `errorMessage` |
| `job_sub_management_status` | `Optional[dict]` | `jobSubManagementStatus` |

### Fixture Fields (16 total, 13 undeclared)

| Field | JSON Key | Fixture Value | Proposed Type | Notes |
|-------|----------|---------------|---------------|-------|
| `success` | `success` | `false` | Already declared | — |
| `error_message` | `errorMessage` | `"Specified provider..."` | Already declared | — |
| `documents` | `documents` | `[]` | `Optional[List[str]]` | Document URLs from operation |
| `errors` | `errors` | `null` | `Optional[dict]` | Error detail object |
| `confirm_required` | `confirmRequired` | `false` | `Optional[bool]` | User confirmation needed |
| `notifications` | `notifications` | `[]` | `Optional[List[str]]` | User notification messages |
| `shipment_id` | `shipmentId` | `null` | `Optional[str]` | Shipment UUID |
| `shipment_accept_identifier` | `shipmentAcceptIdentifier` | `null` | `Optional[str]` | Carrier acceptance ref |
| `weight` | `weight` | `{pounds, ...}` | `Optional[ShipmentWeight]` | Reuse existing model |
| `total_net_charge_amount` | `totalNetChargeAmount` | `0.0` | `Optional[float]` | Total charge |
| `currency_code` | `currencyCode` | `null` | `Optional[str]` | Currency (e.g., USD) |
| `international_info_required` | `internationalInfoRequired` | `false` | `Optional[bool]` | Intl info flag |
| `ship_out_date_required` | `shipOutDateRequired` | `false` | `Optional[bool]` | Ship date flag |
| `fed_ex_express_freight_detail_required` | `fedExExpressFreightDetailRequired` | `false` | `Optional[bool]` | FedEx detail flag |
| `carrier_api` | `carrierAPI` | `0` | `Optional[int]` | Carrier API code |

### Nested Object: `weight`

The `weight` field maps to `ShipmentWeight` already defined in `ab/api/models/shipments.py:116`:

```python
class ShipmentWeight(ResponseModel):
    pounds: Optional[float] = Field(None, description="Weight in pounds")
    original_weight: Optional[float] = Field(None, alias="originalWeight", ...)
    original_weight_measure_unit: Optional[str] = Field(None, alias="originalWeightMeasureUnit", ...)
```

Fixture `weight` value matches exactly: `{"pounds": 0.0, "originalWeight": null, "originalWeightMeasureUnit": null}`.

**Decision**: Import and reuse `ShipmentWeight` rather than creating a new model.
**Rationale**: Same shape, same source API. Avoids duplication per constitution Principle I (mixin-based composition).
**Alternatives considered**: Create a `ServiceWeight` alias (rejected: identical fields, unnecessary indirection).

## `jobSubManagementStatus` Typing

### Decision: Keep as `Optional[dict]` for now
**Rationale**: The field is declared in the model but absent from the captured fixture. No fixture evidence exists to determine its exact structure. Typing it further would require a live capture showing a non-null value.
**Alternatives considered**: Remove the field (rejected: it was explicitly added in a prior feature; may appear in other endpoints' responses).

## Examples Audit

### Decision: All examples already exist and cover the 21 endpoints
**Rationale**: Every affected endpoint group has a corresponding example script that calls the endpoint:
- `examples/payments.py` — covers all 6 payment endpoints
- `examples/shipments.py` — covers all 5 shipment endpoints
- `examples/timeline.py` — covers all 3 timeline endpoints (increment, undo, delete)
- `examples/jobs.py` — covers changeAgent, item/notes, item update
- `examples/commodities.py` — covers commodity-map DELETE
- `examples/views.py` — covers views DELETE
- `examples/parcels.py` — covers parcelitems DELETE

No new example scripts needed. Examples reference the endpoint methods, not the response model fields directly, so no updates required for the model expansion.

## Documentation Gaps

### Decision: Create missing Sphinx doc stubs for payments, shipments, commodities, views
**Rationale**: Constitution Principle VI requires Sphinx docs for all public models and endpoints. Currently missing:
- `docs/api/payments.md` — no dedicated API docs
- `docs/api/shipments.md` — no dedicated API docs
- `docs/models/payments.md` — no model docs
- `docs/models/commodities.md` — no model docs
- `docs/models/views.md` — no model docs

Existing `docs/models/common.md` and `docs/models/jobs.md` use `automodule` directives which will automatically pick up expanded fields.

**Alternatives considered**: Document only ServiceBaseResponse (rejected: Principle VI requires completeness, and these gaps predate this feature).

## Test Strategy

### Decision: Add `test_service_base_response` fixture-validation test
**Rationale**: G3 requires tests that load the fixture, validate the model, and assert no extra fields. A single test covers all 21 endpoints since they share the model.
**Alternatives considered**: Per-endpoint tests (rejected: redundant — same model, same fixture, same validation logic).

## Gate Baseline Update

### Decision: Update `tests/gate_baseline.json` after model expansion
**Rationale**: The ratchet test compares current gate results against the baseline. Adding G1 to all 21 endpoint entries ensures the ratchet prevents future regression.
**Process**: Run gate evaluation after model expansion, capture new baseline, commit.
