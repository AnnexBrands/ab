"""Fixture validation tests for global Note models."""

from ab.api.models.notes import GlobalNote, SuggestedUser
from tests.conftest import require_fixture


class TestNotesModels:
    def test_global_note(self):
        data = require_fixture("GlobalNote", "GET", "/note")
        GlobalNote.model_validate(data)

    def test_suggested_user(self):
        data = require_fixture("SuggestedUser", "GET", "/note/suggestUsers")
        SuggestedUser.model_validate(data)
