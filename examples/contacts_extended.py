"""Example: Extended contact operations.

Covers aggregated history, history graph data, merge preview, history creation,
and merge. Live SDK example — real call, real printed pydantic response. Migrated
from the deprecated runner (examples/_contacts_extended.py) to the plain-script form.

See also: https://ab-sdk.readthedocs.io/en/latest/api/contacts.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_CONTACT_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /contacts/{contactId}/history/aggregated
    print("\n# api.contacts.get_history_aggregated(...)")
    result = api.contacts.get_history_aggregated(str(TEST_CONTACT_ID))
    print(format_result(result))
    save("ContactHistoryAggregated.json", result)

    # GET /contacts/{contactId}/history/graphdata
    print("\n# api.contacts.get_history_graph_data(...)")
    result = api.contacts.get_history_graph_data(str(TEST_CONTACT_ID))
    print(format_result(result))
    save("ContactGraphData.json", result)

    # POST /contacts/{mergeToId}/merge/preview — read-only preview, safe to run.
    print("\n# api.contacts.merge_preview(..., data=ContactMergeRequest(...))")
    result = api.contacts.merge_preview(
        str(TEST_CONTACT_ID), data=load_request("ContactMergeRequest.json")
    )
    print(format_result(result))
    save("ContactMergePreview.json", result)

    # POST /contacts/{contactId}/history — creates a history record (mutating).
    print("\n# api.contacts.post_history(..., data=ContactHistoryCreateRequest(...))")
    if mutations_enabled():
        result = api.contacts.post_history(
            str(TEST_CONTACT_ID), data=load_request("ContactHistoryCreateRequest.json")
        )
        print(format_result(result))
        save("ContactHistory.json", result)
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # PUT /contacts/{mergeToId}/merge — merges contacts (mutating).
    print("\n# api.contacts.merge(..., data=ContactMergeRequest(...))")
    if mutations_enabled():
        result = api.contacts.merge(
            str(TEST_CONTACT_ID), data=load_request("ContactMergeRequest.json")
        )
        print(format_result(result))
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")


if __name__ == "__main__":
    main()
