# Quickstart: Extended Operations Endpoints

**Feature**: 008-extended-operations

Quick-reference for developers implementing this feature. Follow the DISCOVER workflow for each batch.

## Setup

```bash
# Ensure you're on the feature branch
git checkout 008-extended-operations

# Install dev dependencies
pip install -e ".[dev]"

# Verify existing tests pass
pytest
```

## Creating a New Endpoint Group (e.g., RFQ)

### Step 1: Models (`ab/api/models/rfq.py`)

```python
from ab.api.models.base import RequestModel, ResponseModel
from pydantic import Field
from typing import Optional

class QuoteRequestDisplayInfo(ResponseModel):
    """RFQ listing entry — GET /job/{jobDisplayId}/rfq."""
    rfq_id: Optional[str] = Field(None, alias="rfqId", description="RFQ ID")
    # ... add fields from swagger + ABConnectTools research

class AcceptModel(RequestModel):
    """Body for POST /rfq/{rfqId}/accept."""
    notes: Optional[str] = Field(None, description="Acceptance notes")
```

### Step 2: Register Models (`ab/api/models/__init__.py`)

```python
from ab.api.models.rfq import QuoteRequestDisplayInfo, AcceptModel
# Add to __all__
```

### Step 3: Endpoint (`ab/api/endpoints/rfq.py`)

```python
from ab.api.base import BaseEndpoint
from ab.api.route import Route
from typing import Any

_GET = Route("GET", "/rfq/{rfqId}", response_model="QuoteRequestDisplayInfo")
_ACCEPT = Route("POST", "/rfq/{rfqId}/accept", request_model="AcceptModel", response_model="ServiceBaseResponse")

class RFQEndpoint(BaseEndpoint):
    def get(self, rfq_id: str) -> Any:
        """GET /rfq/{rfqId} (ACPortal)"""
        return self._request(_GET.bind(rfqId=rfq_id))

    def accept(self, rfq_id: str, **kwargs: Any) -> Any:
        """POST /rfq/{rfqId}/accept (ACPortal)"""
        return self._request(_ACCEPT.bind(rfqId=rfq_id), json=kwargs)
```

### Step 4: Register Endpoint (`ab/api/endpoints/__init__.py` + `ab/client.py`)

```python
# __init__.py
from ab.api.endpoints.rfq import RFQEndpoint

# client.py — in _init_endpoints()
self.rfq = RFQEndpoint(self._acportal)
```

### Step 5: Example (`examples/rfq.py`)

```python
from ab.client import ABConnectAPI

api = ABConnectAPI(env="staging")
rfqs = api.jobs.list_rfqs(job_display_id=12345)
print(rfqs)
```

### Step 6: Test + Fixture

```python
# tests/models/test_rfq_models.py (one file per endpoint group)
class TestRFQModels:
    def test_quote_request_display_info(self):
        data = require_fixture("QuoteRequestDisplayInfo", "GET", "/rfq/{rfqId}")
        model = QuoteRequestDisplayInfo.model_validate(data)
        assert model.rfq_id is not None
```

Note: `require_fixture()` is provided by `conftest.py` and auto-skips when the fixture JSON has not been captured yet.

### Step 7: Sphinx Docs

Create `docs/rfq.rst` with endpoint description, code example, and model cross-reference.

## Extending an Existing Endpoint (e.g., On-Hold on Jobs)

### Step 1: Add Routes to `ab/api/endpoints/jobs.py`

```python
# On-Hold routes
_LIST_ON_HOLD = Route("GET", "/job/{jobDisplayId}/onhold", response_model="List[ExtendedOnHoldInfo]")
_POST_ON_HOLD = Route("POST", "/job/{jobDisplayId}/onhold", request_model="SaveOnHoldRequest", response_model="SaveOnHoldResponse")
```

### Step 2: Add Methods to `JobsEndpoint`

```python
# ---- On-Hold ----------------------------------------------------------

def list_on_hold(self, job_display_id: int) -> Any:
    """GET /job/{jobDisplayId}/onhold (ACPortal)"""
    return self._request(_LIST_ON_HOLD.bind(jobDisplayId=job_display_id))

def create_on_hold(self, job_display_id: int, **kwargs: Any) -> Any:
    """POST /job/{jobDisplayId}/onhold (ACPortal)"""
    return self._request(_POST_ON_HOLD.bind(jobDisplayId=job_display_id), json=kwargs)
```

### Step 3: Add Models to `ab/api/models/jobs.py`

```python
class ExtendedOnHoldInfo(ResponseModel):
    """On-hold record — GET /job/{jobDisplayId}/onhold."""
    id: Optional[str] = Field(None, description="On-hold record ID")
    # ...

class SaveOnHoldRequest(RequestModel):
    """Body for POST/PUT on-hold."""
    reason: str = Field(..., description="Hold reason")
    # ...
```

## Key Patterns

- **Route.bind()**: Returns a new frozen Route with path params substituted
- **`**kwargs` → `json=kwargs`**: For POST/PUT bodies, pass kwargs as JSON
- **`**params` → `params=params`**: For GET query params
- **`response_model="List[Model]"`**: For endpoints returning arrays
- **`response_model="ServiceBaseResponse"`**: For action endpoints returning status
- **Company methods**: Use `self._resolve(company_id)` for code→UUID resolution

## Testing Commands

```bash
# Run all tests
pytest

# Run fixture validation only
pytest tests/models/

# Run swagger param compliance
pytest tests/test_example_params.py

# Run swagger coverage check
pytest tests/test_swagger_compliance.py

# Lint
ruff check .
```

## FIXTURES.md Format

```markdown
| /endpoint/path | METHOD | ReqModel | req-status | RespModel | resp-status | overall | Notes |
```

Status values: `captured`, `needs-data`, `—` (not applicable)
