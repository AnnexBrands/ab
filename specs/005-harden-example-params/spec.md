# Feature Specification: Harden Example Parameters Against Swagger

**Feature Branch**: `005-harden-example-params`
**Created**: 2026-02-14
**Status**: Draft
**Input**: User description: "Harden our artifacts and workflow. The example for address.validate was using parameters that did not match swagger, and were not found in ABConnectTools. That is to say, they were guessed. Go through the examples and confirm any request body and params do not have conflict in the schema."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Fix Parameter Mismatches in Examples and Endpoints (Priority: P1)

A developer runs an example and gets an unexpected error or silent failure because the example passes parameter names that don't match the actual API. Every example's lambda call must use parameter names that align with the endpoint method signatures, and every endpoint method must map its Python parameters to the correct API parameter names as defined in swagger.

**Why this priority**: Incorrect parameter mappings affect every caller of the SDK, not just examples. The address.validate example is a concrete instance — it passes `street`, `city`, `state`, `zip_code`, `country` but the API expects `Line1`, `City`, `State`, `Zip` (no `Country`). The mismatch originates in the endpoint layer and propagates to examples.

**Independent Test**: Run each corrected example entry against the staging API and confirm no parameter-name rejections or unexpected 400 errors.

**Acceptance Scenarios**:

1. **Given** the address.validate example, **When** a developer runs it, **Then** the parameters sent match the swagger spec for GET /api/address/isvalid (`Line1`, `City`, `State`, `Zip`).
2. **Given** the address.get_property_type example, **When** a developer runs it, **Then** the parameters sent include all required swagger fields (`Address1`, `City`, `State`, `ZipCode`).
3. **Given** the forms.get_operations example, **When** a developer runs it, **Then** the query parameter sent is `type`, not `opsType`.
4. **Given** any example file, **When** a developer reads the lambda call, **Then** every keyword argument and dict key corresponds to a parameter or request-body field defined in the swagger schema.

---

### User Story 2 - Automated Validation Guard (Priority: P2)

A developer adds a new example or modifies an existing one. A test validates that every example's parameters and request bodies are consistent with the swagger schemas, catching drift before it reaches the main branch.

**Why this priority**: Fixing today's mismatches is necessary but insufficient. Without an automated guard, the same class of error will recur as new examples are added.

**Independent Test**: Run the validation test with a deliberately wrong parameter name and confirm it fails.

**Acceptance Scenarios**:

1. **Given** an example that passes a parameter not defined in swagger, **When** the validation test runs, **Then** the test fails with a clear message naming the example, entry, and unknown parameter.
2. **Given** all examples are correct, **When** the validation test runs, **Then** all tests pass.

---

### Edge Cases

- What happens when an endpoint method accepts `**kwargs` (e.g. `jobs.search()`) — the validation test should still check passed arguments against swagger, even if the method signature is open-ended.
- What happens when the swagger spec defines optional parameters that the example omits — the validation test should only flag unknown parameters, not missing optional ones.
- What happens when a swagger operation defines a request body with `additionalProperties: true` — arbitrary keys are acceptable and should not be flagged.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Every example lambda call MUST use parameter names that match the corresponding endpoint method signature.
- **FR-002**: Every endpoint method MUST map its Python parameters to the correct API query-parameter or request-body field names as defined in the swagger specification.
- **FR-003**: The `AddressEndpoint.validate()` method MUST accept and map parameters matching swagger GET /api/address/isvalid: `Line1`, `City`, `State`, `Zip`.
- **FR-004**: The `AddressEndpoint.get_property_type()` method MUST accept and map all required parameters from swagger GET /api/address/propertytype: `Address1`, `City`, `State`, `ZipCode`, plus optional `Address2`.
- **FR-005**: The `FormsEndpoint.get_operations()` method MUST map its type parameter to the swagger query-parameter name `type`, not `opsType`.
- **FR-006**: An automated test MUST validate that every example entry's parameters are consistent with the swagger schema for the corresponding endpoint.
- **FR-007**: The validation test MUST cover both query parameters and request-body fields.
- **FR-008**: Examples that pass fabricated parameters (not in swagger and not in ABConnectTools) MUST be corrected or removed.

### Key Entities

- **Example Entry**: A registered demonstration in an example file — has a name, a lambda call, and optional model/fixture metadata.
- **Endpoint Method**: A Python method in `ab/api/endpoints/` that maps Python parameter names to API parameter names and builds HTTP requests.
- **Swagger Operation**: An API operation defined in the swagger JSON schemas, specifying path, method, parameters, and request body.

## Assumptions

- The swagger JSON files in `ab/api/schemas/` are the authoritative source of truth for API parameter names.
- ABConnectTools at `/usr/src/pkgs/ABConnectTools/` is a secondary reference for understanding how parameters were historically used, but swagger takes precedence.
- Fixing endpoint method signatures is in scope when the endpoint itself maps to wrong parameter names — this is not just an examples-only fix.
- The validation test does not need to make live API calls; it can cross-reference example parameters against swagger statically.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Zero examples produce parameter-name errors when run against the live staging API.
- **SC-002**: 100% of endpoint methods map Python parameters to the correct swagger-defined API parameter names for all implemented operations.
- **SC-003**: An automated validation test covers every example entry and catches parameter mismatches, achieving 100% example coverage.
- **SC-004**: The validation test runs as part of the standard test suite and completes in under 10 seconds.
