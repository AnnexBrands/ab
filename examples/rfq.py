"""Example: RFQ lifecycle operations (9 methods).

Covers standalone RFQ operations (get, accept, decline, cancel, accept_winner,
add_comment, get_for_job) plus job-scoped RFQ queries (list_rfqs, get_rfq_status).
"""

from examples._runner import ExampleRunner
from tests.constants import LIVE_JOB_DISPLAY_ID

runner = ExampleRunner("RFQ", env="staging")
LIVE_RFQ_ID = "PLACEHOLDER"

# ═══════════════════════════════════════════════════════════════════════
# Standalone RFQ Operations
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "get",
    lambda api: api.rfq.get(LIVE_RFQ_ID),
    response_model="QuoteRequestDisplayInfo",
    fixture_file="QuoteRequestDisplayInfo.json",
)

runner.add(
    "get_for_job",
    lambda api: api.rfq.get_for_job(str(LIVE_JOB_DISPLAY_ID)),
    response_model="List[QuoteRequestDisplayInfo]",
)

runner.add(
    "accept",
    lambda api, data=None: api.rfq.accept(LIVE_RFQ_ID, **(data or {})),
    request_model="AcceptModel",
    request_fixture_file="AcceptModel.json",
)

runner.add(
    "decline",
    lambda api: api.rfq.decline(LIVE_RFQ_ID),
)

runner.add(
    "cancel",
    lambda api: api.rfq.cancel(LIVE_RFQ_ID),
)

runner.add(
    "accept_winner",
    lambda api: api.rfq.accept_winner(LIVE_RFQ_ID),
)

runner.add(
    "add_comment",
    lambda api, data=None: api.rfq.add_comment(LIVE_RFQ_ID, **(data or {})),
    request_model="AcceptModel",
    request_fixture_file="AcceptModel.json",
)

# ═══════════════════════════════════════════════════════════════════════
# Job-Scoped RFQ Queries
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "list_rfqs",
    lambda api: api.jobs.list_rfqs(LIVE_JOB_DISPLAY_ID),
    response_model="List[QuoteRequestDisplayInfo]",
)

runner.add(
    "get_rfq_status",
    lambda api: api.jobs.get_rfq_status(LIVE_JOB_DISPLAY_ID, "LTL", "COMPANY_ID"),
    response_model="QuoteRequestStatus",
    fixture_file="QuoteRequestStatus.json",
)

if __name__ == "__main__":
    runner.run()
