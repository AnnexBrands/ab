# Data Model: Update Constitution — Sources of Truth Hierarchy

**Date**: 2026-02-21
**Branch**: `010-update-constitution`

## Overview

This is a documentation-only feature. There are no database entities, Pydantic models, or data structures to define. The "data model" for this feature is the hierarchy itself.

## Sources of Truth Hierarchy

```text
┌─────────────────────────────────────────────────┐
│  1. API Server Source Code                      │
│     /src/ABConnect/                             │
│     Controllers, DTOs, Services                 │
│     → Definitive behavior, fields, validation   │
├─────────────────────────────────────────────────┤
│  2. Captured Fixtures                           │
│     tests/fixtures/*.json                       │
│     Real API responses from staging/production  │
│     → Validated response shapes, regression     │
├─────────────────────────────────────────────────┤
│  3. Swagger Specifications                      │
│     /swagger/v1/swagger.json (per API surface)  │
│     Auto-generated, sometimes incomplete        │
│     → Endpoint discovery, parameter naming      │
└─────────────────────────────────────────────────┘
```

## Conflict Resolution Rules

| Source A | Source B | Winner | Action |
| -------- | -------- | ------ | ------ |
| Server source | Swagger | Server source | Document swagger deviation in model comment |
| Server source | Fixture | Server source | Re-capture fixture from updated API |
| Fixture | Swagger | Fixture | Fixture reflects real API behavior |

## Degradation Policy

When higher-ranked sources are unavailable, fall through:

1. **Server source unavailable** → Use fixtures as authority, then swagger
2. **No fixtures captured** → Use swagger as starting point, track as needing validation
3. **All three available** → Server source is definitive
