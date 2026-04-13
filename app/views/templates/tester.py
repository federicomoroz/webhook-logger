TESTER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WEBHOOK TESTER // FEDERICO MOROZ</title>
  <link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
  <link href="https://fonts.googleapis.com/css2?family=VT323&family=Share+Tech+Mono&display=swap" rel="stylesheet">
  <style>
    :root {
      --g-hi:   #39ff14;
      --g-mid:  #20c020;
      --g-dim:  #147814;
      --g-mute: #0d500d;
      --bg:     #080808;
      --bg-alt: #0c0f0c;
      --red:    #ff5050;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { background: var(--bg); color: var(--g-mid); font-family: 'Share Tech Mono', monospace; min-height: 100vh; }

    header {
      background: #000;
      border-bottom: 1px solid var(--g-mute);
      display: flex; align-items: center; gap: 20px;
      padding: 10px 24px;
      position: sticky; top: 0; z-index: 100;
    }
    .back { color: var(--g-dim); font-size: 0.8rem; letter-spacing: 1px; text-decoration: none; border: 1px solid var(--g-mute); padding: 4px 12px; transition: all 0.1s; }
    .back:hover { color: var(--g-hi); border-color: var(--g-dim); background: rgba(57,255,20,0.05); }
    .header-title { color: var(--g-dim); font-size: 0.78rem; letter-spacing: 2px; }

    .container { max-width: 820px; margin: 0 auto; padding: 32px 20px 60px; }

    .page-title { font-family: 'VT323', monospace; font-size: 2.4rem; color: var(--g-hi); letter-spacing: 4px; margin-bottom: 4px; }
    .page-sub { font-size: 0.75rem; color: var(--g-dim); letter-spacing: 2px; margin-bottom: 28px; }

    hr { border: none; border-top: 1px solid var(--g-mute); margin: 20px 0; }

    .field { margin-bottom: 16px; }
    .label { font-size: 0.72rem; color: var(--g-dim); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; display: block; }

    .url-row { display: flex; gap: 10px; }
    select, input[type=text], textarea {
      -webkit-appearance: none; appearance: none;
      background: var(--bg-alt);
      border: 1px solid var(--g-mute);
      color: var(--g-mid);
      font-family: 'Share Tech Mono', monospace;
      font-size: 0.88rem;
      outline: none;
      padding: 8px 12px;
      border-radius: 0;
      width: 100%;
      transition: border-color 0.1s;
    }
    select { width: auto; min-width: 90px; flex-shrink: 0; cursor: pointer; }
    select option { background: var(--bg); }
    input:focus, textarea:focus, select:focus { border-color: var(--g-dim); }
    textarea { resize: vertical; min-height: 140px; font-size: 0.82rem; }

    .btn-execute {
      background: rgba(57,255,20,0.08);
      border: 1px solid var(--g-mid);
      color: var(--g-hi);
      cursor: pointer;
      font-family: 'Share Tech Mono', monospace;
      font-size: 0.85rem;
      letter-spacing: 2px;
      padding: 10px 28px;
      text-transform: uppercase;
      transition: all 0.1s;
      margin-top: 4px;
    }
    .btn-execute:hover { background: rgba(57,255,20,0.15); border-color: var(--g-hi); }
    .btn-execute:disabled { opacity: 0.4; cursor: not-allowed; }

    #response-box {
      margin-top: 24px;
      border: 1px solid var(--g-mute);
      background: var(--bg-alt);
      padding: 16px 20px;
      display: none;
    }
    .resp-title { font-size: 0.72rem; color: var(--g-dim); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px; }
    .resp-meta { display: flex; gap: 24px; margin-bottom: 12px; flex-wrap: wrap; }
    .resp-meta span { font-size: 0.82rem; }
    .resp-meta .key { color: var(--g-dim); }
    .resp-meta .val { color: var(--g-hi); }
    .resp-meta .val.ok { color: var(--g-hi); }
    .resp-meta .val.err { color: var(--red); }
    .resp-body {
      background: #030503;
      border: 1px solid var(--g-mute);
      color: var(--g-mid);
      font-size: 0.8rem;
      padding: 12px;
      white-space: pre-wrap;
      word-break: break-all;
      max-height: 300px;
      overflow-y: auto;
    }
    .spinner { color: var(--g-dim); font-size: 0.82rem; margin-top: 16px; display: none; }
    .error-msg { color: var(--red); font-size: 0.82rem; margin-top: 12px; display: none; }

    ::-webkit-scrollbar { width: 5px; background: #000; }
    ::-webkit-scrollbar-thumb { background: var(--g-mute); }
  </style>
</head>
<body>
<header>
  <a class="back" href="/">&#8592; HOME</a>
  <span class="header-title">WEBHOOK LOGGER &nbsp;//&nbsp; TESTER</span>
</header>

<div class="container">
  <div class="page-title">WEBHOOK TESTER</div>
  <div class="page-sub">SEND HTTP REQUESTS TO ANY ENDPOINT &mdash; BUILT BY FEDERICO MOROZ</div>
  <hr>

  <div class="field url-row">
    <select id="method">
      <option>POST</option>
      <option>GET</option>
      <option>PUT</option>
      <option>PATCH</option>
      <option>DELETE</option>
    </select>
    <input type="text" id="url" placeholder="https://hooks.airtable.com/workflows/v1/..." spellcheck="false">
  </div>

  <div class="field">
    <span class="label">&gt; Payload (JSON)</span>
    <textarea id="payload" spellcheck="false">{
  "email": "fedegfs@gmail.com"
}</textarea>
  </div>

  <button class="btn-execute" id="send-btn" onclick="sendRequest()">&gt; EXECUTE REQUEST</button>
  <div class="spinner" id="spinner">&gt; SENDING...</div>
  <div class="error-msg" id="error-msg"></div>

  <div id="response-box">
    <div class="resp-title">&gt; RESPONSE</div>
    <div class="resp-meta">
      <span><span class="key">STATUS &nbsp;</span><span class="val" id="r-status"></span></span>
      <span><span class="key">ELAPSED </span><span class="val" id="r-elapsed"></span></span>
      <span><span class="key">RESULT &nbsp;</span><span class="val" id="r-ok"></span></span>
    </div>
    <pre class="resp-body" id="r-body"></pre>
  </div>
</div>

<script>
async function sendRequest() {
  const url     = document.getElementById('url').value.trim();
  const method  = document.getElementById('method').value;
  const rawBody = document.getElementById('payload').value.trim();

  if (!url) { showError('URL is required.'); return; }

  let payload = {};
  if (rawBody) {
    try { payload = JSON.parse(rawBody); }
    catch(e) { showError('Invalid JSON: ' + e.message); return; }
  }

  setLoading(true);
  hideError();
  document.getElementById('response-box').style.display = 'none';

  try {
    const res = await fetch('/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, method, payload }),
    });

    if (!res.ok) {
      const err = await res.json();
      showError(err.detail || 'Server error.');
      return;
    }

    const data = await res.json();
    showResponse(data);
  } catch(e) {
    showError('Network error: ' + e.message);
  } finally {
    setLoading(false);
  }
}

function showResponse(data) {
  document.getElementById('r-status').textContent  = data.status_code;
  document.getElementById('r-elapsed').textContent = data.elapsed_ms + 'ms';
  const okEl = document.getElementById('r-ok');
  okEl.textContent  = data.ok ? 'OK' : 'ERROR';
  okEl.className    = 'val ' + (data.ok ? 'ok' : 'err');
  document.getElementById('r-status').className = 'val ' + (data.ok ? 'ok' : 'err');

  let body = data.body;
  try { body = JSON.stringify(JSON.parse(body), null, 2); } catch(_) {}
  document.getElementById('r-body').textContent = body || '(empty response)';
  document.getElementById('response-box').style.display = 'block';
}

function setLoading(on) {
  document.getElementById('send-btn').disabled      = on;
  document.getElementById('spinner').style.display  = on ? 'block' : 'none';
}
function showError(msg) {
  const el = document.getElementById('error-msg');
  el.textContent    = '> ERROR: ' + msg;
  el.style.display  = 'block';
}
function hideError() {
  document.getElementById('error-msg').style.display = 'none';
}

document.getElementById('payload').addEventListener('keydown', function(e) {
  if (e.key === 'Tab') {
    e.preventDefault();
    const s = this.selectionStart;
    this.value = this.value.substring(0, s) + '  ' + this.value.substring(this.selectionEnd);
    this.selectionStart = this.selectionEnd = s + 2;
  }
});
</script>
</body>
</html>"""
