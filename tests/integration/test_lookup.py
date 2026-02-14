"""Live integration tests for Lookup API (T075)."""

import pytest

pytestmark = pytest.mark.live


class TestLookupIntegration:
    def test_get_contact_types(self, api):
        result = api.lookup.get_contact_types()
        assert result is not None

    def test_get_countries(self, api):
        result = api.lookup.get_countries()
        assert result is not None

    def test_get_job_statuses(self, api):
        result = api.lookup.get_job_statuses()
        assert result is not None

    def test_get_items(self, api):
        # May return 204 No Content
        result = api.lookup.get_items()
