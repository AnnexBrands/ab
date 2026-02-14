"""Live integration tests for Users API (T076)."""

import pytest

pytestmark = pytest.mark.live


class TestUsersIntegration:
    def test_list_users(self, api):
        result = api.users.list({"page": 1, "pageSize": 5})
        assert result is not None

    def test_get_roles(self, api):
        result = api.users.get_roles()
        assert result is not None
