"""Live integration tests for Users API."""

import pytest

from tests.conftest import load_request_fixture

pytestmark = pytest.mark.live


class TestUsersIntegration:
    def test_list_users(self, api):
        data = load_request_fixture("ListRequest")
        result = api.users.list(data)
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
        # API returns a plain list of role-name strings.
        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0], str)
