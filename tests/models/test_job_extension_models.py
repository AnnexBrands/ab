"""Fixture validation tests for Job Extension models (009)."""

from tests.conftest import require_fixture

from ab.api.models.jobs import (
    BookingResult,
    DocumentConfig,
    JobAccessLevel,
    JobFeedback,
    SubManagementStatus,
    TrackingInfoV2,
    TrackingShipment,
)


class TestJobExtensionModels:
    def test_document_config(self):
        data = require_fixture("DocumentConfig", "GET", "/job/documentConfig")
        DocumentConfig.model_validate(data)

    def test_job_feedback(self):
        data = require_fixture("JobFeedback", "GET", "/job/feedback/{jobDisplayId}")
        JobFeedback.model_validate(data)

    def test_job_access_level(self):
        data = require_fixture("JobAccessLevel", "GET", "/job/jobAccessLevel")
        JobAccessLevel.model_validate(data)

    def test_sub_management_status(self):
        data = require_fixture("SubManagementStatus", "GET", "/job/{jobDisplayId}/submanagementstatus")
        SubManagementStatus.model_validate(data)

    def test_booking_result(self):
        data = require_fixture("BookingResult", "POST", "/job/{jobDisplayId}/book")
        BookingResult.model_validate(data)

    def test_tracking_shipment(self):
        data = require_fixture("TrackingShipment", "GET", "/job/{jobDisplayId}/tracking/shipment/{proNumber}")
        TrackingShipment.model_validate(data)

    def test_tracking_info_v2(self):
        data = require_fixture("TrackingInfoV2", "GET", "/v2/job/{jobDisplayId}/tracking/{historyAmount}")
        TrackingInfoV2.model_validate(data)
