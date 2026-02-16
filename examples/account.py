"""Example: Account operations (10 endpoints)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Account", env="staging")

# ── Profile ──────────────────────────────────────────────────────────

runner.add(
    "get_profile",
    lambda api: api.account.get_profile(),
    response_model="UserProfile",
    fixture_file="UserProfile.json",
)

# ── Verify Reset Token ──────────────────────────────────────────────

runner.add(
    "verify_reset_token",
    lambda api: api.account.verify_reset_token(
        username="test@example.com",
        token="test-token",
    ),
    response_model="TokenVerification",
    fixture_file="TokenVerification.json",
)

# ── Register (needs data) ───────────────────────────────────────────

runner.add(
    "register",
    lambda api: api.account.register(
        # TODO: capture fixture — needs valid registration data
    ),
    request_model="RegisterRequest",
    response_model="AccountResponse",
)

if __name__ == "__main__":
    runner.run()
