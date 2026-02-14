"""Fixture validation tests for Note models."""

from tests.conftest import require_fixture

from ab.api.models.jobs import JobNote


class TestNoteModels:
    def test_job_note(self):
        data = require_fixture("JobNote", "GET", "/job/{id}/note")
        model = JobNote.model_validate(data)
        assert model.id is not None
        assert model.comment is not None
        assert model.modify_date is not None
