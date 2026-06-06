from ab import ABConnectAPI
from examples.constants import TEST_JOB_DISPLAY_ID

api = ABConnectAPI(env="staging")
result = api.jobs.change_agent(
    TEST_JOB_DISPLAY_ID,
    data={
        "serviceType": 3,
        "agentId": "47b22fe2-fd16-e611-ae37-00155d426802",
        "recalculatePrice": False,
        "applyRebate": False,
    },
)
print(result)
