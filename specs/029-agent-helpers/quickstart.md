# Quickstart: 029 — Agent Assignment Helpers

## Scenario 1: Change Origin Agent

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

# Change origin agent using a friendly code
result = api.jobs.agent.oa(12345, "3P-5153")
if result:
    print("Origin agent changed successfully")
else:
    print(f"Failed: {result.error_message}")
    result.raise_for_error()
```

## Scenario 2: Change Delivery Agent with Price Recalculation

```python
result = api.jobs.agent.da(
    12345,
    "9999AZ",
    recalculate_price=True,
    apply_rebate=True,
)
print(f"Success: {result.success}")
```

## Scenario 3: Change Agent with Explicit Service Type

```python
from ab.api.models.enums import ServiceType

# Change pick-only agent
result = api.jobs.agent.change(
    12345,
    "9999AZ",
    service_type=ServiceType.PICK,
)

# Using raw integer (forward-compatible)
result = api.jobs.agent.change(12345, "9999AZ", service_type=1)
```

## Scenario 4: Using UUID Directly (No Code Resolution)

```python
# If you already have the agent UUID, pass it directly
result = api.jobs.agent.oa(12345, "ed282b80-54fe-4f42-bf1b-69103ce1f76c")
# The resolver detects it's already a UUID and skips the cache lookup
```

## Scenario 5: UAT Validation

```bash
# 1. Run full test suite (expect 0 failures)
cd src && pytest --tb=line -q

# 2. Run gate regression test
pytest tests/test_gate_regression.py -v

# 3. Run mock coverage integrity
pytest tests/test_mock_coverage.py -v

# 4. Update gate baseline (after new endpoint is added)
python scripts/update_gate_baseline.py

# 5. Regenerate FIXTURES.md
python scripts/generate_progress.py --fixtures
```
