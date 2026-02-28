# Data Model: Refine Request Models

**Feature**: 019-refine-request-models
**Date**: 2026-02-27

## Entities

### 1. RequestModel (base — existing, unchanged)

The base class for all outbound request bodies. Already exists in `ab/api/models/base.py`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| *(class config)* | `ConfigDict` | — | `extra="forbid"`, `populate_by_name=True`, `alias_generator=_to_camel` |

**Relationships**: Parent of all request model subclasses and request mixins.

---

### 2. Request Mixins (new — added to `ab/api/models/mixins.py`)

Reusable field groups composed into request models via multiple inheritance.

#### 2a. PaginatedRequestMixin

| Field | Type | Required | Default | Alias | Description |
|-------|------|----------|---------|-------|-------------|
| page | `int` | No | `1` | `page` | Page number (1-based) |
| page_size | `int` | No | `25` | `pageSize` | Items per page |

**Used by**: `ListRequest`, `JobSearchRequest`, `ContactSearchRequest`, report request models.

#### 2b. SortableRequestMixin

| Field | Type | Required | Default | Alias | Description |
|-------|------|----------|---------|-------|-------------|
| sort_by | `Optional[str]` | No | `None` | `sortBy` | Field name to sort by |
| sort_dir | `Optional[bool]` | No | `None` | `sortDir` | Sort direction (true=ascending) |

**Used by**: `ListRequest`, search request models with simple sort.

**Note**: Models that use a complex sort object (e.g., `JobSearchRequest.sort_by: SortByModel`) override this mixin field at the subclass level.

#### 2c. SearchableRequestMixin

| Field | Type | Required | Default | Alias | Description |
|-------|------|----------|---------|-------|-------------|
| search_text | `Optional[str]` | No | `None` | `searchText` | Free-text search query |

**Used by**: `JobSearchRequest`, `CompanySearchRequest`, `CommoditySearchRequest`, `ContactSearchRequest`.

#### 2d. DateRangeRequestMixin

| Field | Type | Required | Default | Alias | Description |
|-------|------|----------|---------|-------|-------------|
| start_date | `Optional[str]` | No | `None` | `startDate` | Range start date (ISO 8601) |
| end_date | `Optional[str]` | No | `None` | `endDate` | Range end date (ISO 8601) |

**Used by**: Report request models, history request models.

---

### 3. Refined Request Models (existing — updated)

Each existing request model is refined by:
1. Correcting required vs optional based on C# source
2. Adding `description` to every `Field()`
3. Composing shared mixins where applicable
4. Aligning `alias` values with actual API field names

**Example: Before → After**

```python
# BEFORE
class JobSearchRequest(RequestModel):
    search_text: Optional[str] = Field(None, alias="searchText", description="Search query")
    page_no: int = Field(1, alias="pageNo", description="Page number")
    page_size: int = Field(25, alias="pageSize", description="Results per page")
    sort_by: SortByModel = Field(default_factory=..., alias="sortBy", description="Sort configuration")

# AFTER
class JobSearchRequest(PaginatedRequestMixin, SearchableRequestMixin):
    """Body for POST /job/searchByDetails.

    Searches jobs by text across multiple fields. Supports pagination
    and configurable sort order.
    """
    # Override PaginatedRequestMixin.page → pageNo (API-specific alias)
    page: int = Field(1, alias="pageNo", description="Page number (1-based)")
    sort_by: SortByModel = Field(
        default_factory=lambda: SortByModel(sort_by_field=1, sort_dir=True),
        alias="sortBy",
        description="Sort configuration (field index + direction)",
    )
```

---

### 4. EndpointGateStatus (existing — extended)

Extended with G6 field for request model quality tracking.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| endpoint_path | `str` | Yes | API path |
| method | `str` | Yes | HTTP method |
| request_model | `str \| None` | No | Request model name |
| response_model | `str \| None` | No | Response model name |
| g1_model_fidelity | `GateResult \| None` | No | Response model field coverage |
| g2_fixture_status | `GateResult \| None` | No | Fixture exists on disk |
| g3_test_quality | `GateResult \| None` | No | Test assertions present |
| g4_doc_accuracy | `GateResult \| None` | No | Return type annotation correct |
| g5_param_routing | `GateResult \| None` | No | Query params via params_model |
| **g6_request_quality** | **`GateResult \| None`** | **No** | **Request model quality (typed sig, descriptions, optionality)** |

---

### 5. Endpoint Method Signature (contract — not a model)

The contract between endpoint classes and their callers. Not a Pydantic model but a structural pattern.

**For body-accepting endpoints (POST/PUT/PATCH)**:

| Parameter | Position | Type | Notes |
|-----------|----------|------|-------|
| self | positional | — | Instance |
| *path_params* | positional | `str` or `int` | One per `{placeholder}` in route path |
| `*` | — | — | Keyword-only separator |
| *model fields* | keyword-only | Typed | Each field from request model, with defaults matching model defaults |
| `data` | keyword-only | `ModelClass \| dict \| None` | Alternative: pass pre-built model/dict (used for large models) |

**For params-accepting endpoints (GET with query params)**:

| Parameter | Position | Type | Notes |
|-----------|----------|------|-------|
| self | positional | — | Instance |
| *path_params* | positional | `str` or `int` | One per `{placeholder}` in route path |
| `*` | — | — | Keyword-only separator |
| *params fields* | keyword-only | Typed | Each field from params model |

---

## Validation Rules

1. **extra="forbid"**: All `RequestModel` subclasses reject unknown fields (existing, unchanged).
2. **Required fields**: Use `Field(...)` (ellipsis) — pydantic raises `ValidationError` if omitted.
3. **Optional fields**: Use `Optional[T] = Field(None, ...)` — excluded from serialized output via `exclude_none=True`.
4. **Default-valued fields**: Use `T = Field(default, ...)` — always serialized (not None, not unset).
5. **Alias enforcement**: `by_alias=True` in `model_dump()` ensures wire format uses camelCase/PascalCase.
6. **Description enforcement**: Automated test asserts every field has non-empty `description`.

## State Transitions

N/A — Request models are stateless value objects. They are constructed, validated, serialized, and discarded within a single method call.
