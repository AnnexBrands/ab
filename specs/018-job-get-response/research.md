# Research: Complete Job Get Response Model

**Feature**: 018-job-get-response
**Date**: 2026-02-23

## Sources Consulted

### Tier 1: API Server Source Code

- **Controller**: `/src/ABConnect/ACPortal/ABC.ACPortal.WebAPI/Controllers/JobController.cs`
  - `GET /api/job/{jobDisplayId}` returns `JobPortalInfo` via `_jobService.GetJobPortalInfoAsync()`
- **Primary DTO**: `/src/ABConnect/AB.ABCEntities/JobEntities/JobPortalInfo.cs`
  - Defines all top-level fields on the response object
  - Constructor accepts `JobDetails` and populates base fields
- **Service**: `/src/ABConnect/ABC.Services/Impl/JobService.cs`
  - `GetJobPortalInfoAsync()` populates additional fields (items, freight, contacts, payment, etc.)
  - Response shape varies by `JobAccessLevel` (Owner/Customer gets full data; Agent gets filtered)

### Tier 2: Captured Fixtures

- **Fixture**: `tests/fixtures/Job.json` (1333 lines, captured from job 2000000)
  - Contains all 33 top-level keys (6 modeled + 27 unmodeled)
  - Nested structures: contacts (3), items (2 with materials), documents (11), jobSummarySnapshot, activeOnHoldInfo, slaInfo

### Tier 3: Swagger

- Not directly consulted (Tier 1 + Tier 2 provide sufficient coverage for this model-completion task)

## Decisions

### D1: Sub-model naming convention

- **Decision**: Follow the C# entity names from server source, adapted to Python conventions
- **Rationale**: Maximizes traceability between SDK and server source (Tier 1 alignment)
- **Mapping**:
  - `JobPortalInfo` → `Job` (already exists, keep name)
  - `JobContactDetails` → `JobContactDetails`
  - `ContactDetails` (nested in JobContactDetails.contact) → `ContactDetails`
  - `EmailDetails` → `JobContactEmail`
  - `PhoneDetails` → `JobContactPhone`
  - `Items` → `JobItem`
  - `MasterMaterials` → `JobItemMaterial` (reuse existing `JobParcelItemMaterial` if compatible)
  - `JobSummary` → `JobSummarySnapshot`
  - `OnHoldInfo` → `ActiveOnHoldInfo`
  - `DocumentDetails` → `JobDocument`
  - `SlaInfo` → `JobSlaInfo`
  - `FreightTrackingLastDetails` → `JobFreightInfo`
  - `FreightShimpment` → `JobFreightItem`
  - `ShipmentPlanProvider` → kept as-is (already in model scope)
  - `PaymentInfo` → `JobPaymentInfo`
  - `AgentPaymentInfo` → `JobAgentPaymentInfo`
- **Alternatives considered**: Using generic names (e.g., `Contact`, `Document`) — rejected because they'd collide with existing models in contacts.py and documents.py

### D2: Reuse of existing models

- **Decision**: Reuse `CompanyAddress` from `ab.api.models.common` for contact address fields. Reuse `Coordinates` for nested GPS.
- **Rationale**: The `customerContact.address` structure in the fixture exactly matches `CompanyAddress` fields.
- **Alternatives considered**: Creating a separate `JobContactAddress` — rejected because the shapes are identical and the constitution mandates DRY sub-models.

### D3: Handling of `customer`, `pickup`, `delivery` (null fields)

- **Decision**: Keep as `Optional[dict]` per FR-007 — these are null in the current fixture and cannot be validated without real data.
- **Rationale**: Typing them without fixture validation would violate Constitution Principle II (no fabricated data).
- **Alternatives considered**: Typing them speculatively from swagger — rejected per Tier hierarchy (fixture is Tier 2, swagger is Tier 3).

### D4: Contact sub-model depth

- **Decision**: Type 3 levels deep for contacts: `JobContactDetails` → `ContactDetails` (with company as dict) → address/email/phone as typed models. The `contact.company` sub-object within `ContactDetails` stays as `Optional[dict]` since it's a lightweight company summary with no dedicated fixture.
- **Rationale**: The fixture provides concrete data for address/email/phone fields. The nested `company` inside `contact` is a small dict (8 keys) that would require a separate fixture to validate properly.
- **Alternatives considered**: Full 4-level typing including company — deferred until a company-contact fixture is captured.

### D5: JobItem depth

- **Decision**: Type the full ~75 fields from the fixture, including nested `materials` list reusing the existing `JobParcelItemMaterial` model pattern.
- **Rationale**: The fixture provides complete data for 2 items with full material lists. All fields are observable and validatable.
- **Alternatives considered**: Leaving items as dict — rejected because items are the richest data in the Job response and the primary consumer use case.

### D6: Fields from server source not in fixture

- **Decision**: Only model fields that appear in the captured fixture. Fields from server source DTOs that are absent from the fixture (e.g., `jobType` field exists in fixture as null — model it as Optional) will be typed according to the C# type information.
- **Rationale**: Constitution Principle II requires fixture validation. Nullable fields present in the fixture (even as null) are modeled. Fields completely absent from the fixture are not added.
- **Alternatives considered**: Adding all server-source fields proactively — rejected because absent fields suggest they may be conditionally populated based on access level.

### D7: Test assertion strategy

- **Decision**: Enable `assert_no_extra_fields(model)` for top-level Job model AND add recursive checks for key nested sub-models (contacts, items, snapshot, documents).
- **Rationale**: A top-level-only check would miss drift in nested structures. The company model tests already follow this pattern.
- **Alternatives considered**: Top-level only check — rejected because nested dicts could silently accumulate extras.
