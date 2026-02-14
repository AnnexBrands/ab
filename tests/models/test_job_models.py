"""Fixture validation tests for Job models (T061)."""

import pytest

from tests.conftest import load_fixture

from ab.api.models.jobs import CalendarItem, Job, JobPrice, JobSearchResult, JobUpdatePageConfig


class TestJobModels:
    @pytest.mark.mock
    def test_job(self):
        data = load_fixture("Job")
        model = Job.model_validate(data)
        assert model.id is not None or model.job_display_id is not None

    @pytest.mark.mock
    def test_job_search_result(self):
        data = load_fixture("JobSearchResult")
        model = JobSearchResult.model_validate(data)
        assert model.job_display_id is not None

    @pytest.mark.mock
    def test_job_price(self):
        data = load_fixture("JobPrice")
        model = JobPrice.model_validate(data)
        # JobPrice may have varying fields depending on fixture source

    @pytest.mark.mock
    def test_calendar_item(self):
        data = load_fixture("CalendarItem")
        model = CalendarItem.model_validate(data)

    @pytest.mark.mock
    def test_job_update_page_config(self):
        data = load_fixture("JobUpdatePageConfig")
        model = JobUpdatePageConfig.model_validate(data)
