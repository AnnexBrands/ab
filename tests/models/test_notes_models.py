"""Fixture validation tests for global note models."""

from ab.api.models.notes import (
    GlobalNote,
    GlobalNoteCreateRequest,
    NoteRequest,
    SuggestedUser,
)
from tests.conftest import (
    assert_no_extra_fields,
    first_or_skip,
    load_request_fixture,
    require_fixture,
)


class TestGlobalNoteModel:
    def test_validates_all_rows(self):
        data = require_fixture("GlobalNote", "GET", "/note")
        assert isinstance(data, list) and data, "fixture must be a non-empty list"
        for row in data:
            model = GlobalNote.model_validate(row)
            assert_no_extra_fields(model)

    def test_swagger_shape(self):
        data = require_fixture("GlobalNote", "GET", "/note")
        model = GlobalNote.model_validate(first_or_skip(data))
        # Required swagger fields per ``Notes``.
        assert isinstance(model.note_id, int)
        # Forward reference: assigned_users[].id -> NoteRequest.assigned_users[].id
        if model.assigned_users:
            assert all(isinstance(u, SuggestedUser) for u in model.assigned_users)

    def test_modifiy_date_alias_round_trips(self):
        # Server uses the "modifiyDate" wire spelling (typo); SDK aliases it
        # to `modified_date`. Round-trip a row that includes the field so we
        # can prove the alias works (data-dependent: the live row may have
        # the field null).
        row = {"noteID": 1, "modifiyDate": "2026-01-02T12:34:56"}
        model = GlobalNote.model_validate(row)
        assert model.modified_date is not None
        # Reverse: dumping with alias produces the original wire spelling.
        dumped = model.model_dump(by_alias=True, exclude_none=True)
        assert "modifiyDate" in dumped


class TestSuggestedUserModel:
    def test_validates_all_rows(self):
        data = require_fixture("SuggestedUser", "GET", "/note/suggestUsers")
        assert isinstance(data, list) and data, "fixture must be a non-empty list"
        for row in data:
            model = SuggestedUser.model_validate(row)
            assert_no_extra_fields(model)

    def test_swagger_shape(self):
        data = require_fixture("SuggestedUser", "GET", "/note/suggestUsers")
        model = SuggestedUser.model_validate(first_or_skip(data))
        assert isinstance(model.id, int)
        assert model.full_name is not None


class TestNoteRequestModel:
    def test_create_fixture_validates(self):
        raw = load_request_fixture("GlobalNoteCreateRequest")
        model = NoteRequest.model_validate(raw)
        assert model.comments and model.category

    def test_update_fixture_validates(self):
        raw = load_request_fixture("GlobalNoteUpdateRequest")
        model = NoteRequest.model_validate(raw)
        # Update uses the same schema -> comments + category required.
        assert model.comments and model.category

    def test_create_and_update_aliases_are_note_request(self):
        assert GlobalNoteCreateRequest is NoteRequest

    def test_required_fields_enforced(self):
        import pytest

        with pytest.raises(Exception):
            NoteRequest.model_validate({})  # missing comments + category
        with pytest.raises(Exception):
            NoteRequest.model_validate({"comments": "hi"})  # missing category
        with pytest.raises(Exception):
            NoteRequest.model_validate({"category": "abc"})  # missing comments
