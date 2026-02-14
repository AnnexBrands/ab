"""Live integration tests for AutoPrice API (T079)."""

import pytest

pytestmark = [pytest.mark.live, pytest.mark.mock]


class TestAutoPriceIntegration:
    @pytest.mark.skip(reason="Requires ABC API accessKey credentials")
    def test_quick_quote(self, api):
        result = api.autoprice.quick_quote({})
        assert result is not None
