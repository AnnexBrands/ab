"""Live integration tests for Jobs API."""

import pytest

from ab.api.models.jobs import CalendarItem, Job, JobPrice, JobSearchResult, JobUpdatePageConfig
from ab.exceptions import RequestError
from tests.conftest import assert_no_extra_fields
from tests.constants import LIVE_JOB_DISPLAY_ID

pytestmark = pytest.mark.live


class TestJobsIntegration:
    def test_get_job(self, api):
        result = api.jobs.get(LIVE_JOB_DISPLAY_ID)
        assert isinstance(result, Job)
        # Job not yet fully typed — skip extra_fields check

    def test_search(self, api):
        result = api.jobs.search(job_display_id=LIVE_JOB_DISPLAY_ID)
        # API returns a single object (not a list) when filtering by jobDisplayId
        assert result is not None
        if isinstance(result, list):
            assert len(result) > 0
            assert isinstance(result[0], JobSearchResult)
        else:
            assert isinstance(result, dict)
            assert result.get("jobDisplayId") == LIVE_JOB_DISPLAY_ID

    def test_search_by_details(self, api):
        try:
            result = api.jobs.search_by_details({
                "searchText": "test",
                "pageNo": 1,
                "pageSize": 25,
                "sortBy": {"sortByField": 1, "sortDir": True},
            })
        except RequestError as exc:
            if exc.status_code >= 500:
                pytest.skip(f"Staging server error: {exc}")
            raise
        assert isinstance(result, list)
        if len(result) > 0:
            assert isinstance(result[0], JobSearchResult)

    def test_get_price(self, api):
        result = api.jobs.get_price(LIVE_JOB_DISPLAY_ID)
        assert isinstance(result, JobPrice)
        assert_no_extra_fields(result)

    def test_get_calendar_items(self, api):
        result = api.jobs.get_calendar_items(LIVE_JOB_DISPLAY_ID)
        assert isinstance(result, list)
        if len(result) > 0:
            assert isinstance(result[0], CalendarItem)
            assert_no_extra_fields(result[0])

    def test_get_update_page_config(self, api):
        result = api.jobs.get_update_page_config(LIVE_JOB_DISPLAY_ID)
        assert isinstance(result, JobUpdatePageConfig)
        assert_no_extra_fields(result)
