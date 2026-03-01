"""Live integration tests for Lookup API."""

import pytest

from ab.api.models.lookup import ContactTypeEntity, CountryCodeDto, JobStatus, LookupItem
from tests.conftest import assert_no_extra_fields
from tests.constants import TEST_ITEM_ID, TEST_JOB_DISPLAY_ID

pytestmark = pytest.mark.live


class TestLookupIntegration:
    def test_get_contact_types(self, api):
        result = api.lookup.get_contact_types()
        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0], ContactTypeEntity)
        assert_no_extra_fields(result[0])

    def test_get_countries(self, api):
        result = api.lookup.get_countries()
        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0], CountryCodeDto)
        assert_no_extra_fields(result[0])

    def test_get_job_statuses(self, api):
        result = api.lookup.get_job_statuses()
        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0], JobStatus)
        assert_no_extra_fields(result[0])

    def test_get_items(self, api):
        result = api.lookup.get_items(
            job_display_id=TEST_JOB_DISPLAY_ID,
            job_item_id=TEST_ITEM_ID,
        )
        # May return 204 No Content
        if result is not None:
            assert isinstance(result, list)
            if len(result) > 0:
                assert isinstance(result[0], LookupItem)
                assert_no_extra_fields(result[0])
