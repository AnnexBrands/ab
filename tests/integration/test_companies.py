"""Live integration tests for Companies API (T070)."""

import pytest

from tests.constants import LIVE_COMPANY_UUID

pytestmark = pytest.mark.live


class TestCompaniesIntegration:
    def test_get_by_id(self, api):
        result = api.companies.get_by_id(LIVE_COMPANY_UUID)
        assert result is not None

    def test_get_details(self, api):
        result = api.companies.get_details(LIVE_COMPANY_UUID)
        assert result is not None

    def test_get_fulldetails(self, api):
        result = api.companies.get_fulldetails(LIVE_COMPANY_UUID)
        assert result is not None

    def test_available_by_current_user(self, api):
        result = api.companies.available_by_current_user()
        assert result is not None
