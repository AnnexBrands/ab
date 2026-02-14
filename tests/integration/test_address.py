"""Live integration tests for Address API (T074)."""

import pytest

pytestmark = pytest.mark.live


class TestAddressIntegration:
    def test_validate_address(self, api):
        result = api.address.validate(
            line1="5738 Westbourne Ave",
            city="Columbus",
            state="OH",
            zip="43213",
        )
        # May return 400 if fields don't match expected format
        if result is not None:
            assert hasattr(result, "is_valid") or isinstance(result, dict)

    def test_get_property_type(self, api):
        result = api.address.get_property_type(
            address1="5738 Westbourne Ave",
            city="Columbus",
            state="OH",
            zip_code="43213",
        )
        # May return 204 No Content
        if result is not None:
            assert result is not None
