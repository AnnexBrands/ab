"""Interactive capture / harmony / sign-off app (feature 037).

A small stdlib ``http.server`` app (no new deps) that complements the static
``html/progress.html`` report. It serves a single-page UI with:

- a **left nav** to drill into endpoints by **tag** (swagger) or **path**,
- per-endpoint **Four-Way Harmony** (impl / example / fixture+test / Sphinx) with
  real test coverage,
- **HTTP request/response capture** logged to SQLite (``ab.progress.db``),
- interactive **sign-off** that the example / tests / Sphinx are acceptable.

Launch via ``python scripts/serve_progress.py`` then open the printed URL.
Read-only against the codebase; all mutable state lives in ``progress.db``.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from ab.progress import db
from ab.progress.harmony import build_harmony, harmony_summary


def _build_payload() -> dict:
    """Endpoints (harmony + sign-off + capture counts) + summary for the UI."""
    rows = build_harmony()
    signoffs = db.get_signoffs()
    counts = db.capture_counts()
    endpoints = []
    for r in rows:
        d = r.to_dict()
        so = signoffs.get(r.endpoint_key, {})
        d["example_ok"] = bool(so.get("example_ok"))
        d["tests_ok"] = bool(so.get("tests_ok"))
        d["sphinx_ok"] = bool(so.get("sphinx_ok"))
        d["signoff_note"] = so.get("note")
        d["capture_count"] = counts.get(r.endpoint_key, 0)
        endpoints.append(d)
    summary = harmony_summary(rows)
    summary["signed_off"] = sum(
        1 for e in endpoints if e["example_ok"] and e["tests_ok"] and e["sphinx_ok"]
    )
    return {"summary": summary, "endpoints": endpoints}


class _Handler(BaseHTTPRequestHandler):
    server_version = "ABProgress/037"

    # -- helpers ------------------------------------------------------------
    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj: object, status: int = 200) -> None:
        self._send(status, json.dumps(obj).encode("utf-8"), "application/json; charset=utf-8")

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return {}

    def log_message(self, *args) -> None:  # quiet
        pass

    # -- routes -------------------------------------------------------------
    def do_GET(self) -> None:  # noqa: N802
        route = urlparse(self.path)
        if route.path in ("/", "/index.html"):
            self._send(200, UI_HTML.encode("utf-8"), "text/html; charset=utf-8")
        elif route.path == "/api/data":
            self._json(_build_payload())
        elif route.path == "/api/captures":
            q = parse_qs(route.query)
            key = (q.get("endpoint") or [""])[0]
            self._json({"captures": db.list_captures(key) if key else []})
        elif route.path == "/api/endpoint":
            from ab.progress.workbench import endpoint_detail

            q = parse_qs(route.query)
            key = (q.get("key") or [""])[0]
            detail = endpoint_detail(key) if key else None
            if detail is None:
                return self._json({"error": "unknown endpoint"}, 404)
            self._json(detail)
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self) -> None:  # noqa: N802
        route = urlparse(self.path)
        body = self._read_body()
        if route.path == "/api/signoff":
            key, field = body.get("endpoint"), body.get("field")
            if not key or field not in ("example_ok", "tests_ok", "sphinx_ok"):
                return self._json({"error": "endpoint and valid field required"}, 400)
            row = db.set_signoff(key, field, bool(body.get("value")), body.get("note"))
            return self._json({"ok": True, "signoff": row})
        if route.path == "/api/capture":
            key = body.get("endpoint")
            if not key:
                return self._json({"error": "endpoint required"}, 400)
            cid = db.add_capture(
                key,
                http_method=body.get("http_method"),
                url=body.get("url"),
                status_code=body.get("status_code"),
                request=body.get("request"),
                response=body.get("response"),
            )
            return self._json({"ok": True, "id": cid, "captures": db.list_captures(key)})
        if route.path == "/api/export":
            path = db.export_signoffs()
            return self._json({"ok": True, "path": str(path)})
        if route.path == "/api/edit":
            key = body.get("endpoint")
            if not key:
                return self._json({"error": "endpoint required"}, 400)
            fields = {k: body[k] for k in ("code", "request_json", "response_json", "response_code", "note") if k in body}
            try:
                row = db.set_edit(key, **fields)
            except ValueError as exc:
                return self._json({"error": str(exc)}, 400)
            db.export_edits()  # keep the committed improvement store fresh for enrichment
            return self._json({"ok": True, "edit": row})
        if route.path == "/api/run":
            from ab.progress.workbench import run_example_for

            key = body.get("endpoint")
            if not key:
                return self._json({"error": "endpoint required"}, 400)
            result = run_example_for(key, confirm_mutation=bool(body.get("confirm")))
            return self._json(result)
        if route.path == "/api/save-fixture":
            from ab.progress.captures import validate_capture

            key = body.get("endpoint")
            if not key:
                return self._json({"error": "endpoint required"}, 400)
            vc = validate_capture(
                key,
                {
                    "endpoint": key,
                    "http_method": body.get("http_method", ""),
                    "path": body.get("path", ""),
                    "response_model": body.get("response_model", ""),
                    "response": body.get("response"),
                },
            )
            if not vc.ok:
                return self._json({"ok": False, "error": vc.error}, 400)
            from ab.progress.report import FIXTURES_DIR as _FX

            (_FX / vc.fixture_name).write_text(
                json.dumps(vc.response_json, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            return self._json({"ok": True, "fixture": vc.fixture_name})
        return self._json({"error": "not found"}, 404)


def _primary_ip() -> str:
    """Best-effort LAN/WSL IP for cross-host (e.g. Windows→WSL2) access."""
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.254", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def serve(host: str = "0.0.0.0", port: int = 8765, *, max_tries: int = 20) -> None:
    """Run the app (blocking). Initializes the DB and imports committed sign-offs.

    Binds ``0.0.0.0`` by default so it is reachable both via ``localhost`` and via the
    machine's IP — important under WSL2 NAT, where a 127.0.0.1-only bind is often not
    forwarded to the Windows browser. If *port* is already in use, advances to the next
    free port rather than crashing, and prints the URLs it actually bound.
    """
    import errno

    db.init_db()
    db.import_signoffs()

    httpd = None
    for candidate in range(port, port + max_tries):
        try:
            httpd = ThreadingHTTPServer((host, candidate), _Handler)
            port = candidate
            break
        except OSError as exc:
            if exc.errno == errno.EADDRINUSE:
                print(f"port {candidate} in use, trying {candidate + 1}…")
                continue
            raise
    if httpd is None:
        raise SystemExit(f"no free port in {port}..{port + max_tries - 1}")

    if host in ("0.0.0.0", "::"):
        print(f"ab progress app -> http://localhost:{port}  (or http://{_primary_ip()}:{port})  (Ctrl-C to stop)")
    else:
        print(f"ab progress app -> http://{host}:{port}  (Ctrl-C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopping")
    finally:
        httpd.server_close()


# ---------------------------------------------------------------------------
# Single-page UI (vanilla JS; no build step, no CDN).
# ---------------------------------------------------------------------------

UI_HTML = r"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ABConnect — Example Capture & Harmony</title>
<style>
:root{--bg:#0f1115;--panel:#171a21;--line:#2a2f3a;--fg:#e6e9ef;--mut:#9aa4b2;--acc:#4c8dff;
--ok:#28a745;--no:#dc3545;--warn:#ffc107;--paste:#fd7e14;}
*{box-sizing:border-box}body{margin:0;font:14px/1.45 system-ui,Segoe UI,Roboto,sans-serif;
background:var(--bg);color:var(--fg);display:flex;height:100vh;overflow:hidden}
#nav{width:340px;min-width:280px;border-right:1px solid var(--line);display:flex;flex-direction:column;background:var(--panel)}
#main{flex:1;overflow:auto;padding:20px 28px}
header.bar{padding:12px 14px;border-bottom:1px solid var(--line)}
h1{font-size:14px;margin:0 0 8px;letter-spacing:.3px}
.tabs{display:flex;gap:6px;margin-bottom:8px}
.tabs button{flex:1;padding:6px;border:1px solid var(--line);background:#1f2430;color:var(--fg);
border-radius:6px;cursor:pointer;font-size:12px}
.tabs button.on{background:var(--acc);border-color:var(--acc);color:#fff}
#search{width:100%;padding:7px 9px;border:1px solid var(--line);background:#10131a;color:var(--fg);border-radius:6px}
#tree{flex:1;overflow:auto;padding:6px 4px}
.grp{margin:2px 0}
.grp>summary{cursor:pointer;padding:5px 8px;color:var(--mut);font-weight:600;list-style:none}
.grp>summary::-webkit-details-marker{display:none}
.grp>summary:hover{color:var(--fg)}
.ep{padding:4px 10px 4px 20px;cursor:pointer;border-radius:5px;display:flex;gap:7px;align-items:center;font-size:12.5px}
.ep:hover{background:#222838}.ep.sel{background:#2a3550}
.dot{width:8px;height:8px;border-radius:50%;flex:none}
.m{font:600 10px/1 monospace;padding:2px 4px;border-radius:3px;background:#222838;color:var(--mut);min-width:38px;text-align:center}
.summary{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:18px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:12px 16px;min-width:96px}
.card .n{font-size:1.6rem;font-weight:700}.card .l{font-size:11px;color:var(--mut);text-transform:uppercase;letter-spacing:.5px}
.det{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px 20px;max-width:900px}
.det h2{margin:0 0 4px;font-size:18px;font-family:monospace}
.kv{color:var(--mut);font-size:12.5px;margin-bottom:14px}
.pill{display:inline-block;padding:2px 9px;border-radius:20px;font-size:11px;font-weight:600;margin-right:6px}
.harm{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0 18px}
.h{padding:8px 12px;border-radius:8px;border:1px solid var(--line);min-width:120px;background:#10131a}
.h .t{font-size:11px;color:var(--mut);text-transform:uppercase}.h .v{font-weight:700;margin-top:2px}
.h.ok{border-color:var(--ok)}.h.no{border-color:var(--no)}
.section{margin-top:18px;border-top:1px solid var(--line);padding-top:14px}
.section h3{font-size:13px;margin:0 0 10px;color:var(--mut);text-transform:uppercase;letter-spacing:.5px}
label.ck{display:flex;align-items:center;gap:9px;padding:7px 0;cursor:pointer}
label.ck input{width:17px;height:17px;accent-color:var(--ok)}
textarea{width:100%;background:#10131a;color:var(--fg);border:1px solid var(--line);border-radius:7px;
padding:8px;font:12px/1.4 monospace;min-height:90px;resize:vertical}
input.txt{background:#10131a;color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:7px 9px}
button.go{background:var(--acc);color:#fff;border:none;border-radius:7px;padding:8px 16px;cursor:pointer;font-weight:600}
button.go:hover{filter:brightness(1.1)}
.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:10px}
.cap{border:1px solid var(--line);border-radius:7px;padding:8px 10px;margin:8px 0;background:#10131a;font-size:12px}
.cap pre{margin:6px 0 0;max-height:200px;overflow:auto;background:#0b0d12;padding:8px;border-radius:5px}
.muted{color:var(--mut)}.empty{color:var(--mut);padding:40px;text-align:center}
small.note{color:var(--mut)}
/* harmony popover + workbench (feature 037) */
.harm .h[data-pop]{cursor:pointer}
.harm .h[data-pop]:hover{background:#1b2230}
.pop{position:fixed;z-index:50;width:430px;max-height:60vh;overflow:auto;background:var(--panel);
     border:1px solid var(--acc);border-radius:9px;box-shadow:0 8px 30px rgba(0,0,0,.5)}
.pop-h{padding:8px 12px;border-bottom:1px solid var(--line);font-weight:600;display:flex;justify-content:space-between}
.pop-x{cursor:pointer;color:var(--mut)}.pop-x:hover{color:var(--fg)}
.pop-b{padding:10px 12px}.pop-b pre{margin:0;background:#0b0d12;padding:8px;border-radius:6px;overflow:auto}
.pop-b a{color:var(--acc);word-break:break-all}
.wb{display:flex;gap:18px;margin-top:14px}
.wb-col{flex:1;min-width:0}
.wb-col h3{font-size:13px;margin:0 0 8px;color:var(--mut);text-transform:uppercase;letter-spacing:.5px}
textarea.code{min-height:150px;background:#0b0d12}
.codes{display:flex;gap:6px;flex-wrap:wrap;margin:4px 0}
.code-pill{background:#1f2430;border:1px solid var(--line);border-radius:5px;padding:2px 8px;font:600 12px monospace}
</style></head>
<body>
<div id="nav">
  <header class="bar">
    <h1>Example Capture &amp; Harmony</h1>
    <div class="muted" style="font-size:11px;margin-bottom:8px">path › tag › endpoint — click to expand</div>
    <input id="search" placeholder="filter endpoints…">
  </header>
  <div id="tree"></div>
</div>
<div id="main"><div class="empty">Loading…</div></div>
<script>
let DATA=null, SEL=null, FILTER='', OPEN=new Set(), SELE=null, DETAIL=null;
const $=s=>document.querySelector(s), ce=(t,c)=>{const e=document.createElement(t);if(c)e.className=c;return e;};
const RUN={passing:['#28a745','pass'],failing:['#dc3545','fail'],not_verified:['#6c757d','not run'],
awaiting_data:['#ffc107','needs data'],awaiting_paste:['#fd7e14','paste'],binary:['#6610f2','binary'],
missing_example:['#dc3545','no example']};
function api(p,opt){return fetch(p,opt).then(r=>r.json());}
async function load(){DATA=await api('/api/data');renderSummary();renderTree();if(SEL)renderDetail(find(SEL));}
function find(k){return DATA.endpoints.find(e=>e.endpoint_key===k);}
function renderSummary(){/* summary cards live atop detail when nothing selected */}
function epColor(e){return RUN[e.run_status]?RUN[e.run_status][0]:'#6c757d';}
function epMatch(e){return !FILTER||e.endpoint_key.toLowerCase().includes(FILTER)||e.path.toLowerCase().includes(FILTER);}
function doneCount(eps){return eps.filter(e=>e.example_ok&&e.tests_ok&&e.sphinx_ok).length;}
function hasSel(eps){return SEL&&eps.some(e=>e.endpoint_key===SEL);}
function buildTree(){
  // path-segment -> tag -> [endpoints]
  const segs={};
  for(const e of DATA.endpoints){
    if(!epMatch(e))continue;
    const seg='/'+(e.path.replace(/^\//,'').split('/')[0]||'');
    const tag=(e.tags&&e.tags.length?e.tags[0]:'(untagged)');
    ((segs[seg]=segs[seg]||{})[tag]=segs[seg][tag]||[]).push(e);
  }
  return segs;
}
function epRow(e){
  const row=ce('div','ep'+(SEL===e.endpoint_key?' sel':''));
  const dot=ce('span','dot');dot.style.background=epColor(e);
  const m=ce('span','m');m.textContent=e.http_method;
  const t=ce('span');t.textContent=e.endpoint_key.replace(/^api\./,'');
  row.append(dot,m,t);
  row.onclick=()=>{SEL=e.endpoint_key;renderDetail(e);renderTree();};
  return row;
}
function node(key,label,depth,forceOpen){
  const d=ce('details','grp');
  d.dataset.key=key;
  d.open = forceOpen || OPEN.has(key) || !!FILTER;
  d.addEventListener('toggle',()=>{ if(d.open)OPEN.add(key); else OPEN.delete(key); });
  const s=ce('summary');s.style.paddingLeft=(8+depth*14)+'px';s.textContent=label;d.appendChild(s);
  return d;
}
function renderTree(){
  const tree=$('#tree');tree.innerHTML='';
  const segs=buildTree();
  for(const seg of Object.keys(segs).sort()){
    const tags=segs[seg];
    const tagNames=Object.keys(tags).sort();
    const allEps=tagNames.map(t=>tags[t]).flat();
    const segKey='seg:'+seg;
    const d=node(segKey,`${seg}  (${doneCount(allEps)}/${allEps.length})`,0,hasSel(allEps));
    if(tagNames.length===1){
      // single tag for this path → collapse the redundant tag layer
      allEps.sort((a,b)=>a.endpoint_key.localeCompare(b.endpoint_key)).forEach(e=>d.appendChild(epRow(e)));
    } else {
      for(const tag of tagNames){
        const eps=tags[tag].sort((a,b)=>a.endpoint_key.localeCompare(b.endpoint_key));
        const td=node(segKey+'|'+tag,`${tag}  (${doneCount(eps)}/${eps.length})`,1,hasSel(eps));
        eps.forEach(e=>td.appendChild(epRow(e)));
        d.appendChild(td);
      }
    }
    tree.appendChild(d);
  }
}
function hpill(label,ok,key,extra){
  return `<div class="h ${ok?'ok':'no'}" data-pop="${key}"><div class="t">${label}</div>
    <div class="v">${ok?'✓':'✗'}${extra?' '+extra:''} ▾</div></div>`;}
function renderDetail(e){
  if(!e){$('#main').innerHTML='<div class="empty">Select an endpoint.</div>';return;}
  SELE=e; DETAIL=null;
  const [rc,rl]=RUN[e.run_status]||['#6c757d',e.run_status];
  const cov=e.coverage_pct!=null?Math.round(e.coverage_pct)+'%':'—';
  $('#main').innerHTML=`
  <div class="det">
    <h2><span style="color:${rc}">${e.http_method}</span> ${escapeHtml(e.path)}</h2>
    <div class="kv">${e.endpoint_key} · ${e.api_surface} · tags: ${(e.tags||[]).join(', ')||'—'}
      · <span class="pill" style="background:${rc};color:#fff">${rl}</span></div>
    <div class="harm">
      ${hpill('Implementation',e.has_impl,'impl')}
      ${hpill('Example',e.has_example,'example')}
      ${hpill('Fixture',e.has_fixture,'fixture')}
      ${hpill('Test',e.has_test,'test',cov)}
      ${hpill('Sphinx',e.has_sphinx,'sphinx')}
      <div class="h"><div class="t">Harmony</div><div class="v">${e.harmony_score}/4</div></div>
    </div>
    <div class="section"><h3>Interactive sign-off</h3>
      <label class="ck"><input type="checkbox" data-f="example_ok" ${e.example_ok?'checked':''}> Example is acceptable</label>
      <label class="ck"><input type="checkbox" data-f="tests_ok" ${e.tests_ok?'checked':''}> Tests are acceptable</label>
      <label class="ck"><input type="checkbox" data-f="sphinx_ok" ${e.sphinx_ok?'checked':''}> Sphinx is acceptable</label>
    </div>
    <div id="wb" class="muted" style="margin-top:14px">loading workbench…</div>
  </div>`;
  $('#main').querySelectorAll('.ck input').forEach(cb=>cb.onchange=()=>signoff(e.endpoint_key,cb.dataset.f,cb.checked));
  $('#main').querySelectorAll('.h[data-pop]').forEach(h=>h.onclick=ev=>showPop(ev,h.dataset.pop));
  api('/api/endpoint?key='+encodeURIComponent(e.endpoint_key)).then(d=>{DETAIL=d;renderWorkbench(e,d);});
}
function renderWorkbench(e,d){
  const wb=$('#wb');if(!wb||!d||d.error)return;
  const reqBody=(d.edit&&d.edit.request_json)||(d.request_fixture!=null?JSON.stringify(d.request_fixture,null,2):'');
  const respJson=(d.edit&&d.edit.response_json)||(d.response_fixture!=null?JSON.stringify(d.response_fixture,null,2):'');
  const codes=Object.keys(d.response_codes||{});
  wb.className='wb';
  wb.innerHTML=`
   <div class="wb-col">
     <h3>Request</h3>
     <textarea id="wb-code" class="code">${escapeHtml((d.edit&&d.edit.code)||d.snippet||'')}</textarea>
     <div class="muted" style="font-size:12px;margin-top:8px">request body JSON${d.request_model?' ('+escapeHtml(d.request_model)+')':''}:</div>
     <textarea id="wb-req">${escapeHtml(reqBody)}</textarea>
     <div class="row" style="margin-top:10px">
       <button class="go" id="wb-run">▶ Run example</button>
       ${e.http_method!=='GET'?'<label class="ck" style="padding:0;font-size:12px"><input type="checkbox" id="wb-confirm"> confirm: mutates staging</label>':''}
       <button class="go" id="wb-save" style="background:#444">Save improvement</button>
       <span id="wb-msg" class="muted"></span>
     </div>
   </div>
   <div class="wb-col">
     <h3>Response</h3>
     <div class="muted" style="font-size:12px">available response codes:</div>
     <div class="codes">${codes.length?codes.map(c=>`<span class="code-pill" title="${escapeHtml(d.response_codes[c])}">${c}</span>`).join(''):'<span class="muted">none documented</span>'}</div>
     <div class="muted" style="font-size:12px;margin-top:8px">latest saved fixture (${escapeHtml(d.response_model||'—')}.json):</div>
     <textarea id="wb-resp">${escapeHtml(respJson)}</textarea>
     <div class="row" style="margin-top:8px"><button class="go" id="wb-savefx" style="background:#444">Save as fixture</button>
       <span id="wb-fxmsg" class="muted"></span></div>
     <div id="wb-runout"></div>
     <div id="caps"></div>
   </div>`;
  $('#wb-run').onclick=()=>runExample(e);
  $('#wb-save').onclick=()=>saveEdit(e);
  $('#wb-savefx').onclick=()=>saveFixture(e,d);
  loadCaps(e.endpoint_key);
}
function runExample(e){
  const msg=$('#wb-msg');msg.textContent='running…';
  const confirm=$('#wb-confirm')?$('#wb-confirm').checked:false;
  api('/api/run',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({endpoint:e.endpoint_key,confirm})}).then(r=>{
    if(r.needs_confirm){msg.textContent='check "confirm" to run a mutating call';return;}
    if(r.error&&!r.ok)msg.textContent='error: '+r.error;
    else msg.textContent=r.matched===true?'ran ✓ matches fixture':(r.matched===false?'ran — DIFF vs fixture':'ran (rc '+r.returncode+')');
    renderRunOut(r);
    if(r.response!=null&&$('#wb-resp'))$('#wb-resp').value=JSON.stringify(r.response,null,2);
    load();loadCaps(e.endpoint_key);
  });
}
function renderRunOut(r){
  const box=$('#wb-runout');if(!box)return;
  let h='<div class="section" style="margin-top:12px"><h3>Run output</h3>';
  if(r.matched!=null)h+=r.matched?'<span class="pill" style="background:#28a745;color:#fff">matches fixture</span>'
    :'<span class="pill" style="background:#dc3545;color:#fff">DIFF vs fixture</span>';
  if(r.diff)h+='<pre>'+escapeHtml(r.diff)+'</pre>';
  if(r.stdout)h+='<div class="muted" style="margin-top:6px">stdout:</div><pre>'+escapeHtml(r.stdout)+'</pre>';
  box.innerHTML=h+'</div>';
}
function saveEdit(e){
  api('/api/edit',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({endpoint:e.endpoint_key,code:$('#wb-code').value,
      request_json:$('#wb-req').value,response_json:$('#wb-resp').value})})
    .then(()=>{$('#wb-msg').textContent='saved → tests/example_edits.json (for enrichment)';});
}
function saveFixture(e,d){
  api('/api/save-fixture',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({endpoint:e.endpoint_key,response_model:d.response_model,
      http_method:e.http_method,path:e.path,response:parseMaybe($('#wb-resp').value)})})
    .then(r=>{$('#wb-fxmsg').textContent=r.ok?('wrote tests/fixtures/'+r.fixture):('error: '+r.error);load();});
}
function showPop(ev,kind){
  ev.stopPropagation();closePop();
  const d=DETAIL;if(!d)return;
  let title='',html='';
  if(kind==='impl'){title='Implementation';html='<pre>'+escapeHtml(d.impl_source||'(source unavailable)')+'</pre>';}
  else if(kind==='example'){title='Example';html='<div class="muted">'+escapeHtml(d.example_path||'no canonical example')+'</div><pre>'+escapeHtml(d.snippet||'')+'</pre>';}
  else if(kind==='sphinx'){title='Sphinx docs';html='<a href="'+escapeHtml(d.doc_url)+'" target="_blank" rel="noopener">'+escapeHtml(d.doc_url)+'</a>'+(d.doc_path?'<div class="muted">local: '+escapeHtml(d.doc_path)+'</div>':'<div class="muted">per-endpoint page not generated yet</div>');}
  else if(kind==='fixture'){title='Fixture';html=d.response_fixture!=null?'<pre>'+escapeHtml(JSON.stringify(d.response_fixture,null,2)).slice(0,4000)+'</pre>':'<div class="muted">no fixture captured</div>';}
  else if(kind==='test'){title='Test coverage';html='<div>endpoint source coverage: '+(SELE&&SELE.coverage_pct!=null?Math.round(SELE.coverage_pct)+'%':'—')+'</div><div class="muted" style="margin-top:6px">refresh: coverage run --source=ab -m pytest -m "not live" &amp;&amp; coverage json</div>';}
  const pop=ce('div','pop');pop.id='pop';
  pop.innerHTML='<div class="pop-h">'+title+' <span class="pop-x">×</span></div><div class="pop-b">'+html+'</div>';
  document.body.appendChild(pop);
  const r=ev.currentTarget.getBoundingClientRect();
  pop.style.top=Math.min(r.bottom+6,window.innerHeight-100)+'px';
  pop.style.left=Math.max(8,Math.min(r.left,window.innerWidth-440))+'px';
  pop.querySelector('.pop-x').onclick=closePop;
}
function closePop(){const p=$('#pop');if(p)p.remove();}
document.addEventListener('click',ev=>{const p=$('#pop');
  if(p&&!p.contains(ev.target)&&!ev.target.closest('.h[data-pop]'))closePop();});
function signoff(key,field,value){
  api('/api/signoff',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({endpoint:key,field,value})}).then(()=>load());
}
function parseMaybe(t){t=t.trim();if(!t)return null;try{return JSON.parse(t);}catch(e){return t;}}
function loadCaps(key){api('/api/captures?endpoint='+encodeURIComponent(key)).then(r=>renderCaps(r.captures));}
function renderCaps(caps){
  const box=$('#caps');if(!box)return;
  if(!caps.length){box.innerHTML='<div class="muted" style="margin-top:10px">No captures logged yet.</div>';return;}
  box.innerHTML='<h3 style="margin-top:16px">Captures &amp; run output ('+caps.length+')</h3>'+caps.map(c=>{
    const src=c.source==='run'?'<span class="pill" style="background:#4c8dff;color:#fff">run</span>'
      :'<span class="pill" style="background:#fd7e14;color:#fff">paste</span>';
    return `<div class="cap">${src} <b>${c.http_method||''}</b> ${escapeHtml(c.url||'')} ${c.status_code?('· '+c.status_code):''}
    <span class="muted">· ${c.created_at}</span>
    ${c.response!=null?'<pre>'+escapeHtml(JSON.stringify(c.response,null,2)).slice(0,4000)+'</pre>':''}</div>`;}).join('');
}
function escapeHtml(s){return s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
$('#search').oninput=ev=>{FILTER=ev.target.value.toLowerCase();renderTree();};
load();
</script>
</body></html>"""
