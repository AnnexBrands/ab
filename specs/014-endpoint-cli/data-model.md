# Data Model: Endpoint CLI

**Feature**: 014-endpoint-cli
**Date**: 2026-02-22

## Entities

### EndpointRegistry

**Purpose**: Runtime mapping of attribute names to endpoint instances and their metadata. Built by introspecting an `ABConnectAPI` instance.

| Field | Type | Description |
|-------|------|-------------|
| name | str | Attribute name on ABConnectAPI (e.g., "address", "companies", "rfq") |
| endpoint | BaseEndpoint | The endpoint instance |
| methods | list[MethodInfo] | Public methods on the endpoint |

**Discovery rules**:
- Include attributes that are `BaseEndpoint` subclass instances
- Exclude private/internal attributes (`_acportal`, `_catalog`, `_abc`, `_resolver`, `_settings`)
- 23 endpoint groups total

### MethodInfo

**Purpose**: Metadata about a single callable method on an endpoint, extracted via `inspect.signature()`.

| Field | Type | Description |
|-------|------|-------------|
| name | str | Method name (e.g., "validate", "get_by_id") |
| callable | Callable | Bound method reference |
| positional_params | list[ParamInfo] | Positional parameters (path params) |
| keyword_params | list[ParamInfo] | Keyword-only parameters (query/body params) |
| docstring | str or None | Method's docstring (contains HTTP method + path) |

**Discovery rules**:
- Include methods where `not name.startswith("_")`
- Exclude inherited object methods (`__init__`, `__repr__`, etc.)
- Extract signature via `inspect.signature(method)`

### ParamInfo

**Purpose**: Metadata about a single method parameter.

| Field | Type | Description |
|-------|------|-------------|
| name | str | Python parameter name (e.g., "company_id", "line1") |
| cli_name | str | CLI flag form (e.g., "--company-id", "--line1") |
| annotation | type or None | Type annotation if present |
| default | Any | Default value, or `inspect.Parameter.empty` |
| required | bool | True if no default value |
| kind | str | "positional" or "keyword" |

### Alias

**Purpose**: Shorthand name mapping, shared between `ex` and `ab`/`abs` CLIs.

| Field | Type | Description |
|-------|------|-------------|
| alias | str | Short name (e.g., "addr", "co", "ct") |
| target | str | Full endpoint attribute name (e.g., "address", "companies", "contacts") |

**Source**: Single shared dict, currently defined in `examples/__main__.py`, to be extracted to shared location.

**Full alias table (23 aliases for 23 endpoints)**:

| Alias | Target | Alias | Target |
|-------|--------|-------|--------|
| addr | address | note | notes |
| q | autoprice | parc | parcels |
| cat | catalog | pay | payments |
| co | companies | sell | sellers |
| ct | contacts | ship | shipments |
| doc | documents | tk | timeline |
| form | forms | track | tracking |
| job | jobs | u | users |
| lu | lookup | lead | web2lead |
| lot | lots | | |

*Note: Not all endpoints have aliases (e.g., `dashboard`, `reports`, `views`, `partners`, `commodities`, `commodity_maps` have no alias in `ex`). The CLI still reaches them by full name or prefix match.*

## Relationships

```
ABConnectAPI
  ├── address: AddressEndpoint
  │     ├── validate(*, line1, city, state, zip)
  │     └── get_property_type(*, address1, address2, city, state, zip_code)
  ├── companies: CompaniesEndpoint
  │     ├── get_by_id(company_id)
  │     ├── get_details(company_id)
  │     ├── search(*, search_text, page, page_size, ...)
  │     └── ... (24 methods total)
  ├── jobs: JobsEndpoint
  │     ├── get(job_display_id)
  │     ├── search(*, job_display_id)
  │     └── ... (31 methods total)
  └── ... (23 endpoint groups, ~200+ methods total)

ALIASES ──shared──> ex CLI (examples/__main__.py)
ALIASES ──shared──> ab/abs CLI (ab/cli/__main__.py)

ab entry point ──creates──> ABConnectAPI(env=None)  [production]
abs entry point ──creates──> ABConnectAPI(env="staging")
```

## CLI Argument Mapping

```
CLI Input                          Python Call
─────────────                      ───────────
ab jobs get 2000000                api.jobs.get(2000000)
abs addr validate --line1=X        api.address.validate(line1="X")
ab co get_by_id ABC123             api.companies.get_by_id("ABC123")
ab co search --search-text=test    api.companies.search(search_text="test")
ab jobs create --body='{"key":1}'  api.jobs.create({"key": 1})
```

**Type coercion rules**:
- All CLI args arrive as strings
- Integers: detected by annotation or if value is digit-only
- Booleans: `true`/`false`/`1`/`0`
- JSON bodies: parsed from `--body` flag or stdin
- Lists: not supported in initial version (use `--body` for complex types)
