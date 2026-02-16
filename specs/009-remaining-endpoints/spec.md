# Feature Specification: Remaining API Endpoints

**Feature Branch**: `009-remaining-endpoints`
**Created**: 2026-02-14
**Status**: Complete
**Input**: User description: "Implement remaining ACPortal and ABC API endpoints to achieve full SDK coverage"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Admin Configuration Access (Priority: P1)

A developer building an internal admin tool needs to programmatically manage company setup — configuring brands, geographic regions, carrier assignments, and packaging options. Today they must use the ACPortal web UI manually for each change. With SDK coverage of Company Setup endpoints, they can automate bulk configuration tasks.

**Why this priority**: Company Setup (18 endpoints) is the largest remaining group and enables administrative automation, which is a key driver for SDK adoption in internal tooling.

**Independent Test**: Can be fully tested by calling company setup endpoints with valid configuration data and verifying the SDK returns properly typed responses.

**Acceptance Scenarios**:

1. **Given** a valid SDK client, **When** the developer calls a company setup endpoint, **Then** the SDK returns a typed response matching the API schema
2. **Given** an invalid configuration payload, **When** the developer calls a company setup endpoint, **Then** the SDK raises a descriptive error

---

### User Story 2 - Admin Settings Management (Priority: P1)

A developer maintaining an ACPortal deployment needs to read and update system-level settings programmatically — including application preferences, feature flags, and operational parameters. The SDK should expose Admin Settings endpoints so these can be managed via scripts and CI/CD pipelines rather than manual UI interaction.

**Why this priority**: Admin Settings (13 endpoints) is the second-largest remaining group and is essential for deployment automation and environment management.

**Independent Test**: Can be fully tested by calling admin settings endpoints and verifying typed responses are returned with correct field structures.

**Acceptance Scenarios**:

1. **Given** a valid SDK client with admin credentials, **When** the developer retrieves admin settings, **Then** the SDK returns typed settings objects
2. **Given** a settings update request, **When** the developer submits valid changes, **Then** the SDK confirms the update and returns the modified settings

---

### User Story 3 - Account and Authentication Operations (Priority: P2)

A developer building a user provisioning system needs to manage accounts and authentication flows programmatically — creating users, managing sessions, resetting credentials. These endpoints complete the auth story beyond the existing basic user CRUD.

**Why this priority**: Account/Auth (10 endpoints) fills a gap in the existing user management surface and is needed for complete provisioning workflows.

**Independent Test**: Can be fully tested by invoking account/auth endpoints and verifying the SDK handles authentication-related request/response patterns correctly.

**Acceptance Scenarios**:

1. **Given** a valid SDK client, **When** the developer calls an account management endpoint, **Then** the SDK returns properly typed account data
2. **Given** invalid credentials in a request, **When** the developer calls an auth endpoint, **Then** the SDK raises an appropriate authentication error

---

### User Story 4 - Miscellaneous Job Operations (Priority: P2)

A developer building custom job processing workflows needs access to the remaining job-related endpoints not covered in Features 001 and 008 — including specialized job actions, extended status queries, and supplementary job data. These fill the final gaps in job lifecycle coverage.

**Why this priority**: Job Misc (9 endpoints) completes full job lifecycle coverage, which is the SDK's core value proposition.

**Independent Test**: Can be fully tested by calling the remaining job endpoints and verifying typed response models match the API schema.

**Acceptance Scenarios**:

1. **Given** an existing job, **When** the developer calls a miscellaneous job endpoint, **Then** the SDK returns typed job data
2. **Given** a job action endpoint, **When** the developer submits a valid action, **Then** the SDK confirms the action and returns the updated state

---

### User Story 5 - Physical Resource Management (Priority: P3)

A developer integrating with logistics systems needs to manage materials and trucks programmatically — querying available materials, managing truck assignments, and tracking physical resources tied to jobs.

**Why this priority**: Materials/Trucks (8 endpoints) supports logistics integrations but is a lower-frequency use case.

**Independent Test**: Can be fully tested by calling materials/trucks endpoints and verifying typed responses.

**Acceptance Scenarios**:

1. **Given** a valid SDK client, **When** the developer queries materials or trucks, **Then** the SDK returns typed resource data

---

### User Story 6 - Integration and Communication Endpoints (Priority: P3)

A developer building integrations with external systems needs access to the remaining endpoint groups: Webhooks (6), SMS Templates (5), Intacct accounting integration (5), E-Sign (2), Notifications (1), and remaining ABC endpoints (7). These enable event-driven architectures, communication template management, accounting sync, and electronic signature workflows.

**Why this priority**: These are specialized integration endpoints used by specific workflows rather than general-purpose SDK operations.

**Independent Test**: Can be fully tested by calling each integration endpoint group and verifying typed responses match the API schema.

**Acceptance Scenarios**:

1. **Given** a valid SDK client, **When** the developer calls a webhook management endpoint, **Then** the SDK returns typed webhook configuration data
2. **Given** a valid SDK client, **When** the developer calls an SMS template endpoint, **Then** the SDK returns typed template data
3. **Given** a valid SDK client, **When** the developer calls an Intacct integration endpoint, **Then** the SDK returns typed accounting data

---

### User Story 7 - Extended CRUD Operations (Priority: P3)

A developer needs access to the remaining extended CRUD operations for existing entity types: Address extensions (2), Document extensions (2), and User extensions (1). These complete the CRUD surface for entities already partially covered.

**Why this priority**: These are small incremental additions to existing endpoint groups and round out existing coverage.

**Independent Test**: Can be fully tested by calling extended CRUD endpoints and verifying typed responses.

**Acceptance Scenarios**:

1. **Given** an existing entity, **When** the developer calls an extended CRUD endpoint, **Then** the SDK returns properly typed data consistent with the existing entity models

---

### Edge Cases

- What happens when an endpoint requires admin-level permissions the current token does not have?
- How does the SDK handle endpoints that return empty responses (204 No Content)?
- What happens when an Intacct or E-Sign integration endpoint is called but the tenant lacks the corresponding integration?
- How does the SDK handle deprecated or undocumented query parameters found only in swagger but not in the live API?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: SDK MUST expose all remaining ACPortal endpoints (95) as typed, callable methods organized by functional group
- **FR-002**: SDK MUST expose all remaining ABC endpoints (7) as typed, callable methods
- **FR-003**: Each new endpoint MUST have a corresponding Route definition with HTTP method, path, and response model
- **FR-004**: Each new endpoint MUST have a typed response model derived from the swagger specification
- **FR-005**: New endpoint methods MUST follow the established `**kwargs` signature pattern with optional `request_model` and `params_model` on Route
- **FR-006**: New endpoints MUST be organized into endpoint files following established conventions (one file per logical group, extending existing files where appropriate)
- **FR-007**: Each new endpoint MUST have a fixture validation test that can skip gracefully when no response fixture is captured yet
- **FR-008**: Each new endpoint MUST be tracked in FIXTURES.md using the unified 4D format (Req Model, Req Fixture, Resp Model, Resp Fixture)
- **FR-009**: SDK MUST maintain backward compatibility — no existing endpoint signatures, models, or imports may change
- **FR-010**: New endpoints MUST include example scripts demonstrating basic usage for each functional group

### Key Entities

- **Route**: Endpoint definition with method, path, response model, request_model, and params_model
- **Endpoint Group**: Logical grouping of related endpoints in a single file (e.g., `admin.py`, `webhooks.py`)
- **Response Model**: Typed representation of the API response for each endpoint
- **Request Model**: Typed representation of request parameters (where applicable)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: ACPortal API coverage reaches 100% (299/299 endpoints callable through the SDK)
- **SC-002**: ABC API coverage reaches 100% (12/12 endpoints callable through the SDK)
- **SC-003**: Every new endpoint has a fixture validation test (pass or skip-with-reason)
- **SC-004**: All existing tests continue to pass with no regressions
- **SC-005**: FIXTURES.md tracking is complete for all endpoints (226 existing + 102 new = 328 total)
- **SC-006**: Each new endpoint group has at least one example script demonstrating usage
- **SC-007**: SDK installs and imports without errors after all additions

## Assumptions

- The swagger specifications in `ab/api/schemas/` accurately reflect the remaining endpoints
- The established patterns from Features 001, 007, and 008 (Route definitions, `**kwargs` signatures, typed models, fixture validation) apply unchanged to all remaining endpoints
- Endpoint groupings follow the categories identified in the project-state.md gap analysis
- Response fixtures will be captured separately by running examples against a staging environment (not part of this feature's implementation scope)
- The feature will be implemented in phases (multiple PRs) to keep review scope manageable, following the same pattern as Features 001 and 008

## Scope Boundaries

### In Scope

- All 95 remaining ACPortal endpoints across 30 swagger tag groups: Company Setup (Calendar, External Accounts, Document Templates, Settings, Container Thickness, Material, Truck, Planner), Admin (Advanced Settings, Carrier Error Messages, Global Settings, Log Buffer), Account, Extended Jobs (misc, booking, tracking v2, e-sign), Integrations (Intacct, Webhooks), Communication (SMS Templates, Notifications), Extended Entities (Companies, Contacts, Address, Documents, Users), Values
- All 7 remaining ABC endpoints (Test diagnostics, Web2Lead v2, AutoPrice v1, LogBuffer, Report)
- Route definitions, response models, request models (where needed), fixture validation tests, example scripts, FIXTURES.md tracking
- Documentation pages for new endpoint groups

### Out of Scope

- Capturing response fixtures from staging (separate operational task)
- Modifying existing endpoints or models
- Adding new SDK core features (client, auth, HTTP layer changes)
- Performance optimization or caching
- Integration testing against live APIs

## Dependencies

- Feature 001 (SDK core, merged)
- Feature 007 (request model methodology, merged)
- Feature 008 (extended operations, merged)
- Swagger specifications must be current and accurate
