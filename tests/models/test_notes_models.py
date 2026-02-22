"""Fixture validation tests for global Note models."""

from ab.api.models.notes import GlobalNote, SuggestedUser
from tests.conftest import assert_no_extra_fields, require_fixture


class TestNotesModels:
    def test_global_note(self):
        data = require_fixture("GlobalNote", "GET", "/note")
        model = GlobalNote.model_validate(data)
        assert isinstance(model, GlobalNote)
        assert_no_extra_fields(model)

    def test_suggested_user(self):
        data = require_fixture("SuggestedUser", "GET", "/note/suggestUsers")
        model = SuggestedUser.model_validate(data)
        assert isinstance(model, SuggestedUser)
        assert_no_extra_fields(model)
