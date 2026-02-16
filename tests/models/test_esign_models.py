"""Fixture validation tests for E-Sign models (009)."""

from tests.conftest import require_fixture

from ab.api.models.esign import ESignData, ESignResult


class TestESignModels:
    def test_esign_result(self):
        data = require_fixture("ESignResult", "GET", "/e-sign/result")
        ESignResult.model_validate(data)

    def test_esign_data(self):
        data = require_fixture("ESignData", "GET", "/e-sign/{jobDisplayId}/{bookingKey}")
        ESignData.model_validate(data)
