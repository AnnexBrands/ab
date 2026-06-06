"""Example: Address operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (``examples/_address.py``) to the plain-script form.

These endpoints take explicit snake_case query-param kwargs (Constitution IX), so
the call uses real inline values rather than a request fixture.
See also: https://ab-sdk.readthedocs.io/en/latest/api/address.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import save


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /address/isvalid
    print("\n# api.address.validate(line1=..., city=..., state=..., zip=...)")
    result = api.address.validate(
        line1="7580 Metropolitan Dr", city="San Diego", state="CA", zip="92108"
    )
    print(format_result(result))
    save("AddressIsValidResult.json", result)

    # GET /address/propertytype — returns an int property-type code.
    print("\n# api.address.get_property_type(address1=..., city=..., state=..., zip_code=...)")
    result = api.address.get_property_type(
        address1="7580 Metropolitan Dr",
        address2="Ste 200",
        city="San Diego",
        state="CA",
        zip_code="92108",
    )
    print(format_result(result))
    save("PropertyType.json", result)


if __name__ == "__main__":
    main()
