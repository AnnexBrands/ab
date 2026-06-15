"""Example: Jobs core operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runners (examples/_jobs.py and examples/_freight_providers.py) to the
plain-script form.

Read-only GET/search calls run unguarded; state-changing calls (create, save,
update, update_item, add_item_notes, add_freight_items) are wrapped in
``if mutations_enabled():`` — set ``AB_RUN_MUTATIONS=1`` to run them.
See also: https://ab-sdk.readthedocs.io/en/latest/api/jobs.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_COMPANY_CODE, TEST_ITEM_ID, TEST_JOB_DISPLAY_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /job/{jobDisplayId}
    print(f"\n# api.jobs.get({TEST_JOB_DISPLAY_ID!r})")
    result = api.jobs.get(TEST_JOB_DISPLAY_ID)
    print(format_result(result))
    save("Job.json", result)

    # GET /job/search — explicit snake_case query kwargs.
    print(f"\n# api.jobs.search(job_display_id={TEST_JOB_DISPLAY_ID!r})")
    result = api.jobs.search(job_display_id=TEST_JOB_DISPLAY_ID)
    print(format_result(result))
    save("JobSearchResult.json", result)

    # GET /job/{jobDisplayId}/price
    print(f"\n# api.jobs.get_price({TEST_JOB_DISPLAY_ID!r})")
    result = api.jobs.get_price(TEST_JOB_DISPLAY_ID)
    print(format_result(result))
    save("JobPrice.json", result)

    # GET /job/{jobDisplayId}/calendaritems
    print(f"\n# api.jobs.get_calendar_items({TEST_JOB_DISPLAY_ID!r})")
    result = api.jobs.get_calendar_items(TEST_JOB_DISPLAY_ID)
    print(format_result(result))
    save("CalendarItem.json", result)

    # GET /job/{jobDisplayId}/packagingcontainers
    print(f"\n# api.jobs.get_packaging_containers({TEST_JOB_DISPLAY_ID!r})")
    result = api.jobs.get_packaging_containers(TEST_JOB_DISPLAY_ID)
    print(format_result(result))
    save("PackagingContainer.json", result)

    # GET /job/{jobDisplayId}/updatePageConfig
    print(f"\n# api.jobs.get_update_page_config({TEST_JOB_DISPLAY_ID!r})")
    result = api.jobs.get_update_page_config(TEST_JOB_DISPLAY_ID)
    print(format_result(result))
    save("JobUpdatePageConfig.json", result)

    # POST /job/searchByDetails — read-only search; body from request fixture.
    print("\n# api.jobs.search_by_details(data=JobSearchRequest(...))")
    result = api.jobs.search_by_details(data=load_request("JobSearchRequest.json"))
    print(format_result(result))
    save("JobSearchResult.json", result)

    # POST /job — creates a job (mutating).
    print("\n# api.jobs.create(data=JobCreateRequest(...))")
    if mutations_enabled():
        result = api.jobs.create(data=load_request("JobCreateRequest.json"))
        print(format_result(result))
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # PUT /job/save — saves a job (mutating).
    print("\n# api.jobs.save(data=JobSaveRequest(...))")
    if mutations_enabled():
        result = api.jobs.save(data=load_request("JobSaveRequest.json"))
        print(format_result(result))
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # POST /job/update (ABC surface) — updates a job (mutating).
    print("\n# api.jobs.update(data=JobUpdateRequest(...))")
    if mutations_enabled():
        result = api.jobs.update(data=load_request("JobUpdateRequest.json"))
        print(format_result(result))
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # PUT /job/{jobDisplayId}/item/{itemId} — updates an item (mutating).
    print(f"\n# api.jobs.update_item({TEST_JOB_DISPLAY_ID!r}, {TEST_ITEM_ID!r}, data=ItemUpdateRequest(...))")
    if mutations_enabled():
        result = api.jobs.update_item(
            TEST_JOB_DISPLAY_ID,
            TEST_ITEM_ID,
            data=load_request("ItemUpdateRequest.json"),
        )
        print(format_result(result))
        save("ServiceBaseResponse.json", result)
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # POST /job/{jobDisplayId}/item/notes — adds item notes (mutating).
    print(f"\n# api.jobs.add_item_notes({TEST_JOB_DISPLAY_ID!r}, data=ItemNotesRequest(...))")
    if mutations_enabled():
        result = api.jobs.add_item_notes(
            TEST_JOB_DISPLAY_ID,
            data=load_request("ItemNotesRequest.json"),
        )
        print(format_result(result))
        save("ServiceBaseResponse.json", result)
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # POST /job/{jobDisplayId}/freightitems — adds freight items (mutating).
    print(f"\n# api.jobs.add_freight_items({TEST_JOB_DISPLAY_ID!r}, data=FreightItemsRequest(...))")
    if mutations_enabled():
        result = api.jobs.add_freight_items(
            TEST_JOB_DISPLAY_ID,
            data=load_request("FreightItemsRequest.json"),
        )
        print(format_result(result))
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # POST /job/transfer/{jobDisplayId} — transfers the job to a franchisee
    # (mutating). ``franchisee_id`` is positional and accepts a company code
    # (resolved to a UUID by the SDK) or a UUID directly; see TransferModel.
    print(f"\n# api.jobs.transfer({TEST_JOB_DISPLAY_ID!r}, {TEST_COMPANY_CODE!r})")
    if mutations_enabled():
        result = api.jobs.transfer(TEST_JOB_DISPLAY_ID, TEST_COMPANY_CODE)
        print(format_result(result))
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # POST /job/{jobDisplayId}/book — books the job: confirms the quote into
    # a booked job (mutating; irreversible through the API).
    print(f"\n# api.jobs.book({TEST_JOB_DISPLAY_ID!r})")
    if mutations_enabled():
        api.jobs.book(TEST_JOB_DISPLAY_ID)
        print("  (booked)")
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (books the job on staging)")


if __name__ == "__main__":
    main()
