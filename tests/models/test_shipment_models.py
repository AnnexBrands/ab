"""Fixture validation tests for Shipment models."""

from ab.api.models.shipments import (
    Accessorial,
    GlobalAccessorial,
    RateQuote,
    RatesState,
    ShipmentInfo,
    ShipmentOriginDestination,
)
from tests.conftest import require_fixture


class TestShipmentModels:
    def test_rate_quote(self):
        data = require_fixture("RateQuote", "GET", "/job/{id}/shipment/ratequotes")
        model = RateQuote.model_validate(data)
        assert model.carrier_name is not None

    def test_shipment_origin_destination(self):
        data = require_fixture("ShipmentOriginDestination", "GET", "/job/{id}/shipment/origindestination")
        model = ShipmentOriginDestination.model_validate(data)
        assert model.origin is not None
        assert model.destination is not None

    def test_accessorial(self):
        data = require_fixture("Accessorial", "GET", "/job/{id}/shipment/accessorials")
        model = Accessorial.model_validate(data)
        assert model.id is not None
        assert model.name is not None

    def test_rates_state(self):
        data = require_fixture("RatesState", "GET", "/job/{id}/shipment/ratesstate")
        model = RatesState.model_validate(data)
        assert model.state is not None

    def test_shipment_info(self):
        data = require_fixture("ShipmentInfo", "GET", "/shipment")
        model = ShipmentInfo.model_validate(data)
        assert model.shipment_id is not None

    def test_global_accessorial(self):
        data = require_fixture("GlobalAccessorial", "GET", "/shipment/accessorials")
        model = GlobalAccessorial.model_validate(data)
        assert model.id is not None
        assert model.name is not None
