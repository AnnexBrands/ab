# Feature Specification: Agent Assignment Helpers

**Feature Branch**: `029-agent-helpers`
**Created**: 2026-03-03
**Status**: Draft
**Input**: User description: "implement POST_CHANGE_AGENT and helpers to enable api.jobs.agent.oa(job, '3P-5153'). Review last spec and PR, make sure README.md covers agent responsibilities but suggests UAT including run suite of tests, what to watch for and how to remediate at each point, including running scripts to keep progress, etc up to date."

## User Scenarios & Testing

### User Story 1 — Change Origin Agent via Code (Priority: P1)

An SDK consumer needs to reassign the origin agent (pick-and-pack provider) for a job using a friendly agent code like "3P-5153" instead of a raw UUID. The system resolves the code to a UUID, calls the agent change endpoint, and returns a clear success/failure result.

**Why this priority**: This is the core business operation — agent reassignment is the primary use case that drives all other work in this feature.

**Independent Test**: Call `api.jobs.agent.oa(job_display_id, "3P-5153")` against staging and verify a success response is returned. The job's origin agent should change to the resolved company.

**Acceptance Scenarios**:

1. **Given** a valid job display ID and a resolvable agent code, **When** the user calls `api.jobs.agent.oa(job, "3P-5153")`, **Then** the system resolves the code to a UUID, sends a POST request to change the origin agent, and returns a success response.
2. **Given** a valid job display ID and a UUID (not a code), **When** the user calls `api.jobs.agent.oa(job, "ed282b80-...")`, **Then** the system uses the UUID directly without cache lookup and returns a success response.
3. **Given** an unresolvable agent code, **When** the user calls `api.jobs.agent.oa(job, "INVALID")`, **Then** the system passes the raw code to the API and returns whatever error the API provides.

---

### User Story 2 — Change Delivery Agent via Code (Priority: P2)

An SDK consumer needs to reassign the delivery agent for a job, with the same code-resolution convenience as origin agent changes.

**Why this priority**: Same operation as US1 but for a different service type. Depends on the same endpoint and infrastructure — trivial once US1 works.

**Independent Test**: Call `api.jobs.agent.da(job_display_id, "9999AZ")` and verify the delivery agent changes.

**Acceptance Scenarios**:

1. **Given** a valid job and agent code, **When** the user calls `api.jobs.agent.da(job, "9999AZ")`, **Then** the delivery agent is changed and a success response is returned.
2. **Given** optional flags, **When** the user calls `api.jobs.agent.da(job, code, recalculate_price=True)`, **Then** the price is recalculated as part of the agent change.

---

### User Story 3 — Generic Agent Change with Service Type (Priority: P3)

A power user needs to change an agent for any service type (pick, pack, pick-and-pack, delivery) using the lower-level `change()` method with explicit service type control.

**Why this priority**: Covers the full API surface for edge cases where the convenience methods (`oa`/`da`) don't match the desired service type.

**Independent Test**: Call `api.jobs.agent.change(job, code, service_type=1)` to change the pick-only agent and verify success.

**Acceptance Scenarios**:

1. **Given** a valid job, agent code, and any service type value (0-4), **When** the user calls `api.jobs.agent.change(job, code, service_type)`, **Then** the agent is changed for that specific service type.
2. **Given** recalculate_price and apply_rebate flags, **When** the user provides these optional parameters, **Then** they are included in the request body.

---

### User Story 4 — SDK README with Agent Responsibilities Guide (Priority: P4)

The README.md should be updated to cover the agent sub-endpoint, and should include a section guiding AI agents (and human developers) through the UAT process: how to run the test suite, what scripts to run to keep progress metrics current, what to watch for in test output, and how to remediate common issues.

**Why this priority**: Documentation ensures the agent assignment feature is discoverable and that future contributors (human or AI) can maintain quality standards without tribal knowledge.

**Independent Test**: Read the README and verify it contains: the agent endpoint group, a UAT guide with step-by-step commands, expected outputs, common failure patterns, and remediation steps.

**Acceptance Scenarios**:

1. **Given** a developer reading the README, **When** they look at the endpoint groups table, **Then** `api.jobs.agent` is listed with its methods (`oa`, `da`, `change`).
2. **Given** an AI agent or developer performing UAT, **When** they follow the README's UAT guide, **Then** they can run the full test suite, identify any failures, run progress/baseline scripts, and confirm all quality gates pass.
3. **Given** a test failure occurs, **When** the developer consults the README's troubleshooting section, **Then** they find specific remediation steps for common failure patterns (fixture missing, model mismatch, gate regression, FIXTURES.md drift).

---

### Edge Cases

- What happens when the agent code resolves to a UUID but the UUID is not a valid agent for the target job's company? The API returns a failure response with an error message. The SDK surfaces this unchanged.
- What happens when the cache service is unreachable? The resolver falls back to passing the raw code to the API (existing resolver behavior).
- What happens when service_type is 0 (UNDEFINED)? The request is sent as-is. The API determines behavior for undefined service types.
- What happens when the job display ID doesn't exist? The API returns an error response. The SDK surfaces the error via the standard response model.

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide an endpoint method that sends a POST request to `/job/{jobDisplayId}/changeAgent` with a request body containing service type, agent ID, recalculate price flag, and apply rebate flag.
- **FR-002**: System MUST provide an `oa()` convenience method that changes the origin agent (service type: pick-and-pack) for a given job, accepting a friendly agent code or UUID.
- **FR-003**: System MUST provide a `da()` convenience method that changes the delivery agent for a given job, accepting a friendly agent code or UUID.
- **FR-004**: System MUST provide a `change()` method that accepts an explicit service type parameter for agent changes beyond the two convenience methods.
- **FR-005**: System MUST resolve friendly agent codes (e.g., "3P-5153", "9999AZ") to UUIDs before sending the request, using the existing code resolution mechanism.
- **FR-006**: System MUST validate outbound request bodies against a request model that enforces field names and types.
- **FR-007**: System MUST validate inbound responses against the existing success/error response model.
- **FR-008**: System MUST expose the agent helpers as a sub-group (e.g., `api.jobs.agent.*`) following the existing helper pattern used by timeline operations.
- **FR-009**: The README MUST be updated with the agent endpoint group, a UAT guide covering test execution, progress scripts, common failures, and remediation.
- **FR-010**: System MUST include a service type enumeration covering: undefined (0), pick (1), pack (2), pick-and-pack (3), and delivery (4).
- **FR-011**: System MUST produce test fixtures (request and response) and pass all applicable quality gates for the new endpoint.

### Key Entities

- **ChangeJobAgentRequest**: Outbound request containing the target agent ID, service type, recalculate price flag, and apply rebate flag.
- **ServiceType**: Enumeration of agent service types — undefined, pick, pack, pick-and-pack, delivery.
- **ServiceBaseResponse**: Existing success/error response wrapper (already defined in the system).
- **AgentHelpers**: Sub-endpoint helper providing `oa()`, `da()`, and `change()` convenience methods with code-to-UUID resolution.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Calling `api.jobs.agent.oa(job, agent_code)` successfully changes the origin agent and returns a success response when tested against the staging environment.
- **SC-002**: All existing tests continue to pass (zero regressions) — the gate regression ratchet test detects no losses.
- **SC-003**: The new endpoint passes quality gates G1 (model fidelity), G4 (return type annotation), G5 (parameter routing), and G6 (request model quality). G2 and G3 pass if staging fixtures are captured; otherwise they skip gracefully.
- **SC-004**: The README contains a complete UAT guide that enables a developer to validate the entire SDK in under 10 minutes by following documented steps.
- **SC-005**: Running the gate baseline update script after implementation shows the new endpoint's gates added to the baseline with no regressions.
- **SC-006**: The fixture tracking file accurately reflects the new endpoint's status after running the progress generation script.

## Assumptions

- The ABConnect POST `/job/{jobDisplayId}/changeAgent` endpoint exists and accepts the documented request payload (service type, agent ID, recalculate price, apply rebate).
- The service type enumeration values (0-4) match the live API's expected integer values.
- The existing code resolver handles agent code resolution identically to company code resolution (same cache service, same lookup pattern).
- The standard success/error response model already in the system is sufficient for the change agent response.
- Staging API credentials are available for live fixture capture; if not, mock fixtures will be used and the endpoint will skip G2/G3 gracefully.
