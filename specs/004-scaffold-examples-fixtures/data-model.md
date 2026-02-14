# Data Model: Scaffold Examples & Fixtures

**Feature**: 004-scaffold-examples-fixtures
**Date**: 2026-02-14

## Entities

### ExampleEntry

A single structured entry representing one endpoint method demonstration within an example file.

| Field | Type | Description |
|-------|------|-------------|
| name | string | Method identifier used for CLI selection (e.g., "validate", "get_property_type") |
| call | callable | Function that accepts the API client and calls the endpoint method with request parameters |
| response_model | string (optional) | Name of the Pydantic response model class (e.g., "AddressIsValidResult"). Matches Route.response_model. |
| request_model | string (optional) | Name of the Pydantic request model class (e.g., "QuickQuoteRequest"). None for query-param-only endpoints. |
| fixture_file | string (optional) | Filename for fixture output (e.g., "AddressIsValidResult.json"). Convention: `{ModelClassName}.json`. |

**Validation Rules**:
- `name` must be unique within a runner instance.
- `fixture_file` follows existing naming convention: `{ModelClassName}.json`.
- `call` must accept exactly one argument (the ABConnectAPI instance).

### ExampleRunner

The execution orchestrator that manages entries, initializes the API client, and handles fixture capture.

| Field | Type | Description |
|-------|------|-------------|
| title | string | Display name for the example group (e.g., "Address") |
| entries | list[ExampleEntry] | Registered structured entries |
| api_kwargs | dict | Keyword arguments passed to ABConnectAPI constructor |

**Behaviors**:
- Lazy API client initialization (created on first use).
- CLI argument parsing for selective entry execution.
- Per-entry execution with output display and fixture saving.
- Error reporting without aborting remaining entries.

### Relationships

```
ExampleRunner 1 ──── * ExampleEntry
     │                      │
     │ creates lazily        │ calls
     ▼                      ▼
ABConnectAPI          Endpoint Method
     │                      │
     │                      │ returns
     │                      ▼
     │               Pydantic Model
     │                      │
     │                      │ serializes to
     │                      ▼
     │               Fixture JSON File
     │                 (tests/fixtures/)
```

### State Transitions

An ExampleEntry has an implicit lifecycle based on its request data completeness:

```
[Scaffolded]  ──(fill request data)──▶  [Ready]  ──(run)──▶  [Captured]
     │                                     │                      │
     │ TODO markers present                │ All params filled     │ Fixture file exists
     │ Runner skips or warns               │ Runner can execute    │ Fixture validated
```

## File Layout

```
examples/
├── __init__.py          # Package marker (new)
├── _runner.py           # ExampleRunner + ExampleEntry + save logic (new)
├── address.py           # Runner-wrapped entries for AddressEndpoint (new)
├── autoprice.py         # Migrated to runner pattern
├── catalog.py           # Migrated to runner pattern
├── companies.py         # Migrated to runner pattern
├── contacts.py          # Migrated to runner pattern
├── documents.py         # Migrated to runner pattern
├── forms.py             # Migrated to runner pattern
├── jobs.py              # Migrated + expanded (2 → 28+ methods)
├── lookup.py            # Runner-wrapped entries for LookupEndpoint (new)
├── lots.py              # Migrated + expanded (1 → all methods)
├── notes.py             # Migrated to runner pattern
├── parcels.py           # Migrated to runner pattern
├── payments.py          # Migrated to runner pattern
├── sellers.py           # Migrated to runner pattern
├── shipments.py         # Migrated to runner pattern
├── timeline.py          # Migrated to runner pattern
├── tracking.py          # Migrated to runner pattern
├── users.py             # Runner-wrapped entries for UsersEndpoint (new)
└── web2lead.py          # Migrated to runner pattern
```
