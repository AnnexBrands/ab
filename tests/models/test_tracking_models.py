"""Fixture validation tests for Tracking models."""

from tests.conftest import require_fixture

from ab.api.models.jobs import TrackingInfo, TrackingInfoV3


class TestTrackingModels:
    def test_tracking_info(self):
        data = require_fixture("TrackingInfo", "GET", "/job/{id}/tracking")
        model = TrackingInfo.model_validate(data)
        assert model.status is not None
        assert model.carrier_name is not None

    def test_tracking_info_v3(self):
        data = require_fixture("TrackingInfoV3", "GET", "/v3/job/{id}/tracking/{historyAmount}")
        model = TrackingInfoV3.model_validate(data)
        assert model.shipment_status is not None
