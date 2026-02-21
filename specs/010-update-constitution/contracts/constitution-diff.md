# Constitution Change Contract: Sources of Truth Hierarchy

**Date**: 2026-02-21
**Constitution Version**: 2.2.0 → 2.3.0
**Bump Type**: MINOR (new section added, existing principles updated)

## Sync Impact Report (to be placed in constitution HTML comment)

```
Version change: 2.2.0 → 2.3.0
Bump rationale: MINOR — New "Sources of Truth" section added between
  Core Principles and API Coverage & Scope. Codifies a three-tier
  hierarchy: (1) API server source at /src/ABConnect/, (2) captured
  fixtures from real API responses, (3) swagger specifications.
  Driven by stakeholder input: server source has always been the
  ground truth but was never documented in the constitution.
Modified principles:
  - II. Example-Driven Fixture Capture: Added server source as
    research source (step 0, before ABConnectTools and swagger).
    Contextualized fixtures as Tier 2 in the hierarchy.
  - IV. Swagger-Informed, Reality-Validated: Added cross-reference
    to Sources of Truth hierarchy. Clarified swagger's position
    as Tier 3 (informational, not authoritative).
Added sections:
  - Sources of Truth (new top-level section between Core Principles
    and API Coverage & Scope)
Removed sections: None
Templates requiring updates:
  - .claude/workflows/DISCOVER.md — Phase D updated to include
    server source research step and path reference table
Follow-up TODOs: None
```

## Change 1: New "Sources of Truth" Section

**Location**: After "Core Principles" (after Principle IX), before "API Coverage & Scope"

**Content**:

```markdown
## Sources of Truth

When information about API behavior conflicts across sources, the
following hierarchy determines which source is authoritative:

1. **API Server Source Code** (`/src/ABConnect/`) — The actual .NET
   server implementation. Controllers define route behavior, DTOs
   define response/request shapes, services implement business logic.
   This is the ultimate authority for what the API does.

   Key paths:
   - ACPortal controllers: `ACPortal/ABC.ACPortal.WebAPI/Controllers/`
   - ACPortal DTOs: `ACPortal/ABC.ACPortal.WebAPI/Models/`
   - ABC controllers: `ABC.WebAPI/Controllers/`
   - ABC DTOs: `ABC.WebAPI/Models/`
   - Shared entities: `AB.ABCEntities/`
   - Business logic: `ABC.Services/`

2. **Captured Fixtures** (`tests/fixtures/`) — Real responses from
   the live API, captured by running examples against staging. These
   are validated evidence of actual API behavior at a point in time.
   Fixtures are strong truth — they reflect what the API actually
   returned.

3. **Swagger Specifications** — Auto-generated OpenAPI specs served
   by each API surface. Useful for endpoint discovery, parameter
   naming, and initial schema research. However, ACPortal swagger
   is known to frequently omit fields, declare wrong types, or miss
   entire response models. Swagger is informational, not
   authoritative.

**Degradation policy**: When a higher-ranked source is unavailable
(e.g., server source not accessible in CI), use the next available
source. When no fixtures exist for a new endpoint, swagger is the
starting reference — track the endpoint as needing validation.

**Conflict resolution**: When sources disagree, the higher-ranked
source wins. If server source contradicts a fixture, re-capture the
fixture. If a fixture contradicts swagger, trust the fixture and
document the swagger deviation.
```

## Change 2: Principle II Update

**Location**: Principle II, research sources list (currently items 1-2)

**Change**: Add server source as item 0 (before ABConnectTools):

```markdown
**Before writing an example**, the developer (human or agent) MUST
research the endpoint's requirements from these sources, in order
of authority (see Sources of Truth):

0. **API Server Source** (`/src/ABConnect/`) — Read the controller
   action for the endpoint to understand parameter binding, required
   fields, and response construction. Read the DTO classes for exact
   field names and types. This is the definitive source when
   available.
1. **ABConnectTools** — [existing text unchanged]
2. **Swagger specs** — [existing text unchanged]
```

## Change 3: Principle IV Update

**Location**: Principle IV, opening paragraph

**Change**: Add cross-reference to Sources of Truth:

```markdown
The three swagger specs (ACPortal, Catalog-API, ABC-API) are
reference inputs, not authoritative contracts (Tier 3 in the
Sources of Truth hierarchy). ACPortal swagger in particular is
known to frequently omit fields, declare wrong types, or miss
entire response models. The API server source code is the ultimate
authority (Tier 1); captured fixtures are strong evidence of
actual behavior (Tier 2).
```

## Change 4: DISCOVER Workflow Phase D Update

**Location**: `.claude/workflows/DISCOVER.md`, Phase D steps

**Change**: Add step 0 for server source research, add server source paths to reference table:

```markdown
For each endpoint in the group:

0. **Server source** (when accessible): Read the controller action
   at `/src/ABConnect/{project}/Controllers/{Service}Controller.cs`
   to see exact parameter binding, required fields, response
   construction, and any validation logic. Read DTOs at
   `/src/ABConnect/{project}/Models/` for exact field names and
   types. This is the ultimate source of truth.
1. **Routes**: [existing text unchanged]
...
```

Add to reference path table:

```markdown
## ABConnect Server Source Paths

| What | Path |
|------|------|
| ACPortal controllers | `/src/ABConnect/ACPortal/ABC.ACPortal.WebAPI/Controllers/` |
| ACPortal DTOs | `/src/ABConnect/ACPortal/ABC.ACPortal.WebAPI/Models/` |
| ABC controllers | `/src/ABConnect/ABC.WebAPI/Controllers/` |
| ABC DTOs | `/src/ABConnect/ABC.WebAPI/Models/` |
| Shared entities | `/src/ABConnect/AB.ABCEntities/` |
| Business logic | `/src/ABConnect/ABC.Services/` |
```
