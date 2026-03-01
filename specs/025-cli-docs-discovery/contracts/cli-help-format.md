# Contract: CLI Help & Listing Output Formats

**Feature**: 025-cli-docs-discovery | **Date**: 2026-03-01

## 1. Method Help (`ab <module> <method> --help`)

Format: structured plain-text card rendered to stderr.

```
  <method_name>
  ──────────────

  <docstring first paragraph, RST markup stripped>

  Route   <HTTP_METHOD> <path_with_params>
  Python  api.<module>.<method>(<params>) -> <return_type>
  CLI     ab <module> <method> <positional_args> [--keyword-args]

  Returns: <return_type>

  Positional arguments:
    <name> (<type>)

  Keyword arguments:
    --<flag>=VALUE (<type>) [default: <value>]
    --<flag>=VALUE (<type>) (required)

  Response model: <ModelName>
    <field>       <type>       <description>
    <field>       <type>       <description>

  Request model: <ModelName>
    <field>       <type>       <description>

  Params model: <ModelName>
    <field>       <type>       <description>
```

### Rules

- Route line: omit if method has no Route (helper)
- Python line: always shown with full dotted path
- CLI line: always shown
- Returns line: show "Any" if no typed return, omit if None
- Response/Request/Params model sections: only shown if Route has the respective model
- Model fields: show up to 10 fields with types and Field descriptions
- RST `:class:ModelName` in docstring → stripped to `ModelName`

---

## 2. Method Listing (`ab <module>` — no method specified)

Format: table rendered to stderr.

```
  <module_name> — <count> methods

  Helpers (no API route):
  ──────────────────────
  <method>                       <param_summary>

  API Methods:
  ────────────
  <HTTP> <path>                  <method>(<params>) -> <return_type>
  <HTTP> <path>                  <method>(<params>) -> <return_type>
```

### Rules

- Helpers section: shown first, only if routeless methods exist (FR-012a)
- API Methods section: sorted by HTTP path
- Each row shows: HTTP method, URI pattern, Python method name, signature, return type
- No `--list` flag required (FR-012)

---

## 3. Top-Level Listing (`ab` — no arguments)

Format: table rendered to stderr.

```
  <Endpoint>             <Methods>   <Path Root>   Aliases
  ─────────────────────  ─────────   ──────────    ──────────
  <name>                 <count>     <path_root>   <alias1, alias2>

  <N> endpoints, <M> methods
```

### Rules

- Sorted alphabetically by endpoint name
- Path root: common path prefix (e.g., "/job", "/contacts")
- Aliases: from shared ALIASES registry
- No `--list` flag required

---

## 4. ExampleRunner Auto-Discovery Contract

When `ExampleRunner.add()` is called with `response_model=None`:
1. Resolve the endpoint class from the runner's `endpoint_attr` (e.g., `"jobs"`)
2. Use `RouteResolver.resolve_routes_for_class()` to get method → Route mapping
3. Look up `entry.name` in the mapping
4. If found: set `entry.response_model` from `Route.response_model` (inner name for `List[X]`)
5. If found: set `entry.fixture_file` to `"{ModelName}.json"`
6. If `Route.request_model` exists: set `entry.request_model` and `entry.request_fixture_file`
7. If not found: leave fields as None (graceful fallback for helpers)

Explicit values always override auto-discovery.

---

## 5. Progress Report Output Contract

### HTML structure (progress.html)

```
<h2>Endpoint Coverage by Class</h2>
  For each EndpointClassProgress:
    <h3>{class_name} ({total_methods} methods) — aliases: {aliases}</h3>
    <p>Path root: {path_root}</p>

    If helpers exist:
      <h4>Helpers</h4>
      <table>
        <tr><th>Method</th><th>Python Path</th><th>Ex</th><th>CLI</th></tr>
        <tr><td>method</td><td>api.jobs.method</td><td>yes/no</td><td>yes/no</td></tr>
      </table>

    For each sub_group:
      <h4>{sub_root} ({count} methods)</h4>
      <table>
        <tr><th>HTTP</th><th>Path</th><th>Method</th><th>Python Path</th><th>Return</th><th>Ex</th><th>CLI</th><th>Gates</th></tr>
        <tr>...</tr>
      </table>
```

### FIXTURES.md additions

Each row includes a new "Python Path" column showing the dotted method path:

```
| Endpoint Path | Method | Python Path | Req Model | Resp Model | G1 | ... |
```
