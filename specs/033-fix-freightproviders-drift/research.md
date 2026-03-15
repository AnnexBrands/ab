# Research: Fix FreightProviders Drift

**Feature**: 033-fix-freightproviders-drift
**Date**: 2026-03-15

## R1: PricedFreightProvider Response Shape

**Decision**: Expand from 3 stub fields to 15 typed fields per ACPortal swagger schema, plus nested `CarrierAccountInfo` model and `CarrierAPI` enum.

**Rationale**: The swagger schema at `ab/api/schemas/acportal.json` (line 21112) defines 15 properties for the PricedFreightProvider response. The live API confirms this — CLI calls produce "extra fields not in model" warnings for every field beyond the 3 stubs. Constitution I (Model Fidelity) requires all response fields be typed.

**Alternatives considered**:
- Keep `dict` fields and suppress warnings — rejected: violates Constitution I and hides drift.
- Model only the fields the user currently accesses — rejected: other SDK consumers would hit the same warnings.

**Swagger-defined fields** (15 fields):

| Field | Type | Nullable | Alias |
|-------|------|----------|-------|
| optionIndex | int | No | optionIndex |
| shipmentType | str (UUID) | No | shipmentType |
| providerAPI | CarrierAPI (int enum) | No | providerAPI |
| providerId | str (UUID) | Yes | providerId |
| providerCode | str | Yes | providerCode |
| providerCompanyName | str | Yes | providerCompanyName |
| totalSell | float | No | totalSell |
| transit | int | Yes | transit |
| quoteNo | str | Yes | quoteNo |
| proNum | str | Yes | proNum |
| optionActive | bool | No | optionActive |
| shipmentAccepted | bool | No | shipmentAccepted |
| shipmentAcceptedDate | str (datetime) | Yes | shipmentAcceptedDate |
| obtainNFMJobState | str | Yes | obtainNFMJobState |
| usedCarrierAccountInfo | CarrierAccountInfo | No | usedCarrierAccountInfo |

**Nested model — CarrierAccountInfo** (3 fields):

| Field | Type | Nullable |
|-------|------|----------|
| id | int | No |
| key | str | Yes |
| friendlyName | str | Yes |

**CarrierAPI enum values**: 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14, 20

## R2: ShipmentPlanProvider Request Shape

**Decision**: Expand from 1 stub field (`provider_data: dict`) to 22 typed fields per swagger schema.

**Rationale**: The current model has a single `Optional[dict]` field which completely bypasses `extra="forbid"` validation (Constitution IX). Swagger defines 22 distinct fields including nested `CarrierAccountInfo` and `CarrierAPI`.

**Alternatives considered**:
- Keep `dict` and rely on server-side validation — rejected: violates Constitution IX; the API silently ignores unrecognized fields.

**Swagger-defined fields** (22 fields):

| Field | Type | Nullable | Alias |
|-------|------|----------|-------|
| jobID | str (UUID) | Yes | jobID |
| freightQuoteOptionsId | str (UUID) | Yes | freightQuoteOptionsId |
| providerID | str (UUID) | Yes | providerID |
| isPrimary | bool | No | isPrimary |
| providerCompanyCode | str | Yes | providerCompanyCode |
| providerCompanyName | str | Yes | providerCompanyName |
| originalCompanyName | str | Yes | originalCompanyName |
| freightAmount | float | No | freightAmount |
| accessorialAmount | float | No | accessorialAmount |
| cafNote | str | Yes | cafNote |
| quoteNo | str | Yes | quoteNo |
| proNum | str | Yes | proNum |
| transit | int | Yes | transit |
| shipmentType | str (UUID) | Yes | shipmentType |
| miles | float | No | miles |
| logo | str | Yes | logo |
| optionIndex | int | No | optionIndex |
| optionActive | bool | No | optionActive |
| shipmentAccepted | bool | No | shipmentAccepted |
| shipmentAcceptedDate | str (datetime) | Yes | shipmentAcceptedDate |
| usedAPI | CarrierAPI (int enum) | No | usedAPI |
| billToFranchiseeId | str (UUID) | Yes | billToFranchiseeId |
| billToCompanyCode | str | Yes | billToCompanyCode |
| obtainNFMJobState | str | Yes | obtainNFMJobState |
| usedCarrierAccountInfo | CarrierAccountInfo | No | usedCarrierAccountInfo |

## R3: RateQuoteRequest Shape

**Decision**: Expand to match swagger `SetRateModel` schema — 4 typed fields.

**Rationale**: Swagger at `ab/api/schemas/acportal.json` (line 23101) defines the `SetRateModel` schema used by POST ratequote. The 4 fields are: `ratesKey` (str, required), `carrierCode` (str, required), `carrierAccountId` (int, nullable), `active` (bool, nullable).

**Alternatives considered**: N/A — swagger is clear and authoritative for this schema.

## R4: FreightItemsRequest Shape

**Decision**: Expand to match swagger `SaveAllFreightItemsRequest` schema — 3 fields with nested `FreightShipment` (24 fields, mapped from swagger's `FreightShimpment`).

**Rationale**: Swagger at `ab/api/schemas/acportal.json` (line 21857) defines `SaveAllFreightItemsRequest` with `jobModifiedDate`, `forceUpdate`, and `freightItems` (array of `FreightShimpment`). The `FreightShimpment` schema (line 17996) has 24+ properties covering dimensions, identifiers, and metadata. Note: swagger has a typo "Shimpment"; our model uses corrected spelling `FreightShipment`.

## R5: Progress Artifact Drift

**Decision**: Update `api-surface.md` "AB done" counter from "0 of 3" to reflect reality. Regenerate FIXTURES.md and progress.html after model/fixture updates.

**Rationale**: The endpoints have been implemented since feature 008 but `api-surface.md` was never updated. FIXTURES.md gates pass falsely because the empty fixture causes test skips, which the gate evaluator interprets as "no failures" rather than "no data."

**Root cause chain**:
1. Empty fixture `[]` → `first_or_skip()` calls `pytest.skip()` → test reports as "skipped" not "failed"
2. Gate evaluator sees "no failures" for skipped tests → marks G3 (Test Quality) as PASS
3. G1 (Model Fidelity) evaluator checks model exists and has fields → PASS (doesn't validate against real data)
4. G2 (Fixture Status) checks fixture file exists → PASS (file exists, even though it's `[]`)
5. All gates pass → status = "complete" in FIXTURES.md
6. Progress.html renders from FIXTURES.md → shows 100% passing

**Fix**: After expanding models and capturing real fixtures, regenerate both artifacts. Gates will then evaluate against real data.

## R6: api-surface.md "AB done" Counter

**Decision**: The "AB" column in the api-surface.md table uses "—" to mean "not done" and specific markers for done status. The "AB done: X of Y" line at the end of each group is a manual counter. Update the freight section to mark all 3 endpoints as done.

**Rationale**: Code exists for all 3 endpoints (routes, methods, models, example). The counter should reflect this.
