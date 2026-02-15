"""Fixture validation tests for Partner models."""

from tests.conftest import require_fixture

from ab.api.models.partners import Partner


class TestPartnerModels:
    def test_partner(self):
        data = require_fixture("Partner", "GET", "/partner/{id}")
        model = Partner.model_validate(data)
