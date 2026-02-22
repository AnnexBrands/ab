"""Live integration tests for Web2Lead API."""

import pytest

from ab.api.models.web2lead import Web2LeadResponse
from tests.conftest import assert_no_extra_fields

pytestmark = [pytest.mark.live, pytest.mark.mock]


class TestWeb2LeadIntegration:
    @pytest.mark.skip(reason="Requires ABC API accessKey credentials")
    def test_get(self, api):
        result = api.web2lead.get()
        assert isinstance(result, Web2LeadResponse)
        assert_no_extra_fields(result)
