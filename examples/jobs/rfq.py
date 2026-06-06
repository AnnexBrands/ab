"""Example: api.jobs.rfq — job-scoped RFQ listing and per-company status.

Live SDK example — real call, real printed pydantic response. Authored for
feature 037 (endpoint previously had no example).

This is the job-scoped ``api.jobs.rfq`` subgroup (the two
``/job/{jobDisplayId}/rfq/*`` routes). It is distinct from the top-level
``api.rfq`` lifecycle group demonstrated in ``examples/rfq.py``.

See also: https://ab-sdk.readthedocs.io/en/latest/api/jobs.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import save
from examples.constants import (
    TEST_JOB_DISPLAY_ID,
    TEST_RFQ_COMPANY_ID,
    TEST_RFQ_SERVICE_TYPE,
)


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /job/{jobDisplayId}/rfq — list the job's quote requests (read-only)
    print(f"\n# api.jobs.rfq.list({TEST_JOB_DISPLAY_ID})")
    result = api.jobs.rfq.list(TEST_JOB_DISPLAY_ID)
    print(format_result(result))
    save("QuoteRequestDisplayInfo.json", result)

    # GET /job/{jobDisplayId}/rfq/statusof/{rfqServiceType}/forcompany/{companyId}
    # — RFQ status code for one company + service type (read-only; resp=int).
    print(
        f"\n# api.jobs.rfq.status({TEST_JOB_DISPLAY_ID}, "
        f"{TEST_RFQ_SERVICE_TYPE!r}, {TEST_RFQ_COMPANY_ID!r})"
    )
    status = api.jobs.rfq.status(
        TEST_JOB_DISPLAY_ID, TEST_RFQ_SERVICE_TYPE, TEST_RFQ_COMPANY_ID
    )
    print(format_result(status))  # int — no fixture to save


if __name__ == "__main__":
    main()
