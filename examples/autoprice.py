"""Example: AutoPrice operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (``examples/_autoprice.py``).
See also: https://ab-sdk.readthedocs.io/en/latest/api/autoprice.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save


def main() -> None:
    api = ABConnectAPI(env="staging")
    body = load_request("QuoteRequestModel.json")

    # POST /AutoPrice/QuickQuote — instant quote for an items payload.
    print("\n# api.autoprice.quick_quote(data=QuoteRequestModel)")
    result = api.autoprice.quick_quote(data=body)
    print(format_result(result))
    save("QuickQuoteResponse.json", result)

    # POST /AutoPrice/QuoteRequest — full quote request (creates a quote
    # request on staging; guarded).
    if mutations_enabled():
        print("\n# api.autoprice.quote_request(data=QuoteRequestModel)")
        result = api.autoprice.quote_request(data=body)
        print(format_result(result))
        save("QuoteRequestResponse.json", result)
    else:
        print(
            "# api.autoprice.quote_request skipped — set AB_RUN_MUTATIONS=1 to run "
            "(creates a quote request on staging)"
        )


if __name__ == "__main__":
    main()
