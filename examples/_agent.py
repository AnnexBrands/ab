"""Example: Agent assignment operations (1 endpoint, via api.jobs.agent.*)."""

from examples._runner import ExampleRunner
from tests.constants import TEST_JOB_DISPLAY_ID

runner = ExampleRunner("Agent", env="staging")

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "change_agent",
    lambda api, data=None: api.jobs.change_agent(
        TEST_JOB_DISPLAY_ID,
        data=data or {
            "serviceType": 3,
            "agentId": "ed282b80-54fe-4f42-bf1b-69103ce1f76c",
            "recalculatePrice": False,
            "applyRebate": False,
        },
    ),
    request_model="ChangeJobAgentRequest",
    request_fixture_file="ChangeJobAgentRequest.json",
    response_model="ServiceBaseResponse",
    fixture_file="ServiceBaseResponse.json",
)

if __name__ == "__main__":
    runner.run()
