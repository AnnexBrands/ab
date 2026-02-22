"""Live integration tests for Address API."""

import pytest

from ab.api.models.address import AddressIsValidResult
from tests.conftest import assert_no_extra_fields, load_request_kwargs

pytestmark = pytest.mark.live


class TestAddressIntegration:
    def test_validate_address(self, api):
        params = load_request_kwargs("AddressValidateParams")
        result = api.address.validate(**params)
        # May return 400 if fields don't match expected format
        if result is not None:
            assert isinstance(result, AddressIsValidResult)
            assert_no_extra_fields(result)

    def test_get_property_type(self, api):
        params = load_request_kwargs("AddressPropertyTypeParams")
        result = api.address.get_property_type(**params)
        # May return 204 No Content
        if result is not None:
            assert isinstance(result, int)
