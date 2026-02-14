"""Fixture validation tests for Timeline models."""

from tests.conftest import require_fixture

from ab.api.models.jobs import TimelineAgent, TimelineTask


class TestTimelineModels:
    def test_timeline_task(self):
        data = require_fixture("TimelineTask", "GET", "/job/{id}/timeline")
        model = TimelineTask.model_validate(data)
        assert model.task_code is not None
        assert model.is_completed is not None

    def test_timeline_agent(self):
        data = require_fixture("TimelineAgent", "GET", "/job/{id}/timeline/{taskCode}/agent")
        model = TimelineAgent.model_validate(data)
        assert model.contact_id is not None
        assert model.name is not None
