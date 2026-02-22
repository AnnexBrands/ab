"""Fixture validation tests for extended Contact models."""

from ab.api.models.contacts import (
    ContactGraphData,
    ContactHistory,
    ContactHistoryAggregated,
    ContactMergePreview,
)
from tests.conftest import assert_no_extra_fields, require_fixture


class TestExtendedContactModels:
    def test_contact_history(self):
        data = require_fixture("ContactHistory", "POST", "/contacts/{id}/history")
        model = ContactHistory.model_validate(data)
        assert isinstance(model, ContactHistory)
        assert_no_extra_fields(model)

    def test_contact_history_aggregated(self):
        data = require_fixture("ContactHistoryAggregated", "GET", "/contacts/{id}/history/aggregated")
        model = ContactHistoryAggregated.model_validate(data)
        assert isinstance(model, ContactHistoryAggregated)
        assert_no_extra_fields(model)

    def test_contact_graph_data(self):
        data = require_fixture("ContactGraphData", "GET", "/contacts/{id}/history/graphdata")
        model = ContactGraphData.model_validate(data)
        assert isinstance(model, ContactGraphData)
        assert_no_extra_fields(model)

    def test_contact_merge_preview(self):
        data = require_fixture("ContactMergePreview", "POST", "/contacts/{id}/merge/preview")
        model = ContactMergePreview.model_validate(data)
        assert isinstance(model, ContactMergePreview)
        assert_no_extra_fields(model)
