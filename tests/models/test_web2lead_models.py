"""Fixture validation tests for Web2Lead models."""

import pytest

from ab.api.models.web2lead import Web2LeadResponse
from tests.conftest import assert_no_extra_fields, require_fixture


class TestWeb2LeadModels:
    @pytest.mark.live
    def test_web2lead_response(self):
        data = require_fixture("Web2LeadResponse", "GET", "/Web2Lead", required=True)
        model = Web2LeadResponse.model_validate(data)
        assert isinstance(model, Web2LeadResponse)
        assert_no_extra_fields(model)
