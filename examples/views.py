"""Example: Views (saved grids) operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (examples/_views.py) to the plain-script form.

See also: https://ab-sdk.readthedocs.io/en/latest/api/views.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_VIEW_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /views/all
    print("\n# api.views.list()")
    result = api.views.list()
    print(format_result(result))
    save("GridViewDetails.json", result)

    # GET /views/{viewId}
    print(f"\n# api.views.get({TEST_VIEW_ID!r})")
    result = api.views.get(TEST_VIEW_ID)
    print(format_result(result))
    save("GridViewDetails.json", result)

    # GET /views/{viewId}/accessinfo
    print(f"\n# api.views.get_access_info({TEST_VIEW_ID!r})")
    result = api.views.get_access_info(TEST_VIEW_ID)
    print(format_result(result))
    save("GridViewAccess.json", result)

    # GET /views/datasetsps
    print("\n# api.views.get_dataset_sps()")
    result = api.views.get_dataset_sps()
    print(format_result(result))
    save("StoredProcedureColumn.json", result)

    # GET /views/datasetsp/{spName}
    sp_name = "spName"  # legacy literal — replace with a real stored-procedure name
    print(f"\n# api.views.get_dataset_sp({sp_name!r})")
    result = api.views.get_dataset_sp(sp_name)
    print(format_result(result))
    save("StoredProcedureColumn.json", result)

    # POST /views
    if mutations_enabled():
        print("\n# api.views.create(data=GridViewCreateRequest(...))")
        result = api.views.create(data=load_request("GridViewCreateRequest.json"))
        print(format_result(result))
        save("GridViewDetails.json", result)
    else:
        print("\n# api.views.create skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # PUT /views/{viewId}/access — no response model to save.
    if mutations_enabled():
        print(f"\n# api.views.update_access({TEST_VIEW_ID!r}, data=GridViewAccess(...))")
        result = api.views.update_access(TEST_VIEW_ID, data=load_request("GridViewAccess.json"))
        print(format_result(result))
    else:
        print("\n# api.views.update_access skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # DELETE /views/{viewId}
    if mutations_enabled():
        print(f"\n# api.views.delete({TEST_VIEW_ID!r})")
        result = api.views.delete(TEST_VIEW_ID)
        print(format_result(result))
        save("ServiceBaseResponse.json", result)
    else:
        print("\n# api.views.delete skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")


if __name__ == "__main__":
    main()
