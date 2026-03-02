# Feature Specification: Reports & Lookups Quality Gates

**Feature Branch**: `027-reports-lookups-gates`
**Created**: 2026-03-01
**Status**: Draft
**Input**: User description: "use C# ground truth to get all /reports and /lookups passing. swagger gives examples. you have userid and company aka franchisee id in constants"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Correct Report Response Models (Priority: P1)

All 8 `/reports` endpoints currently fail G1 (Model Fidelity) and G2 (Fixture Status) because the response models use placeholder dict-based fields instead of the actual flat properties returned by the API. The swagger spec defines concrete field-level schemas for each report response type. Models must be rewritten to match the swagger/C# ground truth, and response fixtures must be captured from the staging API.

**Report endpoints in scope**:
- POST /reports/insurance (InsuranceReport)
- POST /reports/sales (SalesForecastReport)
- POST /reports/sales/summary (SalesForecastSummary)
- POST /reports/salesDrilldown (RevenueCustomer)
- POST /reports/topRevenueCustomers (RevenueCustomer)
- POST /reports/topRevenueSalesReps (RevenueCustomer)
- POST /reports/referredBy (ReferredByReport)
- POST /reports/web2Lead (Web2LeadReport)

**Why this priority**: Reports are the largest block of completely broken models (all 8 fail G1/G2). Fixing them yields the highest gate-count improvement per effort.

**Independent Test**: Run `ex reports <method>` for each endpoint and confirm no "received extras" warnings. Run `python scripts/generate_progress.py` and confirm all 8 report endpoints pass G1 and G2.

**Acceptance Scenarios**:

1. **Given** the InsuranceReport model has fields matching swagger (jobNumber, franchisee, insuranceType, noOfPiece, totalCost, jobDate, insuranceCost, carrier, intacctDate, totalRecords), **When** validated against a captured fixture, **Then** no extra fields remain in `__pydantic_extra__`
2. **Given** all 6 report response models are corrected, **When** the progress report runs, **Then** all 8 report endpoints pass G1 (Model Fidelity)
3. **Given** response fixtures are captured for each report model, **When** the progress report runs, **Then** all 8 report endpoints pass G2 (Fixture Status)

---

### User Story 2 - Correct Extended Lookup Response Models (Priority: P2)

12 extended `/lookup` endpoints (added in 008-extended-operations) fail G1 and G2. Most use `LookupValue` as a generic catch-all model but the actual API responses may differ. The swagger also reveals a DensityClassMap response mismatch (Python expects DensityClassEntry but API returns GuidSequentialRangeValue). Models must be validated against swagger and live responses, fixtures captured.

**Extended lookup endpoints in scope**:
- GET /lookup/{masterConstantKey} (LookupValue)
- GET /lookup/{masterConstantKey}/{valueId} (LookupValue)
- GET /lookup/accessKeys (AccessKey)
- GET /lookup/accessKey/{accessKey} (AccessKey)
- GET /lookup/PPCCampaigns (LookupValue)
- GET /lookup/parcelPackageTypes (ParcelPackageType)
- GET /lookup/documentTypes (LookupValue)
- GET /lookup/comonInsurance (LookupValue)
- GET /lookup/densityClassMap (DensityClassEntry / GuidSequentialRangeValue)
- GET /lookup/referCategory (LookupValue)
- GET /lookup/referCategoryHeirachy (LookupValue)
- GET /lookup/resetMasterConstantCache (operational — may not need fixture)

**Why this priority**: Second largest block of failing endpoints. Many share the LookupValue model so fixing one model can pass multiple gates simultaneously.

**Independent Test**: Run `ex lookup <method>` for each endpoint and confirm no extras. Run progress report and confirm extended lookup endpoints pass G1 and G2.

**Acceptance Scenarios**:

1. **Given** the LookupValue model fields match the live API response, **When** validated against a captured fixture, **Then** no extra fields remain
2. **Given** the DensityClassEntry model is corrected to match the actual API response shape, **When** the densityClassMap fixture is validated, **Then** G1 passes
3. **Given** fixtures are captured for all extended lookup endpoints, **When** the progress report runs, **Then** at least 10 of 12 extended lookup endpoints pass G1 and G2

---

### User Story 3 - Verify Existing Basic Lookup Models (Priority: P3)

4 basic lookup endpoints already pass all gates (contactTypes, countries, jobStatuses, items). However, the swagger reveals minor discrepancies (e.g., ContactTypeEntity has `id` + `value` in swagger but Python model adds `name` + `description`; CountryCodeDto has `code` field not in swagger). Verify these against live responses and fix if any extras are actually present.

**Why this priority**: These already pass gates. Only fix if live responses reveal mismatches the current fixtures don't cover.

**Independent Test**: Re-run the 4 basic lookup examples and confirm they still pass all gates after any model changes.

**Acceptance Scenarios**:

1. **Given** the 4 basic lookup endpoints currently pass all gates, **When** models are re-verified against live responses, **Then** they continue to pass all gates
2. **Given** swagger shows ContactTypeEntity has only `id` + `value`, **When** the live API is checked, **Then** the model is updated to match whichever source is authoritative (live response > swagger per constitution)

---

### Edge Cases

- What happens when a report endpoint returns an empty result set (e.g., no insurance claims in the date range)? The model must handle empty arrays gracefully.
- What happens when the resetMasterConstantCache endpoint returns a non-JSON or void response? This endpoint is operational and may not produce a fixture-worthy response.
- How does the system handle report responses that are lists of flat objects (swagger defines them as arrays) vs single objects?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST replace placeholder report response models (InsuranceReport, SalesForecastReport, SalesForecastSummary, RevenueCustomer, ReferredByReport, Web2LeadReport) with field-level models matching the swagger schema definitions
- **FR-002**: System MUST capture response fixtures from the staging API for all 6 report response models using existing constants (TEST_COMPANY_UUID as franchiseeId, TEST_USER_CONTACT_ID as userId)
- **FR-003**: System MUST validate extended lookup response models (LookupValue, AccessKey, ParcelPackageType, DensityClassEntry) against live API responses and fix any field mismatches
- **FR-004**: System MUST capture response fixtures for all extended lookup endpoints that currently lack them
- **FR-005**: System MUST ensure all nullable fields from swagger are marked Optional in the models, and non-nullable fields are required
- **FR-006**: System MUST use the existing example runner infrastructure to capture fixtures (no manual fixture creation)
- **FR-007**: System MUST update fixture-validation tests to cover newly captured fixtures
- **FR-008**: System MUST maintain backward compatibility — existing passing gates (basic lookups, G3-G6 on reports/lookups) must not regress

### Key Entities

- **InsuranceReport**: Flat record with jobNumber, franchisee, insuranceType, noOfPiece, totalCost, jobDate, insuranceCost, carrier, intacctDate, totalRecords
- **SalesForecastReport**: Flat record with franchisee, company, jobID, jobType, quoteDate, bookedDate, revenue, profit, grossMargin, status, industry, customerZipCode, intacctDate, totalRecords
- **SalesForecastSummary**: Summary with revenue, profit, grossMargin, closeRatio
- **RevenueCustomer**: Simple record with id and name
- **ReferredByReport**: Flat record with referredBy, referredName, referredByCategory, quoteDate, bookedDate, revenue, profit, customer, jobDisplayID, industry, customerZipCode, intacctDate, totalRecords
- **Web2LeadReport**: Flat record with franchiseeID, type, jobDisplayID, intacctStatus, leadDate, companyName, referPage, entryURL, submissionPage, howHeard, email, phone, shipFrom, shipTo, referredName, customerComments, currentBookPrice, currentBookProfit, referredByCategory, totalRecords
- **LookupValue**: Reusable lookup entry (id, name, description, value — verify against live)
- **AccessKey**: Access key entry (key, description — verify against live)
- **ParcelPackageType**: Package type entry (id, name, dimensions — verify against live)
- **DensityClassEntry**: Density class mapping — swagger calls it GuidSequentialRangeValue (rangeEnd, value) — must verify against live response

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 8 report endpoints pass G1 (Model Fidelity) — up from 0/8 currently passing
- **SC-002**: All 8 report endpoints pass G2 (Fixture Status) — up from 0/8 currently passing
- **SC-003**: At least 10 of 12 extended lookup endpoints pass G1 and G2 (resetMasterConstantCache may be excluded as operational)
- **SC-004**: Overall "all gates pass" count increases by at least 15 endpoints (from 50 to 65+)
- **SC-005**: Zero test regressions — pytest pass count remains at 520+ with no new failures
- **SC-006**: No existing passing gates regress (basic lookups remain complete, G3-G6 on reports/lookups remain passing)

## Assumptions

- The staging API is accessible and returns data for report endpoints when called with the existing TEST_COMPANY_UUID and TEST_USER_CONTACT_ID constants
- Report endpoints accept date range parameters; reasonable defaults (e.g., last 365 days) will be used to ensure non-empty responses
- The swagger schema in acportal.json is a reliable guide for field names and types, but live API responses take precedence per constitution Tier 2 > Tier 3
- The resetMasterConstantCache endpoint is a cache-clearing operation and may not produce a meaningful fixture; it can be excluded from G1/G2 targets
- Extended lookup endpoints that return LookupValue share the same response shape and can reuse a single fixture if the model is correct
