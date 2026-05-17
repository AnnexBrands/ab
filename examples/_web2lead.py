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

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "post",
    lambda api, data=None: api.web2lead.post(data=data or {}),
    request_model="Web2LeadRequest",
    request_fixture_file="Web2LeadRequest.json",
    response_model="Web2LeadResponse",
    fixture_file="Web2LeadResponse.json",
)

if __name__ == "__main__":
    runner.run()
