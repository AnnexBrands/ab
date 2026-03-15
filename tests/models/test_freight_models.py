"""Fixture validation tests for Freight Provider models."""

from ab.api.models.jobs import CarrierAccountInfo, PricedFreightProvider, ShipmentPlanProvider
from tests.conftest import assert_no_extra_fields, first_or_skip, load_request_fixture, require_fixture


class TestFreightModels:
    def test_priced_freight_provider(self):
        data = require_fixture("PricedFreightProvider", "GET", "/job/{id}/freightproviders")
        item = first_or_skip(data)
        model = PricedFreightProvider.model_validate(item)
        assert isinstance(model, PricedFreightProvider)
        assert_no_extra_fields(model)

    def test_priced_freight_provider_fields(self):
        """Verify key fields are populated in the captured fixture."""
        data = require_fixture("PricedFreightProvider", "GET", "/job/{id}/freightproviders")
        item = first_or_skip(data)
        model = PricedFreightProvider.model_validate(item)
        assert model.option_index is not None
        assert model.provider_code is not None
        assert model.provider_company_name is not None
        assert model.total_sell is not None

    def test_carrier_account_info_nested(self):
        """Verify nested CarrierAccountInfo is parsed as a typed model."""
        data = require_fixture("PricedFreightProvider", "GET", "/job/{id}/freightproviders")
        item = first_or_skip(data)
        model = PricedFreightProvider.model_validate(item)
        info = model.used_carrier_account_info
        assert info is not None
        assert isinstance(info, CarrierAccountInfo)
        assert_no_extra_fields(info)
        assert info.id is not None

    def test_shipment_plan_provider(self):
        """Verify ShipmentPlanProvider parses fixture with typed CarrierAccountInfo."""
        data = load_request_fixture("ShipmentPlanProvider")
        model = ShipmentPlanProvider.model_validate(data)
        assert isinstance(model, ShipmentPlanProvider)
        assert_no_extra_fields(model)
        assert model.used_carrier_account_info is not None
        assert isinstance(model.used_carrier_account_info, CarrierAccountInfo)
