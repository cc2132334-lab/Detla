import streamlit as st
import streamlit.components.v1 as components

# --- 1. FULL PAGE CONFIG ---
st.set_page_config(
    page_title="Delta Terminal v1.4.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. HIDE ALL STREAMLIT UI & TOOLBARS ---
st.markdown("""
<style>
    header, header[data-testid="stHeader"] {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    #MainMenu, footer, div[data-testid="stStatusWidget"] {display: none !important;}
    [data-testid="manage-app-button"], button[title="Manage app"], div[class*="viewerBadge"], div[class*="manage-app"] {display: none !important;}
    div[data-testid="stFloatingActions"] {display: none !important;}
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
        width: 100% !important;
        height: 100vh !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. TERMINAL + SMC QUANT ENGINE ---
terminal_html = """
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Delta Terminal</title>
<style>
  /* LIGHT THEME (DEFAULT) */
  :root[data-theme="light"] {
    --bg-page: #f4f6fa;
    --card-bg: #ffffff;
    --card-border: #e2e8f0;
    --tile-bg: #f8fafc;
    --tile-border: #edf2f7;
    --text-primary: #0f172a;
    --text-muted: #64748b;
    --neon-green: #059669;
    --neon-red: #e11d48;
    --neon-cyan: #0284c7;
    --neon-yellow: #d97706;
    --header-border: #e2e8f0;
    --clock-bg: #e0f2fe;
    --clock-border: #bae6fd;
    --clock-text: #0369a1;
    --shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    --pill-bg: #f8fafc;
    --log-bg: #0f172a;
    --log-text: #38bdf8;
  }

  /* DARK THEME */
  :root[data-theme="dark"] {
    --bg-page: #080b11;
    --card-bg: rgba(18, 24, 38, 0.85);
    --card-border: rgba(255, 255, 255, 0.08);
    --tile-bg: rgba(255, 255, 255, 0.03);
    --tile-border: rgba(255, 255, 255, 0.05);
    --text-primary: #ffffff;
    --text-muted: #8b9bb4;
    --neon-green: #00f090;
    --neon-red: #ff3366;
    --neon-cyan: #00e5ff;
    --neon-yellow: #ffb800;
    --header-border: rgba(255, 255, 255, 0.06);
    --clock-bg: rgba(0, 229, 255, 0.08);
    --clock-border: rgba(0, 229, 255, 0.2);
    --clock-text: #00e5ff;
    --shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    --pill-bg: rgba(255, 255, 255, 0.03);
    --log-bg: #05070a;
    --log-text: #00e5ff;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }
  body { background: var(--bg-page); color: var(--text-primary); padding: 12px; overflow-x: hidden; transition: background 0.2s ease, color 0.2s ease; padding-bottom: 50px; }

  .header {
    display: flex; justify-content: space-between; align-items: center;
    padding: 6px 4px 14px 4px; border-bottom: 1px solid var(--header-border); margin-bottom: 14px;
  }
  .header-left { display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 14px; letter-spacing: 0.8px; }
  .pulse-dot { width: 8px; height: 8px; background: var(--neon-green); border-radius: 50%; box-shadow: 0 0 8px var(--neon-green); animation: pulse 1.5s infinite; }
  @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.3; transform: scale(0.8); } }

  .header-right { display: flex; align-items: center; gap: 8px; }
  .utc-clock { font-size: 11px; font-weight: 600; color: var(--clock-text); background: var(--clock-bg); padding: 5px 8px; border-radius: 6px; border: 1px solid var(--clock-border); }

  .theme-toggle-btn {
    background: var(--tile-bg);
    border: 1px solid var(--card-border);
    color: var(--text-primary);
    font-size: 14px;
    padding: 4px 9px;
    border-radius: 6px;
    cursor: pointer;
  }

  /* CARDS GRID */
  .grid { display: grid; grid-template-columns: 1fr; gap: 14px; margin-bottom: 16px; }
  @media(min-width: 768px) { .grid { grid-template-columns: 1fr 1fr; } }

  .card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 16px;
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
  }
  .card::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
    opacity: 0.6;
  }

  .card-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; }
  .coin-badge { font-size: 18px; font-weight: 800; }
  .spot-tag { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

  .price-box { text-align: right; }
  .live-price { font-size: 26px; font-weight: 800; font-family: monospace; }
  .price-up { color: var(--neon-green) !important; }
  .price-down { color: var(--neon-red) !important; }

  /* METRICS TILES */
  .metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }
  .tile {
    background: var(--tile-bg);
    border: 1px solid var(--tile-border);
    border-radius: 10px;
    padding: 10px;
  }
  .tile-title { font-size: 11px; color: var(--text-muted); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }
  .tile-val { font-size: 14px; font-weight: 700; font-family: monospace; }

  /* DISTANCE TAGS */
  .dist-row { margin-top: 12px; display: flex; gap: 8px; }
  .dist-pill {
    flex: 1; display: flex; justify-content: space-between; align-items: center;
    padding: 8px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; font-family: monospace;
    background: var(--pill-bg); border: 1px solid var(--card-border);
  }
  .dist-pos { color: var(--neon-green); font-weight: 700; }
  .dist-neg { color: var(--neon-red); font-weight: 700; }

  /* SMC SECTION */
  .smc-container {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 16px;
    box-shadow: var(--shadow);
  }
  .smc-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 12px; border-bottom: 1px solid var(--tile-border); padding-bottom: 8px;
  }
  .smc-title { font-size: 14px; font-weight: 800; letter-spacing: 0.5px; display: flex; align-items: center; gap: 6px; }

  /* SMC PANELS GRID */
  .smc-grid { display: grid; grid-template-columns: 1fr; gap: 12px; }
  @media(min-width: 768px) { .smc-grid { grid-template-columns: 1fr 1fr; } }

  .smc-card {
    background: var(--tile-bg);
    border: 1px solid var(--tile-border);
    border-radius: 12px;
    padding: 12px;
  }
  .smc-card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
  .setup-badge { padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; text-transform: uppercase; }
  .badge-buy { background: rgba(5, 150, 105, 0.15); color: var(--neon-green); border: 1px solid var(--neon-green); }
  .badge-sell { background: rgba(225, 29, 72, 0.15); color: var(--neon-red); border: 1px solid var(--neon-red); }
  .badge-wait { background: rgba(217, 119, 6, 0.15); color: var(--neon-yellow); border: 1px solid var(--neon-yellow); }

  .trade-param-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 8px; }
  .trade-param-box { background: var(--card-bg); border: 1px solid var(--card-border); padding: 8px; border-radius: 8px; text-align: center; }
  .param-lbl { font-size: 10px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 3px; font-weight: 600; }
  .param-val { font-size: 12px; font-weight: 700; font-family: monospace; }

  .smc-detail { font-size: 11px; color: var(--text-muted); line-height: 1.4; }
  .smc-highlight { color: var(--text-primary); font-weight: 600; }

  /* LOG CONSOLE */
  .console-box {
    margin-top: 14px;
    background: var(--log-bg);
    border-radius: 10px;
    padding: 10px 12px;
    font-family: monospace;
    font-size: 11px;
    color: var(--log-text);
    height: 110px;
    overflow-y: auto;
    border: 1px solid rgba(0, 0, 0, 0.1);
  }
  .log-line { margin-bottom: 4px; display: flex; gap: 8px; }
  .log-time { color: var(--text-muted); }
</style>
</head>
<body>

<!-- TOP HEADER -->
<div class="header">
  <div class="header-left">
    <div class="pulse-dot"></div>
    <span>DELTA QUANT ENGINE</span>
  </div>
  <div class="header-right">
    <div class="utc-clock" id="utc-clock">00:00:00 UTC</div>
    <button class="theme-toggle-btn" id="theme-btn" onclick="toggleTheme()" title="Toggle Theme">🌙</button>
  </div>
</div>

<!-- LIVE CARDS -->
<div class="grid">
  <!-- BTC -->
  <div class="card" id="card-btc">
    <div class="card-top">
      <div>
        <div class="coin-badge">🟠 BTC/USD</div>
        <div class="spot-tag">Spot: <span id="btc-spot">--</span> | Vol: <span id="btc-vol">--</span></div>
      </div>
      <div class="price-box">
        <div class="live-price" id="btc-price">Loading...</div>
      </div>
    </div>
    <div class="metrics-grid">
      <div class="tile">
        <div class="tile-title">Today High (UTC)</div>
        <div class="tile-val" style="color: var(--neon-cyan);" id="btc-cdh">--</div>
      </div>
      <div class="tile">
        <div class="tile-title">Today Low (UTC)</div>
        <div class="tile-val" style="color: var(--neon-yellow);" id="btc-cdl">--</div>
      </div>
      <div class="tile">
        <div class="tile-title">Prev Day High (PDH)</div>
        <div class="tile-val" id="btc-pdh">--</div>
      </div>
      <div class="tile">
        <div class="tile-title">Prev Day Low (PDL)</div>
        <div class="tile-val" id="btc-pdl">--</div>
      </div>
    </div>
    <div class="dist-row">
      <div class="dist-pill">
        <span style="color: var(--text-muted)">Dist to PDH:</span>
        <span id="btc-dist-pdh">--</span>
      </div>
      <div class="dist-pill">
        <span style="color: var(--text-muted)">Dist to PDL:</span>
        <span id="btc-dist-pdl">--</span>
      </div>
    </div>
  </div>

  <!-- ETH -->
  <div class="card" id="card-eth">
    <div class="card-top">
      <div>
        <div class="coin-badge">🔷 ETH/USD</div>
        <div class="spot-tag">Spot: <span id="eth-spot">--</span> | Vol: <span id="eth-vol">--</span></div>
      </div>
      <div class="price-box">
        <div class="live-price" id="eth-price">Loading...</div>
      </div>
    </div>
    <div class="metrics-grid">
      <div class="tile">
        <div class="tile-title">Today High (UTC)</div>
        <div class="tile-val" style="color: var(--neon-cyan);" id="eth-cdh">--</div>
      </div>
      <div class="tile">
        <div class="tile-title">Today Low (UTC)</div>
        <div class="tile-val" style="color: var(--neon-yellow);" id="eth-cdl">--</div>
      </div>
      <div class="tile">
        <div class="tile-title">Prev Day High (PDH)</div>
        <div class="tile-val" id="eth-pdh">--</div>
      </div>
      <div class="tile">
        <div class="tile-title">Prev Day Low (PDL)</div>
        <div class="tile-val" id="eth-pdl">--</div>
      </div>
    </div>
    <div class="dist-row">
      <div class="dist-pill">
        <span style="color: var(--text-muted)">Dist to PDH:</span>
        <span id="eth-dist-pdh">--</span>
      </div>
      <div class="dist-pill">
        <span style="color: var(--text-muted)">Dist to PDL:</span>
        <span id="eth-dist-pdl">--</span>
      </div>
    </div>
  </div>
</div>

<!-- SMC DETAILS & TRADE LOG WINDOW -->
<div class="smc-container">
  <div class="smc-header">
    <div class="smc-title">🎯 SMC QUANT STRUCTURE & TRADE EXECUTION LOG</div>
    <div style="font-size: 11px; color: var(--text-muted)">Auto Liquidity & OB Model</div>
  </div>

  <div class="smc-grid">
    <!-- BTC SMC SETUP -->
    <div class="smc-card">
      <div class="smc-card-top">
        <span style="font-weight: 700; font-size: 13px;">BTCUSD Setup: <span id="btc-smc-state">ANALYZING</span></span>
        <span class="setup-badge badge-wait" id="btc-badge">WAITING</span>
      </div>
      <div class="trade-param-row">
        <div class="trade-param-box">
          <div class="param-lbl">Signal / Action</div>
          <div class="param-val" id="btc-action">MONITOR</div>
        </div>
        <div class="trade-param-box">
          <div class="param-lbl">Entry / Zone</div>
          <div class="param-val" id="btc-entry">--</div>
        </div>
        <div class="trade-param-box">
          <div class="param-lbl">Stop Loss</div>
          <div class="param-val" style="color: var(--neon-red);" id="btc-sl">--</div>
        </div>
      </div>
      <div class="smc-detail" id="btc-narrative">Scanning daily range equilibrium and liquidity pools...</div>
    </div>

    <!-- ETH SMC SETUP -->
    <div class="smc-card">
      <div class="smc-card-top">
        <span style="font-weight: 700; font-size: 13px;">ETHUSD Setup: <span id="eth-smc-state">ANALYZING</span></span>
        <span class="setup-badge badge-wait" id="eth-badge">WAITING</span>
      </div>
      <div class="trade-param-row">
        <div class="trade-param-box">
          <div class="param-lbl">Signal / Action</div>
          <div class="param-val" id="eth-action">MONITOR</div>
        </div>
        <div class="trade-param-box">
          <div class="param-lbl">Entry / Zone</div>
          <div class="param-val" id="eth-entry">--</div>
        </div>
        <div class="trade-param-box">
          <div class="param-lbl">Stop Loss</div>
          <div class="param-val" style="color: var(--neon-red);" id="eth-sl">--</div>
        </div>
      </div>
      <div class="smc-detail" id="eth-narrative">Scanning daily range equilibrium and liquidity pools...</div>
    </div>
  </div>

  <!-- REAL-TIME CONSOLE AUDIT LOG -->
  <div class="console-box" id="console-logs">
    <div class="log-line"><span class="log-time">[SYSTEM]</span> SMC Execution Engine online. Listening to Delta Exchange tick feed...</div>
  </div>
</div>

<script>
  // THEME MANAGEMENT
  let currentTheme = localStorage.getItem('delta_theme') || 'light';
  applyTheme(currentTheme);

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    document.getElementById('theme-btn').innerText = theme === 'light' ? '🌙' : '☀️';
    localStorage.setItem('delta_theme', theme);
  }

  function toggleTheme() {
    currentTheme = currentTheme === 'light' ? 'dark' : 'light';
    applyTheme(currentTheme);
  }

  // CLOCK
  function updateClock() {
    const now = new Date();
    document.getElementById('utc-clock').innerText = now.toUTCString().split(' ')[4] + ' UTC';
  }
  setInterval(updateClock, 1000);
  updateClock();

  // STATE DATA
  const state = {
    BTCUSD: { price: 0, spot: 0, vol: 0, cdh: 0, cdl: 0, pdh: 0, pdl: 0, dec: 1, lastSignal: '' },
    ETHUSD: { price: 0, spot: 0, vol: 0, cdh: 0, cdl: 0, pdh: 0, pdl: 0, dec: 2, lastSignal: '' }
  };

  function fmt(val, dec) {
    if(!val || isNaN(val)) return '--';
    return Number(val).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  }

  // LOG AUDIT FUNCTION
  function addLog(msg) {
    const box = document.getElementById('console-logs');
    const now = new Date().toTimeString().split(' ')[0];
    const el = document.createElement('div');
    el.className = 'log-line';
    el.innerHTML = `<span class="log-time">[${now}]</span> ${msg}`;
    box.appendChild(el);
    box.scrollTop = box.scrollHeight;
  }

  // FETCH CANDLES
  async function fetchDailyStats() {
    try {
      const symbols = ['BTCUSD', 'ETHUSD'];
      for (const sym of symbols) {
        const nowSec = Math.floor(Date.now() / 1000);
        const startSec = nowSec - (86400 * 3);
        const res = await fetch(`https://api.india.delta.exchange/v2/history/candles?resolution=1d&symbol=${sym}&start=${startSec}&end=${nowSec}`);
        const data = await res.json();
        
        if (data.result && data.result.length >= 2) {
          const today = data.result[0];
          const yesterday = data.result[1];

          state[sym].pdh = parseFloat(yesterday.high);
          state[sym].pdl = parseFloat(yesterday.low);
          state[sym].cdh = parseFloat(today.high);
          state[sym].cdl = parseFloat(today.low);

          updateUI(sym);
          evaluateSMC(sym);
        }
      }
    } catch(e) {
      console.log("Stats fetch err", e);
    }
  }

  // SMC LOGIC ENGINE
  function evaluateSMC(sym) {
    const d = state[sym];
    if (!d.price || !d.pdh || !d.pdl) return;

    const prefix = sym === 'BTCUSD' ? 'btc' : 'eth';
    const equilibrium = (d.pdh + d.pdl) / 2; // 50% discount / premium level
    const distToPDH = d.price - d.pdh;
    const distToPDL = d.price - d.pdl;

    let action = 'MONITOR';
    let badgeClass = 'badge-wait';
    let statusText = 'IN RANGE';
    let entry = '--';
    let sl = '--';
    let narrative = '';

    // RULE 1: Bearish Liquidity Sweep (Price sweeps PDH and rejects)
    if (distToPDH >= 0 || (distToPDH > -50 && d.price < d.cdh)) {
      action = 'SELL / SHORT';
      badgeClass = 'badge-sell';
      statusText = 'PDH LIQUIDITY GRAB';
      entry = `$${fmt(d.price, d.dec)}`;
      sl = `$${fmt(Math.max(d.cdh, d.pdh) * 1.003, d.dec)}`;
      narrative = `Liquidity swept above PDH ($${fmt(d.pdh, d.dec)}). Smart money hunting buy-stops. Expecting mitigation towards EQ ($${fmt(equilibrium, d.dec)}).`;
    }
    // RULE 2: Bullish Liquidity Sweep (Price sweeps PDL and bounces)
    else if (distToPDL <= 0 || (distToPDL < 50 && d.price > d.cdl)) {
      action = 'BUY / LONG';
      badgeClass = 'badge-buy';
      statusText = 'PDL LIQUIDITY GRAB';
      entry = `$${fmt(d.price, d.dec)}`;
      sl = `$${fmt(Math.min(d.cdl, d.pdl) * 0.997, d.dec)}`;
      narrative = `Liquidity raided below PDL ($${fmt(d.pdl, d.dec)}). Sell stops mitigated. Targeting internal liquidity and PDH.`;
    }
    // RULE 3: Premium / Discount Equilibrium
    else {
      if (d.price > equilibrium) {
        statusText = 'PREMIUM ZONE (BOS RETEST)';
        action = 'WAIT SHORT';
        narrative = `Price trading in Premium array (> 50% EQ). Look for Bearish Order Blocks around PDH for short confirmation.`;
      } else {
        statusText = 'DISCOUNT ZONE (OB REACTION)';
        action = 'WAIT LONG';
        narrative = `Price trading in Discount array (< 50% EQ). High probability bullish demand zone active near PDL.`;
      }
      entry = `EQ: $${fmt(equilibrium, d.dec)}`;
      sl = d.price > equilibrium ? `SL > $${fmt(d.pdh, d.dec)}` : `SL < $${fmt(d.pdl, d.dec)}`;
    }

    // UPDATE SMC UI
    document.getElementById(`${prefix}-smc-state`).innerText = statusText;
    const badgeEl = document.getElementById(`${prefix}-badge`);
    badgeEl.innerText = action;
    badgeEl.className = `setup-badge ${badgeClass}`;

    document.getElementById(`${prefix}-action`).innerText = action;
    document.getElementById(`${prefix}-entry`).innerText = entry;
    document.getElementById(`${prefix}-sl`).innerText = sl;
    document.getElementById(`${prefix}-narrative`).innerText = narrative;

    // LOG TRIGGER
    if (d.lastSignal !== action && action !== 'MONITOR') {
      d.lastSignal = action;
      addLog(`<strong>${sym}</strong> SMC trigger: <strong>${action}</strong> | Entry: ${entry} | SL: ${sl}`);
    }
  }

  function updateUI(sym) {
    const d = state[sym];
    const prefix = sym === 'BTCUSD' ? 'btc' : 'eth';

    if (d.pdh) document.getElementById(`${prefix}-pdh`).innerText = '$' + fmt(d.pdh, d.dec);
    if (d.pdl) document.getElementById(`${prefix}-pdl`).innerText = '$' + fmt(d.pdl, d.dec);
    if (d.cdh) document.getElementById(`${prefix}-cdh`).innerText = '$' + fmt(d.cdh, d.dec);
    if (d.cdl) document.getElementById(`${prefix}-cdl`).innerText = '$' + fmt(d.cdl, d.dec);

    if (d.spot) document.getElementById(`${prefix}-spot`).innerText = '$' + fmt(d.spot, d.dec);
    if (d.vol) document.getElementById(`${prefix}-vol`).innerText = fmt(d.vol, 0);

    if (d.price && d.pdh) {
      const diffPDH = d.price - d.pdh;
      const elPDH = document.getElementById(`${prefix}-dist-pdh`);
      elPDH.innerText = (diffPDH >= 0 ? '+' : '') + fmt(diffPDH, d.dec);
      elPDH.className = diffPDH >= 0 ? 'dist-pos' : 'dist-neg';
    }

    if (d.price && d.pdl) {
      const diffPDL = d.price - d.pdl;
      const elPDL = document.getElementById(`${prefix}-dist-pdl`);
      elPDL.innerText = (diffPDL >= 0 ? '+' : '') + fmt(diffPDL, d.dec);
      elPDL.className = diffPDL >= 0 ? 'dist-pos' : 'dist-neg';
    }
  }

  // DIRECT CLIENT WEBSOCKET
  function connectWS() {
    const ws = new WebSocket("wss://socket.india.delta.exchange");

    ws.onopen = () => {
      addLog("Connected to Delta WebSocket live stream.");
      ws.send(JSON.stringify({
        type: "subscribe",
        payload: {
          channels: [{ name: "v2/ticker", symbols: ["BTCUSD", "ETHUSD"] }]
        }
      }));
    };

    ws.onmessage = (evt) => {
      const msg = JSON.parse(evt.data);
      const sym = msg.symbol;
      if (sym && state[sym]) {
        const d = state[sym];
        const newPrice = parseFloat(msg.mark_price || msg.close || 0);

        if (newPrice > 0) {
          const pEl = document.getElementById(sym === 'BTCUSD' ? 'btc-price' : 'eth-price');
          if (d.price && newPrice !== d.price) {
            pEl.classList.remove('price-up', 'price-down');
            void pEl.offsetWidth;
            pEl.classList.add(newPrice > d.price ? 'price-up' : 'price-down');
          }

          d.price = newPrice;
          pEl.innerText = '$' + fmt(newPrice, d.dec);

          if (!d.cdh || newPrice > d.cdh) d.cdh = newPrice;
          if (!d.cdl || newPrice < d.cdl) d.cdl = newPrice;

          evaluateSMC(sym);
        }

        if (msg.spot_price) d.spot = parseFloat(msg.spot_price);
        if (msg.volume) d.vol = parseFloat(msg.volume);

        updateUI(sym);
      }
    };

    ws.onclose = () => {
      addLog("WebSocket disconnected. Retrying in 2 seconds...");
      setTimeout(connectWS, 2000);
    };
  }

  fetchDailyStats();
  setInterval(fetchDailyStats, 60000);
  connectWS();
</script>
</body>
</html>
"""

components.html(terminal_html, height=920, scrolling=True)
