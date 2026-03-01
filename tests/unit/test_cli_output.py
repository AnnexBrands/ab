"""Integration tests for CLI help and listing output."""

from __future__ import annotations

import io
import sys

from ab.cli.discovery import MethodInfo, ParamInfo, discover_endpoints_from_class
from ab.cli.parser import (
    _format_cli_syntax,
    _format_python_signature,
    _strip_rst,
    print_method_help,
)


class TestStripRst:
    def test_strips_class_role(self) -> None:
        assert _strip_rst(":class:`ModelName`") == "ModelName"

    def test_strips_meth_role(self) -> None:
        assert _strip_rst(":meth:`foo`") == "foo"

    def test_preserves_plain_text(self) -> None:
        assert _strip_rst("plain text") == "plain text"


class TestFormatPythonSignature:
    def test_basic_signature(self) -> None:
        method = MethodInfo(
            name="get",
            positional_params=[ParamInfo(name="job_id", cli_name="--job-id", annotation=int)],
            return_annotation="Job",
        )
        result = _format_python_signature("jobs", method)
        assert result == "api.jobs.get(job_id: int) -> Job"

    def test_no_return_type(self) -> None:
        method = MethodInfo(name="create", positional_params=[])
        result = _format_python_signature("jobs", method)
        assert result == "api.jobs.create()"


class TestFormatCliSyntax:
    def test_with_positional(self) -> None:
        method = MethodInfo(
            name="get",
            positional_params=[ParamInfo(name="job_id", cli_name="--job-id")],
        )
        result = _format_cli_syntax("jobs", method)
        assert result == "ab jobs get <job_id>"

    def test_with_keyword(self) -> None:
        method = MethodInfo(
            name="search",
            keyword_params=[ParamInfo(name="status", cli_name="--status", kind="keyword")],
        )
        result = _format_cli_syntax("jobs", method)
        assert result == "ab jobs search [--status=VALUE]"


class TestPrintMethodHelp:
    def _capture_help(self, method: MethodInfo, module_name: str = "") -> str:
        buf = io.StringIO()
        old_stderr = sys.stderr
        sys.stderr = buf
        try:
            print_method_help(method, module_name=module_name)
        finally:
            sys.stderr = old_stderr
        return buf.getvalue()

    def test_contains_route_line(self) -> None:
        from ab.api.route import Route

        route = Route("GET", "/job/{jobDisplayId}", response_model="Job")
        method = MethodInfo(
            name="get",
            positional_params=[ParamInfo(name="job_display_id", cli_name="--job-display-id", annotation=int)],
            route=route,
            return_annotation="Job",
        )
        output = self._capture_help(method, "jobs")
        assert "GET /job/{jobDisplayId}" in output

    def test_contains_python_signature(self) -> None:
        from ab.api.route import Route

        route = Route("GET", "/job/{jobDisplayId}", response_model="Job")
        method = MethodInfo(
            name="get",
            positional_params=[ParamInfo(name="job_display_id", cli_name="--job-display-id", annotation=int)],
            route=route,
            return_annotation="Job",
        )
        output = self._capture_help(method, "jobs")
        assert "api.jobs.get" in output

    def test_contains_cli_syntax(self) -> None:
        method = MethodInfo(
            name="get",
            positional_params=[ParamInfo(name="job_id", cli_name="--job-id", annotation=int)],
        )
        output = self._capture_help(method, "jobs")
        assert "ab jobs get" in output


class TestDiscovery:
    def test_discover_returns_endpoints(self) -> None:
        registry = discover_endpoints_from_class()
        assert len(registry) > 0

    def test_endpoint_has_aliases(self) -> None:
        registry = discover_endpoints_from_class()
        jobs = registry.get("jobs")
        assert jobs is not None
        assert "job" in jobs.aliases

    def test_endpoint_has_path_root(self) -> None:
        registry = discover_endpoints_from_class()
        jobs = registry.get("jobs")
        assert jobs is not None
        assert jobs.path_root == "/job"

    def test_method_has_route(self) -> None:
        registry = discover_endpoints_from_class()
        jobs = registry.get("jobs")
        get_method = next((m for m in jobs.methods if m.name == "get"), None)
        assert get_method is not None
        assert get_method.route is not None
        assert get_method.route.path == "/job/{jobDisplayId}"

    def test_method_has_return_annotation(self) -> None:
        registry = discover_endpoints_from_class()
        jobs = registry.get("jobs")
        get_method = next((m for m in jobs.methods if m.name == "get"), None)
        assert get_method is not None
        assert get_method.return_annotation == "Job"
