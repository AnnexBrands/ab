# Quickstart: Remaining API Endpoints (009)

## Overview

Feature 009 adds the final 102 endpoints to achieve 100% SDK coverage. It follows the same patterns established in Features 001, 007, and 008.

## Implementation Pattern

Every new endpoint follows the same 4-artifact pattern:

### 1. Route Definition (in endpoint file)
```python
_GET_CALENDAR = Route(
    "GET",
    "/company/{companyId}/calendar/{date}",
    response_model="CalendarDay",
)
```

### 2. Endpoint Method (in endpoint class)
```python
def get_calendar(self, company_id: str, date: str, **kwargs: Any) -> Any:
    """GET /company/{companyId}/calendar/{date}"""
    return self._request(
        _GET_CALENDAR,
        companyId=company_id,
        date=date,
        **kwargs,
    )
```

### 3. Pydantic Model (in model file)
```python
class CalendarDay(ResponseModel):
    """Calendar day data for a company."""
    date: Optional[str] = Field(None, alias="date")
    # ... fields from swagger schema
```

### 4. Fixture Validation Test (in test file)
```python
def test_calendar_day():
    fixture = load_fixture("CalendarDay")
    if fixture is None:
        pytest.skip("Fixture needed: run examples/company_setup.py")
    model = CalendarDay(**fixture)
    assert model
```

## Phase Execution Order

1. **Phase 1** (39 endpoints): `company_setup.py` + `admin.py`
2. **Phase 2** (22 endpoints): `account.py` + extend `jobs.py`
3. **Phase 3** (21 endpoints): `intacct.py`, `esign.py`, `webhooks.py`, `sms_templates.py`, `notifications.py`, `values.py`
4. **Phase 4** (20 endpoints): Extend `companies.py`, `contacts.py`, `address.py`, `documents.py` + ABC gaps

## Key Files Reference

| File | Purpose |
|------|---------|
| `ab/api/endpoints/*.py` | Endpoint classes with Route definitions |
| `ab/api/models/*.py` | Pydantic response/request models |
| `examples/*.py` | Runnable scripts for fixture capture |
| `tests/models/*.py` | Fixture validation tests |
| `docs/*.rst` | Sphinx documentation pages |
| `FIXTURES.md` | 4D tracking (Req Model, Req Fixture, Resp Model, Resp Fixture) |
| `ab/client.py` | Register new endpoint classes |

## DISCOVER Workflow Reference

See `.claude/workflows/DISCOVER.md` for the full phased workflow. Key phases per endpoint group:

- **D**: Research swagger + ABConnectTools for params, bodies, transport
- **I**: Create Pydantic models from swagger schemas
- **S**: Write endpoint methods with correct Route definitions
- **C**: Write examples, run against staging
- **O**: Run pytest, check Four-Way Harmony
- **V**: Commit checkpoint
- **E**: Write Sphinx docs
- **R**: Create PR
