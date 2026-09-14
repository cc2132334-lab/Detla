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
 --chart-bg:rgba(4,8,15,0.85);
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
 --chart-bg:rgba(241,245,249,0.9);
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
   radial-gradient(circle at 15% 0%,rgba(0,217,255,.07),transparent 35%),
   radial-gradient(circle at 90% 15%,rgba(75,156,255,.06),transparent 30%),
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
 transition:all .2s ease;
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
 transition:transform .2s ease, box-shadow .2s ease, border-color .2s ease;
}
.market-card:hover{
 border-color:var(--border2);
 box-shadow:0 18px 42px rgba(0,0,0,.45);
}
.market-card:before{
 content:"";
 position:absolute;
 left:0;right:0;top:0;height:2px;
 background:linear-gradient(90deg,transparent,var(--cyan),transparent);
 opacity:.85;
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
.live-price{font:900 24px monospace;white-space:nowrap;transition:color .15s ease, text-shadow .15s ease}
.price-up{color:var(--green)!important;text-shadow:0 0 10px rgba(0,229,154,0.45)}
.price-down{color:var(--red)!important;text-shadow:0 0 10px rgba(255,66,107,0.45)}
.price-change{font:800 10px monospace;color:var(--red);margin-top:3px}

/* DYNAMIC CANDLESTICK CHART CONTAINER */
.chart-container{
 height:180px;
 width:100%;
 margin:12px 0 12px;
 border-radius:12px;
 background:var(--chart-bg);
 border:1px solid var(--border);
 position:relative;
 overflow:hidden;
 box-shadow:inset 0 0 18px rgba(0,0,0,0.35);
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
 transition:border-color .2s ease;
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
 transition:all .2s ease;
}
.tab.active{background:var(--blue);color:#fff;box-shadow:0 3px 10px rgba(37,99,235,0.3)}

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
 transition:all .2s ease;
}
.step span{display:block;font-size:7px;margin-bottom:2px}
.step.active-step{
 color:var(--text);
 border-color:var(--green);
 background:color-mix(in srgb,var(--green) 8%,transparent);
 font-weight:800;
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

/* DESKTOP SIDE PANEL */
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
.bottom-nav{display:none}

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
 .chart-container{height:165px}
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
 .chart-container{height:150px}
 .section-title{font-size:9px}
}

/* =========================================================
   FINAL UI SKIN — VISUAL ONLY
   Exact dashboard composition requested; no strategy/data logic changed.
   ========================================================= */
.app{max-width:1480px}
body{padding:10px 14px 82px;background:radial-gradient(900px 420px at 8% -8%,rgba(0,217,255,.10),transparent 62%),radial-gradient(800px 380px at 95% 2%,rgba(132,63,255,.10),transparent 60%),var(--bg)}
.header{position:relative;min-height:72px;margin-bottom:8px;border-radius:20px;padding:10px 16px;background:linear-gradient(110deg,rgba(7,16,28,.96),rgba(9,19,34,.88));border-color:rgba(0,217,255,.20);overflow:hidden}
.header:after{content:"";position:absolute;right:18%;top:-80px;width:260px;height:180px;background:radial-gradient(circle,rgba(0,217,255,.10),transparent 70%);pointer-events:none}
.logo{width:46px;height:46px;border-radius:14px;font-size:25px;background:linear-gradient(135deg,rgba(0,217,255,.22),rgba(125,65,255,.15));box-shadow:0 0 24px rgba(0,217,255,.08)}
.brand-title{font-size:22px;letter-spacing:.9px}.brand-sub{font-size:8px;letter-spacing:1.2px}
.header-right{gap:10px}.live{padding:8px 12px;border-radius:20px}.clock{padding:8px 11px;border-radius:10px}.theme-btn{width:42px;height:36px;border-radius:18px}
.top-nav{margin-bottom:9px;padding:4px 8px;border-radius:15px;background:rgba(7,15,26,.86);border-color:rgba(0,217,255,.10);backdrop-filter:blur(14px)}
.top-nav button{padding:9px 8px;font-size:10px;border-radius:10px}.top-nav button.active{background:linear-gradient(135deg,#087dff,#2457d6);box-shadow:0 6px 20px rgba(37,99,235,.32)}
.market-grid{gap:12px;margin-bottom:10px}.market-card{border-radius:18px;padding:13px 16px;background:linear-gradient(145deg,#081525,#0b1727);border-color:rgba(0,217,255,.20)}
.market-card:before{height:1px}.market-head{align-items:center}.asset-icon{width:42px;height:42px;border-radius:50%;font-size:22px;box-shadow:0 0 18px rgba(0,217,255,.12)}.asset-name{font-size:16px}.spot{font-size:9px}.live-price{font-size:25px}.price-change{font-size:10px}
.market-card .chart-container{height:0;min-height:0;margin:0;border:0;overflow:hidden;opacity:0;pointer-events:none}.market-card .metrics-grid{display:none}
/* Main 3-column dashboard */
.dashboard-grid{display:grid;grid-template-columns:250px minmax(0,1fr) 330px;gap:12px;align-items:stretch}
.panel{background:linear-gradient(145deg,#071321,#0b1726);border:1px solid rgba(0,217,255,.18);border-radius:18px;box-shadow:0 14px 38px rgba(0,0,0,.30);overflow:hidden}
.symbol-panel{min-height:620px}.panel-head{height:56px;display:flex;align-items:center;gap:18px;padding:0 18px;border-bottom:1px solid rgba(148,163,184,.12);font-size:12px;font-weight:900}.panel-head .active-line{align-self:stretch;display:flex;align-items:center;border-bottom:2px solid var(--cyan);color:#fff}
.search-box{margin:14px;padding:11px 13px;border:1px solid rgba(0,217,255,.16);border-radius:10px;color:var(--muted);font-size:10px;background:rgba(2,8,16,.6)}
.symbol-list{padding:0 12px}.symbol-item{display:flex;align-items:center;justify-content:space-between;padding:13px 10px;margin-bottom:8px;border:1px solid rgba(0,217,255,.14);border-radius:12px;background:linear-gradient(110deg,rgba(0,217,255,.07),rgba(0,0,0,.10));}.symbol-left{display:flex;align-items:center;gap:10px}.symbol-icon{width:34px;height:34px;display:grid;place-items:center;border-radius:50%;font-size:18px}.symbol-name{font-weight:900;font-size:12px}.symbol-price{font:900 12px monospace;margin-top:3px}.symbol-change{font:900 10px monospace;color:var(--green);margin-top:2px}.star{color:#aab5c7;font-size:20px}
.chart-panel{min-width:0;padding:0}.chart-title{display:flex;justify-content:space-between;align-items:center;padding:13px 17px 9px}.chart-symbol{display:flex;align-items:center;gap:10px}.chart-symbol .symbol-icon{width:38px;height:38px}.chart-symbol strong{font-size:18px}.chart-symbol .bigprice{font:900 20px monospace;margin-top:2px}.chart-change{color:var(--green);font:900 11px monospace;margin-left:8px}.ohlc{font:10px monospace;color:#b6c4d8}.chart-large{height:400px;margin:0 12px;border-radius:2px;background:linear-gradient(180deg,rgba(3,12,22,.96),rgba(3,9,17,.98));border:1px solid rgba(0,217,255,.11);overflow:hidden}.chart-large canvas{width:100%;height:100%;display:block}.chart-controls{display:flex;align-items:center;gap:6px;padding:9px 14px;border-top:1px solid rgba(148,163,184,.10);color:#d5deea;font-size:9px}.chart-controls span{padding:5px 8px}.chart-controls .on{background:#0b6fd7;border-radius:7px;color:#fff}.chart-options{margin-left:auto;display:flex;gap:12px;color:#c1ccda}.chart-options b{color:var(--cyan)}
.signal-panel{min-height:620px}.signal-panel .section-title{font-size:15px}.signal-panel .section-head{padding:15px 16px;margin:0}.signal-card{margin:0 12px 10px;padding:13px;border-radius:14px;background:linear-gradient(145deg,rgba(8,20,33,.96),rgba(6,14,25,.96));border-color:rgba(0,217,255,.12)}.signal-card .pipeline{display:none}.signal-card .params{grid-template-columns:1fr 1fr 1fr}.signal-card .signal-targets{grid-template-columns:1fr 1fr}.signal-card .explain{font-size:9px;margin-top:8px}.signal-card .signal-top{margin-bottom:8px}.signal-asset{font-size:14px}.badge{font-size:9px;padding:6px 9px}
.sentiment{margin:12px;border:1px solid rgba(0,217,255,.15);border-radius:14px;padding:14px;background:rgba(3,12,21,.65)}.sent-title{font-size:12px;font-weight:900;margin-bottom:10px}.sent-body{display:flex;align-items:center;gap:16px}.donut{width:104px;height:104px;border-radius:50%;background:conic-gradient(#00e59a 0 78%,#ff426b 78% 95%,#7386a6 95% 100%);display:grid;place-items:center;position:relative}.donut:after{content:"";width:70px;height:70px;border-radius:50%;background:#081421;position:absolute}.donut-text{position:relative;z-index:1;text-align:center;font-weight:900}.donut-text b{display:block;font-size:20px}.donut-text small{color:var(--green);font-size:9px}.legend{font-size:10px;line-height:2}.legend span{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px}.lg-green{background:#00e59a}.lg-red{background:#ff426b}.lg-blue{background:#7386a6}
.bottom-grid{display:grid;grid-template-columns:1.15fr 1fr;gap:12px;margin-top:12px}.bottom-panel{min-height:180px}.metrics-show{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding:14px}.metric-big{padding:14px 8px;border:1px solid rgba(0,217,255,.16);border-radius:11px;background:rgba(4,13,23,.72);text-align:center}.metric-big .lbl{color:#a0aec0;font-size:9px}.metric-big .num{font:900 21px monospace;margin-top:10px;color:var(--cyan)}.metric-big:nth-child(2) .num{color:#d78cff}.metric-big:nth-child(3) .num{color:#25e0d0}.metric-big:nth-child(4) .num{color:#00e59a}
.activity-list{padding:6px 14px 12px}.activity{display:grid;grid-template-columns:42px 22px 1fr auto;gap:8px;align-items:center;padding:8px 0;border-bottom:1px solid rgba(148,163,184,.09);font-size:9px}.activity:last-child{border-bottom:0}.activity-time{color:#a0aec0;font-family:monospace}.activity-icon{width:18px;height:18px;border-radius:50%;display:grid;place-items:center;background:#00b98a;color:#06120e;font-weight:900}.activity-icon.red{background:#ff426b;color:#fff}.activity-tag{color:#9aa8bb;font-family:monospace}
.footer-ui{display:flex;justify-content:space-between;align-items:center;margin-top:12px;padding:14px 10px;border-top:1px solid rgba(0,217,255,.10);color:#38c9f2;font-size:9px;letter-spacing:.4px}.footer-quote{color:#6f8299;letter-spacing:2px}
/* Hide old order-block/SMC section visually; JS strategy state remains untouched. */
#smc{display:none!important}
#logs{display:none!important}
.legacy-hidden{display:none!important}
@media(max-width:1100px){.dashboard-grid{grid-template-columns:210px minmax(0,1fr) 290px}.chart-large{height:350px}.brand-title{font-size:18px}}
@media(max-width:850px){.dashboard-grid{grid-template-columns:1fr}.symbol-panel,.signal-panel{min-height:auto}.chart-large{height:330px}.bottom-grid{grid-template-columns:1fr}.top-nav button:nth-child(n+5){display:none}.market-grid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){body{padding:7px 7px 72px}.header{padding:8px 10px}.brand-sub{display:none}.brand-title{font-size:15px}.logo{width:38px;height:38px}.clock{display:none}.market-grid{grid-template-columns:1fr;gap:7px}.market-card{padding:10px 12px}.market-card .asset-icon{width:34px;height:34px;font-size:18px}.live-price{font-size:20px}.dashboard-grid{gap:8px}.symbol-panel{display:none}.chart-large{height:285px;margin:0 7px}.chart-title{padding:10px}.ohlc{display:none}.metrics-show{grid-template-columns:repeat(2,1fr)}.top-nav{overflow:auto}.top-nav button{min-width:72px}.bottom-nav{display:flex!important}}
</style>
</head>

<body>
<div class="app">
<header class="header">
 <div class="brand"><div class="logo">⚡</div><div><div class="brand-title">DELTA TERMINAL</div><div class="brand-sub">TRADE SMARTER &nbsp;|&nbsp; TRADE DISCIPLINED</div></div></div>
 <div class="header-right"><div class="live"><span class="live-dot"></span>Live Market</div><div class="clock" id="utc-clock">00:00:00 UTC</div><button class="theme-btn" id="theme-btn" onclick="toggleTheme()">☀️</button></div>
</header>
<nav class="top-nav">
 <button class="active" onclick="scrollToSection('markets',this)">⌂ Dashboard</button>
 <button onclick="scrollToSection('markets',this)">▥ Market</button>
 <button onclick="scrollToSection('smc',this)">◈ SMC</button>
 <button onclick="scrollToSection('signals',this)">⚡ Signals</button>
 <button onclick="scrollToSection('markets',this)">☆ Watchlist</button>
 <button onclick="scrollToSection('logs',this)">⌁ Analytics</button>
 <button onclick="toggleTheme()">⚙ Settings</button>
</nav>
<section id="markets">
 <div class="market-grid">
  <div class="market-card"><div class="market-head"><div class="asset"><div class="asset-icon">🟠</div><div><div class="asset-name">BTCUSD</div><div class="spot">Spot: <span id="btc-spot">--</span> • Vol: <span id="btc-vol">--</span></div></div></div><div class="price"><div class="live-price" id="btc-price">Loading...</div><div class="price-change" id="btc-change">LIVE</div></div></div><div class="chart-container"><canvas id="btc-chart"></canvas></div><div class="metrics-grid"><div class="metric"><div class="metric-label">PDH</div><div class="metric-value cyan" id="btc-pdh">--</div></div><div class="metric"><div class="metric-label">PDL</div><div class="metric-value yellow" id="btc-pdl">--</div></div><div class="metric"><div class="metric-label">Dist PDH</div><div class="metric-value" id="btc-dist-pdh">--</div></div><div class="metric"><div class="metric-label">Dist PDL</div><div class="metric-value" id="btc-dist-pdl">--</div></div></div><div class="metrics-grid"><div class="metric"><div class="metric-label">Today High</div><div class="metric-value cyan" id="btc-cdh">--</div></div><div class="metric"><div class="metric-label">Today Low</div><div class="metric-value yellow" id="btc-cdl">--</div></div><div class="metric"><div class="metric-label">Market</div><div class="metric-value green">LIVE</div></div><div class="metric"><div class="metric-label">Feed</div><div class="metric-value green">TICK</div></div></div></div>
  <div class="market-card"><div class="market-head"><div class="asset"><div class="asset-icon">🔷</div><div><div class="asset-name">ETHUSD</div><div class="spot">Spot: <span id="eth-spot">--</span> • Vol: <span id="eth-vol">--</span></div></div></div><div class="price"><div class="live-price" id="eth-price">Loading...</div><div class="price-change" id="eth-change">LIVE</div></div></div><div class="chart-container"><canvas id="eth-chart"></canvas></div><div class="metrics-grid"><div class="metric"><div class="metric-label">PDH</div><div class="metric-value cyan" id="eth-pdh">--</div></div><div class="metric"><div class="metric-label">PDL</div><div class="metric-value yellow" id="eth-pdl">--</div></div><div class="metric"><div class="metric-label">Dist PDH</div><div class="metric-value" id="eth-dist-pdh">--</div></div><div class="metric"><div class="metric-label">Dist PDL</div><div class="metric-value" id="eth-dist-pdl">--</div></div></div><div class="metrics-grid"><div class="metric"><div class="metric-label">Today High</div><div class="metric-value cyan" id="eth-cdh">--</div></div><div class="metric"><div class="metric-label">Today Low</div><div class="metric-value yellow" id="eth-cdl">--</div></div><div class="metric"><div class="metric-label">Market</div><div class="metric-value green">LIVE</div></div><div class="metric"><div class="metric-label">Feed</div><div class="metric-value green">TICK</div></div></div></div>
 </div>
</section>
<div class="dashboard-grid">
 <aside class="panel symbol-panel">
  <div class="panel-head"><span class="active-line">Symbols</span><span>Watchlist</span></div>
  <div class="search-box">⌕ &nbsp;Search symbol...</div>
  <div class="symbol-list">
   <div class="symbol-item"><div class="symbol-left"><div class="symbol-icon">🟠</div><div><div class="symbol-name">BTCUSD</div><div class="symbol-price" id="side-btc">--</div><div class="symbol-change">LIVE</div></div></div><div class="star">☆</div></div>
   <div class="symbol-item"><div class="symbol-left"><div class="symbol-icon">🔷</div><div><div class="symbol-name">ETHUSD</div><div class="symbol-price" id="side-eth">--</div><div class="symbol-change">LIVE</div></div></div><div class="star">☆</div></div>
  </div>
 </aside>
 <main class="panel chart-panel">
  <div class="chart-title"><div class="chart-symbol"><div class="symbol-icon">🟠</div><div><strong>BTCUSD</strong><div><span class="bigprice" id="btc-price-main">--</span><span class="chart-change" id="btc-change-main">LIVE</span></div></div></div><div class="ohlc">O <span id="btc-o">--</span> &nbsp; H <span id="btc-h">--</span> &nbsp; L <span id="btc-l">--</span> &nbsp; C <span id="btc-c">--</span></div></div>
  <div class="chart-large"><canvas id="btc-chart-main"></canvas></div>
  <div class="chart-controls"><span>1m</span><span class="on">5m</span><span>15m</span><span>1h</span><span>4h⌄</span><span>⌗</span><span>⛶</span><div class="chart-options"><span>Volume <b>☑</b></span><span>SMC <b>☑</b></span><span>Liquidity <b>☑</b></span><span>SFP <b>☑</b></span><span>MSS <b>☑</b></span><span>Auto</span><span>⚙</span></div></div>
 </main>
 <aside class="panel signal-panel" id="signals">
  <div class="section-head"><div class="section-title">🎯 Live Signals</div><span style="color:var(--cyan);font-size:10px">View All →</span></div>
  <div class="tabs" style="margin:0 12px 10px"><button class="tab active" id="sfp-tab-15m" onclick="switchSFPTF('15m')">15M</button><button class="tab" id="sfp-tab-5m" onclick="switchSFPTF('5m')">5M</button></div>
  <div class="signal-card"><div class="signal-top"><span class="signal-asset">🟠 BTCUSD <span class="sfp-tf-label">15M</span></span><span class="badge badge-wait" id="btc-sfp-badge">NO SWEEP</span></div><div class="pipeline"><div class="step active-step" id="btc-step-1">ZONE</div><div class="step" id="btc-step-2">SWEEP</div><div class="step" id="btc-step-3">MSS</div><div class="step" id="btc-step-4">EXEC</div></div><div class="params"><div class="param"><div class="param-lbl">Signal</div><div class="param-val" id="btc-sfp-signal">WAIT</div></div><div class="param"><div class="param-lbl">Entry</div><div class="param-val" id="btc-sfp-entry">--</div></div><div class="param"><div class="param-lbl">SL</div><div class="param-val red" id="btc-sfp-sl">--</div></div></div><div class="params signal-targets"><div class="param"><div class="param-lbl">TP1 / EQ</div><div class="param-val green" id="btc-sfp-tp1">--</div></div><div class="param"><div class="param-lbl">TP2 / Pool</div><div class="param-val cyan" id="btc-sfp-tp2">--</div></div></div><div class="explain" id="btc-sfp-rationale">Waiting for institutional sweep at HTF key levels...</div></div>
  <div class="signal-card"><div class="signal-top"><span class="signal-asset">🔷 ETHUSD <span class="sfp-tf-label">15M</span></span><span class="badge badge-wait" id="eth-sfp-badge">NO SWEEP</span></div><div class="pipeline"><div class="step active-step" id="eth-step-1">ZONE</div><div class="step" id="eth-step-2">SWEEP</div><div class="step" id="eth-step-3">MSS</div><div class="step" id="eth-step-4">EXEC</div></div><div class="params"><div class="param"><div class="param-lbl">Signal</div><div class="param-val" id="eth-sfp-signal">WAIT</div></div><div class="param"><div class="param-lbl">Entry</div><div class="param-val" id="eth-sfp-entry">--</div></div><div class="param"><div class="param-lbl">SL</div><div class="param-val red" id="eth-sfp-sl">--</div></div></div><div class="params signal-targets"><div class="param"><div class="param-lbl">TP1 / EQ</div><div class="param-val green" id="eth-sfp-tp1">--</div></div><div class="param"><div class="param-lbl">TP2 / Pool</div><div class="param-val cyan" id="eth-sfp-tp2">--</div></div></div><div class="explain" id="eth-sfp-rationale">Waiting for institutional sweep at HTF key levels...</div></div>
  <div class="sentiment"><div class="sent-title">Market Sentiment</div><div class="sent-body"><div class="donut"><div class="donut-text"><b>78%</b><small>Bullish</small></div></div><div class="legend"><div><span class="lg-green"></span>Bullish &nbsp; 78%</div><div><span class="lg-red"></span>Bearish &nbsp; 17%</div><div><span class="lg-blue"></span>Neutral &nbsp;&nbsp; 5%</div></div></div></div>
 </aside>
</div>
<div class="bottom-grid">
 <section class="panel bottom-panel"><div class="section-head" style="padding:14px 16px;margin:0"><div class="section-title">▣ Key Metrics</div></div><div class="metrics-show"><div class="metric-big"><div class="lbl">Open Positions</div><div class="num">0</div></div><div class="metric-big"><div class="lbl">Total Signals</div><div class="num">12</div></div><div class="metric-big"><div class="lbl">Win Rate</div><div class="num">83.3%</div></div><div class="metric-big"><div class="lbl">Today P&amp;L</div><div class="num">+2.45%</div></div></div></section>
 <section class="panel bottom-panel"><div class="section-head" style="padding:14px 16px;margin:0"><div class="section-title">♟ Recent Activity</div><span style="color:var(--cyan);font-size:10px">View All →</span></div><div class="activity-list" id="activity-list"><div class="activity"><span class="activity-time">13:22</span><span class="activity-icon">↑</span><span>BUY signal generated on BTCUSD</span><span class="activity-tag">Bullish MSS</span></div><div class="activity"><span class="activity-time">13:18</span><span class="activity-icon red">↓</span><span>SELL signal generated on ETHUSD</span><span class="activity-tag">Bearish SFP</span></div><div class="activity"><span class="activity-time">13:15</span><span class="activity-icon">↟</span><span>Liquidity Sweep detected on ETHUSD</span><span class="activity-tag">Sweep High</span></div><div class="activity"><span class="activity-time">13:12</span><span class="activity-icon">↑</span><span>MSS confirmed on BTCUSD</span><span class="activity-tag">Trend Change</span></div><div class="activity"><span class="activity-time">13:08</span><span class="activity-icon red">↑</span><span>Price rejected from key level on ETHUSD</span><span class="activity-tag">Rejection</span></div></div></section>
</div>
<div class="footer-ui"><span>DELTA TERMINAL v2.0 &nbsp;|&nbsp; Real-time Market Analysis &nbsp;|&nbsp; Built for Smarter Traders</span><span class="footer-quote">“PATIENCE &nbsp; DISCIPLINE &nbsp; CONSISTENCY &nbsp; = &nbsp; FREEDOM”</span></div>
<!-- Hidden legacy UI anchors: retained only so the existing strategy/render functions continue to work unchanged. -->
<div class="legacy-hidden">
 <section id="smc"><button id="tab-15m"></button><button id="tab-5m"></button><span id="btc-smc-state"></span><span id="btc-badge"></span><span id="btc-ob-type"></span><span id="btc-ob-range"></span><span id="btc-ob-status"></span><span id="btc-action"></span><span id="btc-entry"></span><span id="btc-sl"></span><span id="btc-narrative"></span><span id="eth-smc-state"></span><span id="eth-badge"></span><span id="eth-ob-type"></span><span id="eth-ob-range"></span><span id="eth-ob-status"></span><span id="eth-action"></span><span id="eth-entry"></span><span id="eth-sl"></span><span id="eth-narrative"></span></section>
 <section id="logs"><span id="log-active-tf">15M</span><div id="console-logs"><div class="log-line"><span class="log-time">[INIT]</span> SFP + MSS Strategy Engine active.</div></div></section>
 <canvas id="eth-chart"></canvas>
</div>
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
  candles:[],
  '15m':{action:'MONITOR',state:'SCANNING',obType:'--',obRange:'--',obStatus:'UNTESTED',entry:'--',sl:'--',narrative:''},
  '5m':{action:'MONITOR',state:'SCANNING',obType:'--',obRange:'--',obStatus:'UNTESTED',entry:'--',sl:'--',narrative:''},
  sfp_15m:{signal:'WAIT',badge:'NO SWEEP',entry:'--',sl:'--',tp1:'--',tp2:'--',step:1,rationale:'',lastSig:''},
  sfp_5m:{signal:'WAIT',badge:'NO SWEEP',entry:'--',sl:'--',tp1:'--',tp2:'--',step:1,rationale:'',lastSig:''}
 },
 ETHUSD:{
  price:0,spot:0,vol:0,cdh:0,cdl:0,pdh:0,pdl:0,dec:2,
  candles:[],
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

/* =========================================================================
   ZOOMED 5M CANDLESTICK ENGINE (PROPER CANDLE BODIES & INDEPENDENT SCALE)
   ========================================================================= */
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

 const candles=d.candles;
 if(!candles||candles.length===0) return;

 // 1. SCALE DIRECTLY ON CANDLE EXTREMES (NEVER COMPRESS CANDLES FOR DISTANT PDL/PDH)
 let min=Infinity;
 let max=-Infinity;
 for(const c of candles){
  if(c.low<min) min=c.low;
  if(c.high>max) max=c.high;
 }

 if(d.price>0){
  if(d.price<min) min=d.price;
  if(d.price>max) max=d.price;
 }

 // Provide comfortable 15% breathing room top and bottom
 const pad=Math.max((max-min)*0.15, (min*0.0008));
 min-=pad;
 max+=pad;

 const getY=(val)=>h-((val-min)/(max-min))*(h-24)-12;

 // Subtle background price grid
 ctx.save();
 ctx.strokeStyle='rgba(148,163,184,0.07)';
 ctx.lineWidth=1;
 for(let step=1; step<=3; step++){
  const yGrid=h*(step/4);
  ctx.beginPath();
  ctx.moveTo(0,yGrid);
  ctx.lineTo(w,yGrid);
  ctx.stroke();
 }
 ctx.restore();

 // Draw PDH Reference Line only if inside candle zoom range
 if(d.pdh&&d.pdh>=min&&d.pdh<=max){
  const yPDH=getY(d.pdh);
  ctx.save();
  ctx.setLineDash([4,3]);
  ctx.strokeStyle='rgba(0,217,255,0.7)';
  ctx.lineWidth=1.2;
  ctx.beginPath();
  ctx.moveTo(0,yPDH);
  ctx.lineTo(w-54,yPDH);
  ctx.stroke();
  ctx.fillStyle='rgba(0,217,255,0.9)';
  ctx.font='bold 9px monospace';
  ctx.fillText('PDH',4,yPDH-3);
  ctx.restore();
 }

 // Draw PDL Reference Line only if inside candle zoom range
 if(d.pdl&&d.pdl>=min&&d.pdl<=max){
  const yPDL=getY(d.pdl);
  ctx.save();
  ctx.setLineDash([4,3]);
  ctx.strokeStyle='rgba(255,189,60,0.7)';
  ctx.lineWidth=1.2;
  ctx.beginPath();
  ctx.moveTo(0,yPDL);
  ctx.lineTo(w-54,yPDL);
  ctx.stroke();
  ctx.fillStyle='rgba(255,189,60,0.9)';
  ctx.font='bold 9px monospace';
  ctx.fillText('PDL',4,yPDL+10);
  ctx.restore();
 }

 // Render Bold Chunky Candlesticks
 const count=candles.length;
 const chartWidth=w-56;
 const slotWidth=chartWidth/count;
 const candleWidth=Math.max(4.5,Math.min(14,slotWidth*0.72));

 for(let i=0;i<count;i++){
  const c=candles[i];
  const xCenter=i*slotWidth+slotWidth/2+6;

  const yOpen=getY(c.open);
  const yClose=getY(c.close);
  const yHigh=getY(c.high);
  const yLow=getY(c.low);

  const isBullish=c.close>=c.open;
  const color=isBullish?'#00e59a':'#ff426b';

  // 1. Thick Central Wick
  ctx.save();
  ctx.strokeStyle=color;
  ctx.lineWidth=1.5;
  ctx.beginPath();
  ctx.moveTo(xCenter,yHigh);
  ctx.lineTo(xCenter,yLow);
  ctx.stroke();
  ctx.restore();

  // 2. Chunky Candle Body with minimum height of 3px
  const bodyTop=Math.min(yOpen,yClose);
  const bodyHeight=Math.max(3.5,Math.abs(yClose-yOpen));

  ctx.save();
  ctx.fillStyle=color;
  if(i===count-1){
   ctx.shadowColor=color;
   ctx.shadowBlur=8; // Dynamic glow for live candle
  }
  ctx.fillRect(xCenter-candleWidth/2,bodyTop,candleWidth,bodyHeight);
  ctx.restore();
 }

 // Live Horizontal Price Tracker & Pill Tag
 if(d.price&&d.price>=min&&d.price<=max){
  const yP=getY(d.price);
  const lastC=candles[count-1];
  const isBull=lastC.close>=lastC.open;
  const pColor=isBull?'#00e59a':'#ff426b';

  ctx.save();
  ctx.setLineDash([3,2]);
  ctx.strokeStyle=pColor;
  ctx.lineWidth=1.2;
  ctx.beginPath();
  ctx.moveTo(0,yP);
  ctx.lineTo(w-55,yP);
  ctx.stroke();

  // Price Box on the right axis
  ctx.fillStyle=pColor;
  ctx.fillRect(w-54,yP-8,52,16);
  ctx.fillStyle='#070b12';
  ctx.font='bold 9px monospace';
  ctx.fillText(fmt(d.price,d.dec===1?1:2),w-50,yP+3.5);
  ctx.restore();
 }
}

/* ===============================================================
   FETCH 5M CANDLE HISTORY (LAST 22 CANDLES FOR CLEAN VIEW)
   =============================================================== */
async function fetchCandleHistory(sym){
 try{
  const nowSec=Math.floor(Date.now()/1000);
  const startSec=nowSec-(300*24); // 24 candles of 5 minutes each
  const res=await fetch(`https://api.india.delta.exchange/v2/history/candles?resolution=5m&symbol=${sym}&start=${startSec}&end=${nowSec}`);
  const data=await res.json();
  if(data.result&&data.result.length>0){
   state[sym].candles=data.result.map(c=>({
    open:parseFloat(c.open),
    high:parseFloat(c.high),
    low:parseFloat(c.low),
    close:parseFloat(c.close),
    time:c.time||c.timestamp||0
   })).sort((a,b)=>a.time-b.time);
   drawLiveChart(sym);
  }
 }catch(e){}
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

    if(!state[sym].candles||state[sym].candles.length===0){
     fetchCandleHistory(sym);
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
  addLog("ALL","Delta live ticks connected. 5M Candlestick feed active.");
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

    // DYNAMIC 5-MINUTE CANDLESTICK UPDATE
    if(!d.candles) d.candles=[];
    const now=Date.now();
    if(d.candles.length===0){
     d.candles.push({open:newPrice,high:newPrice,low:newPrice,close:newPrice,time:now});
    }else{
     const lastC=d.candles[d.candles.length-1];
     if(lastC.time&&now-lastC.time>300000){ // 5-minute candle roll (300,000 ms)
      if(d.candles.length>22) d.candles.shift();
      d.candles.push({open:newPrice,high:newPrice,low:newPrice,close:newPrice,time:now});
     }else{
      lastC.close=newPrice;
      if(newPrice>lastC.high) lastC.high=newPrice;
      if(newPrice<lastC.low) lastC.low=newPrice;
     }
    }

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

setInterval(()=>{
  fetchDailyStats();
}, 60000);

fetchDailyStats();
connectWS();

/* Visual-only chart mirror: renders the existing BTC candle data on the new central canvas. */
(function(){
 function mirror(){
  const src=document.getElementById('btc-chart'), dst=document.getElementById('btc-chart-main');
  if(!src||!dst)return;
  const d=typeof state!=='undefined'&&state.BTCUSD;
  if(!d||!d.candles||!d.candles.length)return;
  const r=dst.parentElement.getBoundingClientRect(); dst.width=Math.max(10,r.width*devicePixelRatio); dst.height=Math.max(10,r.height*devicePixelRatio);
  const c=dst.getContext('2d'); const W=dst.width,H=dst.height; c.clearRect(0,0,W,H);
  c.fillStyle='#06111d'; c.fillRect(0,0,W,H);
  const cs=d.candles.slice(-40); let lo=Math.min(...cs.map(x=>x.low)),hi=Math.max(...cs.map(x=>x.high)); if(hi<=lo){hi=lo+1}
  const pad=18*devicePixelRatio, chartW=W-70*devicePixelRatio, chartH=H-35*devicePixelRatio, step=chartW/cs.length;
  c.strokeStyle='rgba(83,140,180,.14)';c.lineWidth=1*devicePixelRatio;
  for(let i=0;i<7;i++){let y=pad+i*(chartH/6);c.beginPath();c.moveTo(0,y);c.lineTo(chartW,y);c.stroke()}
  for(let i=0;i<9;i++){let x=i*(chartW/8);c.beginPath();c.moveTo(x,0);c.lineTo(x,chartH);c.stroke()}
  const y=v=>pad+(hi-v)/(hi-lo)*chartH;
  cs.forEach((x,i)=>{const xx=i*step+step*.5, yo=y(x.open), yc=y(x.close), yh=y(x.high), yl=y(x.low), up=x.close>=x.open; c.strokeStyle=up?'#00e59a':'#ff426b';c.fillStyle=up?'#00c995':'#ff426b';c.lineWidth=Math.max(1,devicePixelRatio);c.beginPath();c.moveTo(xx,yh);c.lineTo(xx,yl);c.stroke();const bw=Math.max(3,step*.58);c.fillRect(xx-bw/2,Math.min(yo,yc),bw,Math.max(2,Math.abs(yc-yo)));});
  c.fillStyle='#8190a6';c.font=`${9*devicePixelRatio}px monospace`;c.textAlign='right'; for(let i=0;i<5;i++){let v=hi-(hi-lo)*i/4;c.fillText(fmt(v,d.dec),W-5*devicePixelRatio,pad+i*(chartH/4)+3*devicePixelRatio)}
  const p=d.price; if(p){const yp=y(p);c.strokeStyle='#00d9ff';c.setLineDash([4*devicePixelRatio,4*devicePixelRatio]);c.beginPath();c.moveTo(0,yp);c.lineTo(chartW,yp);c.stroke();c.setLineDash([]);c.fillStyle='#00bfa5';c.fillRect(chartW,yp-10*devicePixelRatio,62*devicePixelRatio,20*devicePixelRatio);c.fillStyle='#06111d';c.font=`bold ${9*devicePixelRatio}px monospace`;c.textAlign='left';c.fillText(fmt(p,d.dec),chartW+4*devicePixelRatio,yp+3*devicePixelRatio)}
 }
 function sync(){ const d=typeof state!=='undefined'&&state.BTCUSD; if(d){const p=document.getElementById('btc-price-main'),ch=document.getElementById('btc-change-main'); if(p)p.textContent='$'+fmt(d.price,d.dec); if(ch)ch.textContent=document.getElementById('btc-change')?.textContent||'LIVE'; const c=d.candles?.[d.candles.length-1]; if(c){document.getElementById('btc-o').textContent=fmt(c.open,d.dec);document.getElementById('btc-h').textContent=fmt(c.high,d.dec);document.getElementById('btc-l').textContent=fmt(c.low,d.dec);document.getElementById('btc-c').textContent=fmt(c.close,d.dec)}} mirror();}
 setInterval(sync,500);
})();
</script>
</body>
</html>
"""

components.html(terminal_html, height=1700, scrolling=True)
