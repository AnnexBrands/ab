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
        return self._json({"error": "not found"}, 404)


def serve(host: str = "127.0.0.1", port: int = 8765) -> None:
    """Run the app (blocking). Initializes the DB and imports committed sign-offs."""
    db.init_db()
    db.import_signoffs()
    httpd = ThreadingHTTPServer((host, port), _Handler)
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
</style></head>
<body>
<div id="nav">
  <header class="bar">
    <h1>Example Capture &amp; Harmony</h1>
    <div class="tabs"><button id="t-tags" class="on">Tags</button><button id="t-paths">Paths</button></div>
    <input id="search" placeholder="filter endpoints…">
  </header>
  <div id="tree"></div>
</div>
<div id="main"><div class="empty">Loading…</div></div>
<script>
let DATA=null, MODE='tags', SEL=null, FILTER='';
const $=s=>document.querySelector(s), ce=(t,c)=>{const e=document.createElement(t);if(c)e.className=c;return e;};
const RUN={passing:['#28a745','pass'],failing:['#dc3545','fail'],not_verified:['#6c757d','not run'],
awaiting_data:['#ffc107','needs data'],awaiting_paste:['#fd7e14','paste'],binary:['#6610f2','binary'],
missing_example:['#dc3545','no example']};
function api(p,opt){return fetch(p,opt).then(r=>r.json());}
async function load(){DATA=await api('/api/data');renderSummary();renderTree();if(SEL)renderDetail(find(SEL));}
function find(k){return DATA.endpoints.find(e=>e.endpoint_key===k);}
function renderSummary(){/* summary cards live atop detail when nothing selected */}
function epColor(e){return RUN[e.run_status]?RUN[e.run_status][0]:'#6c757d';}
function groups(){
  const map={};
  for(const e of DATA.endpoints){
    if(FILTER && !e.endpoint_key.toLowerCase().includes(FILTER) && !e.path.toLowerCase().includes(FILTER))continue;
    let keys;
    if(MODE==='tags')keys=(e.tags&&e.tags.length?e.tags:['(untagged)']);
    else keys=['/'+(e.path.replace(/^\//,'').split('/')[0]||'')];
    for(const k of keys){(map[k]=map[k]||[]).push(e);}
  }
  return map;
}
function renderTree(){
  const tree=$('#tree');tree.innerHTML='';
  const map=groups();const keys=Object.keys(map).sort();
  for(const k of keys){
    const d=ce('details','grp');d.open=!!FILTER||keys.length<=4;
    const s=ce('summary');const done=map[k].filter(e=>e.example_ok&&e.tests_ok&&e.sphinx_ok).length;
    s.textContent=`${k}  (${done}/${map[k].length})`;d.appendChild(s);
    for(const e of map[k].sort((a,b)=>a.endpoint_key.localeCompare(b.endpoint_key))){
      const row=ce('div','ep'+(SEL===e.endpoint_key?' sel':''));
      const dot=ce('span','dot');dot.style.background=epColor(e);
      const m=ce('span','m');m.textContent=e.http_method;
      const t=ce('span');t.textContent=e.endpoint_key.replace(/^api\./,'');
      row.append(dot,m,t);row.onclick=()=>{SEL=e.endpoint_key;renderDetail(e);renderTree();};
      d.appendChild(row);
    }
    tree.appendChild(d);
  }
}
function hcard(label,ok,extra){return `<div class="h ${ok?'ok':'no'}"><div class="t">${label}</div>
  <div class="v">${ok?'✓':'✗'}${extra?' '+extra:''}</div></div>`;}
function renderDetail(e){
  if(!e){$('#main').innerHTML='<div class="empty">Select an endpoint.</div>';return;}
  const s=DATA.summary;
  const [rc,rl]=RUN[e.run_status]||['#6c757d',e.run_status];
  const cov=e.coverage_pct!=null?Math.round(e.coverage_pct)+'%':'—';
  $('#main').innerHTML=`
  <div class="summary">
    <div class="card"><div class="n">${s.full_harmony}/${s.total}</div><div class="l">Full harmony</div></div>
    <div class="card"><div class="n">${s.example}</div><div class="l">Examples</div></div>
    <div class="card"><div class="n">${s.fixture}</div><div class="l">Fixtures</div></div>
    <div class="card"><div class="n">${s.signed_off}</div><div class="l">Signed off</div></div>
  </div>
  <div class="det">
    <h2><span style="color:${rc}">${e.http_method}</span> ${e.path}</h2>
    <div class="kv">${e.endpoint_key} · ${e.api_surface} · tags: ${(e.tags||[]).join(', ')||'—'}<br>
      response: <b>${e.response_model||'—'}</b>${e.request_model?' · request: <b>'+e.request_model+'</b>':''}
      · <span class="pill" style="background:${rc};color:#fff">${rl}</span></div>
    <div class="harm">
      ${hcard('Implementation',e.has_impl)}
      ${hcard('Example',e.has_example)}
      ${hcard('Fixture',e.has_fixture)}
      ${hcard('Test (cov)',e.has_test,cov)}
      ${hcard('Sphinx',e.has_sphinx)}
      <div class="h"><div class="t">Harmony</div><div class="v">${e.harmony_score}/4</div></div>
    </div>

    <div class="section"><h3>Interactive sign-off</h3>
      <label class="ck"><input type="checkbox" data-f="example_ok" ${e.example_ok?'checked':''}> Example is acceptable</label>
      <label class="ck"><input type="checkbox" data-f="tests_ok" ${e.tests_ok?'checked':''}> Tests are acceptable</label>
      <label class="ck"><input type="checkbox" data-f="sphinx_ok" ${e.sphinx_ok?'checked':''}> Sphinx is acceptable</label>
      <small class="note">${e.signoff_note?('note: '+e.signoff_note+' · '):''}saved to progress.db</small>
    </div>

    <div class="section"><h3>Log HTTP request / response → SQLite</h3>
      <div class="row">
        <input class="txt" id="cap-method" value="${e.http_method}" style="width:80px">
        <input class="txt" id="cap-url" placeholder="url (optional)" style="flex:1">
        <input class="txt" id="cap-status" placeholder="status" style="width:80px">
      </div>
      <div class="muted" style="font-size:12px">request body JSON${e.request_model?' ('+e.request_model+')':''}:</div>
      <textarea id="cap-req" placeholder="paste request JSON (optional)"></textarea>
      <div class="muted" style="font-size:12px;margin-top:8px">response JSON (${e.response_model||'?'}):</div>
      <textarea id="cap-resp" placeholder="paste real response JSON"></textarea>
      <div class="row" style="margin-top:10px"><button class="go" id="cap-save">Log capture</button>
        <span id="cap-msg" class="muted"></span></div>
      <div id="caps"></div>
    </div>
  </div>`;
  $('#main').querySelectorAll('.ck input').forEach(cb=>cb.onchange=()=>signoff(e.endpoint_key,cb.dataset.f,cb.checked));
  $('#cap-save').onclick=()=>logCapture(e);
  loadCaps(e.endpoint_key);
}
function signoff(key,field,value){
  api('/api/signoff',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({endpoint:key,field,value})}).then(()=>load());
}
function parseMaybe(t){t=t.trim();if(!t)return null;try{return JSON.parse(t);}catch(e){return t;}}
function logCapture(e){
  const payload={endpoint:e.endpoint_key,http_method:$('#cap-method').value,url:$('#cap-url').value,
    status_code:parseInt($('#cap-status').value)||null,request:parseMaybe($('#cap-req').value),
    response:parseMaybe($('#cap-resp').value)};
  api('/api/capture',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
    .then(r=>{$('#cap-msg').textContent='logged #'+r.id;$('#cap-req').value='';$('#cap-resp').value='';
      renderCaps(r.captures);load();});
}
function loadCaps(key){api('/api/captures?endpoint='+encodeURIComponent(key)).then(r=>renderCaps(r.captures));}
function renderCaps(caps){
  const box=$('#caps');if(!box)return;
  if(!caps.length){box.innerHTML='<div class="muted" style="margin-top:10px">No captures logged yet.</div>';return;}
  box.innerHTML='<h3 style="margin-top:16px">Logged captures ('+caps.length+')</h3>'+caps.map(c=>`
    <div class="cap"><b>${c.http_method||''}</b> ${c.url||''} ${c.status_code?('· '+c.status_code):''}
    <span class="muted">· ${c.created_at}</span>
    ${c.response!=null?'<pre>'+escapeHtml(JSON.stringify(c.response,null,2)).slice(0,4000)+'</pre>':''}</div>`).join('');
}
function escapeHtml(s){return s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
$('#t-tags').onclick=()=>{MODE='tags';$('#t-tags').classList.add('on');$('#t-paths').classList.remove('on');renderTree();};
$('#t-paths').onclick=()=>{MODE='paths';$('#t-paths').classList.add('on');$('#t-tags').classList.remove('on');renderTree();};
$('#search').oninput=ev=>{FILTER=ev.target.value.toLowerCase();renderTree();};
load();
</script>
</body></html>"""
