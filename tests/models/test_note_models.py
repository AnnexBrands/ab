"""Fixture validation tests for Note models."""

from ab.api.models.jobs import JobNote
from tests.conftest import assert_no_extra_fields, require_fixture


class TestNoteModels:
    def test_job_note(self):
        data = require_fixture("JobNote", "GET", "/job/{id}/note")
        model = JobNote.model_validate(data)
        assert isinstance(model, JobNote)
        assert_no_extra_fields(model)
