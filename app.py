import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Delta Terminal v2 - Card Style",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
header, header[data-testid="stHeader"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
#MainMenu, footer, div[data-testid="stStatusWidget"],
[data-testid="manage-app-button"], button[title="Manage app"],
div[class*="viewerBadge"], div[class*="manage-app"],
div[data-testid="stFloatingActions"] {display:none !important;}

.block-container {
    padding:0 !important;
    margin:0 !important;
    max-width:100% !important;
}
iframe {
    border:none !important;
    width:100% !important;
    height:100vh !important;
}
</style>
""", unsafe_allow_html=True)

terminal_html = r"""
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Delta Terminal</title>

<style>
:root[data-theme="dark"]{
 --bg:#070b12;
 --bg2:#0b111b;
 --card:#0d1521;
 --card2:#111b29;
 --tile:#0a121d;
 --border:rgba(148,163,184,.16);
 --border2:rgba(0,229,255,.20);
 --text:#f4f7fb;
 --muted:#8190a6;
 --cyan:#00d9ff;
 --green:#00e59a;
 --red:#ff426b;
 --yellow:#ffbd3c;
 --blue:#4b9cff;
 --shadow:0 14px 38px rgba(0,0,0,.34);
 --nav:#09111b;
 --console:#03070c;
 --chart-bg:rgba(3,7,12,0.45);
}

:root[data-theme="light"]{
 --bg:#eef3f8;
 --bg2:#f7f9fc;
 --card:#ffffff;
 --card2:#f5f8fb;
 --tile:#f8fafc;
 --border:rgba(15,23,42,.10);
 --border2:rgba(2,132,199,.22);
 --text:#0f172a;
 --muted:#64748b;
 --cyan:#0284c7;
 --green:#059669;
 --red:#e11d48;
 --yellow:#d97706;
 --blue:#2563eb;
 --shadow:0 12px 30px rgba(15,23,42,.08);
 --nav:#ffffff;
 --console:#0b1220;
 --chart-bg:rgba(241,245,249,0.7);
}

*{
 box-sizing:border-box;
 margin:0;
 padding:0;
 font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
}
html{scroll-behavior:smooth}
body{
 background:
   radial-gradient(circle at 15% 0%,rgba(0,217,255,.055),transparent 28%),
   radial-gradient(circle at 90% 15%,rgba(75,156,255,.045),transparent 25%),
   var(--bg);
 color:var(--text);
 min-height:100vh;
 padding:14px;
 padding-bottom:86px;
 overflow-x:hidden;
 transition:.25s;
}
button{font:inherit}

.app{
 width:100%;
 max-width:1420px;
 margin:0 auto;
}

/* HEADER */
.header{
 position:sticky;
 top:0;
 z-index:50;
 display:flex;
 justify-content:space-between;
 align-items:center;
 min-height:58px;
 margin-bottom:14px;
 padding:10px 14px;
 border:1px solid var(--border);
 border-radius:18px;
 background:color-mix(in srgb,var(--card) 92%,transparent);
 backdrop-filter:blur(18px);
 box-shadow:var(--shadow);
}
.brand{
 display:flex;
 align-items:center;
 gap:10px;
 min-width:0;
}
.logo{
 width:34px;height:34px;
 display:grid;place-items:center;
 border-radius:11px;
 background:linear-gradient(135deg,rgba(0,217,255,.18),rgba(75,156,255,.10));
 border:1px solid var(--border2);
 font-size:20px;
}
.brand-title{
 font-weight:900;
 font-size:14px;
 letter-spacing:.8px;
 white-space:nowrap;
}
.brand-sub{
 color:var(--muted);
 font-size:9px;
 margin-top:2px;
 letter-spacing:.7px;
}
.live{
 display:flex;align-items:center;gap:6px;
 color:var(--green);
 font-size:10px;
 font-weight:900;
 padding:6px 9px;
 border:1px solid color-mix(in srgb,var(--green) 35%,transparent);
 background:color-mix(in srgb,var(--green) 8%,transparent);
 border-radius:9px;
}
.live-dot{
 width:7px;height:7px;border-radius:50%;
 background:var(--green);
 box-shadow:0 0 9px var(--green);
 animation:pulse 1.5s infinite;
}
@keyframes pulse{50%{opacity:.35;transform:scale(.75)}}
.header-right{display:flex;align-items:center;gap:8px}
.clock{
 color:var(--cyan);
 font:700 10px monospace;
 padding:6px 8px;
 border-radius:8px;
 background:color-mix(in srgb,var(--cyan) 7%,transparent);
 border:1px solid color-mix(in srgb,var(--cyan) 18%,transparent);
}
.theme-btn{
 width:32px;height:32px;
 border:1px solid var(--border);
 border-radius:10px;
 background:var(--tile);
 color:var(--text);
 cursor:pointer;
}

/* NAV */
.top-nav{
 display:flex;
 gap:5px;
 margin-bottom:14px;
 padding:5px;
 border:1px solid var(--border);
 border-radius:13px;
 background:var(--card);
}
.top-nav button{
 flex:1;
 border:0;
 border-radius:9px;
 padding:8px 5px;
 background:transparent;
 color:var(--muted);
 font-size:10px;
 font-weight:800;
 cursor:pointer;
}
.top-nav button.active{
 color:#fff;
 background:var(--blue);
 box-shadow:0 5px 16px rgba(37,99,235,.24);
}

/* MARKET CARDS */
.market-grid{
 display:grid;
 grid-template-columns:repeat(2,minmax(0,1fr));
 gap:14px;
 margin-bottom:14px;
}
.market-card{
 position:relative;
 overflow:hidden;
 background:linear-gradient(145deg,var(--card),var(--card2));
 border:1px solid var(--border);
 border-radius:20px;
 padding:16px;
 box-shadow:var(--shadow);
}
.market-card:before{
 content:"";
 position:absolute;
 left:0;right:0;top:0;height:2px;
 background:linear-gradient(90deg,transparent,var(--cyan),transparent);
 opacity:.75;
}
.market-head{
 display:flex;
 justify-content:space-between;
 align-items:flex-start;
 gap:10px;
}
.asset{
 display:flex;
 gap:9px;
 align-items:center;
}
.asset-icon{
 width:34px;height:34px;
 display:grid;place-items:center;
 border-radius:11px;
 background:rgba(255,255,255,.06);
 font-size:18px;
}
.asset-name{font-weight:900;font-size:13px}
.spot{color:var(--muted);font:9px monospace;margin-top:3px}
.price{text-align:right}
.live-price{font:900 23px monospace;white-space:nowrap}
.price-up{color:var(--green)!important}
.price-down{color:var(--red)!important}
.price-change{font:800 10px monospace;color:var(--red);margin-top:3px}

/* LIVE CHART CANVAS */
.chart-container{
 height:62px;
 width:100%;
 margin:10px 0 10px;
 border-radius:10px;
 background:var(--chart-bg);
 border:1px solid var(--border);
 position:relative;
 overflow:hidden;
}
.chart-container canvas{
 width:100%;
 height:100%;
 display:block;
}

.metrics-grid{
 display:grid;
 grid-template-columns:repeat(4,1fr);
 gap:6px;
}
.metric{
 min-width:0;
 padding:8px 7px;
 background:var(--tile);
 border:1px solid var(--border);
 border-radius:10px;
}
.metric-label{
 color:var(--muted);
 font-size:8px;
 font-weight:800;
 text-transform:uppercase;
 margin-bottom:3px;
}
.metric-value{
 font:800 10px monospace;
 white-space:nowrap;
 overflow:hidden;
 text-overflow:ellipsis;
}
.cyan{color:var(--cyan)!important}
.green{color:var(--green)!important}
.red{color:var(--red)!important}
.yellow{color:var(--yellow)!important}

/* SECTION */
.section{
 background:linear-gradient(145deg,var(--card),var(--card2));
 border:1px solid var(--border);
 border-radius:20px;
 padding:15px;
 margin-bottom:14px;
 box-shadow:var(--shadow);
}
.section-head{
 display:flex;
 justify-content:space-between;
 align-items:center;
 gap:10px;
 padding-bottom:11px;
 margin-bottom:12px;
 border-bottom:1px solid var(--border);
}
.section-title{
 font-size:12px;
 font-weight:900;
 letter-spacing:.45px;
 display:flex;
 align-items:center;
 gap:7px;
}
.tabs{
 display:flex;
 gap:3px;
 padding:3px;
 border-radius:9px;
 background:var(--tile);
 border:1px solid var(--border);
 flex-shrink:0;
}
.tab{
 border:0;
 border-radius:6px;
 padding:5px 10px;
 background:transparent;
 color:var(--muted);
 font-size:9px;
 font-weight:900;
 cursor:pointer;
}
.tab.active{background:var(--blue);color:#fff}

/* SIGNAL CARDS */
.signal-grid{
 display:grid;
 grid-template-columns:repeat(2,minmax(0,1fr));
 gap:12px;
}
.signal-card{
 border:1px solid var(--border);
 border-radius:16px;
 padding:13px;
 background:rgba(255,255,255,.025);
}
.signal-top{
 display:flex;
 justify-content:space-between;
 align-items:center;
 gap:8px;
 margin-bottom:10px;
}
.signal-asset{font-size:12px;font-weight:900}
.badge{
 padding:5px 8px;
 border-radius:7px;
 font:900 8px monospace;
 border:1px solid var(--border);
 white-space:nowrap;
}
.badge-buy{color:var(--green);border-color:color-mix(in srgb,var(--green) 45%,transparent);background:color-mix(in srgb,var(--green) 9%,transparent)}
.badge-sell{color:var(--red);border-color:color-mix(in srgb,var(--red) 45%,transparent);background:color-mix(in srgb,var(--red) 9%,transparent)}
.badge-wait{color:var(--yellow);border-color:color-mix(in srgb,var(--yellow) 40%,transparent);background:color-mix(in srgb,var(--yellow) 8%,transparent)}

.pipeline{
 display:grid;
 grid-template-columns:repeat(4,1fr);
 gap:5px;
 margin-bottom:10px;
}
.step{
 text-align:center;
 padding:6px 2px;
 border-radius:8px;
 background:var(--tile);
 border:1px solid var(--border);
 color:var(--muted);
 font-size:8px;
}
.step span{display:block;font-size:7px;margin-bottom:2px}
.step.active-step{
 color:var(--text);
 border-color:var(--green);
 background:color-mix(in srgb,var(--green) 8%,transparent);
}
.params{
 display:grid;
 grid-template-columns:repeat(3,1fr);
 gap:6px;
}
.param{
 padding:8px 6px;
 text-align:center;
 border-radius:9px;
 background:var(--tile);
 border:1px solid var(--border);
}
.param-lbl{
 color:var(--muted);
 font-size:7px;
 font-weight:800;
 text-transform:uppercase;
 margin-bottom:4px;
}
.param-val{font:900 9px monospace;word-break:break-word}
.signal-targets{grid-template-columns:1fr 1fr;margin-top:6px}
.explain{
 margin-top:9px;
 padding:9px 10px;
 border-left:2px solid var(--cyan);
 border-radius:7px;
 background:var(--tile);
 color:var(--muted);
 font-size:9px;
 line-height:1.45;
}

/* SMC */
.smc-grid{
 display:grid;
 grid-template-columns:repeat(2,minmax(0,1fr));
 gap:12px;
}
.smc-card{
 padding:13px;
 border:1px solid var(--border);
 border-radius:15px;
 background:rgba(255,255,255,.022);
}
.smc-top{
 display:flex;
 justify-content:space-between;
 align-items:center;
 gap:8px;
 margin-bottom:9px;
}
.ob-panel{
 display:flex;
 justify-content:space-between;
 align-items:center;
 gap:10px;
 padding:9px;
 border-radius:10px;
 background:var(--tile);
 border:1px solid var(--border);
 margin-bottom:8px;
}
.ob-type{font-size:10px;font-weight:900}
.ob-range{font:9px monospace;color:var(--muted);margin-top:3px}
.ob-status{font-size:7px;padding:4px 6px;border-radius:6px}
.trade-param-row{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:6px}
.trade-param-box{
 text-align:center;padding:8px 5px;border-radius:9px;
 background:var(--tile);border:1px solid var(--border);
}
.param-lbl{font-size:7px;color:var(--muted);font-weight:800;text-transform:uppercase;margin-bottom:3px}
.param-val{font:800 9px monospace}

/* LOGS */
.console-header{
 display:flex;justify-content:space-between;align-items:center;
 margin:13px 0 6px;
 color:var(--muted);font-size:9px;font-weight:800;
}
.console-box{
 height:130px;overflow-y:auto;
 padding:10px;
 border-radius:12px;
 background:var(--console);
 border:1px solid var(--border);
 color:var(--cyan);
 font:9px/1.5 monospace;
}
.log-line{margin-bottom:4px}
.log-time{color:#738197}
.log-tf{color:var(--cyan);font-weight:900}

/* DESKTOP NAVIGATION HINT */
.desktop-layout{
 display:grid;
 grid-template-columns:minmax(0,1fr) 300px;
 gap:14px;
}
.side-panel{
 background:linear-gradient(145deg,var(--card),var(--card2));
 border:1px solid var(--border);
 border-radius:20px;
 padding:14px;
 box-shadow:var(--shadow);
 height:max-content;
 position:sticky;
 top:86px;
}
.side-title{font-size:11px;font-weight:900;margin-bottom:10px}
.side-row{
 display:flex;justify-content:space-between;align-items:center;
 padding:9px;
 margin-bottom:6px;
 border:1px solid var(--border);
 background:var(--tile);
 border-radius:9px;
 font-size:9px;
}
.side-row span:last-child{color:var(--cyan);font-family:monospace}

/* MOBILE BOTTOM NAV */
.bottom-nav{
 display:none;
}

/* TABLET */
@media(max-width:1000px){
 .desktop-layout{display:block}
 .side-panel{display:none}
}

/* MOBILE */
@media(max-width:700px){
 body{padding:9px 9px 78px}
 .header{border-radius:15px;padding:9px 10px;min-height:52px}
 .brand-sub{display:none}
 .logo{width:31px;height:31px}
 .brand-title{font-size:11px}
 .clock{display:none}
 .top-nav{display:none}

 .market-grid{grid-template-columns:1fr;gap:9px}
 .market-card{padding:13px;border-radius:17px}
 .live-price{font-size:20px}
 .metrics-grid{grid-template-columns:repeat(4,1fr)}
 .metric{padding:7px 5px}
 .metric-label{font-size:7px}
 .metric-value{font-size:9px}

 .section{padding:12px;border-radius:17px}
 .section-head{align-items:center}
 .section-title{font-size:10px}
 .tabs{padding:2px}
 .tab{padding:5px 8px;font-size:8px}

 .signal-grid,.smc-grid{grid-template-columns:1fr;gap:9px}
 .signal-card,.smc-card{padding:11px}
 .pipeline{gap:4px}
 .step{font-size:7px;padding:5px 2px}
 .params{gap:5px}
 .param{padding:7px 4px}
 .param-val{font-size:8px}
 .explain{font-size:8px}

 .desktop-layout{display:block}

 .bottom-nav{
  position:fixed;
  left:8px;right:8px;bottom:8px;
  z-index:100;
  display:grid;
  grid-template-columns:repeat(5,1fr);
  gap:2px;
  padding:5px;
  border:1px solid var(--border);
  border-radius:16px;
  background:color-mix(in srgb,var(--nav) 94%,transparent);
  backdrop-filter:blur(18px);
  box-shadow:0 12px 35px rgba(0,0,0,.35);
 }
 .bottom-nav button{
  border:0;background:transparent;color:var(--muted);
  padding:6px 2px 5px;border-radius:10px;
  font-size:7px;font-weight:900;cursor:pointer;
 }
 .bottom-nav button span{display:block;font-size:14px;margin-bottom:2px}
 .bottom-nav button.active{color:var(--cyan);background:color-mix(in srgb,var(--cyan) 8%,transparent)}

 .console-box{height:115px}
}

/* VERY SMALL PHONES */
@media(max-width:380px){
 .metrics-grid{gap:4px}
 .metric-label{font-size:6.5px}
 .metric-value{font-size:8px}
 .live-price{font-size:18px}
 .section-title{font-size:9px}
}
</style>
</head>

<body>
<div class="app">

<header class="header">
 <div class="brand">
  <div class="logo">⚡</div>
  <div>
   <div class="brand-title">DELTA TERMINAL</div>
   <div class="brand-sub">QUANT TRADING DESK • SFP + MSS ENGINE</div>
  </div>
 </div>
 <div class="header-right">
  <div class="live"><span class="live-dot"></span>LIVE</div>
  <div class="clock" id="utc-clock">00:00:00 UTC</div>
  <button class="theme-btn" id="theme-btn" onclick="toggleTheme()">☀️</button>
 </div>
</header>

<nav class="top-nav">
 <button class="active" onclick="scrollToSection('markets',this)">Overview</button>
 <button onclick="scrollToSection('signals',this)">Signals</button>
 <button onclick="scrollToSection('smc',this)">SMC</button>
 <button onclick="scrollToSection('logs',this)">Logs</button>
</nav>

<section id="markets">
 <div class="market-grid">

  <div class="market-card">
   <div class="market-head">
    <div class="asset">
     <div class="asset-icon">🟠</div>
     <div>
      <div class="asset-name">BTC/USD</div>
      <div class="spot">Spot: <span id="btc-spot">--</span> • Vol: <span id="btc-vol">--</span></div>
     </div>
    </div>
    <div class="price">
     <div class="live-price" id="btc-price">Loading...</div>
     <div class="price-change" id="btc-change">LIVE</div>
    </div>
   </div>
   
   <!-- REAL-TIME MINI CHART -->
   <div class="chart-container">
    <canvas id="btc-chart"></canvas>
   </div>

   <div class="metrics-grid">
    <div class="metric"><div class="metric-label">PDH</div><div class="metric-value cyan" id="btc-pdh">--</div></div>
    <div class="metric"><div class="metric-label">PDL</div><div class="metric-value yellow" id="btc-pdl">--</div></div>
    <div class="metric"><div class="metric-label">Dist PDH</div><div class="metric-value" id="btc-dist-pdh">--</div></div>
    <div class="metric"><div class="metric-label">Dist PDL</div><div class="metric-value" id="btc-dist-pdl">--</div></div>
   </div>
   <div class="metrics-grid" style="margin-top:6px">
    <div class="metric"><div class="metric-label">Today High</div><div class="metric-value cyan" id="btc-cdh">--</div></div>
    <div class="metric"><div class="metric-label">Today Low</div><div class="metric-value yellow" id="btc-cdl">--</div></div>
    <div class="metric"><div class="metric-label">Market</div><div class="metric-value green">LIVE</div></div>
    <div class="metric"><div class="metric-label">Feed</div><div class="metric-value green">TICK</div></div>
   </div>
  </div>

  <div class="market-card">
   <div class="market-head">
    <div class="asset">
     <div class="asset-icon">🔷</div>
     <div>
      <div class="asset-name">ETH/USD</div>
      <div class="spot">Spot: <span id="eth-spot">--</span> • Vol: <span id="eth-vol">--</span></div>
     </div>
    </div>
    <div class="price">
     <div class="live-price" id="eth-price">Loading...</div>
     <div class="price-change" id="eth-change">LIVE</div>
    </div>
   </div>

   <!-- REAL-TIME MINI CHART -->
   <div class="chart-container">
    <canvas id="eth-chart"></canvas>
   </div>

   <div class="metrics-grid">
    <div class="metric"><div class="metric-label">PDH</div><div class="metric-value cyan" id="eth-pdh">--</div></div>
    <div class="metric"><div class="metric-label">PDL</div><div class="metric-value yellow" id="eth-pdl">--</div></div>
    <div class="metric"><div class="metric-label">Dist PDH</div><div class="metric-value" id="eth-dist-pdh">--</div></div>
    <div class="metric"><div class="metric-label">Dist PDL</div><div class="metric-value" id="eth-dist-pdl">--</div></div>
   </div>
   <div class="metrics-grid" style="margin-top:6px">
    <div class="metric"><div class="metric-label">Today High</div><div class="metric-value cyan" id="eth-cdh">--</div></div>
    <div class="metric"><div class="metric-label">Today Low</div><div class="metric-value yellow" id="eth-cdl">--</div></div>
    <div class="metric"><div class="metric-label">Market</div><div class="metric-value green">LIVE</div></div>
    <div class="metric"><div class="metric-label">Feed</div><div class="metric-value green">TICK</div></div>
   </div>
  </div>

 </div>
</section>

<div class="desktop-layout">
<div>

<section class="section" id="signals">
 <div class="section-head">
  <div class="section-title">⚡ SFP + MSS SIGNALS</div>
  <div class="tabs">
   <button class="tab active" id="sfp-tab-15m" onclick="switchSFPTF('15m')">15M</button>
   <button class="tab" id="sfp-tab-5m" onclick="switchSFPTF('5m')">5M</button>
  </div>
 </div>

 <div class="signal-grid">

  <div class="signal-card">
   <div class="signal-top">
    <span class="signal-asset">🟠 BTC <span class="sfp-tf-label">15M</span></span>
    <span class="badge badge-wait" id="btc-sfp-badge">NO SWEEP</span>
   </div>

   <div class="pipeline">
    <div class="step active-step" id="btc-step-1"><span>01</span>ZONE</div>
    <div class="step" id="btc-step-2"><span>02</span>SWEEP</div>
    <div class="step" id="btc-step-3"><span>03</span>MSS</div>
    <div class="step" id="btc-step-4"><span>04</span>EXEC</div>
   </div>

   <div class="params">
    <div class="param"><div class="param-lbl">Signal</div><div class="param-val" id="btc-sfp-signal">WAIT</div></div>
    <div class="param"><div class="param-lbl">Entry</div><div class="param-val" id="btc-sfp-entry">--</div></div>
    <div class="param"><div class="param-lbl">SL</div><div class="param-val red" id="btc-sfp-sl">--</div></div>
   </div>
   <div class="params signal-targets">
    <div class="param"><div class="param-lbl">TP1 / EQ</div><div class="param-val green" id="btc-sfp-tp1">--</div></div>
    <div class="param"><div class="param-lbl">TP2 / Pool</div><div class="param-val cyan" id="btc-sfp-tp2">--</div></div>
   </div>
   <div class="explain" id="btc-sfp-rationale">Waiting for institutional sweep at HTF key levels...</div>
  </div>

  <div class="signal-card">
   <div class="signal-top">
    <span class="signal-asset">🔷 ETH <span class="sfp-tf-label">15M</span></span>
    <span class="badge badge-wait" id="eth-sfp-badge">NO SWEEP</span>
   </div>

   <div class="pipeline">
    <div class="step active-step" id="eth-step-1"><span>01</span>ZONE</div>
    <div class="step" id="eth-step-2"><span>02</span>SWEEP</div>
    <div class="step" id="eth-step-3"><span>03</span>MSS</div>
    <div class="step" id="eth-step-4"><span>04</span>EXEC</div>
   </div>

   <div class="params">
    <div class="param"><div class="param-lbl">Signal</div><div class="param-val" id="eth-sfp-signal">WAIT</div></div>
    <div class="param"><div class="param-lbl">Entry</div><div class="param-val" id="eth-sfp-entry">--</div></div>
    <div class="param"><div class="param-lbl">SL</div><div class="param-val red" id="eth-sfp-sl">--</div></div>
   </div>
   <div class="params signal-targets">
    <div class="param"><div class="param-lbl">TP1 / EQ</div><div class="param-val green" id="eth-sfp-tp1">--</div></div>
    <div class="param"><div class="param-lbl">TP2 / Pool</div><div class="param-val cyan" id="eth-sfp-tp2">--</div></div>
   </div>
   <div class="explain" id="eth-sfp-rationale">Waiting for institutional sweep at HTF key levels...</div>
  </div>

 </div>
</section>

<section class="section" id="smc">
 <div class="section-head">
  <div class="section-title">🎯 SMC / ORDER BLOCK</div>
  <div class="tabs">
   <button class="tab active" id="tab-15m" onclick="switchTF('15m')">15M</button>
   <button class="tab" id="tab-5m" onclick="switchTF('5m')">5M</button>
  </div>
 </div>

 <div class="smc-grid">

  <div class="smc-card">
   <div class="smc-top">
    <span style="font-size:11px;font-weight:900">🟠 BTC (<span class="tf-label">15M</span>) • <span id="btc-smc-state">SCANNING</span></span>
    <span class="badge badge-wait" id="btc-badge">WAITING</span>
   </div>
   <div class="ob-panel">
    <div>
     <div class="ob-type" id="btc-ob-type">Scanning OB...</div>
     <div class="ob-range" id="btc-ob-range">Zone: --</div>
    </div>
    <div class="ob-status badge-wait" id="btc-ob-status">UNTESTED</div>
   </div>
   <div class="trade-param-row">
    <div class="trade-param-box"><div class="param-lbl">Action</div><div class="param-val" id="btc-action">MONITOR</div></div>
    <div class="trade-param-box"><div class="param-lbl">Entry / OB</div><div class="param-val" id="btc-entry">--</div></div>
    <div class="trade-param-box"><div class="param-lbl">Stop Loss</div><div class="param-val red" id="btc-sl">--</div></div>
   </div>
   <div class="explain" id="btc-narrative">Scanning OB footprint and structure...</div>
  </div>

  <div class="smc-card">
   <div class="smc-top">
    <span style="font-size:11px;font-weight:900">🔷 ETH (<span class="tf-label">15M</span>) • <span id="eth-smc-state">SCANNING</span></span>
    <span class="badge badge-wait" id="eth-badge">WAITING</span>
   </div>
   <div class="ob-panel">
    <div>
     <div class="ob-type" id="eth-ob-type">Scanning OB...</div>
     <div class="ob-range" id="eth-ob-range">Zone: --</div>
    </div>
    <div class="ob-status badge-wait" id="eth-ob-status">UNTESTED</div>
   </div>
   <div class="trade-param-row">
    <div class="trade-param-box"><div class="param-lbl">Action</div><div class="param-val" id="eth-action">MONITOR</div></div>
    <div class="trade-param-box"><div class="param-lbl">Entry / OB</div><div class="param-val" id="eth-entry">--</div></div>
    <div class="trade-param-box"><div class="param-lbl">Stop Loss</div><div class="param-val red" id="eth-sl">--</div></div>
   </div>
   <div class="explain" id="eth-narrative">Scanning OB footprint and structure...</div>
  </div>

 </div>
</section>

<section class="section" id="logs">
 <div class="console-header">
  <span>📜 AUDIT LOGS • <span id="log-active-tf">15M</span></span>
  <span style="color:var(--cyan);cursor:pointer" onclick="clearLogs()">CLEAR</span>
 </div>
 <div class="console-box" id="console-logs">
  <div class="log-line"><span class="log-time">[INIT]</span> SFP + MSS Strategy Engine active. Listening for Wick Rejections...</div>
 </div>
</section>

</div>

<aside class="side-panel">
 <div class="side-title">⚡ TERMINAL STATUS</div>
 <div class="side-row"><span>WebSocket</span><span>READY</span></div>
 <div class="side-row"><span>BTC/USD</span><span id="side-btc">--</span></div>
 <div class="side-row"><span>ETH/USD</span><span id="side-eth">--</span></div>
 <div class="side-row"><span>SMC Engine</span><span>ACTIVE</span></div>
 <div class="side-row"><span>SFP Engine</span><span>ACTIVE</span></div>
 <div class="side-row"><span>15M / 5M</span><span>READY</span></div>
</aside>
</div>

<div class="bottom-nav">
 <button class="active" onclick="scrollToSection('markets',this)"><span>⌂</span>Markets</button>
 <button onclick="scrollToSection('signals',this)"><span>⚡</span>Signals</button>
 <button onclick="scrollToSection('smc',this)"><span>◈</span>SMC</button>
 <button onclick="scrollToSection('logs',this)"><span>▤</span>Logs</button>
 <button onclick="toggleTheme()"><span>☼</span>Theme</button>
</div>

<script>
/* =========================
   UI HELPERS ONLY
   ========================= */
let currentTheme = localStorage.getItem('delta_theme') || 'dark';

function applyTheme(theme){
 document.documentElement.setAttribute('data-theme',theme);
 document.getElementById('theme-btn').innerText=theme==='light'?'🌙':'☀️';
 localStorage.setItem('delta_theme',theme);
}
function toggleTheme(){
 currentTheme=currentTheme==='light'?'dark':'light';
 applyTheme(currentTheme);
}
applyTheme(currentTheme);

function scrollToSection(id,btn){
 document.getElementById(id)?.scrollIntoView({behavior:'smooth',block:'start'});
 document.querySelectorAll('.top-nav button,.bottom-nav button').forEach(b=>b.classList.remove('active'));
 if(btn) btn.classList.add('active');
}

/* =========================
   ORIGINAL STRATEGY STATE
   ========================= */
let activeTF='15m';
let activeSFPTF='15m';

function switchTF(tf){
 activeTF=tf;
 document.getElementById('tab-15m').classList.toggle('active',tf==='15m');
 document.getElementById('tab-5m').classList.toggle('active',tf==='5m');
 document.querySelectorAll('.tf-label').forEach(el=>el.innerText=tf.toUpperCase());
 renderSMCUI('BTCUSD');
 renderSMCUI('ETHUSD');
}

function switchSFPTF(tf){
 activeSFPTF=tf;
 document.getElementById('sfp-tab-15m').classList.toggle('active',tf==='15m');
 document.getElementById('sfp-tab-5m').classList.toggle('active',tf==='5m');
 document.querySelectorAll('.sfp-tf-label').forEach(el=>el.innerText=tf.toUpperCase());
 document.getElementById('log-active-tf').innerText=tf.toUpperCase();
 renderSFPUI('BTCUSD');
 renderSFPUI('ETHUSD');
 filterLogs();
}

function updateClock(){
 const now=new Date();
 document.getElementById('utc-clock').innerText=now.toUTCString().split(' ')[4]+' UTC';
}
setInterval(updateClock,1000);
updateClock();

const state={
 BTCUSD:{
  price:0,spot:0,vol:0,cdh:0,cdl:0,pdh:0,pdl:0,dec:1,
  history:[],
  '15m':{action:'MONITOR',state:'SCANNING',obType:'--',obRange:'--',obStatus:'UNTESTED',entry:'--',sl:'--',narrative:''},
  '5m':{action:'MONITOR',state:'SCANNING',obType:'--',obRange:'--',obStatus:'UNTESTED',entry:'--',sl:'--',narrative:''},
  sfp_15m:{signal:'WAIT',badge:'NO SWEEP',entry:'--',sl:'--',tp1:'--',tp2:'--',step:1,rationale:'',lastSig:''},
  sfp_5m:{signal:'WAIT',badge:'NO SWEEP',entry:'--',sl:'--',tp1:'--',tp2:'--',step:1,rationale:'',lastSig:''}
 },
 ETHUSD:{
  price:0,spot:0,vol:0,cdh:0,cdl:0,pdh:0,pdl:0,dec:2,
  history:[],
  '15m':{action:'MONITOR',state:'SCANNING',obType:'--',obRange:'--',obStatus:'UNTESTED',entry:'--',sl:'--',narrative:''},
  '5m':{action:'MONITOR',state:'SCANNING',obType:'--',obRange:'--',obStatus:'UNTESTED',entry:'--',sl:'--',narrative:''},
  sfp_15m:{signal:'WAIT',badge:'NO SWEEP',entry:'--',sl:'--',tp1:'--',tp2:'--',step:1,rationale:'',lastSig:''},
  sfp_5m:{signal:'WAIT',badge:'NO SWEEP',entry:'--',sl:'--',tp1:'--',tp2:'--',step:1,rationale:'',lastSig:''}
 }
};

const logsHistory=[];

function fmt(val,dec){
 if(!val||isNaN(val)) return '--';
 return Number(val).toLocaleString('en-US',{minimumFractionDigits:dec,maximumFractionDigits:dec});
}

function addLog(tf,msg){
 const now=new Date().toTimeString().split(' ')[0];
 const item={tf,text:msg,time:now};
 logsHistory.push(item);
 if(logsHistory.length>80) logsHistory.shift();
 if(activeSFPTF===tf||tf==='ALL') appendLogToBox(item);
}

function appendLogToBox(log){
 const box=document.getElementById('console-logs');
 const el=document.createElement('div');
 el.className='log-line';
 el.innerHTML=`<span class="log-time">[${log.time}]</span> <span class="log-tf">[${log.tf.toUpperCase()}]</span> ${log.text}`;
 box.appendChild(el);
 box.scrollTop=box.scrollHeight;
}

function filterLogs(){
 const box=document.getElementById('console-logs');
 box.innerHTML='';
 logsHistory.filter(l=>l.tf===activeSFPTF||l.tf==='ALL').forEach(appendLogToBox);
}

function clearLogs(){
 logsHistory.length=0;
 document.getElementById('console-logs').innerHTML='<div class="log-line"><span class="log-time">[CLEARED]</span> Logs reset.</div>';
}

/* =====================================
   LIVE MINI CHART ENGINE (CANVAS)
   ===================================== */
function drawLiveChart(sym){
 const canvas=document.getElementById(sym==='BTCUSD'?'btc-chart':'eth-chart');
 if(!canvas) return;
 const ctx=canvas.getContext('2d');
 const d=state[sym];

 const rect=canvas.parentElement.getBoundingClientRect();
 if(canvas.width!==rect.width||canvas.height!==rect.height){
  canvas.width=rect.width;
  canvas.height=rect.height;
 }

 const w=canvas.width;
 const h=canvas.height;
 ctx.clearRect(0,0,w,h);

 const hist=d.history;
 if(!hist||hist.length<2) return;

 let min=Math.min(...hist);
 let max=Math.max(...hist);
 if(d.pdh&&d.pdh>max) max=d.pdh;
 if(d.pdl&&d.pdl<min) min=d.pdl;

 const pad=(max-min)*0.08||1;
 min-=pad;
 max+=pad;

 const getY=(val)=>h-((val-min)/(max-min))*(h-12)-6;
 const getX=(idx)=>(idx/(hist.length-1))*(w-16)+8;

 // Draw PDH Reference Line
 if(d.pdh&&d.pdh>=min&&d.pdh<=max){
  const yPDH=getY(d.pdh);
  ctx.save();
  ctx.setLineDash([3,3]);
  ctx.strokeStyle='rgba(0,217,255,0.45)';
  ctx.lineWidth=1;
  ctx.beginPath();
  ctx.moveTo(0,yPDH);
  ctx.lineTo(w,yPDH);
  ctx.stroke();
  ctx.fillStyle='rgba(0,217,255,0.7)';
  ctx.font='7.5px monospace';
  ctx.fillText('PDH',4,yPDH-2);
  ctx.restore();
 }

 // Draw PDL Reference Line
 if(d.pdl&&d.pdl>=min&&d.pdl<=max){
  const yPDL=getY(d.pdl);
  ctx.save();
  ctx.setLineDash([3,3]);
  ctx.strokeStyle='rgba(255,189,60,0.45)';
  ctx.lineWidth=1;
  ctx.beginPath();
  ctx.moveTo(0,yPDL);
  ctx.lineTo(w,yPDL);
  ctx.stroke();
  ctx.fillStyle='rgba(255,189,60,0.7)';
  ctx.font='7.5px monospace';
  ctx.fillText('PDL',4,yPDL+8);
  ctx.restore();
 }

 // Price Curve Path
 ctx.beginPath();
 for(let i=0;i<hist.length;i++){
  const x=getX(i);
  const y=getY(hist[i]);
  if(i===0) ctx.moveTo(x,y);
  else ctx.lineTo(x,y);
 }

 const isUp=hist[hist.length-1]>=hist[0];
 const strokeColor=isUp?'#00e59a':'#ff426b';

 // Area Gradient Fill
 ctx.save();
 const grad=ctx.createLinearGradient(0,0,0,h);
 grad.addColorStop(0,isUp?'rgba(0,229,154,0.22)':'rgba(255,66,107,0.22)');
 grad.addColorStop(1,'transparent');
 ctx.lineTo(getX(hist.length-1),h);
 ctx.lineTo(getX(0),h);
 ctx.closePath();
 ctx.fillStyle=grad;
 ctx.fill();
 ctx.restore();

 // Line Stroke
 ctx.save();
 ctx.strokeStyle=strokeColor;
 ctx.lineWidth=1.8;
 ctx.shadowColor=strokeColor;
 ctx.shadowBlur=4;
 ctx.stroke();
 ctx.restore();

 // Head Glow Dot
 const lastX=getX(hist.length-1);
 const lastY=getY(hist[hist.length-1]);
 ctx.save();
 ctx.beginPath();
 ctx.arc(lastX,lastY,3,0,Math.PI*2);
 ctx.fillStyle=strokeColor;
 ctx.shadowColor=strokeColor;
 ctx.shadowBlur=8;
 ctx.fill();
 ctx.restore();
}

/* =========================
   ORIGINAL DAILY CANDLE DATA
   ========================= */
async function fetchDailyStats(){
 try{
  const symbols=['BTCUSD','ETHUSD'];
  for(const sym of symbols){
   const nowSec=Math.floor(Date.now()/1000);
   const startSec=nowSec-(86400*3);
   const res=await fetch(`https://api.india.delta.exchange/v2/history/candles?resolution=1d&symbol=${sym}&start=${startSec}&end=${nowSec}`);
   const data=await res.json();

   if(data.result&&data.result.length>=2){
    const today=data.result[0];
    const yesterday=data.result[1];

    state[sym].pdh=parseFloat(yesterday.high);
    state[sym].pdl=parseFloat(yesterday.low);
    state[sym].cdh=parseFloat(today.high);
    state[sym].cdl=parseFloat(today.low);

    if(!state[sym].history||state[sym].history.length===0){
     const base=parseFloat(today.close||yesterday.close);
     state[sym].history=[state[sym].cdl,base,state[sym].cdh,base];
    }

    updateMetricsUI(sym);
    drawLiveChart(sym);
    evaluateSMC(sym,'15m');
    evaluateSMC(sym,'5m');
    evaluateSFPStrategy(sym,'15m');
    evaluateSFPStrategy(sym,'5m');
   }
  }
 }catch(e){console.log("Candles err",e);}
}

/* =========================
   ORIGINAL SMC ENGINE
   ========================= */
function evaluateSMC(sym,tf){
 const d=state[sym];
 if(!d.price||!d.pdh||!d.pdl)return;

 const tfData=d[tf];
 const eq=(d.pdh+d.pdl)/2;
 const distToPDH=d.price-d.pdh;
 const distToPDL=d.price-d.pdl;

 const factor=tf==='5m'?0.4:1.0;
 const obBuffer=(d.price*(tf==='5m'?0.0015:0.0035));

 let action='MONITOR';
 let stateText='CONSOLIDATING';
 let obType='';
 let obLow=0,obHigh=0;
 let obStatus='UNTESTED';
 let entry='--';
 let sl='--';
 let narrative='';

 if(distToPDH>=-(25*factor)){
  action='SELL / SHORT';
  stateText=tf==='5m'?'5M CHoCH CONFIRMED':'15M PDH LIQUIDITY SWEEP';
  obType='🔴 Bearish Supply OB';
  obHigh=Math.max(d.cdh,d.pdh);
  obLow=obHigh-obBuffer;
  entry=`$${fmt(obLow,d.dec)} - $${fmt(obHigh,d.dec)}`;
  sl=`$${fmt(obHigh*1.002,d.dec)}`;
  obStatus=d.price>=obLow&&d.price<=obHigh?'MITIGATING':'PENDING TAP';
  narrative=`${tf.toUpperCase()} Supply Order Block created above PDH ($${fmt(d.pdh,d.dec)}). Target internal discount liquidity.`;
 }else if(distToPDL<=(25*factor)){
  action='BUY / LONG';
  stateText=tf==='5m'?'5M CHoCH BREAKOUT':'15M PDL LIQUIDITY RAID';
  obType='🟢 Bullish Demand OB';
  obLow=Math.min(d.cdl,d.pdl);
  obHigh=obLow+obBuffer;
  entry=`$${fmt(obLow,d.dec)} - $${fmt(obHigh,d.dec)}`;
  sl=`$${fmt(obLow*0.998,d.dec)}`;
  obStatus=d.price>=obLow&&d.price<=obHigh?'MITIGATING':'PENDING TAP';
  narrative=`${tf.toUpperCase()} Demand Order Block established near PDL ($${fmt(d.pdl,d.dec)}). Target EQ ($${fmt(eq,d.dec)}).`;
 }else{
  if(d.price>eq){
   stateText='PREMIUM BOS RETEST';
   action=tf==='5m'?'WAIT SHORT':'WATCH PREMIUM';
   obType='Bearish Internal OB';
   obHigh=d.price+obBuffer;
   obLow=d.price;
   entry=`Retest $${fmt(obHigh,d.dec)}`;
   sl=`SL > $${fmt(d.pdh,d.dec)}`;
   obStatus='INACTIVE';
   narrative=`${tf.toUpperCase()} trading above 50% EQ range. High time-frame bears defending supply.`;
  }else{
   stateText='DISCOUNT OB MITIGATION';
   action=tf==='5m'?'WAIT LONG':'WATCH DISCOUNT';
   obType='Bullish Internal OB';
   obLow=d.price-obBuffer;
   obHigh=d.price;
   entry=`Pullback $${fmt(obLow,d.dec)}`;
   sl=`SL < $${fmt(d.pdl,d.dec)}`;
   obStatus='INACTIVE';
   narrative=`${tf.toUpperCase()} testing discount array. Look for shift of character on 5m for entry.`;
  }
 }

 tfData.action=action;
 tfData.state=stateText;
 tfData.obType=obType;
 tfData.obRange=`$${fmt(obLow,d.dec)} - $${fmt(obHigh,d.dec)}`;
 tfData.obStatus=obStatus;
 tfData.entry=entry;
 tfData.sl=sl;
 tfData.narrative=narrative;

 if(activeTF===tf)renderSMCUI(sym);
}

/* =========================
   ORIGINAL SFP + MSS ENGINE
   ========================= */
function evaluateSFPStrategy(sym,tf){
 const d=state[sym];
 if(!d.price||!d.pdh||!d.pdl)return;

 const key=tf==='15m'?'sfp_15m':'sfp_5m';
 const sfp=d[key];
 const eq=(d.pdh+d.pdl)/2;

 const distToPDH=d.price-d.pdh;
 const distToPDL=d.price-d.pdl;
 const fvgBuffer=d.price*(tf==='5m'?0.001:0.002);

 let signal='WAIT';
 let badge='IN RANGE';
 let entry='--';
 let sl='--';
 let tp1=`$${fmt(eq,d.dec)}`;
 let tp2='--';
 let step=1;
 let rationale='';

 if(d.cdh>d.pdh&&d.price<d.pdh){
  step=4;
  signal='SELL SHORT';
  badge='BEARISH SFP + MSS';
  entry=`$${fmt(d.pdh-fvgBuffer,d.dec)} - $${fmt(d.pdh,d.dec)}`;
  sl=`$${fmt(d.cdh+(d.cdh*0.001),d.dec)}`;
  tp2=`$${fmt(d.pdl,d.dec)}`;
  rationale=`<strong>[Institutional Fakeout]:</strong> Price ne PDH ($${fmt(d.pdh,d.dec)}) ko wick se sweep kiya aur range ke andar wapas candle close kar di (SFP). LTF par Market Structure Shift (MSS) confirm hua hai. Entry FVG retest par karein, SL sweep wick ($${fmt(d.cdh,d.dec)}) ke upar rahega. Target Opposing EQL/PDL.`;
 }
 else if(distToPDH>=0){
  step=2;
  signal='WATCH SFP';
  badge='SWEEPING PDH';
  entry='Wait Candle Close Inside';
  sl='Wick High';
  tp2=`$${fmt(d.pdl,d.dec)}`;
  rationale=`Price is sweeping PDH ($${fmt(d.pdh,d.dec)}) right now. Wait for Wick Rejection (SFP) and close below PDH to confirm breakout failure. Do not chase breakout.`;
 }
 else if(d.cdl<d.pdl&&d.price>d.pdl){
  step=4;
  signal='BUY LONG';
  badge='BULLISH SFP + MSS';
  entry=`$${fmt(d.pdl,d.dec)} - $${fmt(d.pdl+fvgBuffer,d.dec)}`;
  sl=`$${fmt(d.cdl-(d.cdl*0.001),d.dec)}`;
  tp2=`$${fmt(d.pdh,d.dec)}`;
  rationale=`<strong>[Institutional Fakeout]:</strong> Sell stops raided below PDL ($${fmt(d.pdl,d.dec)}). Long wick rejection ke sath candle close range ke andar hui (Bullish SFP). LTF MSS confirmed with displacement. Entry FVG retest par, SL sweep wick ($${fmt(d.cdl,d.dec)}) ke niche. Target Opposing EQH/PDH.`;
 }
 else if(distToPDL<=0){
  step=2;
  signal='WATCH SFP';
  badge='SWEEPING PDL';
  entry='Wait Candle Close Inside';
  sl='Wick Low';
  tp2=`$${fmt(d.pdh,d.dec)}`;
  rationale=`Price is raiding liquidity below PDL ($${fmt(d.pdl,d.dec)}). Wait for SFP confirmation (Wick rejection followed by strong close back above PDL) before executing Long.`;
 }
 else{
  step=1;
  signal='MONITOR';
  badge='NO SWEEP';
  entry='Wait Level Tap';
  sl='--';
  tp2=d.price>eq?`$${fmt(d.pdh,d.dec)}`:`$${fmt(d.pdl,d.dec)}`;
  rationale=`Market trading between PDH ($${fmt(d.pdh,d.dec)}) and PDL ($${fmt(d.pdl,d.dec)}). Step 1 (Key Zones Mark) complete hai. Step 2 ke liye liquidity pool (PDH ya PDL) sweep hone ka wait karein.`;
 }

 sfp.signal=signal;
 sfp.badge=badge;
 sfp.entry=entry;
 sfp.sl=sl;
 sfp.tp1=tp1;
 sfp.tp2=tp2;
 sfp.step=step;
 sfp.rationale=rationale;

 if(sfp.lastSig!==signal&&(signal.includes('BUY')||signal.includes('SELL'))){
  sfp.lastSig=signal;
  addLog(tf,`<strong>${sym}</strong>: SFP+MSS Triggered <strong>${signal}</strong> | Entry: ${entry} | SL: ${sl}`);
 }

 if(activeSFPTF===tf)renderSFPUI(sym);
}

/* =========================
   UI RENDERERS
   ========================= */
function renderSMCUI(sym){
 const prefix=sym==='BTCUSD'?'btc':'eth';
 const tfData=state[sym][activeTF];

 document.getElementById(`${prefix}-smc-state`).innerText=tfData.state;

 const badge=document.getElementById(`${prefix}-badge`);
 badge.innerText=tfData.action;
 badge.className=`badge ${tfData.action.includes('BUY')?'badge-buy':tfData.action.includes('SELL')?'badge-sell':'badge-wait'}`;

 document.getElementById(`${prefix}-ob-type`).innerText=tfData.obType;
 document.getElementById(`${prefix}-ob-range`).innerText=`Zone: ${tfData.obRange}`;

 const obStatEl=document.getElementById(`${prefix}-ob-status`);
 obStatEl.innerText=tfData.obStatus;
 obStatEl.className=`ob-status ${tfData.obStatus==='MITIGATING'?'badge-buy':'badge-wait'}`;

 document.getElementById(`${prefix}-action`).innerText=tfData.action;
 document.getElementById(`${prefix}-entry`).innerText=tfData.entry;
 document.getElementById(`${prefix}-sl`).innerText=tfData.sl;
 document.getElementById(`${prefix}-narrative`).innerText=tfData.narrative;
}

function renderSFPUI(sym){
 const prefix=sym==='BTCUSD'?'btc':'eth';
 const key=activeSFPTF==='15m'?'sfp_15m':'sfp_5m';
 const sfp=state[sym][key];

 const badge=document.getElementById(`${prefix}-sfp-badge`);
 badge.innerText=sfp.badge;
 badge.className=`badge ${sfp.signal.includes('BUY')?'badge-buy':sfp.signal.includes('SELL')?'badge-sell':'badge-wait'}`;

 document.getElementById(`${prefix}-sfp-signal`).innerText=sfp.signal;
 document.getElementById(`${prefix}-sfp-entry`).innerText=sfp.entry;
 document.getElementById(`${prefix}-sfp-sl`).innerText=sfp.sl;
 document.getElementById(`${prefix}-sfp-tp1`).innerText=sfp.tp1;
 document.getElementById(`${prefix}-sfp-tp2`).innerText=sfp.tp2;
 document.getElementById(`${prefix}-sfp-rationale`).innerHTML=sfp.rationale;

 for(let i=1;i<=4;i++){
  const el=document.getElementById(`${prefix}-step-${i}`);
  el.classList.toggle('active-step',i<=sfp.step);
 }
}

function updateMetricsUI(sym){
 const d=state[sym];
 const prefix=sym==='BTCUSD'?'btc':'eth';

 if(d.pdh)document.getElementById(`${prefix}-pdh`).innerText='$'+fmt(d.pdh,d.dec);
 if(d.pdl)document.getElementById(`${prefix}-pdl`).innerText='$'+fmt(d.pdl,d.dec);
 if(d.cdh)document.getElementById(`${prefix}-cdh`).innerText='$'+fmt(d.cdh,d.dec);
 if(d.cdl)document.getElementById(`${prefix}-cdl`).innerText='$'+fmt(d.cdl,d.dec);

 if(d.spot)document.getElementById(`${prefix}-spot`).innerText='$'+fmt(d.spot,d.dec);
 if(d.vol)document.getElementById(`${prefix}-vol`).innerText=fmt(d.vol,0);

 if(d.price&&d.pdh){
  const diffPDH=d.price-d.pdh;
  const elPDH=document.getElementById(`${prefix}-dist-pdh`);
  elPDH.innerText=(diffPDH>=0?'+':'')+fmt(diffPDH,d.dec);
  elPDH.className='metric-value '+(diffPDH>=0?'green':'red');
 }
 if(d.price&&d.pdl){
  const diffPDL=d.price-d.pdl;
  const elPDL=document.getElementById(`${prefix}-dist-pdl`);
  elPDL.innerText=(diffPDL>=0?'+':'')+fmt(diffPDL,d.dec);
  elPDL.className='metric-value '+(diffPDL>=0?'green':'red');
 }

 const side=document.getElementById(`side-${prefix}`);
 if(side)side.innerText='$'+fmt(d.price,d.dec);
}

/* ===================================================
   ZERO-LAG WEBSOCKET (ALL_TRADES + V2/TICKER ENGINE)
   =================================================== */
function connectWS(){
 const ws=new WebSocket("wss://socket.india.delta.exchange");

 ws.onopen=()=>{
  addLog("ALL","Delta live ticks connected. Real-time stream active.");
  ws.send(JSON.stringify({
   type:"subscribe",
   payload:{
    channels:[
      {name:"v2/ticker",symbols:["BTCUSD","ETHUSD"]},
      {name:"all_trades",symbols:["BTCUSD","ETHUSD"]}
    ]
   }
  }));
 };

 ws.onmessage=(evt)=>{
  const msg=JSON.parse(evt.data);
  const sym=msg.symbol;

  if(sym&&state[sym]){
   const d=state[sym];
   const newPrice=parseFloat(msg.price||msg.mark_price||msg.close||0);

   if(newPrice>0){
    const pEl=document.getElementById(sym==='BTCUSD'?'btc-price':'eth-price');

    if(d.price&&newPrice!==d.price){
     pEl.classList.remove('price-up','price-down');
     void pEl.offsetWidth;
     pEl.classList.add(newPrice>d.price?'price-up':'price-down');
    }

    d.price=newPrice;
    pEl.innerText='$'+fmt(newPrice,d.dec);

    if(!d.history) d.history=[];
    d.history.push(newPrice);
    if(d.history.length>45) d.history.shift();
    drawLiveChart(sym);

    if(!d.cdh||newPrice>d.cdh)d.cdh=newPrice;
    if(!d.cdl||newPrice<d.cdl)d.cdl=newPrice;

    const chEl=document.getElementById(sym==='BTCUSD'?'btc-change':'eth-change');
    if(chEl){
     chEl.innerText='TICK • '+new Date().toLocaleTimeString();
     chEl.className='price-change '+(d.price>=newPrice?'price-up':'price-down');
    }

    evaluateSMC(sym,'15m');
    evaluateSMC(sym,'5m');
    evaluateSFPStrategy(sym,'15m');
    evaluateSFPStrategy(sym,'5m');
   }

   if(msg.spot_price)d.spot=parseFloat(msg.spot_price);
   if(msg.volume)d.vol=parseFloat(msg.volume);

   updateMetricsUI(sym);
  }
 };

 ws.onclose=()=>{
  addLog("ALL","Websocket dropped. Reconnecting...");
  setTimeout(connectWS,1500);
 };
}

// Keep connection hot with ping
setInterval(()=>{
  fetchDailyStats();
}, 60000);

fetchDailyStats();
connectWS();
</script>
</body>
</html>
"""

components.html(terminal_html, height=1600, scrolling=True)
