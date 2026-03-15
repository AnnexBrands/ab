# Quickstart: Fix FreightProviders Drift

**Feature**: 033-fix-freightproviders-drift
**Date**: 2026-03-15

## Test Scenarios

### Scenario 1: Model Expansion Validation

```python
# After expanding PricedFreightProvider, validate against live data:
from ab import ABConnectAPI

api = ABConnectAPI()
providers = api.jobs.list_freight_providers(2000000)

# Should produce ZERO "extra fields not in model" warnings
# Each provider should have all 15 fields accessible as typed attributes
for p in providers:
    print(f"{p.provider_company_name}: ${p.total_sell} ({p.transit} days)")
    print(f"  Carrier account: {p.used_carrier_account_info.friendly_name}")
```

### Scenario 2: Fixture Capture

```bash
# Run the example to capture a real fixture:
python examples/freight_providers.py

# Verify fixture is populated:
python -c "import json; d=json.load(open('tests/fixtures/PricedFreightProvider.json')); print(f'{len(d)} items'); print(json.dumps(d[0], indent=2) if d else 'EMPTY')"
```

### Scenario 3: Test Validation

```bash
# Run freight model tests — should NOT skip:
pytest tests/models/test_freight_models.py -v

# Expected: all tests PASS (not skip)
```

### Scenario 4: CLI Verification

```bash
# CLI should produce no warnings:
abs job list_freight_providers 2000000

# Expected: clean JSON output, no "extra fields" warnings
```

### Scenario 5: Progress Artifact Consistency

```bash
# Regenerate and verify:
python scripts/generate_progress.py
python scripts/generate_progress.py --fixtures

# Check api-surface.md freight section shows correct "AB done" count
# Check FIXTURES.md shows legitimate gate results
# Check progress.html shows consistent status
```

## Key Files to Modify

| File | Change |
|------|--------|
| `ab/api/models/jobs.py` | Expand PricedFreightProvider (3→15 fields), add CarrierAccountInfo + CarrierAPI, expand ShipmentPlanProvider (1→22 fields) |
| `tests/fixtures/PricedFreightProvider.json` | Replace `[]` with captured live response |
| `tests/fixtures/requests/ShipmentPlanProvider.json` | Replace null stubs with realistic values |
| `tests/models/test_freight_models.py` | Add tests for new models, ensure no skips |
| `examples/freight_providers.py` | Update to exercise full model fields |
| `specs/api-surface.md` | Update "AB done: 0 of 3" → "AB done: 3 of 3" |
| `FIXTURES.md` | Regenerate with accurate gate results |
| `html/progress.html` | Regenerate from updated data |
| `docs/` | Rebuild Sphinx to reflect expanded models |

## Verification Checklist

- [ ] `abs job list_freight_providers 2000000` produces zero extra-field warnings
- [ ] `PricedFreightProvider.json` fixture has at least one populated object
- [ ] `pytest tests/models/test_freight_models.py` — all tests PASS (no skips)
- [ ] `api-surface.md` freight section says "AB done: 3 of 3"
- [ ] `python scripts/generate_progress.py` runs clean with consistent results
- [ ] `python scripts/generate_progress.py --fixtures` shows no regressions
