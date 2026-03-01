"""Live integration tests for Jobs API."""

import pytest

from ab.api.models.jobs import (
    CalendarItem,
    Job,
    JobPrice,
    JobSearchResult,
    JobUpdatePageConfig,
    TimelineAgent,
    TimelineResponse,
    TimelineTask,
)
from ab.exceptions import RequestError
from tests.conftest import assert_no_extra_fields, load_request_fixture
from tests.constants import TEST_JOB_DISPLAY_ID

pytestmark = pytest.mark.live


class TestJobsIntegration:
    def test_get_job(self, api):
        result = api.jobs.get(TEST_JOB_DISPLAY_ID)
        assert isinstance(result, Job)
        assert_no_extra_fields(result)

    def test_search(self, api):
        result = api.jobs.search(job_display_id=TEST_JOB_DISPLAY_ID)
        assert isinstance(result, JobSearchResult)
        assert_no_extra_fields(result)

    def test_search_by_details(self, api):
        data = load_request_fixture("JobSearchRequest")
        try:
            result = api.jobs.search_by_details(data=data)
        except RequestError as exc:
            if exc.status_code >= 400:
                pytest.skip(f"Staging server error: {exc}")
            raise
        assert isinstance(result, list)
        if len(result) > 0:
            assert isinstance(result[0], JobSearchResult)

    def test_get_price(self, api):
        result = api.jobs.get_price(TEST_JOB_DISPLAY_ID)
        assert isinstance(result, JobPrice)
        assert_no_extra_fields(result)

    def test_get_calendar_items(self, api):
        result = api.jobs.get_calendar_items(TEST_JOB_DISPLAY_ID)
        assert isinstance(result, list)
        if len(result) > 0:
            assert isinstance(result[0], CalendarItem)
            assert_no_extra_fields(result[0])

    def test_get_update_page_config(self, api):
        result = api.jobs.get_update_page_config(TEST_JOB_DISPLAY_ID)
        assert isinstance(result, JobUpdatePageConfig)
        assert_no_extra_fields(result)

    def test_get_timeline(self, api):
        result = api.jobs.get_timeline(TEST_JOB_DISPLAY_ID)
        assert isinstance(result, list)
        if len(result) > 0:
            assert isinstance(result[0], TimelineTask)
            assert_no_extra_fields(result[0])

    def test_get_timeline_response(self, api):
        result = api.jobs.get_timeline_response(TEST_JOB_DISPLAY_ID)
        assert isinstance(result, TimelineResponse)
        assert_no_extra_fields(result)
        assert result.tasks is not None
        for task in result.tasks:
            assert_no_extra_fields(task)

    def test_get_timeline_agent(self, api):
        result = api.jobs.get_timeline_agent(TEST_JOB_DISPLAY_ID, "PU")
        if result is not None:
            assert isinstance(result, TimelineAgent)
            assert_no_extra_fields(result)

    def test_timeline_get_task(self, api):
        """Test TimelineHelpers.get_task returns correct task for each code."""
        for code in ["PU", "PK", "ST", "CP"]:
            status_info, task = api.jobs.timeline.get_task(TEST_JOB_DISPLAY_ID, code)
            assert isinstance(status_info, dict)
            if task is not None:
                assert task.get("taskCode") == code
