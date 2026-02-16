"""Example: Intacct operations (5 endpoints)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Intacct", env="staging")

LIVE_JOB_ID = 100001

runner.add(
    "get",
    lambda api: api.intacct.get(LIVE_JOB_ID),
    response_model="JobIntacctData",
    fixture_file="JobIntacctData.json",
)

runner.add(
    "post",
    lambda api: api.intacct.post(
        LIVE_JOB_ID,
        # TODO: capture fixture — needs valid Intacct data
    ),
    request_model="JobIntacctRequest",
    response_model="JobIntacctData",
)

if __name__ == "__main__":
    runner.run()
