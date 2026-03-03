"""Fixture validation tests for Freight Provider models."""

from ab.api.models.jobs import PricedFreightProvider
from tests.conftest import assert_no_extra_fields, first_or_skip, require_fixture


class TestFreightModels:
    def test_priced_freight_provider(self):
        data = require_fixture("PricedFreightProvider", "GET", "/job/{id}/freightproviders")
        item = first_or_skip(data)
        model = PricedFreightProvider.model_validate(item)
        assert isinstance(model, PricedFreightProvider)
        assert_no_extra_fields(model)
