import streamlit as st
import streamlit.components.v1 as components

# --- 1. FULL PAGE CONFIG ---
st.set_page_config(
    page_title="Delta Terminal v1.2.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. KILL ALL STREAMLIT BARS / HEADERS / MANAGE APP ---
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

# --- 3. HIGH-TECH FRONTEND TERMINAL (CLIENT-SIDE WEBSOCKET = ZERO LAG TICK BY TICK) ---
terminal_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Delta Terminal</title>
<style>
  :root {
    --bg-dark: #080b11;
    --card-bg: rgba(18, 24, 38, 0.7);
    --card-border: rgba(255, 255, 255, 0.08);
    --neon-green: #00f090;
    --neon-red: #ff3366;
    --neon-cyan: #00e5ff;
    --neon-yellow: #ffb800;
    --text-primary: #ffffff;
    --text-muted: #8b9bb4;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }
  body { background: var(--bg-dark); color: var(--text-primary); padding: 12px; overflow-x: hidden; }

  .header {
    display: flex; justify-content: space-between; align-items: center;
    padding: 6px 12px 14px 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.06); margin-bottom: 14px;
  }
  .header-left { display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 15px; letter-spacing: 1px; color: #fff; }
  .pulse-dot { width: 8px; height: 8px; background: var(--neon-green); border-radius: 50%; box-shadow: 0 0 8px var(--neon-green); animation: pulse 1.5s infinite; }
  @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.3; transform: scale(0.8); } }
  .utc-clock { font-size: 12px; color: var(--neon-cyan); background: rgba(0, 229, 255, 0.08); padding: 4px 8px; border-radius: 6px; border: 1px solid rgba(0, 229, 255, 0.2); }

  /* CARDS */
  .grid { display: grid; grid-template-columns: 1fr; gap: 14px; }
  @media(min-width: 768px) { .grid { grid-template-columns: 1fr 1fr; } }

  .card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
  }
  .card::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
    opacity: 0.5;
  }

  .card-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; }
  .coin-meta { display: flex; align-items: center; gap: 8px; }
  .coin-badge { font-size: 18px; font-weight: 800; }
  .spot-tag { font-size: 11px; color: var(--text-muted); }

  .price-box { text-align: right; }
  .live-price { font-size: 26px; font-weight: 800; font-family: monospace; transition: color 0.15s ease; }
  .price-up { color: var(--neon-green) !important; text-shadow: 0 0 12px rgba(0, 240, 144, 0.4); }
  .price-down { color: var(--neon-red) !important; text-shadow: 0 0 12px rgba(255, 51, 102, 0.4); }

  /* LEVEL TILES */
  .metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }
  .tile {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 10px;
    padding: 10px;
  }
  .tile-title { font-size: 11px; color: var(--text-muted); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
  .tile-val { font-size: 14px; font-weight: 700; font-family: monospace; }

  /* DISTANCE TAGS */
  .dist-row { margin-top: 12px; display: flex; gap: 8px; }
  .dist-pill {
    flex: 1; display: flex; justify-content: space-between; align-items: center;
    padding: 8px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; font-family: monospace;
    background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.06);
  }
  .dist-pos { color: var(--neon-green); }
  .dist-neg { color: var(--neon-red); }
</style>
</head>
<body>

<div class="header">
  <div class="header-left">
    <div class="pulse-dot"></div>
    <span>DELTA QUANT TICK FEED</span>
  </div>
  <div class="utc-clock" id="utc-clock">00:00:00 UTC</div>
</div>

<div class="grid">
  <!-- BTC CARD -->
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

  <!-- ETH CARD -->
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

<script>
  // Clock update
  function updateClock() {
    const now = new Date();
    document.getElementById('utc-clock').innerText = now.toUTCString().split(' ')[4] + ' UTC';
  }
  setInterval(updateClock, 1000);
  updateClock();

  // State
  const state = {
    BTCUSD: { price: 0, last: 0, spot: 0, vol: 0, cdh: 0, cdl: 0, pdh: 0, pdl: 0, dec: 1 },
    ETHUSD: { price: 0, last: 0, spot: 0, vol: 0, cdh: 0, cdl: 0, pdh: 0, pdl: 0, dec: 2 }
  };

  function fmt(val, dec) {
    if(!val || isNaN(val)) return '--';
    return Number(val).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  }

  // Fetch PDH/PDL and Daily Baseline from Delta REST API
  async function fetchDailyStats() {
    try {
      const symbols = ['BTCUSD', 'ETHUSD'];
      for (const sym of symbols) {
        // Delta sparklines/candles endpoint
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
        }
      }
    } catch(e) {
      console.log("Stats fetch err", e);
    }
  }

  function updateUI(sym) {
    const d = state[sym];
    const prefix = sym === 'BTCUSD' ? 'btc' : 'eth';

    // PDH / PDL / CDH / CDL
    if (d.pdh) document.getElementById(`${prefix}-pdh`).innerText = '$' + fmt(d.pdh, d.dec);
    if (d.pdl) document.getElementById(`${prefix}-pdl`).innerText = '$' + fmt(d.pdl, d.dec);
    if (d.cdh) document.getElementById(`${prefix}-cdh`).innerText = '$' + fmt(d.cdh, d.dec);
    if (d.cdl) document.getElementById(`${prefix}-cdl`).innerText = '$' + fmt(d.cdl, d.dec);

    if (d.spot) document.getElementById(`${prefix}-spot`).innerText = '$' + fmt(d.spot, d.dec);
    if (d.vol) document.getElementById(`${prefix}-vol`).innerText = fmt(d.vol, 0);

    // Distance calculation
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

  // Connect Direct Client WebSocket for ZERO LAG
  function connectWS() {
    const ws = new WebSocket("wss://socket.india.delta.exchange");

    ws.onopen = () => {
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
          
          // Tick Animation Flash
          if (d.price && newPrice !== d.price) {
            pEl.classList.remove('price-up', 'price-down');
            void pEl.offsetWidth; // trigger reflow
            pEl.classList.add(newPrice > d.price ? 'price-up' : 'price-down');
          }

          d.price = newPrice;
          pEl.innerText = '$' + fmt(newPrice, d.dec);

          // Dynamic CDH/CDL
          if (!d.cdh || newPrice > d.cdh) d.cdh = newPrice;
          if (!d.cdl || newPrice < d.cdl) d.cdl = newPrice;
        }

        if (msg.spot_price) d.spot = parseFloat(msg.spot_price);
        if (msg.volume) d.vol = parseFloat(msg.volume);

        updateUI(sym);
      }
    };

    ws.onclose = () => setTimeout(connectWS, 2000);
  }

  fetchDailyStats();
  setInterval(fetchDailyStats, 60000); // 1-minute auto sync
  connectWS();
</script>
</body>
</html>
"""

components.html(terminal_html, height=750, scrolling=False)
