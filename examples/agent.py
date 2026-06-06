"""Example: change a job's agent (api.jobs.change_agent).

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated ``examples/_agent.py`` with the operator-verified working input.

``POST /job/{jobDisplayId}/changeAgent`` mutates staging, so the call is guarded:
set ``AB_RUN_MUTATIONS=1`` (or tick "confirm" in the progress app) to run it.
See also: https://ab-sdk.readthedocs.io/en/latest/api/jobs.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import mutations_enabled, save
from examples.constants import TEST_JOB_DISPLAY_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    if not mutations_enabled():
        print("# api.jobs.change_agent skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")
        return

    print(f"\n# api.jobs.change_agent({TEST_JOB_DISPLAY_ID!r}, data=ChangeJobAgentRequest(...))")
    result = api.jobs.change_agent(
        TEST_JOB_DISPLAY_ID,
        data={
            "serviceType": 3,
            "agentId": "47b22fe2-fd16-e611-ae37-00155d426802",
            "recalculatePrice": False,
            "applyRebate": False,
        },
    )
    print(format_result(result))
    save("ServiceBaseResponse.json", result)


if __name__ == "__main__":
    main()
