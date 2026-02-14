"""Example: AutoPrice operations (2 methods)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("AutoPrice", env="staging")

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "quick_quote",
    lambda api: api.autoprice.quick_quote({
        "originZip": "43213",
        "destinationZip": "90210",
        "weight": 150,
    }),
    request_model="QuoteRequestModel",
    response_model="QuickQuoteResponse",
    fixture_file="QuickQuoteResponse.json",
)

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "quote_request",
    lambda api: api.autoprice.quote_request(
        # TODO: capture fixture — needs items array with weight, class fields
        #       and valid origin/destination
        {
            "originZip": "43213",
            "destinationZip": "90210",
            "items": [{"weight": 150, "class": "70"}],
        },
    ),
    request_model="QuoteRequestModel",
    response_model="QuoteRequestResponse",
)

if __name__ == "__main__":
    runner.run()
