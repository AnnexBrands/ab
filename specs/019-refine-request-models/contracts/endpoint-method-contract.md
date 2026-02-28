# Contract: Endpoint Method Signatures

**Feature**: 019-refine-request-models
**Date**: 2026-02-27

## Overview

This contract defines the structural pattern for all refined endpoint methods. Every endpoint method that accepts request body or query parameters MUST follow one of these two patterns.

---

## Pattern A: Inline Fields (≤ 8 model fields)

Use when the request model has 8 or fewer fields. Each model field becomes a keyword-only argument.

```python
def method_name(
    self,
    path_param: str,              # One per {placeholder} in route
    *,                             # Keyword-only separator
    field_1: type = default,       # From request model
    field_2: type | None = None,   # Optional field
    field_3: type = default,       # With default
) -> ResponseType:
    """HTTP_METHOD /path/{path_param}.

    Args:
        path_param: Description of path parameter.
        field_1: Description matching model Field(description=...).
        field_2: Description matching model Field(description=...).
        field_3: Description matching model Field(description=...).

    Request model: :class:`RequestModelName`
    """
    body = dict(field_1=field_1, field_2=field_2, field_3=field_3)
    return self._request(
        _ROUTE.bind(path_param=path_param),
        json=body,  # or params=body for GET endpoints
    )
```

### Rules

- Path parameters are **positional** arguments before `*`.
- Model fields are **keyword-only** arguments after `*`.
- Default values match the model's `Field()` defaults exactly.
- Required model fields (no default) become required keyword arguments.
- The docstring references the request model class name.
- The `body` dict uses **snake_case** keys — `check()` handles alias conversion.

### Example

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
        search_text: Free-text search across job fields.
        page_no: Page number (1-based).
        page_size: Results per page (max 100).
        sort_by: Sort configuration (field index + direction).

    Request model: :class:`JobSearchRequest`
    """
    body = dict(search_text=search_text, page_no=page_no, page_size=page_size)
    if sort_by is not None:
        body["sort_by"] = sort_by
    return self._request(_SEARCH_BY_DETAILS, json=body)
```

---

## Pattern B: Data Parameter (> 8 model fields)

Use when the request model has more than 8 fields, or when the model contains nested objects (e.g., `customer: dict`, `items: list[dict]`).

```python
def method_name(
    self,
    path_param: str,
    *,
    data: RequestModelName | dict,
) -> ResponseType:
    """HTTP_METHOD /path/{path_param}.

    Args:
        path_param: Description of path parameter.
        data: Request body. Accepts a :class:`RequestModelName`
            instance or a dict with camelCase/snake_case keys.

    Request model: :class:`RequestModelName`
    """
    return self._request(
        _ROUTE.bind(path_param=path_param),
        json=data if isinstance(data, dict) else data.model_dump(
            by_alias=True, exclude_none=True, mode="json"
        ),
    )
```

### Rules

- The `data` parameter accepts both model instances and plain dicts.
- When a dict is passed, `_request()` → `check()` validates and converts it.
- When a model instance is passed, it is already validated.
- The docstring lists the model class name for IDE navigation.
- Path parameters remain positional before `*`.

### Example

```python
def create(
    self,
    *,
    data: JobCreateRequest | dict,
) -> dict:
    """POST /job.

    Args:
        data: Job creation payload with customer, pickup, delivery,
            items, and services. Accepts a :class:`JobCreateRequest`
            instance or a dict.

    Request model: :class:`JobCreateRequest`
    """
    return self._request(_CREATE, json=data)
```

---

## Pattern C: Combined Body + Params

Use when a single endpoint has both `request_model` (body) and `params_model` (query parameters).

```python
def method_name(
    self,
    path_param: str,
    *,
    # Query params (from params_model)
    query_field_1: type | None = None,
    # Body (from request_model — inline or data pattern)
    body_field_1: type,
    body_field_2: type | None = None,
) -> ResponseType:
    """HTTP_METHOD /path/{path_param}.

    Args:
        path_param: Description.
        query_field_1: Query parameter description.
        body_field_1: Body field description.
        body_field_2: Body field description.

    Request model: :class:`BodyModelName`
    Params model: :class:`ParamsModelName`
    """
    body = dict(body_field_1=body_field_1, body_field_2=body_field_2)
    params = dict(query_field_1=query_field_1)
    return self._request(
        _ROUTE.bind(path_param=path_param),
        json=body,
        params=params,
    )
```

### Example

```python
def create_timeline_task(
    self,
    job_display_id: int,
    *,
    # Query params (TimelineCreateParams)
    create_email: bool | None = None,
    # Body fields (TimelineTaskCreateRequest)
    task_code: str,
    scheduled_date: str | None = None,
    comments: str | None = None,
    agent_contact_id: str | None = None,
) -> TimelineTask:
    """POST /job/{jobDisplayId}/timeline.

    Args:
        job_display_id: Job display ID.
        create_email: Send status notification email (query param).
        task_code: Task type code (required).
        scheduled_date: When the task is scheduled.
        comments: Task notes.
        agent_contact_id: Assigned agent contact ID.

    Request model: :class:`TimelineTaskCreateRequest`
    Params model: :class:`TimelineCreateParams`
    """
    body = dict(task_code=task_code, scheduled_date=scheduled_date,
                comments=comments, agent_contact_id=agent_contact_id)
    params = dict(create_email=create_email)
    return self._request(
        _POST_TIMELINE.bind(jobDisplayId=job_display_id),
        json=body,
        params=params,
    )
```

---

## G6 Gate Evaluation Contract

An endpoint passes G6 when ALL of the following are true:

1. **G6a — Typed Signature**: The endpoint method does NOT contain `**kwargs: Any` or `data: dict | Any` for body/params arguments (path params are excluded from this check). Methods for endpoints with `request_model` or `params_model` on their Route MUST use Pattern A, B, or C above.

2. **G6b — Field Descriptions**: Every field in every `RequestModel` subclass referenced by the endpoint's Route has a non-empty `description` in its `Field()` declaration.

3. **G6c — Optionality Verified**: The model source file does NOT contain `# TODO: verify optionality` comments for any field of the referenced request/params model.

**Gate result**: `PASS` if all three sub-criteria pass. `FAIL` with reason listing which sub-criterion failed.

---

## Docstring Contract

Every refined endpoint method MUST have a docstring containing:

1. **First line**: `HTTP_METHOD /path/template` (matches the Route definition)
2. **Args section**: One entry per parameter, matching the `description` from `Field()`
3. **Request model line**: `Request model: :class:\`ModelName\`` (if body is accepted)
4. **Params model line**: `Params model: :class:\`ModelName\`` (if query params are accepted)

This enables Sphinx autodoc to generate complete API reference documentation.
