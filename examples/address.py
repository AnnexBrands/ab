"""Example: Address operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (``examples/_address.py``) to the plain-script form.
See also: https://ab-sdk.readthedocs.io/en/latest/api/address.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, save


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /address/isvalid — query params modelled by AddressValidateParams.
    print("\n# api.address.validate(**AddressValidateParams)")
    params = load_request("AddressValidateParams.json")
    result = api.address.validate(**params)
    print(format_result(result))
    save("AddressIsValidResult.json", result)

    # GET /address/propertytype — returns an int property-type code.
    print("\n# api.address.get_property_type(**AddressPropertyTypeParams)")
    params = load_request("AddressPropertyTypeParams.json")
    result = api.address.get_property_type(**params)
    print(format_result(result))
    save("PropertyType.json", result)


if __name__ == "__main__":
    main()
