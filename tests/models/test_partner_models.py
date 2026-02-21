"""Fixture validation tests for Partner models."""

from ab.api.models.partners import Partner
from tests.conftest import require_fixture


class TestPartnerModels:
    def test_partner(self):
        data = require_fixture("Partner", "GET", "/partner/{id}")
        Partner.model_validate(data)
