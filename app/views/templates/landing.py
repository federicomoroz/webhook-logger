import html

LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WEBHOOK LOGGER // FEDERICO MOROZ</title>
  <link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
  <link href="https://fonts.googleapis.com/css2?family=VT323&family=Share+Tech+Mono&display=swap" rel="stylesheet">
  <style>
    :root {{
      --green:        #15ff00;
      --green-dim:    #0a8f00;
      --green-bright: #39ff14;
      --bg:           #080808;
      --glow:         0 0 8px #15ff00, 0 0 2px #15ff00;
      --glow-soft:    0 0 4px rgba(21,255,0,0.5);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      background: var(--bg);
      color: var(--green);
      font-family: 'Share Tech Mono', monospace;
      min-height: 100vh;
    }}
    .terminal {{
      max-width: 860px;
      margin: 0 auto;
      padding: 40px 24px 60px;
    }}
    .title {{
      font-family: 'VT323', monospace;
      font-size: clamp(2.2rem, 6vw, 3.5rem);
      color: var(--green-bright);
      text-shadow: var(--glow);
      letter-spacing: 4px;
      line-height: 1;
    }}
    .subtitle {{
      font-size: 0.75rem;
      color: var(--green-dim);
      letter-spacing: 2px;
      margin-top: 4px;
      margin-bottom: 28px;
      text-transform: uppercase;
    }}
    hr {{
      border: none;
      border-top: 1px solid var(--green-dim);
      margin: 20px 0;
    }}
    .line {{ margin: 5px 0; font-size: 0.9rem; }}
    .label {{ color: var(--green-dim); }}
    .value {{ color: var(--green-bright); text-shadow: 0 0 4px rgba(21,255,0,0.4); }}
    .ok .value::before {{ content: "[OK] "; color: var(--green); }}
    .section-title {{
      font-family: 'VT323', monospace;
      font-size: 1.4rem;
      color: var(--green-bright);
      letter-spacing: 2px;
      margin-bottom: 12px;
    }}
    .stats-box {{
      border: 1px solid var(--green-dim);
      background: rgba(21,255,0,0.02);
      padding: 16px 20px;
      margin: 24px 0;
    }}
    .stat-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin: 5px 0;
      font-size: 0.88rem;
      gap: 12px;
    }}
    .stat-name {{ color: var(--green); text-transform: uppercase; }}
    .stat-right {{ display: flex; align-items: center; gap: 10px; color: var(--green-bright); }}
    .stat-bar {{ color: var(--green-dim); letter-spacing: -2px; font-size: 0.75rem; }}
    .endpoints-section {{ margin: 24px 0; }}
    .endpoint {{
      display: flex;
      gap: 14px;
      align-items: baseline;
      margin: 6px 0;
      font-size: 0.88rem;
    }}
    .method {{
      width: 68px;
      text-align: center;
      border: 1px solid currentColor;
      padding: 1px 4px;
      font-family: 'VT323', monospace;
      font-size: 1rem;
      flex-shrink: 0;
    }}
    .method.post   {{ color: var(--green); }}
    .method.get    {{ color: #00e5ff; }}
    .method.delete {{ color: #ff4444; }}
    .ep-path {{ color: var(--green-bright); }}
    .ep-desc {{ color: var(--green-dim); }}
    .actions {{ display: flex; gap: 14px; flex-wrap: wrap; margin-top: 28px; }}
    .btn {{
      border: 1px solid var(--green);
      color: var(--green);
      background: transparent;
      padding: 8px 20px;
      font-family: 'Share Tech Mono', monospace;
      font-size: 0.85rem;
      text-decoration: none;
      letter-spacing: 1px;
      text-transform: uppercase;
      cursor: pointer;
      transition: all 0.1s;
    }}
    .btn:hover {{
      background: rgba(21,255,0,0.1);
      box-shadow: 0 0 8px rgba(21,255,0,0.3);
      color: var(--green-bright);
    }}
    .btn.primary {{
      background: rgba(21,255,0,0.1);
      border-color: var(--green-bright);
      color: var(--green-bright);
      text-shadow: 0 0 4px rgba(21,255,0,0.4);
    }}
    .cursor {{
      display: inline-block;
      width: 10px;
      height: 1em;
      background: var(--green);
      animation: blink 1s step-end infinite;
      vertical-align: text-bottom;
      margin-left: 4px;
    }}
    @keyframes blink {{ 0%,100% {{ opacity:1 }} 50% {{ opacity:0 }} }}
    .footer {{ margin-top: 40px; font-size: 0.72rem; color: var(--green-dim); }}
    .footer a {{ color: var(--green-dim); }}
  </style>
</head>
<body>
<div class="terminal">
  <div class="title">WEBHOOK LOGGER</div>
  <div class="subtitle">BUILT BY FEDERICO MOROZ &mdash; BACKEND PORTFOLIO PROJECT</div>

  <div class="line ok"><span class="label">SYSTEM STATUS &nbsp;&nbsp;&nbsp;</span><span class="value">ONLINE</span></div>
  <div class="line ok"><span class="label">DATABASE &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="value">CONNECTED</span></div>
  <div class="line ok"><span class="label">API VERSION &nbsp;&nbsp;&nbsp;&nbsp;</span><span class="value">1.0.0</span></div>
  <div class="line"><span class="label">SESSION UPTIME &nbsp;</span><span class="value" id="uptime">00:00:00</span></div>

  <hr>

  <div class="stats-box">
    <div class="section-title">&gt; EVENT LOG STATISTICS</div>
    {stats_html}
  </div>

  <div class="endpoints-section">
    <div class="section-title">&gt; AVAILABLE COMMANDS</div>
    <div class="endpoint">
      <span class="method post">POST</span>
      <span class="ep-path">/webhooks/{{source}}</span>
      <span class="ep-desc">&mdash; register incoming event</span>
    </div>
    <div class="endpoint">
      <span class="method get">GET</span>
      <span class="ep-path">/events</span>
      <span class="ep-desc">&mdash; query event log &nbsp;[?source=X &amp;limit=N &amp;offset=N]</span>
    </div>
    <div class="endpoint">
      <span class="method get">GET</span>
      <span class="ep-path">/events/{{id}}</span>
      <span class="ep-desc">&mdash; retrieve single record</span>
    </div>
    <div class="endpoint">
      <span class="method get">GET</span>
      <span class="ep-path">/stats</span>
      <span class="ep-desc">&mdash; aggregate counts by source</span>
    </div>
    <div class="endpoint">
      <span class="method delete">DEL</span>
      <span class="ep-path">/events/{{id}}</span>
      <span class="ep-desc">&mdash; purge record from log</span>
    </div>
  </div>

  <div class="actions">
    <a class="btn primary" href="/docs">&gt; INTERACTIVE DOCS</a>
    <a class="btn primary" href="/tester">&gt; SEND WEBHOOK</a>
    <a class="btn" href="/events">&gt; EVENT LOG</a>
    <a class="btn" href="/stats">&gt; STATISTICS</a>
  </div>

  <hr style="margin-top:32px">
  <div class="line"><span style="color:var(--green-dim)">&gt; AWAITING INPUT</span><span class="cursor"></span></div>

  <div class="footer" style="margin-top:24px">
    SOURCE &mdash; <a href="https://github.com/federicomoroz/webhook-logger">github.com/federicomoroz/webhook-logger</a>
  </div>
</div>
<script>
  const t0 = Date.now();
  setInterval(() => {{
    const s = Math.floor((Date.now() - t0) / 1000);
    const pad = n => String(n).padStart(2,'0');
    document.getElementById('uptime').textContent =
      pad(Math.floor(s/3600)) + ':' + pad(Math.floor((s%3600)/60)) + ':' + pad(s%60);
  }}, 1000);
</script>
</body>
</html>"""


def render_landing(rows, total: int) -> str:
    if not rows:
        stats_html = '<div class="stat-row"><span class="stat-name" style="color:var(--green-dim)">NO EVENTS RECORDED YET</span></div>'
    else:
        stats_html = f'<div class="stat-row"><span class="stat-name">TOTAL</span><span class="stat-right">{total} events</span></div>'
        max_count = rows[0].count
        for r in rows:
            bar = "\u2588" * int((r.count / max_count) * 18)
            safe_source = html.escape(r.source)
            stats_html += (
                f'<div class="stat-row">'
                f'<span class="stat-name">{safe_source}</span>'
                f'<span class="stat-right"><span class="stat-bar">{bar}</span> {r.count}</span>'
                f'</div>'
            )
    return LANDING_HTML.format(stats_html=stats_html)
