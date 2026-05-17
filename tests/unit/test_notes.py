"""Unit tests for the notes endpoint group.

Documents the **wire-level behaviour** of the notes methods using a mocked
:class:`~ab.http.HttpClient`. Locks in:

* routes hit by each method,
* ``params`` / ``json`` payloads (alias keys, exclude_none),
* required-field enforcement (swagger ``NoteModel.comments`` and
  ``category``),
* the forward references ``SuggestedUser.id`` ->
  ``NoteRequest.assigned_users[].id`` and
  ``LookupValue.value`` -> ``NoteRequest.category``,
* the shared POST/PUT schema (single :class:`NoteRequest`).

Live behaviour is exercised by ``tests/integration/test_notes.py``.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from ab.api.endpoints.notes import NotesEndpoint
from ab.api.models.notes import (
    GlobalNote,
    GlobalNoteCreateRequest,
    GlobalNoteUpdateRequest,
    NoteRequest,
    SuggestedUser,
)


@pytest.fixture
def client():
    return MagicMock(name="HttpClient")


@pytest.fixture
def notes(client):
    return NotesEndpoint(client)


# ---------------------------------------------------------------------------
# GET /note
# ---------------------------------------------------------------------------


class TestListRoute:
    def test_no_params_sends_empty_query(self, notes, client):
        client.request.return_value = []
        notes.list()
        args, kwargs = client.request.call_args
        assert args == ("GET", "/note")
        assert kwargs["params"] == {}

    def test_filters_use_camel_case_aliases(self, notes, client):
        client.request.return_value = []
        notes.list(
            category=["cat-1", "cat-2"],
            job_id="job-uuid",
            contact_id=42,
            company_id="company-uuid",
        )
        params = client.request.call_args.kwargs["params"]
        assert params == {
            "category": ["cat-1", "cat-2"],
            "jobId": "job-uuid",
            "contactId": 42,
            "companyId": "company-uuid",
        }

    def test_response_casts_to_list_of_global_note(self, notes, client):
        client.request.return_value = [
            {
                "noteID": 1,
                "comments": "hello",
                "category": "cat",
                "isImportant": True,
                "isCompleted": False,
                "modifiyDate": "2026-01-02T12:34:56",
            }
        ]
        out = notes.list()
        assert len(out) == 1
        assert isinstance(out[0], GlobalNote)
        assert out[0].note_id == 1
        # Server typo -> Python attribute.
        assert out[0].modified_date is not None


# ---------------------------------------------------------------------------
# POST /note and PUT /note/{id} -- shared schema
# ---------------------------------------------------------------------------


class TestCreateRoute:
    def test_create_posts_note_request(self, notes, client):
        client.request.return_value = {"noteID": 100, "comments": "x", "category": "c"}
        body = NoteRequest(comments="hello", category="cat-uuid")
        notes.create(data=body)
        args, kwargs = client.request.call_args
        assert args == ("POST", "/note")
        assert kwargs["json"] == {"comments": "hello", "category": "cat-uuid"}

    def test_create_rejects_missing_required_fields(self, notes):
        # NoteRequest.check() validates the dict before sending; comments +
        # category are required by swagger NoteModel.
        with pytest.raises(Exception):
            notes.create(data={"comments": "no-category"})
        with pytest.raises(Exception):
            notes.create(data={"category": "no-comments"})
        with pytest.raises(Exception):
            notes.create(data={})

    def test_create_response_casts_to_global_note(self, notes, client):
        client.request.return_value = {"noteID": 100, "comments": "x", "category": "c"}
        out = notes.create(data=NoteRequest(comments="x", category="c"))
        assert isinstance(out, GlobalNote)
        assert out.note_id == 100


class TestUpdateRoute:
    def test_update_binds_id_and_posts_note_request(self, notes, client):
        client.request.return_value = {"noteID": 7, "comments": "x", "category": "c"}
        body = NoteRequest(comments="updated", category="cat-uuid", is_completed=True)
        notes.update("7", data=body)
        args, kwargs = client.request.call_args
        assert args == ("PUT", "/note/7")
        assert kwargs["json"] == {
            "comments": "updated",
            "category": "cat-uuid",
            "isCompleted": True,
        }

    def test_update_uses_same_required_fields_as_create(self, notes):
        # POST and PUT share NoteModel -> comments + category required on both.
        with pytest.raises(Exception):
            notes.update("7", data={"isCompleted": True})


class TestSharedSchema:
    """``NoteRequest`` is the single source of truth for POST and PUT."""

    def test_legacy_aliases_resolve_to_note_request(self):
        assert GlobalNoteCreateRequest is NoteRequest
        assert GlobalNoteUpdateRequest is NoteRequest

    def test_create_and_update_routes_reference_same_request_model(self):
        from ab.api.endpoints.notes import _CREATE, _UPDATE

        assert _CREATE.request_model == "NoteRequest"
        assert _UPDATE.request_model == "NoteRequest"


# ---------------------------------------------------------------------------
# GET /note/suggestUsers
# ---------------------------------------------------------------------------


class TestSuggestUsersRoute:
    def test_search_key_is_positional_required(self, notes):
        # Method signature makes search_key positional/required -- TypeError
        # if omitted.
        with pytest.raises(TypeError):
            notes.suggest_users()  # type: ignore[call-arg]

    def test_route_and_alias_keys(self, notes, client):
        client.request.return_value = []
        notes.suggest_users("brett", company_id="company-uuid")
        args, kwargs = client.request.call_args
        assert args == ("GET", "/note/suggestUsers")
        # Swagger uses PascalCase aliases for these params.
        assert kwargs["params"] == {
            "SearchKey": "brett",
            "CompanyId": "company-uuid",
        }

    def test_response_casts_to_list_of_suggested_user(self, notes, client):
        client.request.return_value = [
            {"id": 1, "fullName": "Alice"},
            {"id": 2, "fullName": "Bob"},
        ]
        out = notes.suggest_users("a")
        assert len(out) == 2
        assert all(isinstance(u, SuggestedUser) for u in out)
        # Forward reference: id (int) -> NoteRequest.assigned_users[].id
        body = NoteRequest(
            comments="hi", category="cat-uuid",
            assigned_users=[SuggestedUser(id=u.id, fullName=u.full_name) for u in out],
        )
        assert [u.id for u in body.assigned_users] == [1, 2]


# ---------------------------------------------------------------------------
# Forward reference: lookup -> NoteRequest.category
# ---------------------------------------------------------------------------


def test_lookup_category_uuid_feeds_note_request_category():
    """``api.lookup.get_refer_categories()`` returns ``LookupValue`` whose
    ``value`` is the UUID that becomes ``NoteRequest.category``.
    """
    from ab.api.models.lookup import LookupValue

    lv = LookupValue(value="5cf9b0f5-a5fa-43f1-b13c-1d44e8b2ac3b", name="Job Update")
    body = NoteRequest(comments="hi", category=lv.value)
    assert body.category == lv.value
