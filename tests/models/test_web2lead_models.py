"""Fixture validation tests for Web2Lead models (T066)."""

import pytest

from tests.conftest import require_fixture

from ab.api.models.web2lead import Web2LeadResponse


class TestWeb2LeadModels:
    @pytest.mark.live
    def test_web2lead_response(self):
        data = require_fixture("Web2LeadResponse", "GET", "/Web2Lead", required=True)
        model = Web2LeadResponse.model_validate(data)
        assert model.result is not None
        assert model.result.nc_import_failed is True
