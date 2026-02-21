"""Fixture validation tests for Freight Provider models."""

from ab.api.models.jobs import PricedFreightProvider
from tests.conftest import require_fixture


class TestFreightModels:
    def test_priced_freight_provider(self):
        data = require_fixture("PricedFreightProvider", "GET", "/job/{id}/freightproviders")
        PricedFreightProvider.model_validate(data)
