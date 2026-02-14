"""Fixture validation tests for User models (T064)."""

import pytest

from tests.conftest import require_fixture

from ab.api.models.users import User, UserRole


class TestUserModels:
    @pytest.mark.live
    def test_user(self):
        data = require_fixture("User", "POST", "/users/list", required=True)
        model = User.model_validate(data)
        assert model.id is not None

    @pytest.mark.live
    def test_user_role(self):
        data = require_fixture("UserRole", "GET", "/users/roles", required=True)
        # Live API returns plain string; wrap if needed
        if isinstance(data, str):
            data = {"name": data}
        model = UserRole.model_validate(data)
