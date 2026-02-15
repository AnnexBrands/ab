"""Fixture validation tests for extended Contact models."""

from tests.conftest import require_fixture

from ab.api.models.contacts import (
    ContactGraphData,
    ContactHistory,
    ContactHistoryAggregated,
    ContactMergePreview,
)


class TestExtendedContactModels:
    def test_contact_history(self):
        data = require_fixture("ContactHistory", "POST", "/contacts/{id}/history")
        model = ContactHistory.model_validate(data)

    def test_contact_history_aggregated(self):
        data = require_fixture("ContactHistoryAggregated", "GET", "/contacts/{id}/history/aggregated")
        model = ContactHistoryAggregated.model_validate(data)

    def test_contact_graph_data(self):
        data = require_fixture("ContactGraphData", "GET", "/contacts/{id}/history/graphdata")
        model = ContactGraphData.model_validate(data)

    def test_contact_merge_preview(self):
        data = require_fixture("ContactMergePreview", "POST", "/contacts/{id}/merge/preview")
        model = ContactMergePreview.model_validate(data)
