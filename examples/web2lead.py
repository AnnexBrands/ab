"""Example: Web2Lead operations (2 methods)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Web2Lead", env="staging")

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "get",
    lambda api: api.web2lead.get(),
    response_model="Web2LeadResponse",
    fixture_file="Web2LeadResponse.json",
)

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "post",
    lambda api: api.web2lead.post(
        # TODO: capture fixture — needs valid Web2LeadRequest body
        {},
    ),
    request_model="Web2LeadRequest",
    response_model="Web2LeadResponse",
)

if __name__ == "__main__":
    runner.run()
