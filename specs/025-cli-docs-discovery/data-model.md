# Data Model: CLI Docs & Discovery Major Release

**Branch**: `025-cli-docs-discovery` | **Date**: 2026-03-01

## Entity Overview

This feature introduces no new API models (Pydantic). All new entities are internal Python dataclasses used for introspection, display, and progress tracking.

```
Route (existing, frozen)
  ├── RouteResolver ──→ method_name → Route mapping
  │
  ├── MethodInfo (extended)
  │     └── route: Route | None          # NEW field
  │
  ├── ExampleEntry (extended)
  │     └── auto-populated from Route    # NEW behavior
  │
  └── MethodProgress (new)
        └── EndpointClassProgress (new)  # grouping container
```

## Entity Definitions

### Route (existing — no changes)

**Location**: `ab/api/route.py`

| Field | Type | Description |
|-------|------|-------------|
| method | str | HTTP method (GET, POST, PUT, DELETE) |
| path | str | URI path with `{param}` placeholders |
| request_model | str \| None | Name of Pydantic request model |
| params_model | str \| None | Name of Pydantic query params model |
| response_model | str \| None | Name of Pydantic response model |
| api_surface | str | "acportal" \| "catalog" \| "abc" |
| _path_params | frozenset[str] | Extracted `{param}` names (private) |

**Relationships**: Referenced by endpoint methods. Consumed by RouteResolver, CLI help, ExampleRunner, and progress system.

---

### MethodInfo (extended)

**Location**: `ab/cli/discovery.py`

| Field | Type | Description | Status |
|-------|------|-------------|--------|
| name | str | Python method name | existing |
| callable | Any \| None | Bound method reference | existing |
| positional_params | list[ParamInfo] | Positional parameters | existing |
| keyword_params | list[ParamInfo] | Keyword parameters | existing |
| docstring | str \| None | Cleaned docstring text | existing |
| route | Route \| None | Associated Route constant | **NEW** |
| return_annotation | str \| None | Return type annotation string | **NEW** |

**Relationships**: Contains ParamInfo list. Optionally references a Route. Consumed by CLI help, CLI listing, and progress system.

**State transitions**: None (read-only introspection result).

---

### EndpointInfo (extended)

**Location**: `ab/cli/discovery.py`

| Field | Type | Description | Status |
|-------|------|-------------|--------|
| name | str | Endpoint attribute name (e.g., "jobs") | existing |
| endpoint_class | type \| None | The endpoint class | existing |
| methods | list[MethodInfo] | All public methods | existing |
| aliases | list[str] | Short aliases from ALIASES registry | **NEW** |
| path_root | str \| None | Common path root (e.g., "/job") | **NEW** |

**Relationships**: Contains MethodInfo list. Referenced by CLI listing and progress system.

---

### ExampleEntry (extended behavior — no new fields)

**Location**: `examples/_runner.py`

| Field | Type | Description | Status |
|-------|------|-------------|--------|
| name | str | Entry name matching method name | existing |
| call | Callable | Lambda that calls the endpoint | existing |
| response_model | str \| None | Auto-populated from Route if None | existing (behavior change) |
| request_model | str \| None | Auto-populated from Route if None | existing (behavior change) |
| fixture_file | str \| None | Auto-populated as `{Model}.json` if None | existing (behavior change) |
| request_fixture_file | str \| None | Auto-populated as `{Model}.json` if None | existing (behavior change) |

**Behavior change**: Fields that were previously required to be explicitly set are now auto-populated from Route metadata when left as `None`. Explicit values override auto-discovery.

---

### MethodProgress (new)

**Location**: `ab/progress/models.py`

| Field | Type | Description |
|-------|------|-------------|
| dotted_path | str | Python dotted path (e.g., "api.jobs.get_timeline") |
| method_name | str | Python method name |
| http_method | str | HTTP verb (GET, POST, etc.) |
| http_path | str | Raw URI path |
| return_type | str | Response model name or "Any" |
| has_example | bool | Whether an `ex` entry exists |
| has_cli | bool | Whether `ab`/`abs` can call this method |
| has_route | bool | Whether backed by a Route (False for helpers) |
| path_sub_root | str | Path sub-root for grouping (e.g., "timeline") |
| gate_status | EndpointGateStatus \| None | Quality gate results |

**Relationships**: Contained by EndpointClassProgress. References EndpointGateStatus (existing).

---

### EndpointClassProgress (new)

**Location**: `ab/progress/models.py`

| Field | Type | Description |
|-------|------|-------------|
| class_name | str | Endpoint class attribute name (e.g., "jobs") |
| display_name | str | Human-readable name (e.g., "Jobs") |
| aliases | list[str] | Short aliases (e.g., ["job"]) |
| path_root | str | Common API path root (e.g., "/job") |
| helpers | list[MethodProgress] | Routeless helper methods |
| sub_groups | dict[str, list[MethodProgress]] | Methods grouped by path sub-root |
| total_methods | int | Total method count |
| total_with_route | int | Methods backed by a Route |
| total_with_example | int | Methods with example entries |
| total_with_cli | int | Methods callable via CLI |

**Relationships**: Contains MethodProgress lists. Consumed by progress renderer.

---

## Validation Rules

1. **Route resolution**: A method's Route is resolved via source introspection. If no `self._request()` call is found, `route` is `None` and the method is classified as a helper.
2. **Auto-discovery precedence**: Explicit `ExampleEntry` values always override Route-derived values.
3. **Path sub-root extraction**: Take the first path segment after the second `{param}` or after the base path root. E.g., `/job/{id}/timeline/{code}` → `timeline`. `/job/{id}` → `""` (root).
4. **Constant name derivation**: `{camelCase}` → `TEST_SCREAMING_SNAKE` via regex `re.sub(r'([A-Z])', r'_\1', param).upper()`.

## Relationships Diagram

```
ABConnectAPI
  └── endpoint_class (e.g., JobsEndpoint)
        ├── Route constants (module-level)
        │     └── RouteResolver maps methods → Routes
        ├── methods
        │     ├── Route-backed methods (has Route)
        │     └── Helper methods (no Route)
        └── TimelineHelpers (sub-service, helpers)

EndpointClassProgress
  ├── helpers: [MethodProgress]     # routeless, shown first
  └── sub_groups:
        ├── "": [MethodProgress]    # root-level Route methods
        ├── "timeline": [...]       # /job/{id}/timeline/*
        └── "onhold": [...]         # /job/{id}/onhold/*

ExampleRunner
  └── entries: [ExampleEntry]
        └── auto-populated from Route (if fields are None)
```
