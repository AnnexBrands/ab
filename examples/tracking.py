"""Example: Tracking operations (2 methods, via api.jobs.*)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Tracking", env="staging")

LIVE_JOB_DISPLAY_ID = 2000000

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get_tracking",
    lambda api: api.jobs.get_tracking(
        # TODO: capture fixture — needs shipped job ID with tracking data
        LIVE_JOB_DISPLAY_ID,
    ),
    response_model="TrackingInfo",
)

runner.add(
    "get_tracking_v3",
    lambda api: api.jobs.get_tracking_v3(
        # TODO: capture fixture — needs shipped job ID with tracking history
        LIVE_JOB_DISPLAY_ID,
        history_amount=10,
    ),
    response_model="TrackingInfoV3",
)

if __name__ == "__main__":
    runner.run()
