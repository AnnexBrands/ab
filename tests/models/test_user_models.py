"""Fixture validation tests for User models."""

import pytest

from ab.api.models.users import User, UserRole
from tests.conftest import assert_no_extra_fields, require_fixture


class TestUserModels:
    @pytest.mark.live
    def test_user(self):
        data = require_fixture("User", "POST", "/users/list", required=True)
        # User fixture is paginated: {totalCount, data}
        if isinstance(data, dict) and "data" in data:
            items = data["data"]
            assert len(items) > 0, "User fixture has empty data array"
            data = items[0]
        model = User.model_validate(data)
        assert isinstance(model, User)
        assert_no_extra_fields(model)
        assert model.id is not None

    @pytest.mark.live
    def test_user_role(self):
        data = require_fixture("UserRole", "GET", "/users/roles", required=True)
        # Live API returns plain strings, not dicts
        if isinstance(data, list) and data and isinstance(data[0], str):
            model = UserRole(name=data[0])
        elif isinstance(data, str):
            model = UserRole(name=data)
        else:
            model = UserRole.model_validate(data)
        assert isinstance(model, UserRole)
