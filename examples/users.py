"""Example: User operations (4 methods)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Users", env="staging")

# ── Captured fixtures ────────────────────────────────────────────────

runner.add(
    "list",
    lambda api, data=None: api.users.list(data or {}),
    request_model="ListRequest",
    request_fixture_file="ListRequest.json",
    response_model="List[User]",
    fixture_file="User.json",
)

runner.add(
    "get_roles",
    lambda api: api.users.get_roles(),
    response_model="List[str]",
    fixture_file="UserRole.json",
)

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "create",
    lambda api, data=None: api.users.create(data or {}),
    request_model="UserCreateRequest",
    request_fixture_file="UserCreateRequest.json",
)

runner.add(
    "update",
    lambda api, data=None: api.users.update(data or {}),
    request_model="UserUpdateRequest",
    request_fixture_file="UserUpdateRequest.json",
)

if __name__ == "__main__":
    runner.run()
