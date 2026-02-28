"""Example: RFQ lifecycle operations (9 methods).

Covers standalone RFQ operations (get, accept, decline, cancel, accept_winner,
add_comment, get_for_job) plus job-scoped RFQ queries (list_rfqs, get_rfq_status).
"""

from examples._runner import ExampleRunner
from tests.constants import TEST_JOB_DISPLAY_ID

runner = ExampleRunner("RFQ", env="staging")
TEST_RFQ_ID = "PLACEHOLDER"

# ═══════════════════════════════════════════════════════════════════════
# Standalone RFQ Operations
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "get",
    lambda api: api.rfq.get(TEST_RFQ_ID),
    response_model="QuoteRequestDisplayInfo",
    fixture_file="QuoteRequestDisplayInfo.json",
)

runner.add(
    "get_for_job",
    lambda api: api.rfq.get_for_job(str(TEST_JOB_DISPLAY_ID)),
    response_model="List[QuoteRequestDisplayInfo]",
    fixture_file="QuoteRequestDisplayInfo.json",
)

runner.add(
    "accept",
    lambda api, data=None: api.rfq.accept(TEST_RFQ_ID, data=data or {}),
    request_model="AcceptModel",
    request_fixture_file="AcceptModel.json",
)

runner.add(
    "decline",
    lambda api: api.rfq.decline(TEST_RFQ_ID),
)

runner.add(
    "cancel",
    lambda api: api.rfq.cancel(TEST_RFQ_ID),
)

runner.add(
    "accept_winner",
    lambda api: api.rfq.accept_winner(TEST_RFQ_ID),
)

runner.add(
    "add_comment",
    lambda api, data=None: api.rfq.add_comment(TEST_RFQ_ID, data=data or {}),
    request_model="AcceptModel",
    request_fixture_file="AcceptModel.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Job-Scoped RFQ Queries
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "list_rfqs",
    lambda api: api.jobs.list_rfqs(TEST_JOB_DISPLAY_ID),
    response_model="List[QuoteRequestDisplayInfo]",
    fixture_file="QuoteRequestDisplayInfo.json",
)

runner.add(
    "get_rfq_status",
    lambda api: api.jobs.get_rfq_status(TEST_JOB_DISPLAY_ID, "LTL", "COMPANY_ID"),
    response_model="QuoteRequestStatus",
    fixture_file="QuoteRequestStatus.json",
)

if __name__ == "__main__":
    runner.run()
