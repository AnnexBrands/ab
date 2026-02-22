"""Live integration tests for Jobs API."""

import pytest

from ab.api.models.jobs import CalendarItem, Job, JobPrice, JobSearchResult, JobUpdatePageConfig
from tests.conftest import assert_no_extra_fields
from tests.constants import LIVE_JOB_DISPLAY_ID

pytestmark = pytest.mark.live


class TestJobsIntegration:
    def test_get_job(self, api):
        result = api.jobs.get(LIVE_JOB_DISPLAY_ID)
        assert isinstance(result, Job)
        # Job not yet fully typed — skip extra_fields check

    def test_search(self, api):
        result = api.jobs.search()
        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0], JobSearchResult)
        # JobSearchResult not yet fully typed — skip extra_fields check

    def test_search_by_details(self, api):
        result = api.jobs.search_by_details({"searchText": "test"})
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
