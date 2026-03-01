"""Tests for POST /contacts/v2/search — request permutations and response validation.

Covers key-exclusion permutations of ContactSearchRequest (optional fields
succeed when omitted, required fields fail when omitted, extra fields rejected)
and field-level assertions on SearchContactEntityResult.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from ab.api.models.contacts import (
    ContactSearchParams,
    ContactSearchRequest,
    PageOrderedRequest,
    SearchContactEntityResult,
)
from tests.conftest import assert_no_extra_fields, load_request_fixture, require_fixture

REQUESTS_DIR = Path(__file__).parent.parent / "fixtures" / "requests"


def _load_search_fixture() -> dict:
    """Load ContactSearchRequest fixture and return a deep copy."""
    return copy.deepcopy(load_request_fixture("ContactSearchRequest"))


# ---------------------------------------------------------------------------
# US1: Request key-exclusion permutation tests
# ---------------------------------------------------------------------------

_OPTIONAL_SEARCH_FIELDS = [
    "contactDisplayId",
    "fullName",
    "companyName",
    "companyCode",
    "email",
    "phone",
    "companyDisplayId",
]


@pytest.mark.parametrize("field", _OPTIONAL_SEARCH_FIELDS)
def test_request_optional_search_field_omitted(field: str) -> None:
    """Omitting a single optional field from mainSearchRequest succeeds."""
    data = _load_search_fixture()
    del data["mainSearchRequest"][field]
    model = ContactSearchRequest.model_validate(data)
    assert isinstance(model, ContactSearchRequest)


def test_request_main_search_request_omitted() -> None:
    """Omitting mainSearchRequest entirely succeeds (it is Optional)."""
    data = _load_search_fixture()
    del data["mainSearchRequest"]
    model = ContactSearchRequest.model_validate(data)
    assert isinstance(model, ContactSearchRequest)
    assert model.main_search_request is None


def test_request_main_search_request_empty() -> None:
    """Setting mainSearchRequest to empty object succeeds (all fields optional)."""
    data = _load_search_fixture()
    data["mainSearchRequest"] = {}
    model = ContactSearchRequest.model_validate(data)
    assert isinstance(model, ContactSearchRequest)
    assert model.main_search_request is not None


_OPTIONAL_LOAD_OPTIONS_FIELDS = ["sortingBy", "sortingDirection"]


@pytest.mark.parametrize("field", _OPTIONAL_LOAD_OPTIONS_FIELDS)
def test_request_optional_load_option_omitted(field: str) -> None:
    """Omitting a single optional field from loadOptions succeeds."""
    data = _load_search_fixture()
    del data["loadOptions"][field]
    model = ContactSearchRequest.model_validate(data)
    assert isinstance(model, ContactSearchRequest)


def test_request_load_options_only_required() -> None:
    """loadOptions with only pageNumber and pageSize succeeds."""
    data = _load_search_fixture()
    data["loadOptions"] = {"pageNumber": 1, "pageSize": 10}
    model = ContactSearchRequest.model_validate(data)
    assert isinstance(model, ContactSearchRequest)
    assert model.load_options.sorting_by is None
    assert model.load_options.sorting_direction is None


# --- Required field omissions (should fail) ---

_REQUIRED_LOAD_OPTIONS_FIELDS = ["pageNumber", "pageSize"]


@pytest.mark.parametrize("field", _REQUIRED_LOAD_OPTIONS_FIELDS)
def test_request_required_field_omitted_fails(field: str) -> None:
    """Omitting a required field from loadOptions raises ValidationError."""
    data = _load_search_fixture()
    del data["loadOptions"][field]
    with pytest.raises(ValidationError):
        ContactSearchRequest.model_validate(data)


def test_request_load_options_omitted_fails() -> None:
    """Omitting loadOptions entirely raises ValidationError (required)."""
    data = _load_search_fixture()
    del data["loadOptions"]
    with pytest.raises(ValidationError):
        ContactSearchRequest.model_validate(data)


# --- Extra field rejection ---

_EXTRA_FIELD_LEVELS = [
    ("top-level", []),
    ("mainSearchRequest", ["mainSearchRequest"]),
    ("loadOptions", ["loadOptions"]),
]


@pytest.mark.parametrize("level,path", _EXTRA_FIELD_LEVELS, ids=[l for l, _ in _EXTRA_FIELD_LEVELS])
def test_request_extra_field_rejected(level: str, path: list[str]) -> None:
    """Adding an unknown key at any level raises ValidationError (extra='forbid')."""
    data = _load_search_fixture()
    target = data
    for key in path:
        target = target[key]
    target["bogus"] = 1
    with pytest.raises(ValidationError):
        ContactSearchRequest.model_validate(data)


# ---------------------------------------------------------------------------
# US2: Response model validation tests
# ---------------------------------------------------------------------------


def test_response_field_values() -> None:
    """Mock fixture fields bind to correct Python attributes with correct types."""
    data = require_fixture("SearchContactEntityResult", "POST", "/contacts/v2/search", required=True)
    if isinstance(data, list):
        data = data[0]
    model = SearchContactEntityResult.model_validate(data)
    assert isinstance(model, SearchContactEntityResult)
    assert_no_extra_fields(model)

    assert model.contact_id == 30760
    assert isinstance(model.contact_id, int)
    assert model.contact_full_name == "Justine Yigitbasi"
    assert isinstance(model.contact_full_name, str)
    assert model.contact_email == "oh14004@goNavis.com"
    assert isinstance(model.contact_email, str)
    assert model.company_name == "Navis Pack & Ship #14004OH"
    assert isinstance(model.company_name, str)
    assert model.is_prefered is True
    assert isinstance(model.is_prefered, bool)
    assert model.total_records == 1
    assert isinstance(model.total_records, int)


def test_response_all_null_fields() -> None:
    """Model with all fields as None validates successfully."""
    model = SearchContactEntityResult.model_validate({})
    assert isinstance(model, SearchContactEntityResult)
    assert model.contact_id is None
    assert model.contact_full_name is None
    assert model.contact_email is None
    assert model.company_name is None
    assert model.is_prefered is None
    assert model.total_records is None
