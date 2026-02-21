# Research: Update Constitution — Sources of Truth Hierarchy

**Date**: 2026-02-21
**Branch**: `010-update-constitution`

## R1: ABConnect Server Source Structure

**Decision**: The API server source lives at `/src/ABConnect/` (confirmed on this system). The path `/usr/src/ABConnect` does not exist; the constitution should reference `/src/ABConnect` as the primary path.

**Findings**: The server is a .NET/C# solution (`ABConnect.sln`) with these key projects relevant to SDK development:

| Project | What It Contains | SDK Relevance |
| ------- | ---------------- | ------------- |
| `ACPortal/ABC.ACPortal.WebAPI/Controllers/` | ACPortal API controllers (Companies, Contacts, Jobs, Shipment, Lookup, Documents, etc.) | Definitive endpoint behavior — what params are accepted, what responses are returned |
| `ACPortal/ABC.ACPortal.WebAPI/Models/` | ACPortal request/response DTOs (organized by domain: Company/, Job/, Users/, Shared/) | Definitive field names, types, and nullability |
| `ABC.WebAPI/Controllers/` | ABC API controllers (AutoPrice, Company, Job, Report, Web2Lead) | ABC endpoint behavior |
| `ABC.WebAPI/Models/` | ABC request/response DTOs | ABC field definitions |
| `ABC.Services/` | Business logic (CompanyServices/, JobServices/, AutoPack/, CacheServices/) | Deeper understanding of validation rules and side effects |
| `ABC.Services.Interfaces/` | Service interfaces | Contract definitions |
| `AB.ABCEntities/` | Shared entity classes (Address, Company, Job, etc.) | Core domain model — field names and relationships |
| `AB.ABCEntities/ApiEntities/` | API-specific entity shapes | Response shapes that may differ from DB entities |

**Rationale**: Controllers show the exact route definitions, parameter binding, and response construction. Models/DTOs show the exact field names and types the API serializes. Together these are the authoritative source for what the API actually does.

**Alternatives considered**:
- Using only swagger: Rejected — swagger is auto-generated and frequently incomplete/wrong for ACPortal.
- Using only ABConnectTools: Rejected — it's a Python SDK consumer, not the API itself. It may have its own bugs or outdated patterns.

## R2: Current Constitution Treatment of Sources

**Decision**: The constitution (v2.2.0) already has the right spirit but lacks explicit hierarchy.

**Current state**:
- Principle II names ABConnectTools and swagger as research sources (lines 66-75)
- Principle IV says "swagger specs are reference inputs, not authoritative contracts" (line 147)
- Principle IV says "models MUST be validated against real API responses (fixtures)" (line 153)
- The server source is never mentioned in the constitution
- The DISCOVER workflow references ABConnectTools paths (lines 424-437) but not server source paths

**Gap**: No explicit ordering of "when sources conflict, which wins?" The hierarchy is implied but not stated.

## R3: Placement of New Section

**Decision**: Add a new "Sources of Truth" section between the "Core Principles" section and the "API Coverage & Scope" section. This places it after the principles (which reference it) and before the operational sections.

**Rationale**: The hierarchy is a meta-principle that governs how other principles resolve conflicts. It belongs at the top level, not nested inside an existing principle.

**Alternative considered**: Adding it as Principle X. Rejected — it's not a development practice like the other principles; it's a reference hierarchy that the principles point to.

## R4: Degradation Policy

**Decision**: When a higher-ranked source is unavailable, fall through to the next available source. Document this explicitly.

| Scenario | Available Sources | Action |
| -------- | ---------------- | ------ |
| Full development environment | Server source + fixtures + swagger | Use server source as authority |
| CI or no server access | Fixtures + swagger | Use captured fixtures as authority |
| New endpoint, no fixtures yet | Swagger only | Use swagger as starting point, track as needing validation |
| Server source disagrees with fixture | Server source + stale fixture | Server source wins — re-capture fixture |

## R5: DISCOVER Workflow Updates

**Decision**: Add server source to Phase D research steps as step 0 (before ABConnectTools and swagger). Add path reference table.

**Rationale**: Phase D is "Determine Requirements" — the server source is the most authoritative place to determine what an endpoint actually does. It should be checked first when available.
