"""Fixture validation tests for Tracking models."""

from ab.api.models.jobs import TrackingInfo, TrackingInfoV3
from tests.conftest import assert_no_extra_fields, require_fixture


class TestTrackingModels:
    def test_tracking_info(self):
        data = require_fixture("TrackingInfo", "GET", "/job/{id}/tracking")
        model = TrackingInfo.model_validate(data)
        assert isinstance(model, TrackingInfo)
        assert_no_extra_fields(model)

    def test_tracking_info_v3(self):
        data = require_fixture("TrackingInfoV3", "GET", "/v3/job/{id}/tracking/{historyAmount}")
        model = TrackingInfoV3.model_validate(data)
        assert isinstance(model, TrackingInfoV3)
        assert_no_extra_fields(model)
