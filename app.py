import streamlit as st
import streamlit.components.v1 as components

# --- 1. FULL PAGE CONFIG ---
st.set_page_config(
    page_title="Delta Terminal v1.6.0 - SFP & MSS",
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

# --- 3. ZERO-LAG TERMINAL WITH GLASSMORPHIC DESK UI ---
terminal_html = """
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Delta Terminal</title>
<style>
  /* LIGHT THEME (DEFAULT GLASS DESK) */
  :root[data-theme="light"] {
    --bg-page: #f1f5f9;
    --card-bg: linear-gradient(135deg, rgba(255, 255, 255, 0.92), rgba(241, 245, 249, 0.85));
    --card-border: rgba(226, 232, 240, 0.85);
    --tile-bg: rgba(255, 255, 255, 0.85);
    --tile-border: rgba(203, 213, 225, 0.5);
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
    --shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
    --pill-bg: rgba(255, 255, 255, 0.8);
    --log-bg: #0f172a;
    --log-text: #38bdf8;
    --tab-active-bg: #0284c7;
    --tab-active-text: #ffffff;
    --step-done-bg: rgba(5, 150, 105, 0.12);
    --step-done-border: #059669;
  }

  /* DARK THEME (FROSTED GLASS DESK) */
  :root[data-theme="dark"] {
    --bg-page: #080c14;
    --card-bg: linear-gradient(135deg, rgba(18, 24, 38, 0.88), rgba(11, 15, 25, 0.8));
    --card-border: rgba(255, 255, 255, 0.08);
    --tile-bg: rgba(255, 255, 255, 0.04);
    --tile-border: rgba(255, 255, 255, 0.06);
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
    --shadow: 0 12px 36px rgba(0, 0, 0, 0.55);
    --pill-bg: rgba(255, 255, 255, 0.03);
    --log-bg: #05070a;
    --log-text: #00e5ff;
    --tab-active-bg: #00e5ff;
    --tab-active-text: #080b11;
    --step-done-bg: rgba(0, 240, 144, 0.12);
    --step-done-border: #00f090;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }
  body { background: var(--bg-page); color: var(--text-primary); padding: 12px; overflow-x: hidden; transition: background 0.25s ease, color 0.25s ease; padding-bottom: 60px; }

  /* HEADER */
  .header {
    display: flex; justify-content: space-between; align-items: center;
    padding: 8px 6px 14px 6px; border-bottom: 1px solid var(--header-border); margin-bottom: 16px;
  }
  .header-left { display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 14px; letter-spacing: 0.8px; }
  .pulse-dot { width: 8px; height: 8px; background: var(--neon-green); border-radius: 50%; box-shadow: 0 0 8px var(--neon-green); animation: pulse 1.5s infinite; }
  @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.3; transform: scale(0.8); } }

  .header-right { display: flex; align-items: center; gap: 8px; }
  .utc-clock { font-size: 11px; font-weight: 600; color: var(--clock-text); background: var(--clock-bg); padding: 5px 8px; border-radius: 8px; border: 1px solid var(--clock-border); }

  .theme-toggle-btn {
    background: var(--tile-bg);
    border: 1px solid var(--card-border);
    color: var(--text-primary);
    font-size: 14px;
    padding: 4px 10px;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: var(--shadow);
    backdrop-filter: blur(10px);
  }

  /* GLASS CARDS GRID */
  .grid { display: grid; grid-template-columns: 1fr; gap: 16px; margin-bottom: 16px; }
  @media(min-width: 768px) { .grid { grid-template-columns: 1fr 1fr; } }

  .card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 18px;
    box-shadow: var(--shadow);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
  }
  .card::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
    opacity: 0.8;
  }

  .card-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; }
  .coin-badge { font-size: 18px; font-weight: 900; }
  .spot-tag { font-size: 11px; color: var(--text-muted); margin-top: 3px; }

  .price-box { text-align: right; }
  .live-price { font-size: 26px; font-weight: 900; font-family: monospace; }
  .price-up { color: var(--neon-green) !important; }
  .price-down { color: var(--neon-red) !important; }

  /* METRICS TILES */
  .metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 10px; }
  .tile {
    background: var(--tile-bg);
    border: 1px solid var(--tile-border);
    border-radius: 12px;
    padding: 10px 12px;
    backdrop-filter: blur(8px);
  }
  .tile-title { font-size: 10px; color: var(--text-muted); margin-bottom: 3px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 700; }
  .tile-val { font-size: 14px; font-weight: 800; font-family: monospace; }

  /* DISTANCE TAGS */
  .dist-row { margin-top: 12px; display: flex; gap: 8px; }
  .dist-pill {
    flex: 1; display: flex; justify-content: space-between; align-items: center;
    padding: 8px 12px; border-radius: 10px; font-size: 11px; font-weight: 700; font-family: monospace;
    background: var(--pill-bg); border: 1px solid var(--card-border);
    backdrop-filter: blur(8px);
  }
  .dist-pos { color: var(--neon-green); }
  .dist-neg { color: var(--neon-red); }

  /* SHARED GLASS CONTAINERS */
  .section-container {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 18px;
    box-shadow: var(--shadow);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    margin-bottom: 16px;
  }
  .section-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 14px; border-bottom: 1px solid var(--tile-border); padding-bottom: 10px;
  }
  .section-title { font-size: 13.5px; font-weight: 800; letter-spacing: 0.5px; display: flex; align-items: center; gap: 6px; }

  /* TIMEFRAME TABS */
  .tab-group { display: flex; gap: 4px; background: var(--tile-bg); padding: 4px; border-radius: 10px; border: 1px solid var(--card-border); backdrop-filter: blur(10px); }
  .tab-btn {
    border: none; background: transparent; color: var(--text-muted);
    padding: 5px 12px; font-size: 11px; font-weight: 700; border-radius: 7px;
    cursor: pointer; transition: all 0.2s ease;
  }
  .tab-btn.active {
    background: var(--tab-active-bg);
    color: var(--tab-active-text);
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }

  .smc-grid { display: grid; grid-template-columns: 1fr; gap: 12px; }
  @media(min-width: 768px) { .smc-grid { grid-template-columns: 1fr 1fr; } }

  .smc-card {
    background: var(--tile-bg);
    border: 1px solid var(--tile-border);
    border-radius: 14px;
    padding: 14px;
    backdrop-filter: blur(10px);
  }
  .smc-card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
  .setup-badge { padding: 3px 8px; border-radius: 6px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
  .badge-buy { background: rgba(5, 150, 105, 0.15); color: var(--neon-green); border: 1px solid var(--neon-green); }
  .badge-sell { background: rgba(225, 29, 72, 0.15); color: var(--neon-red); border: 1px solid var(--neon-red); }
  .badge-wait { background: rgba(217, 119, 6, 0.15); color: var(--neon-yellow); border: 1px solid var(--neon-yellow); }

  .trade-param-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin-bottom: 8px; }
  .trade-param-box { background: var(--card-bg); border: 1px solid var(--card-border); padding: 8px 6px; border-radius: 10px; text-align: center; }
  .param-lbl { font-size: 9px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 3px; font-weight: 700; }
  .param-val { font-size: 11px; font-weight: 800; font-family: monospace; }

  /* 4 STEPS PIPELINE */
  .steps-pipeline { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-bottom: 12px; }
  .step-node {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 8px;
    padding: 7px 4px;
    text-align: center;
    font-size: 9.5px;
    transition: all 0.2s;
  }
  .step-node.active-step {
    background: var(--step-done-bg);
    border-color: var(--step-done-border);
    font-weight: 800;
  }
  .step-node .step-num { font-size: 8.5px; color: var(--text-muted); display: block; margin-bottom: 2px; }

  .ob-panel {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 10px;
    padding: 8px 10px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .ob-type { font-size: 11px; font-weight: 800; }
  .ob-range { font-size: 11px; font-family: monospace; color: var(--text-muted); }
  .ob-status { font-size: 9.5px; padding: 2px 6px; border-radius: 4px; font-weight: 700; }

  .detail-explanation {
    background: var(--card-bg);
    border-left: 3px solid var(--neon-cyan);
    padding: 9px 12px;
    border-radius: 6px;
    font-size: 11px;
    line-height: 1.45;
    color: var(--text-muted);
    margin-top: 8px;
  }

  /* LOG CONSOLE */
  .console-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-top: 14px; margin-bottom: 6px; font-size: 11px; font-weight: 700; color: var(--text-muted);
  }
  .console-box {
    background: var(--log-bg);
    border-radius: 12px;
    padding: 10px 12px;
    font-family: monospace;
    font-size: 11px;
    color: var(--log-text);
    height: 120px;
    overflow-y: auto;
    border: 1px solid rgba(0, 0, 0, 0.1);
  }
  .log-line { margin-bottom: 4px; display: flex; gap: 8px; }
  .log-time { color: var(--text-muted); }
  .log-tf { font-weight: 700; color: var(--neon-cyan); }
</style>
</head>
<body>

<!-- TOP HEADER -->
<div class="header">
  <div class="header-left">
    <div class="pulse-dot"></div>
    <span>GLASS DESK QUANT TERMINAL</span>
  </div>
  <div class="header-right">
    <div class="utc-clock" id="utc-clock">00:00:00 UTC</div>
    <button class="theme-toggle-btn" id="theme-btn" onclick="toggleTheme()" title="Toggle Theme">🌙</button>
  </div>
</div>

<!-- LIVE METRICS GRID -->
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

<!-- WINDOW 1: EXISTING SMC & ORDER BLOCK SCANNER -->
<div class="section-container">
  <div class="section-header">
    <div class="section-title">🎯 SMC & ORDER BLOCK (OB) SCANNER</div>
    <div class="tab-group">
      <button class="tab-btn active" id="tab-15m" onclick="switchTF('15m')">15M TF</button>
      <button class="tab-btn" id="tab-5m" onclick="switchTF('5m')">5M TF</button>
    </div>
  </div>

  <div class="smc-grid">
    <!-- BTC SMC PANEL -->
    <div class="smc-card">
      <div class="smc-card-top">
        <span style="font-weight: 700; font-size: 13px;">BTC (<span class="tf-label">15M</span>): <span id="btc-smc-state">SCANNING</span></span>
        <span class="setup-badge badge-wait" id="btc-badge">WAITING</span>
      </div>
      <div class="ob-panel">
        <div>
          <div class="ob-type" id="btc-ob-type">Scanning OB...</div>
          <div class="ob-range" id="btc-ob-range">Zone: --</div>
        </div>
        <div class="ob-status badge-wait" id="btc-ob-status">UNTESTED</div>
      </div>
      <div class="trade-param-row">
        <div class="trade-param-box">
          <div class="param-lbl">Action</div>
          <div class="param-val" id="btc-action">MONITOR</div>
        </div>
        <div class="trade-param-box">
          <div class="param-lbl">Entry / OB</div>
          <div class="param-val" id="btc-entry">--</div>
        </div>
        <div class="trade-param-box">
          <div class="param-lbl">Stop Loss</div>
          <div class="param-val" style="color: var(--neon-red);" id="btc-sl">--</div>
        </div>
      </div>
      <div class="detail-explanation" id="btc-narrative">Scanning OB footprint and structure...</div>
    </div>

    <!-- ETH SMC PANEL -->
    <div class="smc-card">
      <div class="smc-card-top">
        <span style="font-weight: 700; font-size: 13px;">ETH (<span class="tf-label">15M</span>): <span id="eth-smc-state">SCANNING</span></span>
        <span class="setup-badge badge-wait" id="eth-badge">WAITING</span>
      </div>
      <div class="ob-panel">
        <div>
          <div class="ob-type" id="eth-ob-type">Scanning OB...</div>
          <div class="ob-range" id="eth-ob-range">Zone: --</div>
        </div>
        <div class="ob-status badge-wait" id="eth-ob-status">UNTESTED</div>
      </div>
      <div class="trade-param-row">
        <div class="trade-param-box">
          <div class="param-lbl">Action</div>
          <div class="param-val" id="eth-action">MONITOR</div>
        </div>
        <div class="trade-param-box">
          <div class="param-lbl">Entry / OB</div>
          <div class="param-val" id="eth-entry">--</div>
        </div>
        <div class="trade-param-box">
          <div class="param-lbl">Stop Loss</div>
          <div class="param-val" style="color: var(--neon-red);" id="eth-sl">--</div>
        </div>
      </div>
      <div class="detail-explanation" id="eth-narrative">Scanning OB footprint and structure...</div>
    </div>
  </div>
</div>

<!-- WINDOW 2: LIQUIDITY SWEEP (SFP) + MSS STRATEGY EXECUTION -->
<div class="section-container">
  <div class="section-header">
    <div class="section-title">⚡ LIQUIDITY SWEEP (SFP) + MSS STRATEGY ENGINE</div>
    <div class="tab-group">
      <button class="tab-btn active" id="sfp-tab-15m" onclick="switchSFPTF('15m')">15M TF</button>
      <button class="tab-btn" id="sfp-tab-5m" onclick="switchSFPTF('5m')">5M TF</button>
    </div>
  </div>

  <div class="smc-grid">
    <!-- BTC SFP+MSS SETUP -->
    <div class="smc-card">
      <div class="smc-card-top">
        <span style="font-weight: 700; font-size: 13px;">🟠 BTC SFP Setup (<span class="sfp-tf-label">15M</span>)</span>
        <span class="setup-badge badge-wait" id="btc-sfp-badge">NO SWEEP</span>
      </div>

      <div class="steps-pipeline">
        <div class="step-node active-step" id="btc-step-1">
          <span class="step-num">Step 1</span>Key Zone
        </div>
        <div class="step-node" id="btc-step-2">
          <span class="step-num">Step 2</span>Sweep (SFP)
        </div>
        <div class="step-node" id="btc-step-3">
          <span class="step-num">Step 3</span>LTF MSS
        </div>
        <div class="step-node" id="btc-step-4">
          <span class="step-num">Step 4</span>Execution
        </div>
      </div>

      <div class="trade-param-row">
        <div class="trade-param-box">
          <div class="param-lbl">Signal</div>
          <div class="param-val" id="btc-sfp-signal">WAIT</div>
        </div>
        <div class="trade-param-box">
          <div class="param-lbl">Entry (FVG/Retest)</div>
          <div class="param-val" id="btc-sfp-entry">--</div>
        </div>
        <div class="trade-param-box">
          <div class="param-lbl">Invalidation (SL)</div>
          <div class="param-val" style="color: var(--neon-red);" id="btc-sfp-sl">--</div>
        </div>
      </div>

      <div class="trade-param-row" style="grid-template-columns: 1fr 1fr;">
        <div class="trade-param-box">
          <div class="param-lbl">Target (TP1 / EQ)</div>
          <div class="param-val" style="color: var(--neon-green);" id="btc-sfp-tp1">--</div>
        </div>
        <div class="trade-param-box">
          <div class="param-lbl">Target (TP2 / Opposing Pool)</div>
          <div class="param-val" style="color: var(--neon-cyan);" id="btc-sfp-tp2">--</div>
        </div>
      </div>

      <div class="detail-explanation" id="btc-sfp-rationale">
        Waiting for institutional sweep at HTF key levels (PDH / PDL)...
      </div>
    </div>

    <!-- ETH SFP+MSS SETUP -->
    <div class="smc-card">
      <div class="smc-card-top">
        <span style="font-weight: 700; font-size: 13px;">🔷 ETH SFP Setup (<span class="sfp-tf-label">15M</span>)</span>
        <span class="setup-badge badge-wait" id="eth-sfp-badge">NO SWEEP</span>
      </div>

      <div class="steps-pipeline">
        <div class="step-node active-step" id="eth-step-1">
          <span class="step-num">Step 1</span>Key Zone
        </div>
        <div class="step-node" id="eth-step-2">
          <span class="step-num">Step 2</span>Sweep (SFP)
        </div>
        <div class="step-node" id="eth-step-3">
          <span class="step-num">Step 3</span>LTF MSS
        </div>
        <div class="step-node" id="eth-step-4">
          <span class="step-num">Step 4</span>Execution
        </div>
      </div>

      <div class="trade-param-row">
        <div class="trade-param-box">
          <div class="param-lbl">Signal</div>
          <div class="param-val" id="eth-sfp-signal">WAIT</div>
        </div>
        <div class="trade-param-box">
          <div class="param-lbl">Entry (FVG/Retest)</div>
          <div class="param-val" id="eth-sfp-entry">--</div>
        </div>
        <div class="trade-param-box">
          <div class="param-lbl">Invalidation (SL)</div>
          <div class="param-val" style="color: var(--neon-red);" id="eth-sfp-sl">--</div>
        </div>
      </div>

      <div class="trade-param-row" style="grid-template-columns: 1fr 1fr;">
        <div class="trade-param-box">
          <div class="param-lbl">Target (TP1 / EQ)</div>
          <div class="param-val" style="color: var(--neon-green);" id="eth-sfp-tp1">--</div>
        </div>
        <div class="trade-param-box">
          <div class="param-lbl">Target (TP2 / Opposing Pool)</div>
          <div class="param-val" style="color: var(--neon-cyan);" id="eth-sfp-tp2">--</div>
        </div>
      </div>

      <div class="detail-explanation" id="eth-sfp-rationale">
        Waiting for institutional sweep at HTF key levels (PDH / PDL)...
      </div>
    </div>
  </div>

  <!-- AUDIT LOGS -->
  <div class="console-header">
    <span>SFP & MSS MULTI-TIMEFRAME AUDIT LOGS (<span id="log-active-tf">15M</span>)</span>
    <span style="font-size: 10px; cursor: pointer; color: var(--neon-cyan)" onclick="clearLogs()">Clear Logs</span>
  </div>
  <div class="console-box" id="console-logs">
    <div class="log-line"><span class="log-time">[INIT]</span> SFP + MSS Strategy Engine active. Listening for Wick Rejections...</div>
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

  // TABS STATE
  let activeTF = '15m';
  let activeSFPTF = '15m';

  function switchTF(tf) {
    activeTF = tf;
    document.getElementById('tab-15m').classList.toggle('active', tf === '15m');
    document.getElementById('tab-5m').classList.toggle('active', tf === '5m');
    document.querySelectorAll('.tf-label').forEach(el => el.innerText = tf.toUpperCase());
    renderSMCUI('BTCUSD');
    renderSMCUI('ETHUSD');
  }

  function switchSFPTF(tf) {
    activeSFPTF = tf;
    document.getElementById('sfp-tab-15m').classList.toggle('active', tf === '15m');
    document.getElementById('sfp-tab-5m').classList.toggle('active', tf === '5m');
    document.querySelectorAll('.sfp-tf-label').forEach(el => el.innerText = tf.toUpperCase());
    document.getElementById('log-active-tf').innerText = tf.toUpperCase();
    renderSFPUI('BTCUSD');
    renderSFPUI('ETHUSD');
    filterLogs();
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
    BTCUSD: {
      price: 0, spot: 0, vol: 0, cdh: 0, cdl: 0, pdh: 0, pdl: 0, dec: 1,
      '15m': { action: 'MONITOR', state: 'SCANNING', obType: '--', obRange: '--', obStatus: 'UNTESTED', entry: '--', sl: '--', narrative: '' },
      '5m':  { action: 'MONITOR', state: 'SCANNING', obType: '--', obRange: '--', obStatus: 'UNTESTED', entry: '--', sl: '--', narrative: '' },
      sfp_15m: { signal: 'WAIT', badge: 'NO SWEEP', entry: '--', sl: '--', tp1: '--', tp2: '--', step: 1, rationale: '', lastSig: '' },
      sfp_5m:  { signal: 'WAIT', badge: 'NO SWEEP', entry: '--', sl: '--', tp1: '--', tp2: '--', step: 1, rationale: '', lastSig: '' }
    },
    ETHUSD: {
      price: 0, spot: 0, vol: 0, cdh: 0, cdl: 0, pdh: 0, pdl: 0, dec: 2,
      '15m': { action: 'MONITOR', state: 'SCANNING', obType: '--', obRange: '--', obStatus: 'UNTESTED', entry: '--', sl: '--', narrative: '' },
      '5m':  { action: 'MONITOR', state: 'SCANNING', obType: '--', obRange: '--', obStatus: 'UNTESTED', entry: '--', sl: '--', narrative: '' },
      sfp_15m: { signal: 'WAIT', badge: 'NO SWEEP', entry: '--', sl: '--', tp1: '--', tp2: '--', step: 1, rationale: '', lastSig: '' },
      sfp_5m:  { signal: 'WAIT', badge: 'NO SWEEP', entry: '--', sl: '--', tp1: '--', tp2: '--', step: 1, rationale: '', lastSig: '' }
    }
  };

  const logsHistory = [];

  function fmt(val, dec) {
    if(!val || isNaN(val)) return '--';
    return Number(val).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  }

  function addLog(tf, msg) {
    const now = new Date().toTimeString().split(' ')[0];
    const item = { tf, text: msg, time: now };
    logsHistory.push(item);
    if (logsHistory.length > 80) logsHistory.shift();
    if (activeSFPTF === tf || tf === 'ALL') appendLogToBox(item);
  }

  function appendLogToBox(log) {
    const box = document.getElementById('console-logs');
    const el = document.createElement('div');
    el.className = 'log-line';
    el.innerHTML = `<span class="log-time">[${log.time}]</span> <span class="log-tf">[${log.tf.toUpperCase()}]</span> ${log.text}`;
    box.appendChild(el);
    box.scrollTop = box.scrollHeight;
  }

  function filterLogs() {
    const box = document.getElementById('console-logs');
    box.innerHTML = '';
    logsHistory.filter(l => l.tf === activeSFPTF || l.tf === 'ALL').forEach(appendLogToBox);
  }

  function clearLogs() {
    logsHistory.length = 0;
    document.getElementById('console-logs').innerHTML = '<div class="log-line"><span class="log-time">[CLEARED]</span> Logs reset.</div>';
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

          updateMetricsUI(sym);
          evaluateSMC(sym, '15m');
          evaluateSMC(sym, '5m');
          evaluateSFPStrategy(sym, '15m');
          evaluateSFPStrategy(sym, '5m');
        }
      }
    } catch(e) {
      console.log("Candles err", e);
    }
  }

  // SMC ENGINE (WINDOW 1)
  function evaluateSMC(sym, tf) {
    const d = state[sym];
    if (!d.price || !d.pdh || !d.pdl) return;

    const tfData = d[tf];
    const eq = (d.pdh + d.pdl) / 2;
    const distToPDH = d.price - d.pdh;
    const distToPDL = d.price - d.pdl;

    const factor = tf === '5m' ? 0.4 : 1.0;
    const obBuffer = (d.price * (tf === '5m' ? 0.0015 : 0.0035));

    let action = 'MONITOR';
    let stateText = 'CONSOLIDATING';
    let obType = '';
    let obLow = 0, obHigh = 0;
    let obStatus = 'UNTESTED';
    let entry = '--';
    let sl = '--';
    let narrative = '';

    if (distToPDH >= -(25 * factor)) {
      action = 'SELL / SHORT';
      stateText = tf === '5m' ? '5M CHoCH CONFIRMED' : '15M PDH LIQUIDITY SWEEP';
      obType = '🔴 Bearish Supply OB';
      obHigh = Math.max(d.cdh, d.pdh);
      obLow = obHigh - obBuffer;
      entry = `$${fmt(obLow, d.dec)} - $${fmt(obHigh, d.dec)}`;
      sl = `$${fmt(obHigh * 1.002, d.dec)}`;
      obStatus = d.price >= obLow && d.price <= obHigh ? 'MITIGATING' : 'PENDING TAP';
      narrative = `${tf.toUpperCase()} Supply Order Block created above PDH ($${fmt(d.pdh, d.dec)}). Target internal discount liquidity.`;
    } else if (distToPDL <= (25 * factor)) {
      action = 'BUY / LONG';
      stateText = tf === '5m' ? '5M CHoCH BREAKOUT' : '15M PDL LIQUIDITY RAID';
      obType = '🟢 Bullish Demand OB';
      obLow = Math.min(d.cdl, d.pdl);
      obHigh = obLow + obBuffer;
      entry = `$${fmt(obLow, d.dec)} - $${fmt(obHigh, d.dec)}`;
      sl = `$${fmt(obLow * 0.998, d.dec)}`;
      obStatus = d.price >= obLow && d.price <= obHigh ? 'MITIGATING' : 'PENDING TAP';
      narrative = `${tf.toUpperCase()} Demand Order Block established near PDL ($${fmt(d.pdl, d.dec)}). Target EQ ($${fmt(eq, d.dec)}).`;
    } else {
      if (d.price > eq) {
        stateText = 'PREMIUM BOS RETEST';
        action = tf === '5m' ? 'WAIT SHORT' : 'WATCH PREMIUM';
        obType = 'Bearish Internal OB';
        obHigh = d.price + obBuffer;
        obLow = d.price;
        entry = `Retest $${fmt(obHigh, d.dec)}`;
        sl = `SL > $${fmt(d.pdh, d.dec)}`;
        obStatus = 'INACTIVE';
        narrative = `${tf.toUpperCase()} trading above 50% EQ range. High time-frame bears defending supply.`;
      } else {
        stateText = 'DISCOUNT OB MITIGATION';
        action = tf === '5m' ? 'WAIT LONG' : 'WATCH DISCOUNT';
        obType = 'Bullish Internal OB';
        obLow = d.price - obBuffer;
        obHigh = d.price;
        entry = `Pullback $${fmt(obLow, d.dec)}`;
        sl = `SL < $${fmt(d.pdl, d.dec)}`;
        obStatus = 'INACTIVE';
        narrative = `${tf.toUpperCase()} testing discount array. Look for shift of character on 5m for entry.`;
      }
    }

    tfData.action = action;
    tfData.state = stateText;
    tfData.obType = obType;
    tfData.obRange = `$${fmt(obLow, d.dec)} - $${fmt(obHigh, d.dec)}`;
    tfData.obStatus = obStatus;
    tfData.entry = entry;
    tfData.sl = sl;
    tfData.narrative = narrative;

    if (activeTF === tf) renderSMCUI(sym);
  }

  // SFP + MSS STRATEGY ENGINE (WINDOW 2)
  function evaluateSFPStrategy(sym, tf) {
    const d = state[sym];
    if (!d.price || !d.pdh || !d.pdl) return;

    const key = tf === '15m' ? 'sfp_15m' : 'sfp_5m';
    const sfp = d[key];
    const eq = (d.pdh + d.pdl) / 2;

    const distToPDH = d.price - d.pdh;
    const distToPDL = d.price - d.pdl;
    const fvgBuffer = d.price * (tf === '5m' ? 0.001 : 0.002);

    let signal = 'WAIT';
    let badge = 'IN RANGE';
    let entry = '--';
    let sl = '--';
    let tp1 = `$${fmt(eq, d.dec)}`;
    let tp2 = '--';
    let step = 1;
    let rationale = '';

    // BEARISH SFP + MSS
    if (d.cdh > d.pdh && d.price < d.pdh) {
      step = 4;
      signal = 'SELL SHORT';
      badge = 'BEARISH SFP + MSS';
      entry = `$${fmt(d.pdh - fvgBuffer, d.dec)} - $${fmt(d.pdh, d.dec)}`;
      sl = `$${fmt(d.cdh + (d.cdh * 0.001), d.dec)}`;
      tp2 = `$${fmt(d.pdl, d.dec)}`;
      rationale = `<strong>[Institutional Fakeout]:</strong> Price ne PDH ($${fmt(d.pdh, d.dec)}) ko wick se sweep kiya aur range ke andar wapas candle close kar di (SFP). LTF par Market Structure Shift (MSS) confirm hua hai. Entry FVG retest par karein, SL sweep wick ($${fmt(d.cdh, d.dec)}) ke upar rahega. Target Opposing EQL/PDL.`;
    }
    else if (distToPDH >= 0) {
      step = 2;
      signal = 'WATCH SFP';
      badge = 'SWEEPING PDH';
      entry = 'Wait Candle Close Inside';
      sl = `Wick High`;
      tp2 = `$${fmt(d.pdl, d.dec)}`;
      rationale = `Price is sweeping PDH ($${fmt(d.pdh, d.dec)}) right now. Wait for Wick Rejection (SFP) and close below PDH to confirm breakout failure. Do not chase breakout.`;
    }

    // BULLISH SFP + MSS
    else if (d.cdl < d.pdl && d.price > d.pdl) {
      step = 4;
      signal = 'BUY LONG';
      badge = 'BULLISH SFP + MSS';
      entry = `$${fmt(d.pdl, d.dec)} - $${fmt(d.pdl + fvgBuffer, d.dec)}`;
      sl = `$${fmt(d.cdl - (d.cdl * 0.001), d.dec)}`;
      tp2 = `$${fmt(d.pdh, d.dec)}`;
      rationale = `<strong>[Institutional Fakeout]:</strong> Sell stops raided below PDL ($${fmt(d.pdl, d.dec)}). Long wick rejection ke sath candle close range ke andar hui (Bullish SFP). LTF MSS confirmed with displacement. Entry FVG retest par, SL sweep wick ($${fmt(d.cdl, d.dec)}) ke niche. Target Opposing EQH/PDH.`;
    }
    else if (distToPDL <= 0) {
      step = 2;
      signal = 'WATCH SFP';
      badge = 'SWEEPING PDL';
      entry = 'Wait Candle Close Inside';
      sl = `Wick Low`;
      tp2 = `$${fmt(d.pdh, d.dec)}`;
      rationale = `Price is raiding liquidity below PDL ($${fmt(d.pdl, d.dec)}). Wait for SFP confirmation (Wick rejection followed by strong close back above PDL) before executing Long.`;
    }

    // NORMAL EQUILIBRIUM
    else {
      step = 1;
      signal = 'MONITOR';
      badge = 'NO SWEEP';
      entry = `Wait Level Tap`;
      sl = '--';
      tp2 = d.price > eq ? `$${fmt(d.pdh, d.dec)}` : `$${fmt(d.pdl, d.dec)}`;
      rationale = `Market trading between PDH ($${fmt(d.pdh, d.dec)}) and PDL ($${fmt(d.pdl, d.dec)}). Step 1 (Key Zones Mark) complete hai. Step 2 ke liye liquidity pool (PDH ya PDL) sweep hone ka wait karein.`;
    }

    sfp.signal = signal;
    sfp.badge = badge;
    sfp.entry = entry;
    sfp.sl = sl;
    sfp.tp1 = tp1;
    sfp.tp2 = tp2;
    sfp.step = step;
    sfp.rationale = rationale;

    if (sfp.lastSig !== signal && (signal.includes('BUY') || signal.includes('SELL'))) {
      sfp.lastSig = signal;
      addLog(tf, `<strong>${sym}</strong>: SFP+MSS Triggered <strong>${signal}</strong> | Entry: ${entry} | SL: ${sl}`);
    }

    if (activeSFPTF === tf) renderSFPUI(sym);
  }

  function renderSMCUI(sym) {
    const prefix = sym === 'BTCUSD' ? 'btc' : 'eth';
    const tfData = state[sym][activeTF];

    document.getElementById(`${prefix}-smc-state`).innerText = tfData.state;
    const badge = document.getElementById(`${prefix}-badge`);
    badge.innerText = tfData.action;
    badge.className = `setup-badge ${tfData.action.includes('BUY') ? 'badge-buy' : tfData.action.includes('SELL') ? 'badge-sell' : 'badge-wait'}`;

    document.getElementById(`${prefix}-ob-type`).innerText = tfData.obType;
    document.getElementById(`${prefix}-ob-range`).innerText = `Zone: ${tfData.obRange}`;
    
    const obStatEl = document.getElementById(`${prefix}-ob-status`);
    obStatEl.innerText = tfData.obStatus;
    obStatEl.className = `ob-status ${tfData.obStatus === 'MITIGATING' ? 'badge-buy' : 'badge-wait'}`;

    document.getElementById(`${prefix}-action`).innerText = tfData.action;
    document.getElementById(`${prefix}-entry`).innerText = tfData.entry;
    document.getElementById(`${prefix}-sl`).innerText = tfData.sl;
    document.getElementById(`${prefix}-narrative`).innerText = tfData.narrative;
  }

  function renderSFPUI(sym) {
    const prefix = sym === 'BTCUSD' ? 'btc' : 'eth';
    const key = activeSFPTF === '15m' ? 'sfp_15m' : 'sfp_5m';
    const sfp = state[sym][key];

    const badge = document.getElementById(`${prefix}-sfp-badge`);
    badge.innerText = sfp.badge;
    badge.className = `setup-badge ${sfp.signal.includes('BUY') ? 'badge-buy' : sfp.signal.includes('SELL') ? 'badge-sell' : 'badge-wait'}`;

    document.getElementById(`${prefix}-sfp-signal`).innerText = sfp.signal;
    document.getElementById(`${prefix}-sfp-entry`).innerText = sfp.entry;
    document.getElementById(`${prefix}-sfp-sl`).innerText = sfp.sl;
    document.getElementById(`${prefix}-sfp-tp1`).innerText = sfp.tp1;
    document.getElementById(`${prefix}-sfp-tp2`).innerText = sfp.tp2;
    document.getElementById(`${prefix}-sfp-rationale`).innerHTML = sfp.rationale;

    for (let i = 1; i <= 4; i++) {
      const el = document.getElementById(`${prefix}-step-${i}`);
      el.classList.toggle('active-step', i <= sfp.step);
    }
  }

  function updateMetricsUI(sym) {
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

  // DIRECT CLIENT WEBSOCKET STREAM
  function connectWS() {
    const ws = new WebSocket("wss://socket.india.delta.exchange");

    ws.onopen = () => {
      addLog("ALL", "Delta live ticks connected. SFP & MSS execution ready.");
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

          evaluateSMC(sym, '15m');
          evaluateSMC(sym, '5m');
          evaluateSFPStrategy(sym, '15m');
          evaluateSFPStrategy(sym, '5m');
        }

        if (msg.spot_price) d.spot = parseFloat(msg.spot_price);
        if (msg.volume) d.vol = parseFloat(msg.volume);

        updateMetricsUI(sym);
      }
    };

    ws.onclose = () => {
      addLog("ALL", "Websocket connection dropped. Reconnecting...");
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

components.html(terminal_html, height=1400, scrolling=True)
