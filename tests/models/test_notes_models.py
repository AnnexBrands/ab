"""Fixture validation tests for global Note models."""

from tests.conftest import require_fixture

from ab.api.models.notes import GlobalNote, SuggestedUser


class TestNotesModels:
    def test_global_note(self):
        data = require_fixture("GlobalNote", "GET", "/note")
        model = GlobalNote.model_validate(data)

    def test_suggested_user(self):
        data = require_fixture("SuggestedUser", "GET", "/note/suggestUsers")
        model = SuggestedUser.model_validate(data)
