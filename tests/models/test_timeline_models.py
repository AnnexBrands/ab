"""Fixture validation tests for Timeline models."""

from ab.api.models.jobs import TimelineAgent, TimelineResponse, TimelineSaveResponse, TimelineTask
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

    def test_timeline_response(self):
        data = require_fixture("TimelineResponse", "GET", "/job/{id}/timeline")
        model = TimelineResponse.model_validate(data)
        assert isinstance(model, TimelineResponse)
        assert_no_extra_fields(model)
        # Validate nested tasks
        assert model.tasks is not None
        for task in model.tasks:
            assert_no_extra_fields(task)

    def test_timeline_save_response(self):
        data = require_fixture("TimelineSaveResponse", "POST", "/job/{id}/timeline")
        model = TimelineSaveResponse.model_validate(data)
        assert isinstance(model, TimelineSaveResponse)
        assert_no_extra_fields(model)
        # Validate nested task
        if model.task is not None:
            assert_no_extra_fields(model.task)
