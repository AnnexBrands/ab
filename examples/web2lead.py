"""Example: Web2Lead operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (``examples/_web2lead.py``).
See also: https://ab-sdk.readthedocs.io/en/latest/api/web2lead.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /web2lead — requires a params model (Web2LeadGetParams). The dict is
    # validated against the model, which accepts the API's alias keys.
    print("\n# api.web2lead.get(params=Web2LeadGetParams)")
    result = api.web2lead.get(params=load_request("Web2LeadGetParams.json"))
    print(format_result(result))
    save("Web2LeadResponse.json", result)

    # POST /web2lead — submit a web lead (set AB_RUN_MUTATIONS=1 to run).
    if mutations_enabled():
        print("\n# api.web2lead.post(data=Web2LeadRequest)")
        result = api.web2lead.post(data=load_request("Web2LeadRequest.json"))
        print(format_result(result))
        save("Web2LeadResponse.json", result)


if __name__ == "__main__":
    main()
