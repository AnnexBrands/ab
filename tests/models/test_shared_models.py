"""Fixture validation tests for ServiceBaseResponse."""

from ab.api.models.shared import ServiceBaseResponse
from ab.api.models.shipments import ShipmentWeight
from tests.conftest import assert_no_extra_fields, require_fixture


class TestServiceBaseResponse:
    def test_service_base_response(self):
        """Validate fixture against expanded model — zero extra fields."""
        data = require_fixture("ServiceBaseResponse", "POST", "/job/{id}/shipment/book")
        model = ServiceBaseResponse.model_validate(data)
        assert isinstance(model, ServiceBaseResponse)
        assert_no_extra_fields(model)

    def test_service_base_response_fields(self):
        """Verify key fields are populated in the captured fixture."""
        data = require_fixture("ServiceBaseResponse", "POST", "/job/{id}/shipment/book")
        model = ServiceBaseResponse.model_validate(data)
        assert model.success is not None
        assert model.documents is not None
        assert model.weight is not None

    def test_weight_nested_model(self):
        """Verify nested ShipmentWeight is parsed as a typed model."""
        data = require_fixture("ServiceBaseResponse", "POST", "/job/{id}/shipment/book")
        model = ServiceBaseResponse.model_validate(data)
        assert model.weight is not None
        assert isinstance(model.weight, ShipmentWeight)
        assert_no_extra_fields(model.weight)
