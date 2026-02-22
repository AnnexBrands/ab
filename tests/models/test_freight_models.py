"""Fixture validation tests for Freight Provider models."""

from ab.api.models.jobs import PricedFreightProvider
from tests.conftest import assert_no_extra_fields, require_fixture


class TestFreightModels:
    def test_priced_freight_provider(self):
        data = require_fixture("PricedFreightProvider", "GET", "/job/{id}/freightproviders")
        model = PricedFreightProvider.model_validate(data)
        assert isinstance(model, PricedFreightProvider)
        assert_no_extra_fields(model)
