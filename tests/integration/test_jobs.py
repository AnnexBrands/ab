"""Live integration tests for Jobs API (T072)."""

import pytest

pytestmark = pytest.mark.live


class TestJobsIntegration:
    def test_search(self, api):
        result = api.jobs.search()
        assert result is not None

    def test_search_by_details(self, api):
        result = api.jobs.search_by_details({"searchText": "test"})
        assert result is not None
