"""Example: Web2Lead operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (``examples/_web2lead.py``).
See also: https://ab-sdk.readthedocs.io/en/latest/api/web2lead.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, save


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /web2lead — current web-lead configuration/response.
    print("\n# api.web2lead.get()")
    result = api.web2lead.get()
    print(format_result(result))
    save("Web2LeadResponse.json", result)

    # POST /web2lead — submit a web lead (mutating; operator-run).
    print("\n# api.web2lead.post(data=Web2LeadRequest)")
    result = api.web2lead.post(data=load_request("Web2LeadRequest.json"))
    print(format_result(result))
    save("Web2LeadResponse.json", result)


if __name__ == "__main__":
    main()
