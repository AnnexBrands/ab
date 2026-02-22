# Quickstart: Unified Test Mock Framework

**Feature**: 013-test-mock-framework
**Date**: 2026-02-21

## What This Feature Does

Adds a mock fixture fallback layer and consolidates test constants so that:
1. Model validation tests run offline (no staging credentials needed)
2. The 13 failing tests are fixed (model mismatches, HTTP 404s)
3. The 32 xfailed tests get params_model classes
4. All test constants come from one shared module
5. Sphinx docs can build with example data offline

## Key Changes

### 1. Fixture Loader Fallback

```python
# tests/conftest.py — load_fixture() gains fallback
FIXTURES_DIR = Path(__file__).parent / "fixtures"
MOCKS_DIR = FIXTURES_DIR / "mocks"

def load_fixture(model_name: str) -> dict | list:
    path = FIXTURES_DIR / f"{model_name}.json"
    if not path.exists():
        path = MOCKS_DIR / f"{model_name}.json"
    return json.loads(path.read_text())
```

### 2. Mock Fixture Directory

```
tests/fixtures/mocks/     # New directory for manually-authored mocks
├── PropertyType.json      # Mock: {"propertyType": "residential", ...}
├── DashboardSummary.json  # Mock: example dashboard data
└── ...                    # One per model lacking a live fixture
```

### 3. Constants Consolidation

```python
# examples/jobs.py — BEFORE
TEST_JOB_DISPLAY_ID = 2000000  # duplicated in 11 files

# examples/jobs.py — AFTER
from tests.constants import TEST_JOB_DISPLAY_ID
```

### 4. Model Fixes

```python
# UserRole — BEFORE: expects dict
class UserRole(ResponseModel):
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)

# UserRole — AFTER: matches actual API (list of strings)
# The endpoint return type changes from List[UserRole] to List[str]
```

### 5. Params Models (xfail resolution)

```python
# New params model for routes with swagger query params
class CatalogListParams(RequestModel):
    page: Optional[int] = Field(None, alias="page")
    page_size: Optional[int] = Field(None, alias="pageSize")

# Route updated with params_model
_LIST = Route("GET", "/catalog", params_model="CatalogListParams", ...)
```

## Running Tests

```bash
# Run all model tests offline (no staging needed)
pytest tests/models/ -v

# Run with mock marker to see which use mock fixtures
pytest tests/models/ -v -m mock

# Run full suite
pytest

# Verify fixture coverage
pytest tests/test_mock_coverage.py -v
```

## Adding a New Mock Fixture

1. Create `tests/fixtures/mocks/{ModelName}.json`
2. Populate with realistic, non-sensitive data matching the model's fields
3. Use camelCase keys (matching API response format)
4. Run `pytest tests/models/test_{domain}_models.py` to validate
5. When a live fixture is later captured, it goes in `tests/fixtures/` and automatically takes precedence
