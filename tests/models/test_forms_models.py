"""Fixture validation tests for Forms models."""

from ab.api.models.forms import FormsShipmentPlan
from tests.conftest import assert_no_extra_fields, require_fixture


class TestFormsModels:
    def test_forms_shipment_plan(self):
        data = require_fixture("FormsShipmentPlan", "GET", "/job/{id}/form/shipments")
        if isinstance(data, list) and data:
            data = data[0]
        model = FormsShipmentPlan.model_validate(data)
        assert isinstance(model, FormsShipmentPlan)
        assert_no_extra_fields(model)
