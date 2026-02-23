# Research: Response Model Rigor

## R1: List-Wrapper Pattern in Live API

**Decision**: Implement generic list-unwrapping in `BaseEndpoint._request` when `response_model="List[X]"` but the response is a dict.

**Rationale**: The user confirmed that `GET /job/{id}/parcelitems` returns `{"modifiedDate": "...", "parcelItems": [...]}` — a dict wrapper around the list. Swagger claims it returns a bare array (`type: "array"`), but per constitution Principle IV (Swagger-Informed, Reality-Validated), the live response is authoritative. The `_request` method line 97 currently returns the raw dict silently when `isinstance(response, list)` is False. This violates Principle I (Pydantic Model Fidelity).

**Alternatives considered**:
- **Per-route explicit wrapper model**: Create a `ParcelItemsResponse` model with `modified_date` and `parcel_items` fields. Rejected — this would require a separate wrapper model for every endpoint that wraps, and there's no way to predict which endpoints wrap without calling them.
- **Fix at the endpoint method level**: Each method that encounters this could manually unwrap. Rejected — fragile, duplicates logic, and new endpoints would hit the same bug.
- **Generic heuristic in `_request`**: When `response_model` says list but response is a dict, find the list-valued key and unwrap. Chosen — single fix point, handles future cases.

**Heuristic design**:
1. If response is a dict and `is_list=True`:
   - Find all keys whose values are lists.
   - If exactly one list key → use it and log a warning.
   - If multiple list keys → prefer the one whose name matches the model name (case-insensitive, e.g., `parcelItems` matches `ParcelItem`).
   - If no list keys → log error and return response (don't crash).
2. Log at `WARNING` level: `"List[{model_name}] response wrapped in dict; unwrapped from key '{key}'. Route: {path}"`

## R2: Missing fixture_file Scope

**Decision**: Add `fixture_file` to all 46 example entries that have `response_model` but missing `fixture_file`.

**Rationale**: Constitution Principle II mandates fixture capture. Constitution Principle III mandates Four-Way Harmony. An example that declares `response_model` but no `fixture_file` violates both — it runs the endpoint but discards the response.

**Findings** (46 entries missing fixture_file across 14 files):
- `parcels.py`: 3 entries (get_parcel_items, get_parcel_items_with_materials, get_packaging_containers)
- `jobs.py`: ~15 entries (timeline, tracking, notes, parcels, item operations)
- `companies.py`: 3 entries (get_details, search, list)
- `shipments.py`: ~7 entries (request_rate_quotes, delete, accessorial, export_data, document)
- `rfq.py`: 2 entries
- `views.py`: 4 entries
- `commodities.py`: 7 entries
- `partners.py`: 2 entries
- `contacts.py`: 1 entry
- `tracking.py`: 2 entries
- `catalog.py`: 2 entries
- `lots.py`: 3 entries
- `reports.py`: 2 entries
- `lookup_extended.py`: 7 entries
- Other: remaining entries

**Convention**: `fixture_file="{ModelName}.json"` for single-object responses, `fixture_file="{ModelName}.json"` for list responses too (the runner already handles list serialization). For `ServiceBaseResponse` responses, use `fixture_file="ServiceBaseResponse.json"` (one shared fixture is fine).

**Special cases**:
- `bytes` responses: Skip fixture_file (runner already handles this).
- `PaginatedList[X]` responses: These use `_paginated_request` not `_request`, fixture_file should use `{X}.json`.
- Entries that will always fail (e.g., `delete_parcel_item` with placeholder ID): Don't add fixture_file since they won't produce a 200.

## R3: Fixture Validation for Array Fixtures

**Decision**: Enhance the existing fixture validation test infrastructure to handle JSON array fixtures.

**Rationale**: Current `require_fixture` loads a fixture and returns it as-is. If the fixture is a JSON array, the test must iterate and validate each element. The `assert_no_extra_fields` helper works on single model instances. Array handling needs to validate the first element (or all elements) against the model.

**Alternatives considered**:
- Validate only first element: Simpler, but misses shape variations between elements. Rejected.
- Validate all elements: More thorough. Chosen — array fixtures are typically small (5-20 items).

## R4: Stale progress.html

**Decision**: Delete `/opt/pack/ab/progress.html` if it exists at root. The file has been moved to `html/progress.html`.

**Rationale**: Simple cleanup. The progress report generator was updated to write to `html/` but the old root-level file was never removed.

**No alternatives needed** — straightforward deletion.
