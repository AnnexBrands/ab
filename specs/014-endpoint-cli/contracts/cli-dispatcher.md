# Contract: CLI Dispatcher Interface

**Feature**: 014-endpoint-cli

## main(env: str | None = None) -> None

**Location**: `ab/cli/__main__.py`

### Behavior

1. Parse `sys.argv[1:]` for module, method, and arguments
2. Create `ABConnectAPI(env=env)` — lazily, only when a method call is needed
3. Dispatch to the appropriate endpoint method
4. Print result to stdout as JSON
5. Exit with status 0 on success, nonzero on failure

### Entry Points

- `ab` → calls `main(env=None)` → production
- `abs` → calls `main(env="staging")` → staging

### Invariants

- Never creates the API client for `--list` or `--help` operations (no credentials needed for discovery)
- All output goes to stdout (errors to stderr)
- Exit codes: 0=success, 1=user error (bad args, unknown endpoint), 2=API error (auth, HTTP failure)

---

## discover_endpoints(api_cls: type) -> dict[str, EndpointInfo]

**Location**: `ab/cli/discovery.py`

### Behavior

1. Inspect `ABConnectAPI.__init__` to find endpoint attribute assignments
2. For each attribute that holds a `BaseEndpoint` subclass:
   - Extract attribute name (e.g., "address", "companies")
   - Extract endpoint class (e.g., `AddressEndpoint`)
   - Enumerate public methods via `inspect.getmembers(cls, predicate=inspect.isfunction)`
   - For each method: extract name, signature, docstring

### Invariants

- Does NOT instantiate ABConnectAPI (class-level inspection only for discovery)
- Returns only user-facing methods (excludes `_`-prefixed)
- Excludes inherited `object` methods

---

## resolve_module(name: str, registry: dict) -> tuple[str, EndpointInfo] | None

**Location**: `ab/cli/__main__.py`

### Behavior

Identical to `examples/__main__._resolve_module()`:
1. Exact match on endpoint attribute names
2. Exact match on aliases
3. Prefix match on names, then alias keys
4. Ambiguity handling: print matching options, return None

### Invariants

- Uses the shared `ALIASES` dict
- Prints to stderr on ambiguity or unknown module
- Returns None on failure (caller handles exit)

---

## resolve_method(name: str, endpoint_info: EndpointInfo) -> MethodInfo | None

**Location**: `ab/cli/__main__.py`

### Behavior

1. Exact match on method name
2. Prefix match on method names
3. Ambiguity handling: print matching methods, return None

### Invariants

- Same prefix/ambiguity semantics as `examples.__main__._resolve_entry()`

---

## parse_cli_args(args: list[str], method: MethodInfo) -> tuple[list, dict]

**Location**: `ab/cli/parser.py`

### Behavior

1. Separate positional args from `--flag` args
2. Map `--param-name=value` → `{"param_name": "value"}`
3. Map `--param-name value` (two-token) → `{"param_name": "value"}`
4. Coerce types based on method signature annotations
5. Handle `--body='{...}'` for JSON request bodies
6. Handle `--help` to print method signature and exit

### Type Coercion

| Annotation | Coercion |
|------------|----------|
| `int` | `int(value)` |
| `bool` | `value.lower() in ("true", "1", "yes")` |
| `float` | `float(value)` |
| `str` or None | No coercion (string passthrough) |
| `dict` or `Any` (for `data` param) | `json.loads(value)` |

### Invariants

- Unknown flags → error with valid parameter list
- Missing required positional args → error with signature
- Returns `(positional_args, keyword_args)` tuple

---

## format_result(result: Any) -> str

**Location**: `ab/cli/formatter.py`

### Behavior

1. Pydantic model → `json.dumps(model.model_dump(by_alias=True, mode="json"), indent=2)`
2. List of Pydantic models → `json.dumps([m.model_dump(...) for m in result], indent=2)`
3. dict or list → `json.dumps(result, indent=2)`
4. Primitive (str, int, bool, None) → `str(result)`
5. bytes → `"<binary response, {len} bytes>"`

### Invariants

- Always returns a string
- JSON output uses 2-space indentation
- Pydantic models use `by_alias=True` for API field names
