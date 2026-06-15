"""Example: Partner operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (``examples/_partners.py``).
See also: https://ab-sdk.readthedocs.io/en/latest/api/partners.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, save

# A real partner id must be supplied to exercise the detail endpoint; until one is
# configured, partners.get reports as awaiting-data.
TEST_PARTNER_ID = "PLACEHOLDER"


def main() -> None:
    api = ABConnectAPI(env="staging")

    print("\n# api.partners.list()")
    result = api.partners.list()
    print(format_result(result))
    save("Partner_list.json", result)

    print(f"\n# api.partners.get({TEST_PARTNER_ID!r})")
    result = api.partners.get(TEST_PARTNER_ID)
    print(format_result(result))

    print("\n# api.partners.search(data=PartnerSearchRequest)")
    result = api.partners.search(data=load_request("PartnerSearchRequest.json"))
    print(format_result(result))


if __name__ == "__main__":
    main()
