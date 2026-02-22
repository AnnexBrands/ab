"""Live integration tests for AutoPrice API."""

import pytest

from ab.api.models.autoprice import QuickQuoteResponse
from tests.conftest import assert_no_extra_fields

pytestmark = [pytest.mark.live, pytest.mark.mock]


class TestAutoPriceIntegration:
    @pytest.mark.skip(reason="Requires ABC API accessKey credentials")
    def test_quick_quote(self, api):
        result = api.autoprice.quick_quote({})
        assert isinstance(result, QuickQuoteResponse)
        assert_no_extra_fields(result)
