"""Unit tests for ``ab.cli.formatter.format_result``.

Locks in the pretty-vs-JSON behaviour:

* Models that implement ``cli_format()`` get rendered through it by default.
* Lists of such models are joined with newlines.
* ``as_json=True`` always emits ``json.dumps`` output, even when
  ``cli_format`` is defined.
* Models without ``cli_format`` (and non-model values) fall back to JSON.
"""

from __future__ import annotations

import json

from pydantic import Field

from ab.api.models.base import ResponseModel
from ab.api.models.dashboard import DashboardSummary, GridViewInfo
from ab.cli.formatter import format_result


class _PlainModel(ResponseModel):
    """A response model with no ``cli_format`` defined."""

    name: str | None = Field(None)


# ---------------------------------------------------------------------------
# Pretty path
# ---------------------------------------------------------------------------


def test_dashboard_summary_pretty_uses_cli_format():
    s = DashboardSummary(
        inboundCount=3,
        outboundCount=7,
        inHouseCount=2,
        localDeliveriesCount=1,
        recentEstimatesCount=4,
    )
    out = format_result(s)
    assert out == s.cli_format()
    assert "inbound=3" in out and "outbound=7" in out


def test_grid_view_info_list_joins_with_newlines():
    views = [
        GridViewInfo(id=1, name="Inbound", dataKey="inbound", isActive=True),
        GridViewInfo(id=2, name="Archived", dataKey="archived", isActive=False),
    ]
    out = format_result(views)
    assert out == "\n".join(v.cli_format() for v in views)
    assert "id=1" in out and "id=2" in out
    # No JSON braces in pretty output.
    assert "{" not in out


# ---------------------------------------------------------------------------
# JSON path
# ---------------------------------------------------------------------------


def test_as_json_overrides_cli_format_for_model():
    s = DashboardSummary(inboundCount=3, outboundCount=7)
    out = format_result(s, as_json=True)
    data = json.loads(out)
    assert data["inboundCount"] == 3
    assert data["outboundCount"] == 7


def test_as_json_overrides_cli_format_for_list():
    views = [GridViewInfo(id=1, name="Inbound", dataKey="inbound", isActive=True)]
    out = format_result(views, as_json=True)
    data = json.loads(out)
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["dataKey"] == "inbound"
    assert data[0]["isActive"] is True


# ---------------------------------------------------------------------------
# Fallback path (no cli_format defined)
# ---------------------------------------------------------------------------


def test_model_without_cli_format_falls_back_to_json():
    out = format_result(_PlainModel(name="x"))
    assert json.loads(out) == {"name": "x"}


def test_list_with_mixed_pretty_capability_falls_back_to_json():
    views = [
        GridViewInfo(id=1, name="Inbound", dataKey="inbound", isActive=True),
        _PlainModel(name="other"),
    ]
    out = format_result(views)
    data = json.loads(out)
    assert isinstance(data, list)
    assert data[1] == {"name": "other"}


# ---------------------------------------------------------------------------
# Primitive / None / bytes
# ---------------------------------------------------------------------------


def test_none_renders_as_null():
    assert format_result(None) == "null"


def test_bytes_renders_size():
    assert format_result(b"abcde") == "<binary response, 5 bytes>"


def test_primitive_passes_through_str():
    assert format_result(42) == "42"


def test_empty_list_falls_back_to_json():
    # No items means the "all items implement cli_format" check is False;
    # the empty list goes through the JSON path.
    assert format_result([]) == "[]"


# ---------------------------------------------------------------------------
# Direct model.cli_format() contracts
# ---------------------------------------------------------------------------


class TestGridViewInfoCliFormat:
    def test_includes_required_fields(self):
        v = GridViewInfo(id=1, name="Inbound", dataKey="inbound", isActive=True)
        s = v.cli_format()
        assert "id=1" in s
        assert "'Inbound'" in s
        assert "'inbound'" in s
        assert "active=True" in s

    def test_handles_missing_id(self):
        v = GridViewInfo(name="x")
        assert "id=—" in v.cli_format()


class TestDashboardSummaryCliFormat:
    def test_all_counts_present(self):
        s = DashboardSummary(
            inboundCount=3, outboundCount=7, inHouseCount=2,
            localDeliveriesCount=1, recentEstimatesCount=4,
        )
        out = s.cli_format()
        for k in ("inbound=", "outbound=", "in_house=", "local_deliveries=", "recent_estimates=", "rows="):
            assert k in out

    def test_rows_counts_data_length(self):
        from ab.api.models.dashboard import DashboardItem

        s = DashboardSummary(inboundCount=0, data=[DashboardItem(location="A"), DashboardItem(location="B")])
        assert "rows=2" in s.cli_format()

    def test_rows_are_emitted_one_per_line(self):
        from ab.api.models.dashboard import DashboardItem

        rows = [
            DashboardItem(location="A", jobDisplayID=100, customer="Acme", step=2, carrier="UPS"),
            DashboardItem(location="B", jobDisplayID=200, customer="Beta", step=3, carrier="FedEx"),
        ]
        out = DashboardSummary(inboundCount=0, data=rows).cli_format()
        lines = out.splitlines()
        # Header + one line per row.
        assert len(lines) == 1 + len(rows)
        assert "job=100" in lines[1]
        assert "Acme" in lines[1]
        assert "UPS" in lines[1]
        assert "job=200" in lines[2]
        assert "FedEx" in lines[2]

    def test_no_rows_returns_header_only(self):
        out = DashboardSummary(inboundCount=0, data=[]).cli_format()
        assert "\n" not in out
        assert "rows=0" in out


class TestDashboardItemCliFormat:
    def test_includes_salient_fields(self):
        from ab.api.models.dashboard import DashboardItem

        item = DashboardItem(
            location="LAX",
            jobDisplayID=12345,
            customer="Acme Corporation",
            step=4,
            next="PK",
            carrier="UPS",
        )
        out = item.cli_format()
        assert "job=12345" in out
        assert "loc=LAX" in out
        assert "Acme" in out
        assert "step=4" in out
        assert "next=PK" in out
        assert "carrier=UPS" in out

    def test_handles_missing_fields(self):
        from ab.api.models.dashboard import DashboardItem

        out = DashboardItem().cli_format()
        assert "job=—" in out
        assert "loc=—" in out
        assert "ship_by=—" in out

    def test_truncates_long_customer(self):
        from ab.api.models.dashboard import DashboardItem

        long_name = "X" * 50
        out = DashboardItem(customer=long_name).cli_format()
        # 30-char cap from cli_format
        assert "X" * 30 in out
        assert "X" * 31 not in out
