"""Unit tests for ab.cli.route_resolver."""

from __future__ import annotations

import pytest

from ab.cli.route_resolver import path_param_to_constant, resolve_routes_for_class


class TestResolveRoutesForClass:
    """Test method-to-Route mapping via source introspection."""

    def test_contacts_endpoint_returns_routes(self) -> None:
        from ab.api.endpoints.contacts import ContactsEndpoint

        routes = resolve_routes_for_class(ContactsEndpoint)
        assert len(routes) > 0, "Should resolve at least one Route"

    def test_known_method_has_correct_route(self) -> None:
        from ab.api.endpoints.jobs import JobsEndpoint

        routes = resolve_routes_for_class(JobsEndpoint)
        assert "get" in routes
        r = routes["get"]
        assert r.method == "GET"
        assert r.path == "/job/{jobDisplayId}"
        assert r.response_model == "Job"

    def test_helper_methods_have_no_route(self) -> None:
        from ab.api.endpoints.jobs import JobsEndpoint

        routes = resolve_routes_for_class(JobsEndpoint)
        # get_timeline is a helper wrapper that doesn't call _request directly
        assert "get_timeline" not in routes

    def test_all_routes_are_route_instances(self) -> None:
        from ab.api.endpoints.contacts import ContactsEndpoint
        from ab.api.route import Route

        routes = resolve_routes_for_class(ContactsEndpoint)
        for name, route in routes.items():
            assert isinstance(route, Route), f"{name} is not a Route"


class TestPathParamToConstant:
    """Test camelCase → TEST_SCREAMING_SNAKE conversion."""

    @pytest.mark.parametrize(
        "param,expected",
        [
            ("jobDisplayId", "TEST_JOB_DISPLAY_ID"),
            ("contactId", "TEST_CONTACT_ID"),
            ("companyId", "TEST_COMPANY_ID"),
            ("id", "TEST_ID"),
            ("sellerId", "TEST_SELLER_ID"),
            ("timelineTaskId", "TEST_TIMELINE_TASK_ID"),
        ],
    )
    def test_conversion(self, param: str, expected: str) -> None:
        assert path_param_to_constant(param) == expected
