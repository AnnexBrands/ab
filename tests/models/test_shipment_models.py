"""Fixture validation tests for Shipment models."""

from ab.api.models.shipments import (
    Accessorial,
    GlobalAccessorial,
    RateQuote,
    RatesState,
    ShipmentInfo,
    ShipmentOriginDestination,
)
from tests.conftest import assert_no_extra_fields, require_fixture


class TestShipmentModels:
    def test_rate_quote(self):
        data = require_fixture("RateQuote", "GET", "/job/{id}/shipment/ratequotes")
        model = RateQuote.model_validate(data)
        assert isinstance(model, RateQuote)
        assert_no_extra_fields(model)

    def test_shipment_origin_destination(self):
        data = require_fixture("ShipmentOriginDestination", "GET", "/job/{id}/shipment/origindestination")
        model = ShipmentOriginDestination.model_validate(data)
        assert isinstance(model, ShipmentOriginDestination)
        assert_no_extra_fields(model)

    def test_accessorial(self):
        data = require_fixture("Accessorial", "GET", "/job/{id}/shipment/accessorials")
        if isinstance(data, list):
            if not data:
                return  # empty list — nothing to validate
            data = data[0]
        model = Accessorial.model_validate(data)
        assert isinstance(model, Accessorial)
        assert_no_extra_fields(model)

    def test_rates_state(self):
        data = require_fixture("RatesState", "GET", "/job/{id}/shipment/ratesstate")
        model = RatesState.model_validate(data)
        assert isinstance(model, RatesState)
        assert_no_extra_fields(model)

    def test_shipment_info(self):
        data = require_fixture("ShipmentInfo", "GET", "/shipment")
        model = ShipmentInfo.model_validate(data)
        assert isinstance(model, ShipmentInfo)
        assert_no_extra_fields(model)

    def test_global_accessorial(self):
        data = require_fixture("GlobalAccessorial", "GET", "/shipment/accessorials")
        if isinstance(data, list) and data:
            data = data[0]
        model = GlobalAccessorial.model_validate(data)
        assert isinstance(model, GlobalAccessorial)
        assert_no_extra_fields(model)
