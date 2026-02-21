# Feature Specification: Update Constitution — Sources of Truth Hierarchy

**Feature Branch**: `010-update-constitution`
**Created**: 2026-02-21
**Status**: Draft
**Input**: User description: "update our constitution - we check swagger, and true fixtures received are a good source of truth. the ultimate source of truth is /usr/src/ABConnect (or /src/ABConnect)--this is the actual API server."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer Resolves Conflicting API Information (Priority: P1)

A developer (human or AI agent) encounters a discrepancy between what swagger says, what a captured fixture shows, and how the actual API server behaves. Today the constitution says "swagger is reference, not authoritative" and "models MUST be validated against real API responses," but it doesn't name the API server source code as the definitive authority or establish a clear precedence order. The developer needs an unambiguous hierarchy to resolve the conflict quickly and correctly.

**Why this priority**: Without a clear hierarchy, developers waste time debating which source to trust, or worse, silently encode wrong behavior into models. This is the core problem the feature solves.

**Independent Test**: Can be fully tested by reviewing the updated constitution and confirming the hierarchy is documented, unambiguous, and referenced from relevant principles.

**Acceptance Scenarios**:

1. **Given** a developer reads the constitution, **When** they look for guidance on resolving a swagger-vs-fixture-vs-server discrepancy, **Then** they find a clearly ordered hierarchy of sources of truth.
2. **Given** swagger declares a field type that contradicts the actual server response, **When** a developer consults the hierarchy, **Then** the hierarchy tells them the server code is the ultimate authority, fixtures are the next best evidence, and swagger is informational.
3. **Given** an AI agent is researching an endpoint during DISCOVER Phase D, **When** it encounters conflicting information, **Then** the constitution directs it to prioritize sources in the documented order.

---

### User Story 2 - Agent Uses Server Source for Deep Research (Priority: P2)

An AI agent working through the DISCOVER workflow needs to understand an endpoint's true behavior — what parameters it actually accepts, what response shape it returns, what validation it performs. The constitution should direct the agent to consult the API server source code at `/usr/src/ABConnect` (or `/src/ABConnect`) as the ultimate authority when swagger or fixtures are ambiguous or incomplete.

**Why this priority**: The API server source code has always been the ground truth, but it was never named in the constitution. Codifying it ensures agents and developers know where to look when other sources fall short.

**Independent Test**: Can be tested by confirming the constitution references the server source paths and that the DISCOVER workflow's Phase D research steps include consulting the server source.

**Acceptance Scenarios**:

1. **Given** the constitution is updated, **When** an agent reads the sources of truth section, **Then** it finds `/usr/src/ABConnect` (or `/src/ABConnect`) named as the ultimate source of truth with a description of what it contains.
2. **Given** a developer cannot determine an endpoint's behavior from swagger alone, **When** they follow the constitution's guidance, **Then** they know to check the server source code before making assumptions.

---

### User Story 3 - Existing Principles Reference the Hierarchy (Priority: P3)

The existing principles (especially II, IV, and IX) already reference swagger and fixtures but don't cross-reference a unified hierarchy. After the update, these principles should point back to the hierarchy so the constitution reads as a coherent whole.

**Why this priority**: Consistency within the constitution prevents future misinterpretation. Lower priority because the hierarchy itself (P1) delivers the core value even without cross-references.

**Independent Test**: Can be tested by reading Principles II, IV, and IX and confirming they reference the sources of truth hierarchy where appropriate.

**Acceptance Scenarios**:

1. **Given** the constitution is updated, **When** a reader encounters Principle IV ("Swagger-Informed, Reality-Validated"), **Then** it references the sources of truth hierarchy for the full precedence order.
2. **Given** the constitution is updated, **When** a reader encounters Principle II (fixture capture), **Then** captured fixtures are contextualized within the hierarchy as a strong source of truth validated against real API behavior.

---

### Edge Cases

- What happens when the server source code at `/usr/src/ABConnect` is not accessible (e.g., CI environment without the server repo)? The hierarchy should degrade gracefully — use fixtures as the best available evidence, then swagger.
- What happens when the server source code and a captured fixture disagree? The server source wins — the fixture may have been captured from an older API version.
- What happens when neither server source nor fixtures are available for a new endpoint? Swagger becomes the starting reference, with the endpoint tracked as needing validation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The constitution MUST include a new section defining the sources of truth hierarchy with explicit precedence order: (1) API server source code, (2) captured fixtures from real API responses, (3) swagger specifications.
- **FR-002**: The hierarchy MUST name the API server source code paths (`/usr/src/ABConnect` or `/src/ABConnect`) and describe what they contain (the actual API server implementation — controllers, models, and business logic).
- **FR-003**: The hierarchy MUST describe when each source is most useful: server source for definitive behavior, fixtures for validated response shapes, swagger for endpoint discovery and parameter naming.
- **FR-004**: The hierarchy MUST include a degradation policy for when higher-ranked sources are unavailable.
- **FR-005**: Principle IV ("Swagger-Informed, Reality-Validated") MUST be updated to reference the sources of truth hierarchy.
- **FR-006**: Principle II ("Example-Driven Fixture Capture") MUST be updated to reference the server source as a research source alongside ABConnectTools and swagger.
- **FR-007**: The DISCOVER workflow's Phase D research steps SHOULD be updated to include consulting the server source code.
- **FR-008**: The constitution version MUST be incremented (MINOR bump — new section added) with a Sync Impact Report.

### Key Entities

- **Sources of Truth Hierarchy**: An ordered list defining which information source takes precedence when sources conflict. Ranked: server source > captured fixtures > swagger specs.
- **API Server Source**: The source code of the ABConnect API server, located at `/usr/src/ABConnect` or `/src/ABConnect`. Contains controllers, request/response DTOs, and business logic that define the actual API behavior.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The constitution contains a clearly labeled "Sources of Truth" section with a numbered precedence order that any developer can follow without ambiguity.
- **SC-002**: All existing principles that reference swagger or fixtures are consistent with the sources of truth hierarchy — no contradictions exist within the document.
- **SC-003**: A developer encountering a swagger-vs-reality conflict can resolve it by reading the constitution alone, without needing to ask a colleague which source to trust.
- **SC-004**: The constitution version is incremented with a Sync Impact Report documenting the changes.

## Assumptions

- The API server source code at `/usr/src/ABConnect` (or `/src/ABConnect`) is accessible from the development environment where agents and developers work. When it's not available (e.g., CI), the hierarchy degrades to fixtures then swagger.
- ABConnectTools (`/usr/src/pkgs/ABConnectTools/`) remains a useful research source for legacy patterns and example values but is not part of the formal truth hierarchy (it's a consumer of the API, not the API itself).
- The existing swagger specs remain useful for endpoint discovery and parameter naming, even though they are the lowest-ranked source of truth.
