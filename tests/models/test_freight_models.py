"""Fixture validation tests for Freight Provider models."""

from tests.conftest import require_fixture

from ab.api.models.jobs import PricedFreightProvider


class TestFreightModels:
    def test_priced_freight_provider(self):
        data = require_fixture("PricedFreightProvider", "GET", "/job/{id}/freightproviders")
        model = PricedFreightProvider.model_validate(data)
