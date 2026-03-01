# Quickstart: Fix Contact Search

## Verification Steps

### 1. Request Model Validation

```bash
python -c "
from ab.api.models.contacts import ContactSearchRequest
import json
d = json.load(open('tests/fixtures/requests/ContactSearchRequest.json'))
m = ContactSearchRequest.model_validate(d)
print('Extra:', len(m.__pydantic_extra__ or {}))
print('mainSearchRequest:', m.main_search_request)
print('loadOptions:', m.load_options)
"
```

Must print `Extra: 0` and show nested objects.

### 2. Response Model Validation

```bash
python -c "
from ab.api.models.contacts import SearchContactEntityResult
import json
d = json.load(open('tests/fixtures/mocks/SearchContactEntityResult.json'))
if isinstance(d, list): d = d[0]
m = SearchContactEntityResult.model_validate(d)
print('Extra:', len(m.__pydantic_extra__ or {}))
print('contact_full_name:', m.contact_full_name)
print('company_name:', m.company_name)
"
```

Must print `Extra: 0`.

### 3. Tests

```bash
# Request fixture validation
pytest tests/models/test_request_fixtures.py -k ContactSearchRequest -x -q

# Response model validation
pytest tests/models/test_contact_models.py::TestContactModels::test_search_contact_entity_result -x -q

# Full suite — no regressions
pytest tests/ -x -q -m "not live"
```

### 4. Gate Check

```bash
python scripts/generate_progress.py --fixtures | grep "v2/search"
```

Must show all PASS.
