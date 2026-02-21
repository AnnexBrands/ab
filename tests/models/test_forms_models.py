"""Fixture validation tests for Forms models."""

from ab.api.models.forms import FormsShipmentPlan
from tests.conftest import require_fixture


class TestFormsModels:
    def test_forms_shipment_plan(self):
        data = require_fixture("FormsShipmentPlan", "GET", "/job/{id}/form/shipments")
        model = FormsShipmentPlan.model_validate(data)
        assert model.shipment_plan_id is not None
        assert model.carrier_name is not None
