"""Example: Extended contact operations (5 methods).

Covers history, aggregated history, graph data, merge preview, and merge.
"""

from examples._runner import ExampleRunner

runner = ExampleRunner("Extended Contacts", env="staging")

LIVE_CONTACT_ID = "PLACEHOLDER"
MERGE_FROM_ID = "PLACEHOLDER"

# ═══════════════════════════════════════════════════════════════════════
# History
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "post_history",
    lambda api: api.contacts.post_history(LIVE_CONTACT_ID, event="SDK test"),
    response_model="ContactHistory",
    fixture_file="ContactHistory.json",
)

runner.add(
    "get_history_aggregated",
    lambda api: api.contacts.get_history_aggregated(LIVE_CONTACT_ID),
    response_model="ContactHistoryAggregated",
    fixture_file="ContactHistoryAggregated.json",
)

runner.add(
    "get_history_graph_data",
    lambda api: api.contacts.get_history_graph_data(LIVE_CONTACT_ID),
    response_model="ContactGraphData",
    fixture_file="ContactGraphData.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Merge
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "merge_preview",
    lambda api: api.contacts.merge_preview(LIVE_CONTACT_ID, mergeFromId=MERGE_FROM_ID),
    response_model="ContactMergePreview",
    fixture_file="ContactMergePreview.json",
)

runner.add(
    "merge",
    lambda api: api.contacts.merge(LIVE_CONTACT_ID, mergeFromId=MERGE_FROM_ID),
)

if __name__ == "__main__":
    runner.run()
