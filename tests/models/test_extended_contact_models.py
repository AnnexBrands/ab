"""Fixture validation tests for extended Contact models."""

from ab.api.models.contacts import (
    ContactGraphData,
    ContactHistory,
    ContactHistoryAggregated,
    ContactMergePreview,
)
from tests.conftest import require_fixture


class TestExtendedContactModels:
    def test_contact_history(self):
        data = require_fixture("ContactHistory", "POST", "/contacts/{id}/history")
        ContactHistory.model_validate(data)

    def test_contact_history_aggregated(self):
        data = require_fixture("ContactHistoryAggregated", "GET", "/contacts/{id}/history/aggregated")
        ContactHistoryAggregated.model_validate(data)

    def test_contact_graph_data(self):
        data = require_fixture("ContactGraphData", "GET", "/contacts/{id}/history/graphdata")
        ContactGraphData.model_validate(data)

    def test_contact_merge_preview(self):
        data = require_fixture("ContactMergePreview", "POST", "/contacts/{id}/merge/preview")
        ContactMergePreview.model_validate(data)
