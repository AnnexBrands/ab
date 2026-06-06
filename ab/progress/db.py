"""SQLite persistence for the interactive capture/sign-off app (feature 037).

Stores two things the static report cannot:
- **captures**: real HTTP request/response logged per endpoint (the operator's
  paste, or a logged live call), so example I/O is retained and reviewable.
- **sign-offs**: per-endpoint human acceptance of example / tests / Sphinx.

stdlib ``sqlite3`` only (no new deps). A fresh connection is opened per call so the
ThreadingHTTPServer handler threads never share a connection. The DB lives at
``progress.db`` (gitignored); sign-offs can be exported to a committed JSON
(``tests/example_signoffs.json``) so they survive across machines.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = REPO_ROOT / "progress.db"
SIGNOFFS_JSON = REPO_ROOT / "tests" / "example_signoffs.json"

_SIGNOFF_FIELDS = ("example_ok", "tests_ok", "sphinx_ok")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path or DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path | None = None) -> None:
    """Create tables if absent."""
    with connect(db_path) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS signoff (
                endpoint_key TEXT PRIMARY KEY,
                example_ok   INTEGER NOT NULL DEFAULT 0,
                tests_ok     INTEGER NOT NULL DEFAULT 0,
                sphinx_ok    INTEGER NOT NULL DEFAULT 0,
                note         TEXT,
                updated_at   TEXT
            );
            CREATE TABLE IF NOT EXISTS capture (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint_key  TEXT NOT NULL,
                http_method   TEXT,
                url           TEXT,
                status_code   INTEGER,
                request_json  TEXT,
                response_json TEXT,
                source        TEXT NOT NULL DEFAULT 'manual',
                created_at    TEXT
            );
            CREATE INDEX IF NOT EXISTS ix_capture_endpoint ON capture(endpoint_key);
            """
        )
        # Migrate older DBs that predate the `source` column.
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(capture)").fetchall()}
        if "source" not in cols:
            conn.execute("ALTER TABLE capture ADD COLUMN source TEXT NOT NULL DEFAULT 'manual'")


# ---- sign-offs -------------------------------------------------------------


def get_signoffs(db_path: Path | None = None) -> dict[str, dict]:
    """Return ``{endpoint_key: {example_ok, tests_ok, sphinx_ok, note, updated_at}}``."""
    with connect(db_path) as conn:
        rows = conn.execute("SELECT * FROM signoff").fetchall()
    out: dict[str, dict] = {}
    for r in rows:
        out[r["endpoint_key"]] = {
            "example_ok": bool(r["example_ok"]),
            "tests_ok": bool(r["tests_ok"]),
            "sphinx_ok": bool(r["sphinx_ok"]),
            "note": r["note"],
            "updated_at": r["updated_at"],
        }
    return out


def set_signoff(
    endpoint_key: str,
    field: str,
    value: bool,
    note: str | None = None,
    db_path: Path | None = None,
) -> dict:
    """Set one sign-off flag (and optional note) for an endpoint; returns the row."""
    if field not in _SIGNOFF_FIELDS:
        raise ValueError(f"unknown sign-off field {field!r}; expected one of {_SIGNOFF_FIELDS}")
    with connect(db_path) as conn:
        conn.execute(
            "INSERT INTO signoff(endpoint_key, example_ok, tests_ok, sphinx_ok, note, updated_at) "
            "VALUES(?,0,0,0,NULL,?) ON CONFLICT(endpoint_key) DO NOTHING",
            (endpoint_key, _now()),
        )
        conn.execute(
            f"UPDATE signoff SET {field}=?, updated_at=? WHERE endpoint_key=?",
            (1 if value else 0, _now(), endpoint_key),
        )
        if note is not None:
            conn.execute(
                "UPDATE signoff SET note=?, updated_at=? WHERE endpoint_key=?",
                (note, _now(), endpoint_key),
            )
        row = conn.execute("SELECT * FROM signoff WHERE endpoint_key=?", (endpoint_key,)).fetchone()
    return dict(row)


def export_signoffs(path: Path | None = None, db_path: Path | None = None) -> Path:
    """Export sign-offs to committed JSON so they survive across machines."""
    path = path or SIGNOFFS_JSON
    data = {"schema": 1, "signoffs": {k: v for k, v in sorted(get_signoffs(db_path).items())}}
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def import_signoffs(path: Path | None = None, db_path: Path | None = None) -> int:
    """Load sign-offs from committed JSON into the DB (idempotent). Returns count."""
    path = path or SIGNOFFS_JSON
    if not path.is_file():
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    for key, v in data.get("signoffs", {}).items():
        for f in _SIGNOFF_FIELDS:
            set_signoff(key, f, bool(v.get(f)), db_path=db_path)
        if v.get("note"):
            set_signoff(key, "example_ok", bool(v.get("example_ok")), note=v["note"], db_path=db_path)
        n += 1
    return n


# ---- captures --------------------------------------------------------------


def add_capture(
    endpoint_key: str,
    *,
    http_method: str | None = None,
    url: str | None = None,
    status_code: int | None = None,
    request: object = None,
    response: object = None,
    source: str = "manual",
    db_path: Path | None = None,
) -> int:
    """Log one HTTP request/response for an endpoint; returns the row id."""
    req = json.dumps(request, ensure_ascii=False) if request is not None else None
    resp = json.dumps(response, ensure_ascii=False) if response is not None else None
    with connect(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO capture(endpoint_key, http_method, url, status_code, request_json, "
            "response_json, source, created_at) VALUES(?,?,?,?,?,?,?,?)",
            (endpoint_key, http_method, url, status_code, req, resp, source, _now()),
        )
        return int(cur.lastrowid)


def set_run_capture(
    endpoint_key: str,
    response: object,
    *,
    http_method: str | None = None,
    fixture: str | None = None,
    matched: bool | None = None,
    db_path: Path | None = None,
) -> int:
    """Record the latest harness-run output for an endpoint (one per endpoint).

    Replaces any prior ``source='run'`` row so the app shows the most recent run's
    JSON response. ``url`` carries a human marker (fixture + match/diff).
    """
    marker = "example-run"
    if fixture:
        marker += f": {fixture}"
    if matched is not None:
        marker += "  (match)" if matched else "  (DIFF vs fixture)"
    with connect(db_path) as conn:
        conn.execute(
            "DELETE FROM capture WHERE endpoint_key=? AND source='run'", (endpoint_key,)
        )
    return add_capture(
        endpoint_key,
        http_method=http_method,
        url=marker,
        response=response,
        source="run",
        db_path=db_path,
    )


def list_captures(endpoint_key: str, db_path: Path | None = None) -> list[dict]:
    """Return all captures for an endpoint, newest first."""
    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM capture WHERE endpoint_key=? ORDER BY id DESC", (endpoint_key,)
        ).fetchall()
    out = []
    for r in rows:
        out.append(
            {
                "id": r["id"],
                "http_method": r["http_method"],
                "url": r["url"],
                "status_code": r["status_code"],
                "request": json.loads(r["request_json"]) if r["request_json"] else None,
                "response": json.loads(r["response_json"]) if r["response_json"] else None,
                "source": r["source"] if "source" in r.keys() else "manual",
                "created_at": r["created_at"],
            }
        )
    return out


def capture_counts(db_path: Path | None = None) -> dict[str, int]:
    """Return ``{endpoint_key: capture_count}``."""
    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT endpoint_key, COUNT(*) AS n FROM capture GROUP BY endpoint_key"
        ).fetchall()
    return {r["endpoint_key"]: r["n"] for r in rows}
