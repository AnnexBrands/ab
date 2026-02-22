"""Fixture validation tests for Timeline models."""

from ab.api.models.jobs import TimelineAgent, TimelineTask
from tests.conftest import assert_no_extra_fields, require_fixture


class TestTimelineModels:
    def test_timeline_task(self):
        data = require_fixture("TimelineTask", "GET", "/job/{id}/timeline")
        model = TimelineTask.model_validate(data)
        assert isinstance(model, TimelineTask)
        assert_no_extra_fields(model)

    def test_timeline_agent(self):
        data = require_fixture("TimelineAgent", "GET", "/job/{id}/timeline/{taskCode}/agent")
        model = TimelineAgent.model_validate(data)
        assert isinstance(model, TimelineAgent)
        assert_no_extra_fields(model)
