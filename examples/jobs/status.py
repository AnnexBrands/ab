"""Example: api.jobs.status — job-scoped status transitions.

Live SDK example — real call, real printed pydantic response. Authored for
feature 037 (endpoint previously had no example).

``set_quote`` flips a job into the *quote* status. It mutates staging state,
so it is guarded behind ``mutations_enabled()`` — set ``AB_RUN_MUTATIONS=1``
to run it.

See also: https://ab-sdk.readthedocs.io/en/latest/api/jobs/status.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import mutations_enabled, save
from examples.constants import TEST_JOB_DISPLAY_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # POST /job/{jobDisplayId}/status/quote — moves the job to quote status.
    print(f"\n# api.jobs.status.set_quote({TEST_JOB_DISPLAY_ID!r})")
    if mutations_enabled():
        result = api.jobs.status.set_quote(TEST_JOB_DISPLAY_ID)
        print(format_result(result))
        save("ServiceBaseResponse.json", result)
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")


if __name__ == "__main__":
    main()
