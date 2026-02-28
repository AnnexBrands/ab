# Research: Refine Request Models

**Feature**: 019-refine-request-models
**Date**: 2026-02-27

## R1: Endpoint Method Signature Pattern

**Decision**: Replace `**kwargs: Any` with explicit keyword-only parameters that construct the request model internally. Accept both model instances and individual kwargs for backwards compatibility.

**Rationale**: The current pattern `def create(self, **kwargs: Any)` provides zero IDE discoverability. The replacement pattern exposes every parameter with types and descriptions. Accepting a pre-built model instance (`data: ModelClass`) preserves backwards compatibility for callers already constructing dicts or model instances.

**Pattern**:
```python
# BEFORE (no IDE hints)
def update_fulldetails(self, company_id: str, **kwargs: Any) -> CompanyDetails:
    """PUT /companies/{companyId}/fulldetails"""
    return self._request(_UPDATE_FULLDETAILS.bind(companyId=self._resolve(company_id)), json=kwargs)

# AFTER (full IDE hints, backwards compatible)
def update_fulldetails(
    self,
    company_id: str,
    *,
    data: CompanyDetails | dict | None = None,
    # ... or explicit fields if the model is small enough ...
) -> CompanyDetails:
    """PUT /companies/{companyId}/fulldetails.

    Args:
        company_id: Company identifier (display ID or UUID).
        data: Full company details to save. Accepts a CompanyDetails
            instance or a dict with camelCase/snake_case keys.

    Request model: :class:`CompanyDetails`
    """
    body = data if data is not None else {}
    return self._request(
        _UPDATE_FULLDETAILS.bind(companyId=self._resolve(company_id)),
        json=body,
    )
```

**For models with few fields** (< ~8 fields), expose fields directly as keyword arguments:
```python
def search(
    self,
    *,
    search_text: str | None = None,
    page_no: int = 1,
    page_size: int = 25,
    sort_by: SortByModel | None = None,
) -> list[JobSearchResult]:
    """POST /job/searchByDetails.

    Args:
        search_text: Text to search for across job fields.
        page_no: Page number (1-based).
        page_size: Results per page.
        sort_by: Sort configuration.

    Request model: :class:`JobSearchRequest`
    """
    body = dict(search_text=search_text, page_no=page_no, page_size=page_size)
    if sort_by is not None:
        body["sort_by"] = sort_by
    return self._request(_SEARCH_BY_DETAILS, json=body)
```

**For models with many fields** (≥ ~8 fields), use the `data` parameter pattern to avoid method signatures with 20+ parameters.

**Alternatives considered**:
- **Overloads with @typing.overload**: Rejected — adds complexity without IDE benefit beyond what explicit params already provide. Pydantic's `model_validate` already handles both dict and model input.
- **Always expose all fields inline**: Rejected for large models (e.g., `JobCreateRequest` with nested dicts) — would create unwieldy signatures.

---

## R2: Required vs Optional Field Determination

**Decision**: Use a three-tier hierarchy to determine field requirements: (1) C# server source at `/src/ABConnect/`, (2) captured test fixtures, (3) swagger specs. Document any deliberate overrides with inline comments.

**Rationale**: Per constitution v2.3.0 Sources of Truth and spec FR-003, the C# source is the authoritative reference. Swagger is known to have errors. Test fixtures provide secondary validation.

**Process per model**:
1. Find the corresponding C# DTO in `/src/ABConnect/{project}/Models/` or `AB.ABCEntities/`
2. Check each property: non-nullable without `?` suffix → **required** (`str = Field(...)`)
3. Check each property: nullable with `?` or has default value → **optional** (`Optional[str] = Field(None)`)
4. Cross-reference with request fixture (`tests/fixtures/requests/{ModelName}.json`)
5. If fixture omits a field the C# source says is required → keep required, add comment noting fixture gap
6. If C# source conflicts with swagger → follow C# source, add comment documenting swagger deviation

**Key C# paths for field determination**:

| SDK Domain | C# Controller Path | C# DTO Path |
|------------|-------------------|-------------|
| Companies | `ACPortal/ABC.ACPortal.WebAPI/Controllers/CompaniesController.cs` | `ACPortal/ABC.ACPortal.WebAPI/Models/Company*.cs` |
| Contacts | `ACPortal/ABC.ACPortal.WebAPI/Controllers/ContactsController.cs` | `ACPortal/ABC.ACPortal.WebAPI/Models/Contact*.cs` |
| Jobs | `ACPortal/ABC.ACPortal.WebAPI/Controllers/JobController.cs` | `AB.ABCEntities/JobEntities/Job*.cs` |
| Address | `ACPortal/ABC.ACPortal.WebAPI/Controllers/AddressController.cs` | Inline parameters |
| Catalog | `Catalog.WebAPI/Controllers/CatalogController.cs` | `Catalog.WebAPI/Models/*.cs` |
| Commodities | `ACPortal/ABC.ACPortal.WebAPI/Controllers/CommodityController.cs` | `ACPortal/ABC.ACPortal.WebAPI/Models/Commodity*.cs` |

**Alternatives considered**:
- **Trust swagger exclusively**: Rejected — swagger is Tier 3 and has known errors (constitution IV).
- **Trust fixtures exclusively**: Rejected — fixtures only show one valid payload, not all valid combinations.

---

## R3: DRY Request Mixin Architecture

**Decision**: Create request-specific mixins in `ab/api/models/mixins.py` for common field groups. Use composition (multiple inheritance) consistent with the existing response model mixin pattern.

**Rationale**: Currently, pagination fields are defined in at least 3 places with inconsistent names and defaults: `ListRequest` (page/page_size), `JobSearchRequest` (page_no/page_size), `ContactSearchRequest` (page_number/page_size). A single mixin eliminates drift.

**Proposed request mixins**:

```python
class PaginatedRequestMixin(RequestModel):
    """Reusable pagination fields for request models."""
    page: int = Field(1, description="Page number (1-based)")
    page_size: int = Field(25, alias="pageSize", description="Items per page")

class SortableRequestMixin(RequestModel):
    """Reusable sort fields for request models."""
    sort_by: Optional[str] = Field(None, alias="sortBy", description="Field name to sort by")
    sort_dir: Optional[bool] = Field(None, alias="sortDir", description="Sort direction (true=ascending)")

class SearchableRequestMixin(RequestModel):
    """Reusable search text field for request models."""
    search_text: Optional[str] = Field(None, alias="searchText", description="Free-text search query")

class DateRangeRequestMixin(RequestModel):
    """Reusable date range fields for request models."""
    start_date: Optional[str] = Field(None, alias="startDate", description="Range start date (ISO 8601)")
    end_date: Optional[str] = Field(None, alias="endDate", description="Range end date (ISO 8601)")
```

**Composition example**:
```python
class JobSearchRequest(PaginatedRequestMixin, SearchableRequestMixin):
    """Body for POST /job/searchByDetails."""
    sort_by: SortByModel = Field(default_factory=..., alias="sortBy", description="Sort configuration")
    # Field override: JobSearchRequest uses a SortByModel instead of plain str
```

**Note**: When a domain model's field differs from the mixin's type (e.g., `sort_by` is a `SortByModel` object instead of a plain string), the subclass overrides the mixin field. Pydantic handles this correctly.

**Alternatives considered**:
- **Protocol-based composition**: Rejected — Protocols add type complexity without Pydantic integration.
- **Standalone helper functions**: Rejected — doesn't provide IDE discoverability on the model itself.
- **Decorators**: Rejected — obscure field sources, hurt IDE introspection.

---

## R4: G6 Quality Gate Design

**Decision**: Add a G6 gate ("Request Model Quality") to the existing G1-G5 gate system in `ab/progress/gates.py`. G6 evaluates three sub-criteria per endpoint.

**Rationale**: FR-010 requires progress.html to track request model refinement. The existing gate infrastructure provides the natural extension point — adding G6 follows the pattern of G1-G5 without creating a parallel tracking system.

**G6 Sub-criteria**:

| Sub-gate | Check | Implementation |
|----------|-------|----------------|
| G6a: Typed Signature | Endpoint method does NOT use `**kwargs: Any` or `data: dict \| Any` for body/params | Static analysis of endpoint source files — scan for `**kwargs` in method signatures of methods that have a route with `request_model` or `params_model` |
| G6b: Field Descriptions | Every field in the request model has a non-empty `description` in `Field()` | Introspect model class via `model_fields` — check each `FieldInfo` for `description` attribute |
| G6c: Correct Optionality | No `[NEEDS VERIFICATION]` comments remain; model fields match C# source | Convention-based — look for `# TODO: verify optionality` markers in model source |

**EndpointGateStatus extension**:
```python
@dataclass
class EndpointGateStatus:
    # ... existing g1-g5 fields ...
    g6_request_quality: GateResult | None = None
```

**Alternatives considered**:
- **Separate tracking system**: Rejected — duplicates infrastructure and creates two sources of truth for endpoint status.
- **Manual checklist only**: Rejected — doesn't integrate into progress.html or provide automated feedback.

---

## R5: Backwards Compatibility Strategy

**Decision**: Endpoint methods continue to accept dicts through the existing `BaseEndpoint._request()` → `model_cls.check()` pipeline. The `check()` method already calls `model_validate()` which accepts both model instances and dicts.

**Rationale**: FR-007 requires existing callers passing dicts to continue working. The current pipeline already handles this — `check()` calls `model_validate(data)` which accepts `dict`, model instance, or any mapping. No changes to `check()` or `_request()` are needed.

**How it works**:
1. Caller passes `json={"searchText": "acme", "pageNo": 1}` (dict with camelCase keys)
2. `_request()` calls `JobSearchRequest.check(body)`
3. `check()` calls `model_validate(body)` — pydantic resolves both camelCase aliases and snake_case names via `populate_by_name=True`
4. `check()` calls `model_dump(by_alias=True, ...)` — serializes back to camelCase
5. Dict is sent as JSON body

**New typed endpoint methods** construct the dict from keyword arguments, then pass it through the same pipeline:
```python
def search(self, *, search_text=None, page_no=1, page_size=25, sort_by=None):
    body = dict(search_text=search_text, page_no=page_no, ...)
    return self._request(_SEARCH_BY_DETAILS, json=body)
```

**No breaking changes**: callers who already pass dicts continue to work because `_request()` → `check()` → `model_validate()` handles dicts transparently.

---

## R6: Field Description Sources

**Decision**: Derive field descriptions from three sources in priority order: (1) C# DTO XML doc comments, (2) swagger parameter descriptions, (3) field name + type inference.

**Rationale**: FR-002 requires every field to have a description. C# DTOs often have `/// <summary>` XML doc comments that provide the most accurate descriptions. Swagger descriptions are a good secondary source. For fields with neither, a concise description can be inferred from the field name and type.

**Description quality guidelines**:
- One line, 5-15 words
- Explain the field's purpose, not just its type
- Include valid value ranges or enums when known
- Include server default when different from client default
- Example: `description="Company display ID (e.g., '14004OH')"` — not just `description="ID"`

**Automated enforcement**: A test in `tests/models/test_request_descriptions.py` will iterate all `RequestModel` subclasses, introspect `model_fields`, and assert every field has a non-empty `description`.
