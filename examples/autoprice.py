"""Example: AutoPrice operations (2 methods)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("AutoPrice", env="staging")

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "quick_quote",
    lambda api, data=None: api.autoprice.quick_quote(data or {}),
    request_model="QuoteRequestModel",
    request_fixture_file="QuoteRequestModel.json",
    response_model="QuickQuoteResponse",
    fixture_file="QuickQuoteResponse.json",
)

runner.add(
    "quote_request",
    lambda api, data=None: api.autoprice.quote_request(data or {}),
    request_model="QuoteRequestModel",
    request_fixture_file="QuoteRequestModel.json",
    response_model="QuoteRequestResponse",
    fixture_file="QuoteRequestResponse.json",
)

if __name__ == "__main__":
    runner.run()
