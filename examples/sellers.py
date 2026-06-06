"""Example: Seller operations (Catalog API).

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (``examples/_sellers.py``).
See also: https://ab-sdk.readthedocs.io/en/latest/api/sellers.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, save
from examples.constants import TEST_SELLER_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    print("\n# api.sellers.list(is_active=True, page_number=1, page_size=25)")
    result = api.sellers.list(is_active=True, page_number=1, page_size=25)
    print(format_result(result))
    save("SellerExpandedDto.json", result)

    print(f"\n# api.sellers.get({TEST_SELLER_ID!r})")
    result = api.sellers.get(TEST_SELLER_ID)
    print(format_result(result))
    save("SellerExpandedDto_detail.json", result)

    # --- Mutating (operator-run; harness never auto-runs these) -------------
    print("\n# api.sellers.create(data=AddSellerRequest)")
    result = api.sellers.create(data=load_request("AddSellerRequest.json"))
    print(format_result(result))
    save("SellerDto.json", result)

    print(f"\n# api.sellers.update({TEST_SELLER_ID!r}, data=UpdateSellerRequest)")
    result = api.sellers.update(TEST_SELLER_ID, data=load_request("UpdateSellerRequest.json"))
    print(format_result(result))
    save("SellerDto.json", result)

    print(f"\n# api.sellers.delete({TEST_SELLER_ID!r})")
    result = api.sellers.delete(TEST_SELLER_ID)
    print(format_result(result))


if __name__ == "__main__":
    main()
