"""Example: User operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (``examples/_users.py``).
See also: https://ab-sdk.readthedocs.io/en/latest/api/users.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save


def main() -> None:
    api = ABConnectAPI(env="staging")

    print("\n# api.users.list(data=ListRequest)")
    result = api.users.list(data=load_request("ListRequest.json"))
    print(format_result(result))
    save("User.json", result)

    print("\n# api.users.get_roles()")
    result = api.users.get_roles()
    print(format_result(result))
    save("UserRole.json", result)

    # --- Mutating (set AB_RUN_MUTATIONS=1 to run; harness never auto-runs these) ---
    if mutations_enabled():
        print("\n# api.users.create(data=UserCreateRequest)")
        result = api.users.create(data=load_request("UserCreateRequest.json"))
        print(format_result(result))

        print("\n# api.users.update(data=UserUpdateRequest)")
        result = api.users.update(data=load_request("UserUpdateRequest.json"))
        print(format_result(result))


if __name__ == "__main__":
    main()
