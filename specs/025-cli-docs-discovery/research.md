# Research: CLI Docs & Discovery Major Release

**Branch**: `025-cli-docs-discovery` | **Date**: 2026-03-01
**Status**: Complete — all unknowns resolved

## Research Tasks

### R1: Route-to-Method Matching Strategy

**Context**: Each endpoint class has module-level Route constants (e.g., `_GET = Route(...)`) and methods that reference them via `self._request(_GET.bind(...))`. No explicit mapping exists between method names and their Routes.

**Decision**: Source-code introspection of method bodies.

**Rationale**: The `discover_endpoints_from_class()` function in `ab/cli/discovery.py` already uses source introspection (regex on `ABConnectAPI._init_endpoints`) to map attribute names to endpoint classes without instantiation. The same proven pattern applies here: parse each method's source code to find `self._request(_ROUTE_NAME` calls, then look up the module-level Route constant.

**Alternatives considered**:

1. **Naming convention** (`_GET_TIMELINE` → `get_timeline`): Fragile. Multiple methods may share Route prefixes. Routes like `_GET_TIMELINE_AGENT` and `_GET_TIMELINE` would conflict. Compound Routes like `_CREATE_TIMELINE_TASK` don't always map cleanly to method names.

2. **Explicit registry** (dict per endpoint class): Requires modifying every endpoint file. High blast radius, adds maintenance burden. Rejected per constitution principle on minimal changes.

3. **Method decorator** (`@route(_GET)`): Requires modifying every method signature across all endpoint files. Major refactor with no incremental path. Rejected.

4. **Docstring parsing** (extract URI from first line like `GET /contacts/{id}`): Docstrings are inconsistent — some have it, some don't. Also, docstrings contain the human-readable URI but not the response model info. Would duplicate Route data.

**Implementation approach**:
```python
# ab/cli/route_resolver.py
import inspect, re
from ab.api.route import Route

def resolve_routes_for_class(cls) -> dict[str, Route]:
    """Map method names to their Route constants via source introspection."""
    module = inspect.getmodule(cls)
    # Collect all Route constants in the module
    route_vars: dict[str, Route] = {}
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, Route):
            route_vars[name] = obj

    # For each public method, find which Route it references
    method_routes: dict[str, Route] = {}
    for method_name in dir(cls):
        if method_name.startswith("_"):
            continue
        method = getattr(cls, method_name, None)
        if not callable(method):
            continue
        try:
            source = inspect.getsource(method)
        except (OSError, TypeError):
            continue
        # Match: self._request(_ROUTE_NAME or _ROUTE_NAME.bind(
        for match in re.finditer(r'(?:self\._request|_request)\(\s*(_[A-Z_]+)', source):
            route_name = match.group(1)
            if route_name in route_vars:
                method_routes[method_name] = route_vars[route_name]
                break  # Take the first Route reference

    return method_routes
```

**Confidence**: HIGH — proven pattern, no external dependencies, handles all current endpoint conventions.

---

### R2: Docstring Format for Dual-Purpose Rendering (Sphinx + CLI)

**Context**: Docstrings currently use `:class:` RST cross-references that render in Sphinx but appear as raw text in CLI `--help`. The spec requires docstrings that serve both.

**Decision**: Keep docstrings as-is (RST format for Sphinx). CLI help is rendered from Route metadata directly, not parsed from docstrings.

**Rationale**: The CLI `--help` output needs structured data: URI, method, params, return type. All of this is available programmatically from the Route object and method signature introspection. Parsing docstrings for this data would be fragile and duplicate what Route already provides.

The docstring's *description* text (purpose of the method) can be displayed in CLI help after stripping RST markup via a simple regex. But the factual metadata (URI, params, return type) comes from the Route.

**Approach**:
- **Sphinx**: Continues using `autodoc` which renders docstrings natively with `:class:` cross-references.
- **CLI `--help`**: Displays Route-derived metadata (URI, signature, return type) in a structured card format. Includes the docstring's first paragraph as a description, with RST `:class:` references stripped to plain text.

**Alternatives considered**:
1. **Markdown docstrings**: Would break existing Sphinx RST rendering. Rejected.
2. **Structured metadata in docstrings** (YAML front matter): Over-engineered. Route already has the data. Rejected.
3. **Google-style docstrings with autodoc-napoleon**: Would require adding `sphinx.ext.napoleon` and converting all existing docstrings. Major refactor. Rejected.

**Confidence**: HIGH — Route-derived metadata is authoritative and complete.

---

### R3: ExampleRunner Auto-Discovery from Routes

**Context**: `ExampleRunner.add()` requires explicit `response_model="Job"` and `fixture_file="Job.json"`. The Route already declares `response_model="Job"`. The spec requires auto-discovery.

**Decision**: Resolve Route metadata at registration time using the endpoint module's Route constants.

**Rationale**: The ExampleRunner's `title` maps to an endpoint class name (e.g., `"Jobs"` → `JobsEndpoint`). Each entry's `name` maps to a method name (e.g., `"get"` → `JobsEndpoint.get`). Using `route_resolver.resolve_routes_for_class()`, we can look up the Route for that method and extract `response_model` and `request_model`.

**Implementation approach**:
```python
# In ExampleRunner.__init__ or a lazy resolver
def _resolve_entry_metadata(self, entry: ExampleEntry) -> None:
    """Auto-populate response_model, fixture_file from Route if not explicit."""
    if entry.response_model is not None and entry.fixture_file is not None:
        return  # Explicit override takes precedence

    route = self._method_routes.get(entry.name)
    if route is None:
        return  # No Route found (helper method) — graceful fallback

    if entry.response_model is None and route.response_model:
        # Parse List[Model] to get the inner model name
        _, model_name = BaseEndpoint._parse_type_string(route.response_model)
        entry.response_model = model_name

    if entry.fixture_file is None and entry.response_model:
        entry.fixture_file = f"{entry.response_model}.json"

    if entry.request_model is None and route.request_model:
        entry.request_model = route.request_model

    if entry.request_fixture_file is None and entry.request_model:
        entry.request_fixture_file = f"{entry.request_model}.json"
```

**Mapping ExampleRunner title → endpoint class**: The ExampleRunner `title` is a display name like `"Jobs"`, `"Contacts"`. The endpoint module file is `examples/jobs.py` → endpoint class `JobsEndpoint`. We can derive this from the example file name or maintain a lightweight registry.

Better approach: pass the endpoint attribute name (e.g., `"jobs"`) to ExampleRunner and use `discover_endpoints_from_class()` to get the class, then `resolve_routes_for_class()` for Routes.

**Confidence**: HIGH — all data is available from Routes.

---

### R4: Progress Report Data Model and Grouping

**Context**: Current progress report groups by API surface (ACPortal, Catalog, ABC). The spec requires grouping by endpoint class (e.g., `jobs`) with sub-sections by path sub-root (e.g., `timeline`, `onhold`).

**Decision**: Build an `EndpointProgress` dataclass that joins Route info, method info, example status, and CLI status. Group by endpoint class using the existing endpoint module structure.

**Rationale**: The `route_index.py` already collects all Routes. By combining this with `discover_endpoints_from_class()` (which gives endpoint classes and methods) and scanning example files (for `ex` entries), we can build a comprehensive progress view.

**Implementation approach**:
```python
@dataclass
class MethodProgress:
    """Unified view of a single endpoint method's coverage."""
    dotted_path: str       # e.g., "api.jobs.get_timeline"
    http_method: str       # e.g., "GET"
    http_path: str         # e.g., "/job/{jobDisplayId}/timeline"
    return_type: str       # e.g., "list[TimelineTask]"
    has_example: bool      # True if ex entry exists
    has_cli: bool          # True if ab/abs callable
    has_route: bool        # True if backed by a Route
    gate_status: EndpointGateStatus | None

@dataclass
class EndpointClassProgress:
    """All methods in an endpoint class, grouped by path sub-root."""
    class_name: str        # e.g., "jobs"
    aliases: list[str]     # e.g., ["job"]
    sub_groups: dict[str, list[MethodProgress]]  # e.g., {"timeline": [...], "onhold": [...], "": [...]}
    helpers: list[MethodProgress]  # routeless methods
```

**Path sub-root extraction**: Parse the Route path's first segment after the root. E.g., `/job/{id}/timeline/{code}` → sub-root is `timeline`. `/job/{id}` → sub-root is empty (root level).

**Confidence**: HIGH — extends existing data model, no external dependencies.

---

### R5: Generic Constants Discovery

**Context**: Currently, constant requirements are manually mapped. The spec requires inferring required constants from URI path parameters.

**Decision**: Pattern-match `{paramName}` in Route paths to `TEST_{PARAM_NAME}` constant names using camelCase → SCREAMING_SNAKE_CASE conversion.

**Rationale**: Existing routes use camelCase path parameters like `{jobDisplayId}`, `{contactId}`, `{companyId}`. The existing constants in `tests/constants.py` follow the pattern `TEST_JOB_DISPLAY_ID`, `TEST_CONTACT_ID`, `TEST_COMPANY_ID`. This is a deterministic 1:1 mapping.

**Implementation approach**:
```python
import re

def path_param_to_constant(param: str) -> str:
    """Convert {camelCase} to TEST_SCREAMING_SNAKE."""
    # Insert underscore before uppercase letters
    snake = re.sub(r'([A-Z])', r'_\1', param).upper()
    if snake.startswith('_'):
        snake = snake[1:]
    return f"TEST_{snake}"

# Example: "jobDisplayId" → "TEST_JOB_DISPLAY_ID"
# Example: "contactId" → "TEST_CONTACT_ID"
```

This already partially exists in `ab/progress/instructions.py` via `detect_required_constants()`. The improvement is to make it generic rather than hardcoded.

**Confidence**: HIGH — deterministic transformation, existing pattern.

---

### R6: Fixture Discovery by Model Name

**Context**: Currently fixture files are manually specified as `fixture_file="Job.json"`. The spec requires resolving fixture files by Route model name.

**Decision**: Convention-based: `{ModelName}.json` in `tests/fixtures/`. This is already the established convention.

**Rationale**: Every fixture file in the repository follows the `{ModelName}.json` naming convention. The ExampleRunner's `_save_fixture()` already saves to `FIXTURES_DIR / entry.fixture_file`. By auto-populating `fixture_file` from `Route.response_model`, we maintain the existing convention without any lookup tables.

**Confidence**: HIGH — convention already established.

---

### R7: CLI Help Card Format

**Context**: The spec requires `--help` to display a structured reference card with URI, Python signature, CLI syntax, return type, and model fields.

**Decision**: Structured plain-text card format rendered to stderr.

**Research — best practices for CLI help formats**:
- **click/typer**: Uses colored sections with USAGE, OPTIONS, ARGUMENTS headers
- **httpie**: Shows HTTP method + URL prominently, then parameters
- **stripe CLI**: Shows resource description, then flags, then examples
- **GitHub CLI**: Uses USAGE section with synopsis, FLAGS, EXAMPLES

**Chosen format** (adapted for SDK context):
```
  jobs get_timeline
  ─────────────────

  Get the timeline tasks for a job.

  Route   GET /job/{jobDisplayId}/timeline
  Python  api.jobs.get_timeline(job_display_id: int) -> list[TimelineTask]
  CLI     ab jobs get_timeline <job_display_id>

  Returns: list[TimelineTask]

  Positional arguments:
    job_display_id (int)

  Response model: TimelineTask
    taskCode       str          Task code (PU, PK, ST, CP)
    taskStatus     str | None   Current status description
    ...
```

This format is scannable, shows all key information, and works in monospace terminals.

**Confidence**: HIGH — follows established CLI help conventions.

---

## Summary of Decisions

| # | Decision | Approach | Confidence |
|---|----------|----------|------------|
| R1 | Route-to-method matching | Source introspection of method bodies | HIGH |
| R2 | Docstring dual-purpose | Route metadata for CLI, RST for Sphinx | HIGH |
| R3 | ExampleRunner auto-discovery | Resolve Route at registration time | HIGH |
| R4 | Progress grouping | EndpointClassProgress dataclass, path sub-root extraction | HIGH |
| R5 | Constants discovery | camelCase → SCREAMING_SNAKE convention | HIGH |
| R6 | Fixture discovery | `{ModelName}.json` convention (existing) | HIGH |
| R7 | CLI help format | Structured plain-text card | HIGH |

All NEEDS CLARIFICATION items from Technical Context have been resolved through research. No external dependencies or new technologies required.
