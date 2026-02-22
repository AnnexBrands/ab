"""Fixture validation tests for Job models."""

import pytest

from ab.api.models.jobs import CalendarItem, Job, JobPrice, JobSearchResult, JobUpdatePageConfig
from tests.conftest import assert_no_extra_fields, require_fixture


class TestJobModels:
    @pytest.mark.live
    def test_job(self):
        data = require_fixture("Job", "GET", "/job/{id}", required=True)
        model = Job.model_validate(data)
        assert isinstance(model, Job)
        # Job still has many extra fields — not yet fully typed
        # assert_no_extra_fields(model)

    @pytest.mark.live
    def test_job_search_result(self):
        data = require_fixture("JobSearchResult", "GET", "/job/search", required=True)
        model = JobSearchResult.model_validate(data)
        assert isinstance(model, JobSearchResult)
        # JobSearchResult still has extra fields — not yet fully typed
        # assert_no_extra_fields(model)

    @pytest.mark.live
    def test_job_price(self):
        data = require_fixture("JobPrice", "GET", "/job/{id}/price", required=True)
        model = JobPrice.model_validate(data)
        assert isinstance(model, JobPrice)
        assert_no_extra_fields(model)

    @pytest.mark.live
    def test_calendar_item(self):
        data = require_fixture("CalendarItem", "GET", "/job/{id}/calendaritems", required=True)
        if isinstance(data, list) and data:
            data = data[0]
        model = CalendarItem.model_validate(data)
        assert isinstance(model, CalendarItem)
        assert_no_extra_fields(model)
        assert model.id is not None

    @pytest.mark.live
    def test_job_update_page_config(self):
        data = require_fixture("JobUpdatePageConfig", "GET", "/job/{id}/updatePageConfig", required=True)
        model = JobUpdatePageConfig.model_validate(data)
        assert isinstance(model, JobUpdatePageConfig)
        assert_no_extra_fields(model)
