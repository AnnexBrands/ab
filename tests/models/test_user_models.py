"""Fixture validation tests for User models (T064)."""

import pytest

from tests.conftest import load_fixture

from ab.api.models.users import User, UserRole


class TestUserModels:
    @pytest.mark.live
    def test_user(self):
        data = load_fixture("User")
        model = User.model_validate(data)
        assert model.id is not None

    @pytest.mark.live
    def test_user_role(self):
        data = load_fixture("UserRole")
        # Live API returns plain string; wrap if needed
        if isinstance(data, str):
            data = {"name": data}
        model = UserRole.model_validate(data)
