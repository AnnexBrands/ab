"""Live integration tests for Jobs API (T072)."""

import pytest

from tests.constants import LIVE_JOB_DISPLAY_ID

pytestmark = pytest.mark.live


class TestJobsIntegration:
    def test_get_job(self, api):
        result = api.jobs.get(LIVE_JOB_DISPLAY_ID)
        assert result is not None

    def test_search(self, api):
        result = api.jobs.search()
        assert result is not None

    def test_search_by_details(self, api):
        result = api.jobs.search_by_details({"searchText": "test"})
        assert result is not None

    def test_get_price(self, api):
        result = api.jobs.get_price(LIVE_JOB_DISPLAY_ID)
        assert result is not None

    def test_get_calendar_items(self, api):
        result = api.jobs.get_calendar_items(LIVE_JOB_DISPLAY_ID)
        assert result is not None

    def test_get_update_page_config(self, api):
        result = api.jobs.get_update_page_config(LIVE_JOB_DISPLAY_ID)
        assert result is not None
