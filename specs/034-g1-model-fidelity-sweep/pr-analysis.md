# PR Analysis: G1 Model Fidelity Sweep

**Branch**: `034-g1-model-fidelity-sweep`
**Date**: 2026-03-15
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md) | **Tasks**: [tasks.md](tasks.md)

## What Changed

This PR closes the G1 (model fidelity) gap for all 21 endpoints that already pass G2 (fixture captured) but fail G1 (extra fields in model). The root cause is a single underdeclared model: `ServiceBaseResponse` (3 fields declared, 16 in the fixture). Expanding it with 13 missing fields brings all 21 endpoints to G1 parity in one atomic change.

### ServiceBaseResponse Expanded (ab/api/models/shared.py)

| Field | Type | Alias | Source |
|-------|------|-------|--------|
| `documents` | `Optional[List[str]]` | — | Fixture: `[]` |
| `errors` | `Optional[dict]` | — | Fixture: `null` |
| `confirm_required` | `Optional[bool]` | `confirmRequired` | Fixture: `false` |
| `notifications` | `Optional[List[str]]` | — | Fixture: `[]` |
| `shipment_id` | `Optional[str]` | `shipmentId` | Fixture: `null` |
| `shipment_accept_identifier` | `Optional[str]` | `shipmentAcceptIdentifier` | Fixture: `null` |
| `weight` | `Optional[ShipmentWeight]` | — | Fixture: `{pounds: 0.0, ...}` |
| `total_net_charge_amount` | `Optional[float]` | `totalNetChargeAmount` | Fixture: `0.0` |
| `currency_code` | `Optional[str]` | `currencyCode` | Fixture: `null` |
| `international_info_required` | `Optional[bool]` | `internationalInfoRequired` | Fixture: `false` |
| `ship_out_date_required` | `Optional[bool]` | `shipOutDateRequired` | Fixture: `false` |
| `fed_ex_express_freight_detail_required` | `Optional[bool]` | `fedExExpressFreightDetailRequired` | Fixture: `false` |
| `carrier_api` | `Optional[int]` | `carrierAPI` | Fixture: `0` |

`ShipmentWeight` (from `ab/api/models/shipments.py`) is reused for the nested `weight` field — no new model class needed.

### Affected Endpoints (21)

All share `response_model="ServiceBaseResponse"`:

| Group | Endpoints |
|-------|-----------|
| Payments (6) | ACHCreditTransfer, attachCustomerBank, banksource, bysource, cancelJobACHVerification, verifyJobACHSource |
| Shipments (5) | shipment DELETE, accessorial POST, accessorial DELETE, book, exportdata |
| Timeline (3) | incrementjobstatus, undoincrementjobstatus, timeline DELETE |
| Jobs (3) | changeAgent, item/notes, item PUT |
| Jobs (1) | parcelitems DELETE |
| Jobs (1) | status/quote |
| Commodity Maps (1) | commodity-map DELETE |
| Views (1) | views DELETE |

### Tests Added (tests/models/test_shared_models.py)

- `test_service_base_response` — loads fixture, validates model, asserts no extra fields
- `test_service_base_response_fields` — verifies key fields populated (success, documents, weight)
- `test_weight_nested_model` — verifies `weight` is a typed `ShipmentWeight` instance with no extra fields

### Gate Baseline Updated (tests/gate_baseline.json)

Added `"G1"` to gate arrays for all 21 endpoints. G1 count: 71 → 92.

### Example Updated (examples/jobs.py)

Added `change_agent` example entry with request model (`ChangeJobAgentRequest`), request fixture, and response model (`ServiceBaseResponse`) references.

### Sphinx Docs Added

| File | Purpose |
|------|---------|
| `docs/api/payments.md` | API docs for PaymentsEndpoint (6 methods) |
| `docs/api/shipments.md` | API docs for ShipmentsEndpoint (methods) |
| `docs/models/payments.md` | Automodule for payment models |
| `docs/models/commodities.md` | Automodule for commodity models |
| `docs/models/views.md` | Automodule for views models |
| `docs/index.md` | Added 8 new entries to api/ and models/ toctrees |

### Other Changes

- `CLAUDE.md`: Updated recent changes list

## Risk Assessment

| Area | Risk | Mitigation |
|------|------|------------|
| ServiceBaseResponse expansion | **Low** — 13 new Optional fields, all backward compatible | All fields default to `None`; no existing code breaks |
| ShipmentWeight import in shared.py | **Low** — cross-module import | `ShipmentWeight` is a stable model with no circular dependency risk |
| ServiceWarningResponse inheritance | **Low** — inherits new fields automatically | Tested via existing fixtures; no extra fields expected |
| Gate baseline ratchet | **Low** — only adds G1 entries | No gates removed; ratchet test validates no regressions |

## Test Results

- **567+ passed**, no new failures or skips
- All 3 ServiceBaseResponse fixture-validation tests pass
- Gate regression test passes with updated baseline

## Spec Coverage

All 4 user stories addressed:
- **US1** (Close G1 Gap): ServiceBaseResponse expanded from 3 to 16 fields — all 21 endpoints pass G1
- **US2** (Test Coverage): 3 fixture-validation tests added in `test_shared_models.py`
- **US3** (Example Coverage): All 21 endpoints confirmed to have example scripts; `change_agent` example added to `jobs.py`
- **US4** (Sphinx Docs): 5 new doc stubs created, toctree updated, zero build warnings
