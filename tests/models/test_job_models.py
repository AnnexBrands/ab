"""Fixture validation tests for Job models."""

import pytest

from ab.api.models.jobs import (
    ActiveOnHoldInfo,
    CalendarItem,
    ContactDetails,
    Job,
    JobContactDetails,
    JobContactEmail,
    JobContactPhone,
    JobDocument,
    JobItem,
    JobItemMaterial,
    JobPrice,
    JobSearchResult,
    JobSlaInfo,
    JobSummarySnapshot,
    JobUpdatePageConfig,
)
from ab.api.models.common import CompanyAddress
from tests.conftest import assert_no_extra_fields, require_fixture


class TestJobModels:
    @pytest.mark.live
    def test_job(self):
        data = require_fixture("Job", "GET", "/job/{id}", required=True)
        model = Job.model_validate(data)
        assert isinstance(model, Job)
        assert_no_extra_fields(model)

        # Recursive sub-model extra-field checks
        if model.customer_contact is not None:
            assert isinstance(model.customer_contact, JobContactDetails)
            assert_no_extra_fields(model.customer_contact)
            if model.customer_contact.contact is not None:
                assert isinstance(model.customer_contact.contact, ContactDetails)
                assert_no_extra_fields(model.customer_contact.contact)
            if model.customer_contact.email is not None:
                assert isinstance(model.customer_contact.email, JobContactEmail)
                assert_no_extra_fields(model.customer_contact.email)
            if model.customer_contact.phone is not None:
                assert isinstance(model.customer_contact.phone, JobContactPhone)
                assert_no_extra_fields(model.customer_contact.phone)
            if model.customer_contact.address is not None:
                assert isinstance(model.customer_contact.address, CompanyAddress)
                assert_no_extra_fields(model.customer_contact.address)

        if model.items:
            item = model.items[0]
            assert isinstance(item, JobItem)
            assert_no_extra_fields(item)
            if item.materials:
                mat = item.materials[0]
                assert isinstance(mat, JobItemMaterial)
                assert_no_extra_fields(mat)

        if model.job_summary_snapshot is not None:
            assert isinstance(model.job_summary_snapshot, JobSummarySnapshot)
            assert_no_extra_fields(model.job_summary_snapshot)

        if model.active_on_hold_info is not None:
            assert isinstance(model.active_on_hold_info, ActiveOnHoldInfo)
            assert_no_extra_fields(model.active_on_hold_info)

        if model.documents:
            doc = model.documents[0]
            assert isinstance(doc, JobDocument)
            assert_no_extra_fields(doc)

        if model.sla_info is not None:
            assert isinstance(model.sla_info, JobSlaInfo)
            assert_no_extra_fields(model.sla_info)

    @pytest.mark.live
    def test_job_search_result(self):
        data = require_fixture("JobSearchResult", "GET", "/job/search", required=True)
        model = JobSearchResult.model_validate(data)
        assert isinstance(model, JobSearchResult)
        assert_no_extra_fields(model)

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
