"""Live integration tests for Companies API."""

import pytest

from ab.api.models.companies import CompanyDetails, CompanySimple
from tests.conftest import assert_no_extra_fields
from tests.constants import TEST_COMPANY_UUID

pytestmark = pytest.mark.live


class TestCompaniesIntegration:
    def test_get_by_id(self, api):
        result = api.companies.get_by_id(TEST_COMPANY_UUID)
        assert isinstance(result, CompanySimple)
        assert_no_extra_fields(result)

    def test_get_details(self, api):
        result = api.companies.get_details(TEST_COMPANY_UUID)
        assert isinstance(result, CompanyDetails)
        assert_no_extra_fields(result)

    def test_get_fulldetails(self, api):
        result = api.companies.get_fulldetails(TEST_COMPANY_UUID)
        assert isinstance(result, CompanyDetails)
        assert_no_extra_fields(result)

    def test_available_by_current_user(self, api):
        result = api.companies.available_by_current_user()
        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0], CompanySimple)
        assert_no_extra_fields(result[0])
