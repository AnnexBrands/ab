"""Live integration tests for Users API."""

import pytest

pytestmark = pytest.mark.live


class TestUsersIntegration:
    def test_list_users(self, api):
        result = api.users.list({"page": 1, "pageSize": 5})
        # /users/list returns {totalCount, data} paginated wrapper;
        # _request with List[User] falls through to raw dict when
        # response is not a plain list.
        assert result is not None
        if isinstance(result, dict):
            assert "data" in result
            assert len(result["data"]) > 0
        else:
            assert isinstance(result, list)
            assert len(result) > 0

    def test_get_roles(self, api):
        result = api.users.get_roles()
        assert result is not None
        # API returns list of strings; result type depends on
        # UserRole model_validate behavior with string input.
        assert isinstance(result, list)
        assert len(result) > 0
