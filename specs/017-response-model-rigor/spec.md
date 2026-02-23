# Feature Specification: Response Model Rigor

**Feature Branch**: `017-response-model-rigor`
**Created**: 2026-02-22
**Status**: Draft
**Input**: User description: "Add rigor to gates and internal requirements. Fix list-wrapper bug in BaseEndpoint._request. Mandate fixture capture for every callable endpoint. Identify breakdown in parcels example. Clean up stale progress.html."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Silent Dict Return Bug (Priority: P1)

When an endpoint's Route declares `response_model="List[X]"` but the live API returns a wrapper object (e.g., `{modifiedDate: ..., parcelItems: [...]}` instead of a bare JSON array), the SDK currently returns the raw dict to the caller with no warning. The caller receives untyped data that violates the Pydantic Model Fidelity principle. The SDK MUST detect this mismatch, log a warning, and attempt to unwrap the list from the response dict rather than silently returning raw data.

**Why this priority**: This is a correctness bug. It means `get_parcel_items()` (and any other endpoint whose server wraps a list) returns a dict instead of `list[ParcelItem]`, breaking the SDK's core contract. Callers must use dict-bracket access instead of model attribute access.

**Independent Test**: Call `get_parcel_items(job_id)` on a job with parcels. The result MUST be a `list[ParcelItem]`, not a raw dict.

**Acceptance Scenarios**:

1. **Given** a Route with `response_model="List[ParcelItem]"` and the API returns `{"modifiedDate": "...", "parcelItems": [...]}`, **When** the SDK processes the response, **Then** it MUST extract the list from the wrapper, validate each item as a `ParcelItem`, and return `list[ParcelItem]`.
2. **Given** a Route with `response_model="List[X]"` and the API returns a dict, **When** the dict contains exactly one key whose value is a list, **Then** the SDK MUST unwrap that list and log a warning identifying the wrapper key.
3. **Given** a Route with `response_model="List[X]"` and the API returns a dict with no list values, **When** the SDK processes the response, **Then** it MUST raise a clear error rather than silently returning the dict.
4. **Given** a Route with `response_model="List[X]"` and the API returns a bare JSON array, **When** the SDK processes the response, **Then** it MUST validate each item as model `X` and return a typed list (existing behavior, no regression).

---

### User Story 2 - Mandatory Fixture Capture (Priority: P2)

Every example entry that has a `response_model` MUST also have a `fixture_file` so that successful calls automatically save a fixture. Currently, many example entries (including all parcels entries) declare `response_model` but omit `fixture_file`, so they run successfully against staging but never persist the response for validation testing. This creates a gap where models can drift from reality undetected.

**Why this priority**: Without fixtures, there is no automated validation that model fields match real API responses. The parcels issue (wrong field names on `ParcelItem`) went undetected because no fixture was ever captured to test against.

**Independent Test**: Run a scan across all example files. Every `runner.add()` call that includes `response_model` MUST also include `fixture_file`. Entries with only `request_fixture_file` or no model are exempt.

**Acceptance Scenarios**:

1. **Given** the parcels example, **When** it runs `get_parcel_items` and receives a 200 response, **Then** a fixture file MUST be saved to `tests/fixtures/ParcelItem.json`.
2. **Given** any example entry with `response_model="SomeModel"` but no `fixture_file`, **When** a developer runs a validation check, **Then** the check MUST report the entry as incomplete.
3. **Given** all example files in the repository, **When** scanned for entries with `response_model` but missing `fixture_file`, **Then** the count of such entries MUST be zero after this feature is complete.

---

### User Story 3 - Fixture-Model Consistency Gate (Priority: P3)

A test gate MUST enforce that every saved fixture validates against its declared Pydantic model without extra fields appearing. This already partially exists through auto-discovered fixture validation tests, but it MUST be comprehensive — covering list-response fixtures (where the fixture is a JSON array and each element must validate) and detecting when the fixture shape does not match the model.

**Why this priority**: This closes the loop. US1 fixes the runtime bug, US2 ensures fixtures are captured, and US3 ensures captured fixtures are validated. Together they form a complete safety net.

**Independent Test**: Save a fixture captured from the live API, run the fixture validation test suite, and confirm it validates cleanly against the model. If extra fields appear, the test warns (existing behavior from `extra="allow"` logging).

**Acceptance Scenarios**:

1. **Given** a captured fixture `ParcelItem.json` containing a single item from the live API, **When** the fixture validation test runs, **Then** it MUST `model_validate()` successfully and report zero extra fields.
2. **Given** a list fixture (JSON array), **When** the test runs, **Then** it MUST validate every element in the array, not just the first.
3. **Given** a fixture that contains fields not in the model, **When** the test runs, **Then** it MUST produce a warning identifying the extra fields (per constitution: `extra="allow"` with `logger.warning`).

---

### User Story 4 - Stale Artifact Cleanup (Priority: P4)

The root-level `progress.html` file has been moved to `html/progress.html` but the root copy was not deleted. Stale build artifacts at the repository root create confusion. The root-level copy MUST be removed.

**Why this priority**: Housekeeping. Low effort, low risk, prevents confusion.

**Independent Test**: After cleanup, `progress.html` at repository root does not exist. `html/progress.html` continues to exist.

**Acceptance Scenarios**:

1. **Given** `progress.html` exists at both the repo root and `html/`, **When** cleanup runs, **Then** only `html/progress.html` MUST remain.

---

### Edge Cases

- What happens when a list-wrapper dict has multiple keys whose values are lists? The SDK should log a warning and attempt to find the key that matches the model name (case-insensitive, pluralized).
- What happens when the API returns an empty list vs an empty wrapper dict with an empty list? Both should produce an empty `list[]`.
- What happens when `fixture_file` auto-generation is applied to an entry whose response is `bytes`? It MUST be skipped (binary responses cannot be JSON-serialized).
- What happens when the example call fails with an error? No fixture should be saved, and the failure should be logged without crashing the runner.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The response dispatch logic MUST detect when a declared `List[X]` response is actually a dict wrapper and MUST unwrap the list rather than returning raw data.
- **FR-002**: When unwrapping a list from a dict wrapper, the SDK MUST log a warning identifying the endpoint path and the wrapper key name so developers can correct the Route or model.
- **FR-003**: Every example entry that declares a `response_model` MUST also declare a `fixture_file` using the convention `{ModelName}.json`.
- **FR-004**: A validation test or lint check MUST exist that scans all example files and fails if any entry has `response_model` without `fixture_file`.
- **FR-005**: The fixture validation test suite MUST handle both single-object and array fixtures, validating every element in an array fixture.
- **FR-006**: The stale `progress.html` at the repository root MUST be deleted.
- **FR-007**: The `_save_fixture` method MUST correctly serialize list responses (including list items that are Pydantic models) even when the original API response was a dict wrapper that got unwrapped.

### Key Entities

- **Route**: Declares HTTP method, path template, and optional `response_model` string (e.g., `"List[ParcelItem]"`).
- **ExampleEntry**: A registered example call with metadata including `response_model`, `fixture_file`, and `request_fixture_file`.
- **BaseEndpoint._request**: Core dispatch method that handles response model validation and casting.
- **Fixture**: A JSON file in `tests/fixtures/` representing a real API response, used by validation tests.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `api.jobs.get_parcel_items(job_id)` returns a list of model instances (not a raw dict) for any job with parcels.
- **SC-002**: Zero example entries exist with `response_model` set but `fixture_file` missing — verified by an automated check.
- **SC-003**: All fixture validation tests pass with zero extra-field warnings on models that have been corrected.
- **SC-004**: The test suite count remains stable or increases (no regressions from 307+ passed).
- **SC-005**: `progress.html` does not exist at the repository root after cleanup.

## Assumptions

- The dict-wrapper pattern (API returning `{modifiedDate: ..., items: [...]}` instead of a bare list) may affect endpoints beyond just `get_parcel_items`. The fix should be generic.
- The heuristic for unwrapping should prefer a key whose value is a list. If multiple list-valued keys exist, prefer the one whose name matches the model name (case-insensitive, with common suffixes like `s`, `Items`, `List`).
- Existing fixture validation tests (auto-discovered via `require_fixture`) already handle single-object fixtures. Array fixture handling may need enhancement.
- The `SaveAllParcelItemsRequest` request model discrepancy (swagger says POST uses a wrapper request, our model is different) is out of scope for this feature — focus is on response models and fixtures.
