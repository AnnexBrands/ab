"""Fixture validation tests for Partner models."""

from ab.api.models.partners import Partner
from tests.conftest import assert_no_extra_fields, require_fixture


class TestPartnerModels:
    def test_partner(self):
        data = require_fixture("Partner", "GET", "/partner/{id}")
        model = Partner.model_validate(data)
        assert isinstance(model, Partner)
        assert_no_extra_fields(model)
