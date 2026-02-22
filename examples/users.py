"""Example: User operations (4 methods)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Users", env="staging")

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "list",
    lambda api: api.users.list({}),
    request_model="ListRequest",
    response_model="List[User]",
    fixture_file="User.json",
)

runner.add(
    "get_roles",
    lambda api: api.users.get_roles(),
    response_model="List[str]",
    fixture_file="UserRole.json",
)

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "create",
    lambda api: api.users.create(
        # TODO: capture fixture — needs UserCreateRequest body
        {},
    ),
    request_model="UserCreateRequest",
    # no response model
)

runner.add(
    "update",
    lambda api: api.users.update(
        # TODO: capture fixture — needs UserUpdateRequest body
        {},
    ),
    request_model="UserUpdateRequest",
    # no response model
)

if __name__ == "__main__":
    runner.run()
