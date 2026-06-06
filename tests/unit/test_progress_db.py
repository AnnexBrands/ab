"""Tests for the SQLite sign-off / capture layer (feature 037, T042)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ab.progress import db


@pytest.fixture
def tmpdb(tmp_path: Path) -> Path:
    p = tmp_path / "t.db"
    db.init_db(p)
    return p


def test_signoff_upsert_and_get(tmpdb: Path) -> None:
    db.set_signoff("api.x.y", "example_ok", True, db_path=tmpdb)
    db.set_signoff("api.x.y", "tests_ok", True, note="looks good", db_path=tmpdb)
    so = db.get_signoffs(tmpdb)["api.x.y"]
    assert so["example_ok"] is True
    assert so["tests_ok"] is True
    assert so["sphinx_ok"] is False
    assert so["note"] == "looks good"


def test_signoff_rejects_unknown_field(tmpdb: Path) -> None:
    with pytest.raises(ValueError):
        db.set_signoff("api.x.y", "bogus_ok", True, db_path=tmpdb)


def test_signoff_export_import_roundtrip(tmp_path: Path) -> None:
    src = tmp_path / "src.db"
    dst = tmp_path / "dst.db"
    db.init_db(src)
    db.init_db(dst)
    db.set_signoff("api.a.b", "sphinx_ok", True, db_path=src)
    out = tmp_path / "signoffs.json"
    db.export_signoffs(out, db_path=src)
    assert out.is_file()
    n = db.import_signoffs(out, db_path=dst)
    assert n == 1
    assert db.get_signoffs(dst)["api.a.b"]["sphinx_ok"] is True


def test_capture_add_list_count(tmpdb: Path) -> None:
    cid = db.add_capture(
        "api.x.y", http_method="GET", status_code=200, response={"ok": True}, db_path=tmpdb
    )
    assert cid >= 1
    caps = db.list_captures("api.x.y", db_path=tmpdb)
    assert len(caps) == 1
    assert caps[0]["response"] == {"ok": True}
    assert caps[0]["status_code"] == 200
    assert db.capture_counts(tmpdb)["api.x.y"] == 1
