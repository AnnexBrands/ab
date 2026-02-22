# Quickstart: Endpoint CLI

**Feature**: 014-endpoint-cli
**Date**: 2026-02-22

## What This Feature Does

Adds two console commands (`ab` and `abs`) that call ABConnect API endpoints directly from the terminal. Works exactly like the existing `ex` command for aliases and navigation, but executes real API calls instead of running example scripts.

- `ab` → production API (`ABConnectAPI()`)
- `abs` → staging API (`ABConnectAPI(env="staging")`)

## Key Changes

### 1. Console Script Entry Points

```toml
# pyproject.toml
[project.scripts]
ex = "examples.__main__:main"
ab = "ab.cli:main_prod"        # NEW
abs = "ab.cli:main_staging"    # NEW
```

### 2. CLI Module Structure

```
ab/cli/
├── __init__.py          # Exports main_prod, main_staging
├── __main__.py          # Core dispatch: main(env=None)
├── aliases.py           # Shared ALIASES dict (imported by both ex and ab)
├── discovery.py         # Endpoint/method introspection
├── parser.py            # CLI argument → Python kwargs conversion
└── formatter.py         # Result → stdout formatting
```

### 3. Shared Aliases

```python
# ab/cli/aliases.py — single source of truth
ALIASES = {
    "addr": "address",
    "q": "autoprice",
    "cat": "catalog",
    "co": "companies",
    "ct": "contacts",
    ...
}

# examples/__main__.py — AFTER (imports shared dict)
from ab.cli.aliases import ALIASES
```

### 4. Endpoint Discovery

```python
# ab/cli/discovery.py
import inspect
from ab.api.base import BaseEndpoint

def discover_endpoints(api):
    """Introspect ABConnectAPI instance for endpoint attributes."""
    endpoints = {}
    for name in dir(api):
        attr = getattr(api, name)
        if isinstance(attr, BaseEndpoint):
            methods = {
                m: inspect.signature(getattr(attr, m))
                for m in dir(attr)
                if not m.startswith("_") and callable(getattr(attr, m))
            }
            endpoints[name] = {"instance": attr, "methods": methods}
    return endpoints
```

### 5. CLI Argument Parsing

```bash
# Positional args → path parameters
ab jobs get 2000000
# Translates to: api.jobs.get(2000000)

# Flag args → keyword parameters
abs addr validate --line1="12742 E Caley Av" --city=Centennial --state=CO --zip=80111
# Translates to: api.address.validate(line1="12742 E Caley Av", city="Centennial", state="CO", zip="80111")

# JSON body for POST endpoints
ab jobs create --body='{"companyId": "abc-123"}'
# Translates to: api.jobs.create({"companyId": "abc-123"})
```

### 6. Output Formatting

```bash
$ abs addr validate --line1="12742 E Caley Av" --city=Centennial --state=CO --zip=80111
{
  "isValid": true,
  "city": "Centennial",
  "state": "CO",
  "zip": "80111",
  "addressType": "residential"
}
```

## Usage Examples

```bash
# List all endpoint groups
ab --list

# List methods in an endpoint
ab jobs --list

# Call a method (production)
ab addr validate --line1="123 Main St" --city=Denver --state=CO --zip=80202

# Call a method (staging)
abs addr validate --line1="123 Main St" --city=Denver --state=CO --zip=80202

# Use aliases and prefix matching
ab co get_by_id ABC123       # co → companies
ab lu countries              # lu → lookup, countries → get_countries

# Dot syntax
ab addr.validate --line1="123 Main St"

# Get help for a method
ab addr validate --help
```

## Running Tests

```bash
# Existing tests (must stay green)
pytest --tb=short -q

# Ruff checks
ruff check .

# Sphinx docs
cd docs && make html

# Manual CLI smoke test
pip install -e . && abs addr validate --line1="12742 E Caley Av" --city=Centennial --state=CO --zip=80111
```
