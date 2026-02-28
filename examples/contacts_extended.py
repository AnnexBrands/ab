"""Example: Extended contact operations (5 methods).

Covers history, aggregated history, graph data, merge preview, and merge.
"""

from examples._runner import ExampleRunner
from tests.constants import TEST_CONTACT_ID

runner = ExampleRunner("Extended Contacts", env="staging")
MERGE_FROM_ID = "PLACEHOLDER"

# ═══════════════════════════════════════════════════════════════════════
# History
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "post_history",
    lambda api, data=None: api.contacts.post_history(TEST_CONTACT_ID, data=data or {"statuses": ""}),
    response_model="ContactHistory",
    fixture_file="ContactHistory.json",
)

runner.add(
    "get_history_aggregated",
    lambda api: api.contacts.get_history_aggregated(TEST_CONTACT_ID),
    response_model="ContactHistoryAggregated",
    fixture_file="ContactHistoryAggregated.json",
)

runner.add(
    "get_history_graph_data",
    lambda api: api.contacts.get_history_graph_data(TEST_CONTACT_ID),
    response_model="ContactGraphData",
    fixture_file="ContactGraphData.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Merge
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "merge_preview",
    lambda api, data=None: api.contacts.merge_preview(TEST_CONTACT_ID, data=data or {"mergeFromId": MERGE_FROM_ID}),
    response_model="ContactMergePreview",
    fixture_file="ContactMergePreview.json",
)

runner.add(
    "merge",
    lambda api, data=None: api.contacts.merge(TEST_CONTACT_ID, data=data or {"mergeFromId": MERGE_FROM_ID}),
)

if __name__ == "__main__":
    runner.run()
