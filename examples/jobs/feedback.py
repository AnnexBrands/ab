"""Example: api.jobs feedback — job feedback selection and cancellation flag.

Live SDK example — real call, real printed pydantic response. The GET is
read-only and runs by default. The POST can change job state when ``cancelJob``
is true, so it is guarded behind ``AB_RUN_MUTATIONS=1``.

See also: https://ab-sdk.readthedocs.io/en/latest/api/jobs.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_JOB_DISPLAY_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /job/feedback/{jobDisplayId} — current feedback selection.
    print(f"\n# api.jobs.get_feedback({TEST_JOB_DISPLAY_ID!r})")
    result = api.jobs.get_feedback(TEST_JOB_DISPLAY_ID)
    print(format_result(result))
    save("FeedbackSaveModel.json", result)

    # POST /job/feedback/{jobDisplayId} — saves feedbackId/cancelJob.
    print(f"\n# api.jobs.save_feedback({TEST_JOB_DISPLAY_ID!r}, data=FeedbackSaveModel(...))")
    if mutations_enabled():
        response = api.jobs.save_feedback(
            TEST_JOB_DISPLAY_ID,
            data=load_request("FeedbackSaveModel.json"),
        )
        print(format_result(response))
        save("ServiceBaseResponse.json", response)
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (may mutate staging)")


if __name__ == "__main__":
    main()
