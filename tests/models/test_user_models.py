"""Fixture validation tests for User models."""

import pytest

from ab.api.models.users import User
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

    def test_user_role(self):
        data = require_fixture("UserRole", "GET", "/users/roles")
        # API returns List[str], not a Pydantic model
        assert isinstance(data, list), f"Expected list, got {type(data)}"
        if not data:
            pytest.skip("UserRole fixture is an empty list")
        assert isinstance(data[0], str), f"Expected str items, got {type(data[0])}"
