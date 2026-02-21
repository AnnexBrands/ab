"""Fixture validation tests for Job models (T061)."""

import pytest

from ab.api.models.jobs import CalendarItem, Job, JobPrice, JobSearchResult, JobUpdatePageConfig
from tests.conftest import require_fixture


class TestJobModels:
    @pytest.mark.live
    def test_job(self):
        data = require_fixture("Job", "GET", "/job/{id}", required=True)
        model = Job.model_validate(data)
        assert model.job_display_id == 2000000

    @pytest.mark.live
    def test_job_search_result(self):
        data = require_fixture("JobSearchResult", "GET", "/job/search", required=True)
        model = JobSearchResult.model_validate(data)
        assert model.job_display_id is not None
        assert model.customer_full_name is not None

    @pytest.mark.live
    def test_job_price(self):
        data = require_fixture("JobPrice", "GET", "/job/{id}/price", required=True)
        model = JobPrice.model_validate(data)
        assert model.total_sell_price == 22.0

    @pytest.mark.live
    def test_calendar_item(self):
        data = require_fixture("CalendarItem", "GET", "/job/{id}/calendaritems", required=True)
        model = CalendarItem.model_validate(data)
        assert model.id is not None
        assert model.name is not None

    @pytest.mark.live
    def test_job_update_page_config(self):
        data = require_fixture("JobUpdatePageConfig", "GET", "/job/{id}/updatePageConfig", required=True)
        model = JobUpdatePageConfig.model_validate(data)
        assert model.page_controls is not None
