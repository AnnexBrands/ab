"""Integration tests for CLI help and listing output."""

from __future__ import annotations

import io
import json
import sys
from unittest.mock import MagicMock, patch

import pytest

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


# ---------------------------------------------------------------------------
# --json flag round-trip
# ---------------------------------------------------------------------------


def _run_cli(argv: list[str], result: object, capsys) -> str:
    """Drive ``ab.cli.__main__.main`` with a mocked endpoint return value."""
    from ab.cli.__main__ import main

    api = MagicMock()
    api.dashboard.get.return_value = result

    with patch("ab.cli.__main__._create_api", return_value=api):
        with patch.object(sys, "argv", ["ab", *argv]):
            main()
    return capsys.readouterr().out


class TestJsonFlag:
    """The ``--json`` flag forces JSON output; default uses ``cli_format``."""

    def test_default_uses_cli_format(self, capsys):
        from ab.api.models.dashboard import DashboardSummary

        summary = DashboardSummary(inboundCount=3, outboundCount=7, inHouseCount=2)
        out = _run_cli(["dashboard", "get"], summary, capsys)
        assert "inbound=3" in out
        # No JSON formatting in the default path.
        assert "{" not in out

    def test_json_flag_emits_json(self, capsys):
        from ab.api.models.dashboard import DashboardSummary

        summary = DashboardSummary(inboundCount=3, outboundCount=7)
        out = _run_cli(["dashboard", "get", "--json"], summary, capsys)
        data = json.loads(out)
        assert data["inboundCount"] == 3
        assert data["outboundCount"] == 7

    def test_json_flag_position_independent(self, capsys):
        from ab.api.models.dashboard import DashboardSummary

        summary = DashboardSummary(inboundCount=1)
        # Place --json before the module name.
        out = _run_cli(["--json", "dashboard", "get"], summary, capsys)
        assert json.loads(out)["inboundCount"] == 1


# ---------------------------------------------------------------------------
# Help token recognition (?, -h, help, --help)
# ---------------------------------------------------------------------------


class TestHelpTokens:
    """All four help tokens drive the same help screen and skip the API call."""

    def _run_and_capture(self, argv, capsys):
        from ab.cli.__main__ import main

        with patch("ab.cli.__main__._create_api") as mock_create:
            with patch.object(sys, "argv", ["ab", *argv]):
                with pytest.raises(SystemExit) as exc:
                    main()
        # Help paths must exit 0 and must never construct the API client.
        assert exc.value.code == 0
        mock_create.assert_not_called()
        captured = capsys.readouterr()
        # Method-level help is written to stderr; module/top-level listing to stderr too.
        return captured.out + captured.err

    @pytest.mark.parametrize("token", ["?", "-h", "help", "--help"])
    def test_method_help_for_dashboard_get(self, token, capsys):
        output = self._run_and_capture(["dashboard", "get", token], capsys)
        # Help shows the Route line + the CLI invocation pattern + arg names.
        assert "GET /dashboard" in output
        assert "ab dashboard get" in output
        assert "view-id" in output or "view_id" in output
        assert "company-id" in output or "company_id" in output

    @pytest.mark.parametrize("token", ["?", "-h", "help", "--help"])
    def test_module_help_lists_methods(self, token, capsys):
        output = self._run_and_capture(["dashboard", token], capsys)
        assert "dashboard" in output
        # The known dashboard methods should appear in the listing.
        for m in ("get", "get_grid_views", "inbound", "outbound"):
            assert m in output

    @pytest.mark.parametrize("token", ["?", "-h", "help", "--help"])
    def test_top_level_help_lists_endpoints(self, token, capsys):
        output = self._run_and_capture([token], capsys)
        assert "dashboard" in output
        assert "Endpoint" in output
