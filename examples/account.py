"""Example: Account operations.

Live SDK example — real call, real printed pydantic response. Authored when
the ``account`` group was added (endpoint previously reachable only through
the private transport, ``api._acportal.request("GET", "/account/profile")``).

See also: https://ab-sdk.readthedocs.io/en/latest/api/account.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import save


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /account/profile — the authenticated user's own profile.
    print("\n# api.account.get_profile()")
    result = api.account.get_profile()
    print(format_result(result))
    save("AccountProfile.json", result)


if __name__ == "__main__":
    main()
