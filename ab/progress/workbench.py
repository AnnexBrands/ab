"""Per-endpoint workbench data for the interactive app (feature 037).

Powers the request/response example page:
- **request**: the real Python ``import`` + ``api.<group>.<method>(...)`` call, read
  live from the canonical example file (so improving the file shows up here), plus the
  request-body fixture;
- **response**: the swagger-documented response codes and the latest saved fixture JSON.

Read-only against the codebase. Heavy (reads file source + fixtures), so the app loads
it lazily per selected endpoint rather than for the whole list.
"""

from __future__ import annotations

import ast
import inspect
import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
REQUESTS_DIR = FIXTURES_DIR / "requests"
SCHEMAS_DIR = REPO_ROOT / "ab" / "api" / "schemas"


def _normalize(path: str) -> str:
    return re.sub(r"\{[^}]+\}", "{_}", path)


def _swagger_responses_map() -> dict[tuple[str, str], dict[str, str]]:
    """``{(normalized_path, METHOD): {code: description}}`` from the swagger specs."""
    out: dict[tuple[str, str], dict[str, str]] = {}
    for name in ("acportal", "catalog", "abc"):
        spec_path = SCHEMAS_DIR / f"{name}.json"
        if not spec_path.is_file():
            continue
        try:
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for raw_path, methods in spec.get("paths", {}).items():
            stripped = raw_path[4:] if raw_path.startswith("/api/") else raw_path
            for http_method, op in methods.items():
                if not isinstance(op, dict) or "responses" not in op:
                    continue
                codes = {
                    str(code): (resp.get("description") or "") if isinstance(resp, dict) else ""
                    for code, resp in op["responses"].items()
                }
                out[(_normalize(stripped), http_method.upper())] = codes
    return out


_RESP_MAP: dict[tuple[str, str], dict[str, str]] | None = None


def response_codes(path: str, method: str) -> dict[str, str]:
    """Documented response codes for a route (``{code: description}``)."""
    global _RESP_MAP
    if _RESP_MAP is None:
        _RESP_MAP = _swagger_responses_map()
    return _RESP_MAP.get((_normalize(path), method.upper()), {})


def _attr_chain(node: ast.Attribute) -> list[str]:
    parts: list[str] = []
    cur: ast.expr = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if isinstance(cur, ast.Name):
        parts.append(cur.id)
        parts.reverse()
        return parts
    return []


def _extract_call_source(example_path: Path, group: str, method: str) -> str | None:
    """Return the exact source of the first ``api.<group>.<method>(...)`` call, or None."""
    try:
        source = example_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (OSError, SyntaxError):
        return None
    target = f"api.{group}.{method}"
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            chain = _attr_chain(node.func)
            if chain and ".".join(chain) == target:
                seg = ast.get_source_segment(source, node)
                if seg:
                    return seg
    return None


def _snippet(group: str, method: str, example_rel: str | None, route) -> str:
    """Build a *runnable* Python request snippet (real call if available).

    Includes ``from examples.constants import …`` for any ``TEST_*`` the call uses, so
    the snippet can be pasted-and-run as-is (the missing-import bug from UAT).
    """
    call = None
    if example_rel:
        call = _extract_call_source(REPO_ROOT / example_rel, group, method)
    if call is None:
        # Fall back to a generated call from the method signature.
        from ab.progress.example_gen import call_expr_for

        try:
            from ab.cli.discovery import discover_endpoints_from_class

            info = discover_endpoints_from_class().get(group)
            params = []
            if info:
                for m in info.methods:
                    if m.name == method:
                        params = [p.name for p in m.positional_params]
            call, _consts = call_expr_for(group, method, params)
        except Exception:
            call = f"api.{group}.{method}(...)"

    consts = sorted(set(re.findall(r"\bTEST_[A-Z0-9_]+\b", call)))
    lines = ["from ab import ABConnectAPI"]
    if consts:
        lines.append("from examples.constants import " + ", ".join(consts))
    lines += ["", 'api = ABConnectAPI(env="staging")', f"result = {call}", "print(result)"]
    return "\n".join(lines)


def pydantic_repr(model_name: str | None, data: object) -> str | None:
    """Render *data* as the typed pydantic model (for the response 'Pydantic' view)."""
    if not model_name or data is None:
        return None
    import ab.api.models as models_pkg

    cls = getattr(models_pkg, model_name, None)
    if cls is None:
        return None
    try:
        if isinstance(data, list):
            return "[\n  " + ",\n  ".join(repr(cls.model_validate(x)) for x in data) + "\n]"
        return repr(cls.model_validate(data))
    except Exception as exc:  # validation error → surface it (the model disagrees)
        return f"# could not cast to {model_name}: {type(exc).__name__}: {str(exc).splitlines()[0]}"


def _read_json(path: Path) -> object | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _impl_source(info, method: str) -> str | None:
    """Source of the endpoint method implementation (for the Implementation popover)."""
    func = getattr(info.endpoint_class, method, None)
    if func is None:
        return None
    try:
        src = inspect.getsource(func)
    except (OSError, TypeError):
        return None
    src = textwrap.dedent(src)
    return src if len(src) <= 6000 else src[:6000] + "\n# … (truncated)"


def _doc_links(group: str, method: str) -> tuple[str, str | None]:
    """(RTD url, local docs path or None) for the Sphinx popover."""
    from ab.api.rtd import endpoint_doc_url, endpoint_page_slug, endpoint_top_group

    url = endpoint_doc_url(group, method)
    top = endpoint_top_group(group)
    slug = endpoint_page_slug(group, method)
    doc_rel = f"docs/api/{top}/{slug}.md"
    return url, (doc_rel if (REPO_ROOT / doc_rel).is_file() else None)


def endpoint_detail(endpoint_key: str) -> dict | None:
    """Full workbench detail for one endpoint, or None if it is not a routed endpoint."""
    from ab.cli.discovery import discover_endpoints_from_class
    from ab.progress.example_gen import strip_list_wrapper
    from ab.progress.example_index import build_example_index

    group, method = endpoint_key[len("api.") :].rsplit(".", 1)
    info = discover_endpoints_from_class().get(group)
    if not info:
        return None
    route = None
    for m in info.methods:
        if m.name == method and m.route is not None:
            route = m.route
            break
    if route is None:
        return None

    index = build_example_index()
    ex = index.get(endpoint_key)
    example_rel = ex.example_path if ex else None
    doc_url, doc_rel = _doc_links(group, method)

    response_model = strip_list_wrapper(route.response_model or "")
    request_model = route.request_model

    from ab.progress import db

    edit = db.get_edit(endpoint_key)

    return {
        "endpoint_key": endpoint_key,
        "http_method": route.method,
        "path": route.path,
        "response_model": response_model,
        "request_model": request_model,
        "example_path": example_rel,
        "snippet": _snippet(group, method, example_rel, route),
        "impl_source": _impl_source(info, method),
        "doc_url": doc_url,
        "doc_path": doc_rel,
        "response_codes": response_codes(route.path, route.method),
        "request_fixture": _read_json(REQUESTS_DIR / f"{strip_list_wrapper(request_model)}.json")
        if request_model
        else None,
        "response_fixture": _read_json(FIXTURES_DIR / f"{response_model}.json")
        if response_model
        else None,
        "response_pydantic": pydantic_repr(
            response_model, _read_json(FIXTURES_DIR / f"{response_model}.json")
        )
        if response_model
        else None,
        "edit": edit,
    }


def run_code(endpoint_key: str, code: str, *, confirm_mutation: bool = False) -> dict:
    """Execute operator-edited request code against staging and capture the response.

    Runs *code* (the LHS workbench snippet — must assign its call to ``result``) in a
    subprocess with the repo on PYTHONPATH and ``AB_EXAMPLE_CAPTURE_DIR`` set, then reads
    the captured response. GET runs freely; mutations require ``confirm_mutation``.
    """
    from ab.progress import db
    from ab.progress.example_verify import compare

    detail = endpoint_detail(endpoint_key)
    if detail is None:
        return {"ok": False, "error": "not a routed endpoint"}
    http_method = detail["http_method"].upper()
    if http_method != "GET" and not confirm_mutation:
        return {"ok": False, "needs_confirm": True,
                "error": f"{http_method} mutates staging — tick confirm to run"}

    model = detail["response_model"]
    fixture_name = f"{model}.json" if model else None
    epilogue = (
        "\n\ntry:\n"
        "    from examples._capture import save as _ab_save\n"
        '    _ab_save("__run__.json", result)\n'
        "except NameError:\n"
        '    print("RUN_NO_RESULT: assign your call to `result` to capture the response")\n'
    )
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    with tempfile.TemporaryDirectory() as tmp:
        env["AB_EXAMPLE_CAPTURE_DIR"] = tmp
        if confirm_mutation:
            env["AB_RUN_MUTATIONS"] = "1"
        script = Path(tmp) / "_run_snippet.py"
        script.write_text(code + epilogue, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(script)], cwd=str(REPO_ROOT), env=env,
            capture_output=True, text=True, timeout=180,
        )
        produced = _read_json(Path(tmp) / "__run__.json") if fixture_name else None

    out = (proc.stdout + proc.stderr).strip()
    result = {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": out[-4000:],
        "response": produced,
        "fixture": fixture_name,
    }
    if produced is not None:
        result["response_pydantic"] = pydantic_repr(model, produced)
        committed = _read_json(FIXTURES_DIR / fixture_name) if fixture_name else None
        if committed is not None:
            matched, diff = compare(produced, committed)
            result["matched"] = matched
            result["diff"] = diff
        db.init_db()
        db.set_run_capture(endpoint_key, produced, fixture=fixture_name, matched=result.get("matched"))
    return result


def run_example_for(endpoint_key: str, *, confirm_mutation: bool = False) -> dict:
    """Run the endpoint's canonical example live and return its produced response.

    Reuses the harness path: runs the example MODULE in a subprocess with
    AB_EXAMPLE_CAPTURE_DIR pointed at a temp dir, then reads the produced
    ``<Model>.json``. GET runs freely; mutating endpoints require
    ``confirm_mutation`` (which sets AB_RUN_MUTATIONS for the subprocess).
    """
    from ab.progress import db
    from ab.progress.example_index import build_example_index
    from ab.progress.example_verify import compare

    detail = endpoint_detail(endpoint_key)
    if detail is None:
        return {"ok": False, "error": "not a routed endpoint"}

    ex = build_example_index().get(endpoint_key)
    if not ex or not ex.is_canonical or not ex.example_path:
        return {"ok": False, "error": "no canonical example to run"}

    http_method = detail["http_method"].upper()
    if http_method != "GET" and not confirm_mutation:
        return {"ok": False, "needs_confirm": True,
                "error": f"{http_method} mutates staging — confirm to run"}

    module = ex.example_path[:-3].replace("/", ".")
    model = detail["response_model"]
    fixture_name = f"{model}.json" if model else None

    env = dict(os.environ)
    with tempfile.TemporaryDirectory() as tmp:
        env["AB_EXAMPLE_CAPTURE_DIR"] = tmp
        if confirm_mutation:
            env["AB_RUN_MUTATIONS"] = "1"
        proc = subprocess.run(
            [sys.executable, "-m", module],
            cwd=str(REPO_ROOT), env=env, capture_output=True, text=True, timeout=180,
        )
        produced = None
        if fixture_name:
            produced = _read_json(Path(tmp) / fixture_name)

    out = (proc.stdout + proc.stderr).strip()
    result = {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "module": module,
        "stdout": out[-4000:],
        "response": produced,
        "fixture": fixture_name,
    }
    if produced is not None:
        committed = _read_json(FIXTURES_DIR / fixture_name) if fixture_name else None
        if committed is not None:
            matched, detail_diff = compare(produced, committed)
            result["matched"] = matched
            result["diff"] = detail_diff
        db.init_db()
        db.set_run_capture(endpoint_key, produced, fixture=fixture_name,
                           matched=result.get("matched"))
    return result
