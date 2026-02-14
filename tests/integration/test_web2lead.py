"""Live integration tests for Web2Lead API (T080)."""

import pytest

pytestmark = [pytest.mark.live, pytest.mark.mock]


class TestWeb2LeadIntegration:
    @pytest.mark.skip(reason="Requires ABC API accessKey credentials")
    def test_get(self, api):
        result = api.web2lead.get()
        assert result is not None
