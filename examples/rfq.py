"""Example: RFQ lifecycle operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (examples/_rfq.py) to the plain-script form.

See also: https://ab-sdk.readthedocs.io/en/latest/api/rfq.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_JOB_DISPLAY_ID

# No dedicated RFQ-id constant exists; use the legacy literal placeholder. Replace
# with a real RFQ id discovered via api.rfq.get_for_job(...) for a live run.
TEST_RFQ_ID = "PLACEHOLDER"


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /rfq/{rfqId}
    print(f"\n# api.rfq.get({TEST_RFQ_ID!r})")
    result = api.rfq.get(TEST_RFQ_ID)
    print(format_result(result))
    save("QuoteRequestDisplayInfo_single.json", result)

    # GET /rfq/forjob/{jobId}
    print(f"\n# api.rfq.get_for_job({str(TEST_JOB_DISPLAY_ID)!r})")
    result = api.rfq.get_for_job(str(TEST_JOB_DISPLAY_ID))
    print(format_result(result))
    save("QuoteRequestDisplayInfo.json", result)

    # POST /rfq/{rfqId}/accept (state-changing → guarded)
    print(f"\n# api.rfq.accept({TEST_RFQ_ID!r}, data=AcceptModel(...))")
    if mutations_enabled():
        result = api.rfq.accept(TEST_RFQ_ID, data=load_request("AcceptModel.json"))
        print(format_result(result))
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # POST /rfq/{rfqId}/acceptwinner (state-changing → guarded)
    print(f"\n# api.rfq.accept_winner({TEST_RFQ_ID!r})")
    if mutations_enabled():
        result = api.rfq.accept_winner(TEST_RFQ_ID)
        print(format_result(result))
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # POST /rfq/{rfqId}/comment (state-changing → guarded)
    print(f"\n# api.rfq.add_comment({TEST_RFQ_ID!r}, data=AcceptModel(...))")
    if mutations_enabled():
        result = api.rfq.add_comment(TEST_RFQ_ID, data=load_request("AcceptModel.json"))
        print(format_result(result))
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # POST /rfq/{rfqId}/cancel (state-changing → guarded)
    print(f"\n# api.rfq.cancel({TEST_RFQ_ID!r})")
    if mutations_enabled():
        result = api.rfq.cancel(TEST_RFQ_ID)
        print(format_result(result))
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # POST /rfq/{rfqId}/decline (state-changing → guarded)
    print(f"\n# api.rfq.decline({TEST_RFQ_ID!r})")
    if mutations_enabled():
        result = api.rfq.decline(TEST_RFQ_ID)
        print(format_result(result))
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")


if __name__ == "__main__":
    main()
