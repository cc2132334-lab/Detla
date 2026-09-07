import streamlit as st
import streamlit.components.v1 as components

# ============================================================
# DELTA TERMINAL — NEON UI v3
# Backend / Strategy Logic: UNCHANGED
# UI: Neon Dark / Responsive Mobile + Desktop
# ============================================================

st.set_page_config(
    page_title="Delta Terminal v3 - Neon",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit chrome
st.markdown("""
<style>
header,
header[data-testid="stHeader"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
#MainMenu,
footer,
div[data-testid="stStatusWidget"],
[data-testid="manage-app-button"],
button[title="Manage app"],
div[class*="viewerBadge"],
div[class*="manage-app"],
div[data-testid="stFloatingActions"] {
    display:none !important;
}

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
<html lang="en" data-theme="neon">

<head>
<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,
      initial-scale=1.0,
      maximum-scale=1.0,
      user-scalable=no">

<title>Delta Neon Terminal</title>

<style>

/* ============================================================
   NEON THEME
   ============================================================ */

:root {

    --bg: #03050a;
    --bg2: #060a12;

    --panel: rgba(5, 10, 19, 0.92);
    --panel2: rgba(8, 15, 27, 0.95);

    --cyan: #00eaff;
    --cyan2: #009dff;

    --green: #00ff9d;
    --red: #ff286f;
    --yellow: #ffc400;

    --purple: #a855f7;
    --blue: #168cff;

    --text: #edfaff;
    --muted: #6d8098;

    --border:
        rgba(0, 234, 255, 0.18);

    --border-green:
        rgba(0, 255, 157, 0.25);

    --border-red:
        rgba(255, 40, 111, 0.25);

    --shadow:
        0 0 25px rgba(0, 234, 255, 0.04);

    --neon-shadow:
        0 0 14px rgba(0,234,255,.18);

    --console:
        #010409;
}


/* ============================================================
   RESET
   ============================================================ */

* {
    box-sizing:border-box;
    margin:0;
    padding:0;
}

html {
    scroll-behavior:smooth;
}

body {

    background:
        radial-gradient(
            circle at 50% -20%,
            rgba(0,234,255,.09),
            transparent 38%
        ),

        radial-gradient(
            circle at 100% 50%,
            rgba(168,85,247,.045),
            transparent 35%
        ),

        var(--bg);

    color:var(--text);

    min-height:100vh;

    padding:14px;

    padding-bottom:80px;

    overflow-x:hidden;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Roboto,
        Arial,
        sans-serif;
}


/* ============================================================
   APP WIDTH
   ============================================================ */

.app {

    width:100%;

    max-width:1450px;

    margin:auto;
}


/* ============================================================
   GRID BACKGROUND
   ============================================================ */

.app:before {

    content:"";

    position:fixed;

    inset:0;

    pointer-events:none;

    background-image:
        linear-gradient(
            rgba(0,234,255,.018) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(0,234,255,.018) 1px,
            transparent 1px
        );

    background-size:35px 35px;

    mask-image:
        linear-gradient(
            to bottom,
            black,
            transparent 80%
        );

    z-index:-1;
}


/* ============================================================
   HEADER
   ============================================================ */

.header {

    height:62px;

    display:flex;

    align-items:center;

    justify-content:space-between;

    padding:9px 14px;

    margin-bottom:12px;

    background:
        linear-gradient(
            135deg,
            rgba(7,16,29,.98),
            rgba(3,7,14,.94)
        );

    border:
        1px solid var(--border);

    border-radius:15px;

    box-shadow:
        var(--shadow),
        inset 0 0 30px rgba(0,234,255,.015);

    position:sticky;

    top:7px;

    z-index:100;

    backdrop-filter:blur(15px);
}


.brand {

    display:flex;

    align-items:center;

    gap:10px;
}


.logo {

    width:36px;

    height:36px;

    display:grid;

    place-items:center;

    border-radius:10px;

    color:var(--cyan);

    font-size:20px;

    border:1px solid var(--border);

    background:
        rgba(0,234,255,.05);

    box-shadow:
        0 0 15px rgba(0,234,255,.12);
}


.brand-title {

    font-family:monospace;

    font-size:14px;

    font-weight:900;

    letter-spacing:1.5px;

    color:white;

    text-shadow:
        0 0 10px rgba(0,234,255,.35);
}


.brand-sub {

    margin-top:2px;

    font-family:monospace;

    font-size:8px;

    color:var(--muted);

    letter-spacing:1px;
}


.header-right {

    display:flex;

    align-items:center;

    gap:7px;
}


.live {

    display:flex;

    align-items:center;

    gap:6px;

    padding:6px 9px;

    border-radius:7px;

    border:
        1px solid
        rgba(0,255,157,.3);

    color:var(--green);

    background:
        rgba(0,255,157,.05);

    font:900 9px monospace;

    box-shadow:
        0 0 10px rgba(0,255,157,.06);
}


.live-dot {

    width:6px;

    height:6px;

    border-radius:50%;

    background:var(--green);

    box-shadow:
        0 0 9px var(--green);

    animation:pulse 1.4s infinite;
}


@keyframes pulse {

    0%,100% {
        opacity:1;
        transform:scale(1);
    }

    50% {
        opacity:.3;
        transform:scale(.7);
    }
}


.clock {

    padding:6px 8px;

    border-radius:7px;

    border:
        1px solid var(--border);

    color:var(--cyan);

    background:
        rgba(0,234,255,.035);

    font:700 9px monospace;
}


.theme-btn {

    width:30px;

    height:30px;

    border-radius:8px;

    border:
        1px solid var(--border);

    background:
        rgba(0,234,255,.035);

    color:var(--cyan);

    cursor:pointer;
}


/* ============================================================
   TOP NAV
   ============================================================ */

.top-nav {

    display:flex;

    gap:4px;

    padding:4px;

    margin-bottom:12px;

    background:
        rgba(4,9,17,.9);

    border:
        1px solid var(--border);

    border-radius:10px;
}


.top-nav button {

    flex:1;

    border:0;

    background:transparent;

    color:var(--muted);

    padding:8px;

    border-radius:7px;

    font:800 9px monospace;

    cursor:pointer;

    transition:.2s;
}


.top-nav button:hover {

    color:var(--cyan);
}


.top-nav button.active {

    color:#001015;

    background:var(--cyan);

    box-shadow:
        0 0 15px
        rgba(0,234,255,.35);
}


/* ============================================================
   MARKET CARDS
   ============================================================ */

.market-grid {

    display:grid;

    grid-template-columns:
        repeat(2,minmax(0,1fr));

    gap:12px;

    margin-bottom:12px;
}


.market-card {

    position:relative;

    padding:15px;

    border-radius:17px;

    background:
        linear-gradient(
            145deg,
            rgba(8,17,30,.97),
            rgba(3,8,15,.97)
        );

    border:
        1px solid var(--border);

    box-shadow:
        var(--shadow);

    overflow:hidden;
}


.market-card:before {

    content:"";

    position:absolute;

    top:0;

    left:0;

    right:0;

    height:1px;

    background:
        linear-gradient(
            90deg,
            transparent,
            var(--cyan),
            transparent
        );

    box-shadow:
        0 0 8px var(--cyan);
}


.market-card:after {

    content:"";

    position:absolute;

    width:100px;

    height:100px;

    top:-60px;

    right:-40px;

    background:
        rgba(0,234,255,.06);

    filter:blur(35px);

    border-radius:50%;
}


.market-head {

    display:flex;

    align-items:flex-start;

    justify-content:space-between;

    gap:10px;
}


.asset {

    display:flex;

    align-items:center;

    gap:9px;
}


.asset-icon {

    width:36px;

    height:36px;

    display:grid;

    place-items:center;

    border-radius:11px;

    font-size:18px;

    background:
        rgba(255,255,255,.035);

    border:
        1px solid var(--border);

    box-shadow:
        inset 0 0 15px rgba(0,234,255,.025);
}


.asset-name {

    font:900 13px monospace;

    letter-spacing:.3px;
}


.spot {

    margin-top:3px;

    color:var(--muted);

    font:8px monospace;
}


.price {

    text-align:right;
}


.live-price {

    font:900 23px monospace;

    color:white;

    text-shadow:
        0 0 12px rgba(255,255,255,.08);

    white-space:nowrap;
}


.price-up {

    color:var(--green)!important;

    text-shadow:
        0 0 12px
        rgba(0,255,157,.55)!important;
}


.price-down {

    color:var(--red)!important;

    text-shadow:
        0 0 12px
        rgba(255,40,111,.5)!important;
}


.price-change {

    margin-top:3px;

    color:var(--muted);

    font:700 8px monospace;
}


/* ============================================================
   MINI NEON GRAPH
   ============================================================ */

.mini-chart {

    height:32px;

    margin:
        11px 0 9px;

    position:relative;

    overflow:hidden;

    border-radius:8px;

    background:
        linear-gradient(
            180deg,
            rgba(0,234,255,.025),
            transparent
        );

    border-bottom:
        1px solid
        rgba(0,234,255,.05);
}


.mini-chart:before {

    content:"";

    position:absolute;

    left:-10%;

    right:-10%;

    top:8px;

    height:20px;

    background:
        linear-gradient(
            135deg,
            transparent 5%,
            var(--cyan) 6%,
            transparent 7%,
            transparent 19%,
            var(--cyan) 20%,
            transparent 21%,
            transparent 34%,
            var(--cyan) 35%,
            transparent 36%,
            transparent 48%,
            var(--cyan) 49%,
            transparent 50%,
            transparent 66%,
            var(--cyan) 67%,
            transparent 68%,
            transparent 80%,
            var(--cyan) 81%,
            transparent 82%
        );

    opacity:.45;

    filter:
        drop-shadow(
            0 0 4px var(--cyan)
        );
}


/* ============================================================
   METRICS
   ============================================================ */

.metrics-grid {

    display:grid;

    grid-template-columns:
        repeat(4,1fr);

    gap:5px;
}


.metric {

    min-width:0;

    padding:7px 6px;

    border-radius:8px;

    background:
        rgba(0,0,0,.18);

    border:
        1px solid
        rgba(0,234,255,.09);
}


.metric-label {

    color:var(--muted);

    font:700 7px monospace;

    text-transform:uppercase;

    margin-bottom:3px;
}


.metric-value {

    color:var(--text);

    font:800 9px monospace;

    white-space:nowrap;

    overflow:hidden;

    text-overflow:ellipsis;
}


.cyan {
    color:var(--cyan)!important;
}


.green {
    color:var(--green)!important;
}


.red {
    color:var(--red)!important;
}


.yellow {
    color:var(--yellow)!important;
}


/* ============================================================
   MAIN SECTIONS
   ============================================================ */

.section {

    padding:14px;

    margin-bottom:12px;

    border-radius:17px;

    background:
        linear-gradient(
            145deg,
            rgba(7,15,27,.96),
            rgba(3,8,15,.97)
        );

    border:
        1px solid var(--border);

    box-shadow:
        var(--shadow);

    position:relative;

    overflow:hidden;
}


.section:before {

    content:"";

    position:absolute;

    top:0;

    left:0;

    width:100%;

    height:1px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(0,234,255,.6),
            transparent
        );
}


.section-head {

    display:flex;

    align-items:center;

    justify-content:space-between;

    gap:10px;

    margin-bottom:11px;

    padding-bottom:9px;

    border-bottom:
        1px solid
        rgba(0,234,255,.08);
}


.section-title {

    display:flex;

    align-items:center;

    gap:6px;

    color:#fff;

    font:900 11px monospace;

    letter-spacing:.5px;

    text-shadow:
        0 0 8px
        rgba(0,234,255,.15);
}


.tabs {

    display:flex;

    gap:3px;

    padding:3px;

    border-radius:8px;

    background:
        rgba(0,0,0,.3);

    border:
        1px solid
        var(--border);
}


.tab {

    border:0;

    background:transparent;

    color:var(--muted);

    border-radius:5px;

    padding:5px 9px;

    font:900 8px monospace;

    cursor:pointer;
}


.tab.active {

    color:#001015;

    background:var(--cyan);

    box-shadow:
        0 0 12px
        rgba(0,234,255,.3);
}


/* ============================================================
   SIGNAL GRID
   ============================================================ */

.signal-grid {

    display:grid;

    grid-template-columns:
        repeat(2,minmax(0,1fr));

    gap:10px;
}


.signal-card {

    padding:12px;

    border-radius:14px;

    background:
        rgba(0,0,0,.20);

    border:
        1px solid
        rgba(0,234,255,.12);

    box-shadow:
        inset 0 0 20px
        rgba(0,234,255,.012);
}


.signal-card:hover {

    border-color:
        rgba(0,234,255,.28);

    box-shadow:
        0 0 20px
        rgba(0,234,255,.04);
}


.signal-top {

    display:flex;

    align-items:center;

    justify-content:space-between;

    gap:8px;

    margin-bottom:9px;
}


.signal-asset {

    font:900 11px monospace;
}


.badge {

    padding:5px 7px;

    border-radius:6px;

    font:900 7px monospace;

    border:1px solid;

    white-space:nowrap;
}


.badge-buy {

    color:var(--green);

    border-color:
        rgba(0,255,157,.45);

    background:
        rgba(0,255,157,.055);

    box-shadow:
        0 0 10px
        rgba(0,255,157,.08);
}


.badge-sell {

    color:var(--red);

    border-color:
        rgba(255,40,111,.5);

    background:
        rgba(255,40,111,.055);

    box-shadow:
        0 0 10px
        rgba(255,40,111,.08);
}


.badge-wait {

    color:var(--yellow);

    border-color:
        rgba(255,196,0,.4);

    background:
        rgba(255,196,0,.045);
}


/* ============================================================
   PIPELINE
   ============================================================ */

.pipeline {

    display:grid;

    grid-template-columns:
        repeat(4,1fr);

    gap:4px;

    margin-bottom:9px;
}


.step {

    padding:6px 2px;

    text-align:center;

    border-radius:7px;

    border:
        1px solid
        rgba(255,255,255,.06);

    background:
        rgba(0,0,0,.25);

    color:var(--muted);

    font:700 7px monospace;

    transition:.2s;
}


.step span {

    display:block;

    margin-bottom:2px;

    font-size:6px;
}


.step.active-step {

    color:var(--cyan);

    border-color:
        rgba(0,234,255,.35);

    background:
        rgba(0,234,255,.055);

    box-shadow:
        inset 0 0 10px
        rgba(0,234,255,.04),
        0 0 7px
        rgba(0,234,255,.05);
}


/* ============================================================
   PARAMETER BOXES
   ============================================================ */

.params {

    display:grid;

    grid-template-columns:
        repeat(3,1fr);

    gap:5px;
}


.param {

    padding:7px 5px;

    text-align:center;

    border-radius:8px;

    background:
        rgba(0,0,0,.22);

    border:
        1px solid
        rgba(0,234,255,.08);
}


.param-lbl {

    color:var(--muted);

    font:700 6.5px monospace;

    text-transform:uppercase;

    margin-bottom:3px;
}


.param-val {

    color:var(--text);

    font:900 8px monospace;

    word-break:break-word;
}


.signal-targets {

    grid-template-columns:1fr 1fr;

    margin-top:5px;
}


/* ============================================================
   EXPLANATION
   ============================================================ */

.explain {

    margin-top:8px;

    padding:8px 9px;

    border-left:
        2px solid
        var(--cyan);

    border-radius:5px;

    background:
        rgba(0,234,255,.025);

    color:var(--muted);

    font:8px/1.5 monospace;
}


.explain strong {

    color:var(--cyan);
}


/* ============================================================
   SMC
   ============================================================ */

.smc-grid {

    display:grid;

    grid-template-columns:
        repeat(2,minmax(0,1fr));

    gap:10px;
}


.smc-card {

    padding:12px;

    border-radius:14px;

    background:
        rgba(0,0,0,.20);

    border:
        1px solid
        rgba(0,234,255,.11);
}


.smc-top {

    display:flex;

    align-items:center;

    justify-content:space-between;

    gap:8px;

    margin-bottom:8px;
}


.ob-panel {

    display:flex;

    align-items:center;

    justify-content:space-between;

    gap:8px;

    padding:8px;

    margin-bottom:7px;

    border-radius:8px;

    background:
        rgba(0,0,0,.25);

    border:
        1px solid
        rgba(0,234,255,.07);
}


.ob-type {

    font:900 9px monospace;
}


.ob-range {

    margin-top:3px;

    color:var(--muted);

    font:8px monospace;
}


.ob-status {

    font:700 7px monospace;

    padding:4px 6px;

    border-radius:5px;
}


.trade-param-row {

    display:grid;

    grid-template-columns:
        repeat(3,1fr);

    gap:5px;

    margin-bottom:5px;
}


.trade-param-box {

    padding:7px 4px;

    text-align:center;

    border-radius:8px;

    background:
        rgba(0,0,0,.22);

    border:
        1px solid
        rgba(0,234,255,.07);
}


/* ============================================================
   CONSOLE
   ============================================================ */

.console-header {

    display:flex;

    align-items:center;

    justify-content:space-between;

    margin:
        11px 0 5px;

    color:var(--muted);

    font:700 8px monospace;
}


.console-box {

    height:125px;

    overflow-y:auto;

    padding:9px;

    border-radius:10px;

    background:
        var(--console);

    border:
        1px solid
        rgba(0,234,255,.12);

    box-shadow:
        inset 0 0 25px
        rgba(0,234,255,.018);

    color:var(--cyan);

    font:8px/1.55 monospace;
}


.log-line {

    margin-bottom:4px;
}


.log-time {

    color:#4c5c70;
}


.log-tf {

    color:var(--cyan);

    font-weight:900;
}


/* ============================================================
   DESKTOP SIDE PANEL
   ============================================================ */

.desktop-layout {

    display:grid;

    grid-template-columns:
        minmax(0,1fr) 275px;

    gap:12px;
}


.side-panel {

    height:max-content;

    position:sticky;

    top:85px;

    padding:13px;

    border-radius:17px;

    background:
        linear-gradient(
            145deg,
            rgba(7,15,27,.97),
            rgba(3,8,15,.98)
        );

    border:
        1px solid var(--border);

    box-shadow:
        var(--shadow);
}


.side-title {

    color:var(--cyan);

    font:900 10px monospace;

    margin-bottom:9px;

    text-shadow:
        0 0 8px
        rgba(0,234,255,.25);
}


.side-row {

    display:flex;

    align-items:center;

    justify-content:space-between;

    padding:8px;

    margin-bottom:5px;

    border-radius:7px;

    background:
        rgba(0,0,0,.22);

    border:
        1px solid
        rgba(0,234,255,.07);

    color:var(--muted);

    font:8px monospace;
}


.side-row span:last-child {

    color:var(--green);

    font-weight:900;
}


/* ============================================================
   BOTTOM MOBILE NAV
   ============================================================ */

.bottom-nav {

    display:none;
}


/* ============================================================
   TABLET
   ============================================================ */

@media(max-width:1000px) {

    .desktop-layout {

        display:block;
    }

    .side-panel {

        display:none;
    }
}


/* ============================================================
   MOBILE
   ============================================================ */

@media(max-width:700px) {

    body {

        padding:
            8px 8px 78px;
    }


    .header {

        top:5px;

        height:53px;

        padding:7px 9px;

        border-radius:13px;
    }


    .logo {

        width:30px;

        height:30px;

        font-size:17px;
    }


    .brand-title {

        font-size:11px;
    }


    .brand-sub {

        display:none;
    }


    .clock {

        display:none;
    }


    .live {

        font-size:8px;

        padding:5px 7px;
    }


    .theme-btn {

        width:28px;

        height:28px;
    }


    .top-nav {

        display:none;
    }


    .market-grid {

        grid-template-columns:1fr;

        gap:8px;
    }


    .market-card {

        padding:12px;

        border-radius:15px;
    }


    .live-price {

        font-size:19px;
    }


    .metrics-grid {

        gap:4px;
    }


    .metric {

        padding:6px 4px;
    }


    .metric-label {

        font-size:6px;
    }


    .metric-value {

        font-size:8px;
    }


    .section {

        padding:11px;

        border-radius:15px;
    }


    .section-title {

        font-size:9px;
    }


    .tab {

        padding:
            5px 8px;

        font-size:7px;
    }


    .signal-grid,
    .smc-grid {

        grid-template-columns:1fr;

        gap:8px;
    }


    .signal-card,
    .smc-card {

        padding:10px;
    }


    .signal-asset {

        font-size:10px;
    }


    .badge {

        font-size:6.5px;

        padding:5px 6px;
    }


    .params {

        gap:4px;
    }


    .param {

        padding:6px 3px;
    }


    .param-lbl {

        font-size:6px;
    }


    .param-val {

        font-size:7.5px;
    }


    .explain {

        font-size:7.5px;
    }


    .console-box {

        height:110px;

        font-size:7.5px;
    }


    .bottom-nav {

        position:fixed;

        left:7px;

        right:7px;

        bottom:7px;

        z-index:999;

        display:grid;

        grid-template-columns:
            repeat(5,1fr);

        gap:2px;

        padding:4px;

        border-radius:14px;

        background:
            rgba(3,8,15,.94);

        border:
            1px solid
            rgba(0,234,255,.18);

        backdrop-filter:blur(16px);

        box-shadow:
            0 0 25px
            rgba(0,0,0,.55);
    }


    .bottom-nav button {

        border:0;

        border-radius:9px;

        background:transparent;

        color:var(--muted);

        padding:5px 2px;

        font:700 6.5px monospace;

        cursor:pointer;
    }


    .bottom-nav button span {

        display:block;

        margin-bottom:2px;

        font-size:13px;
    }


    .bottom-nav button.active {

        color:var(--cyan);

        background:
            rgba(0,234,255,.055);

        text-shadow:
            0 0 8px
            rgba(0,234,255,.5);
    }
}


/* ============================================================
   SMALL PHONES
   ============================================================ */

@media(max-width:380px) {

    body {

        padding-left:6px;

        padding-right:6px;
    }


    .live-price {

        font-size:17px;
    }


    .metric-label {

        font-size:5.5px;
    }


    .metric-value {

        font-size:7.5px;
    }


    .section-title {

        font-size:8px;
    }
}

</style>
</head>


<body>

<div class="app">


<!-- =========================================================
     HEADER
     ========================================================= -->

<header class="header">

    <div class="brand">

        <div class="logo">
            ⚡
        </div>

        <div>

            <div class="brand-title">
                DELTA TERMINAL
            </div>

            <div class="brand-sub">
                NEON QUANT DESK • SFP + MSS ENGINE
            </div>

        </div>

    </div>


    <div class="header-right">

        <div class="live">
            <span class="live-dot"></span>
            LIVE
        </div>

        <div
            class="clock"
            id="utc-clock">
            00:00:00 UTC
        </div>

        <button
            class="theme-btn"
            id="theme-btn"
            onclick="toggleTheme()">
            ☼
        </button>

    </div>

</header>


<!-- =========================================================
     NAV
     ========================================================= -->

<nav class="top-nav">

    <button
        class="active"
        onclick="scrollToSection('markets',this)">
        OVERVIEW
    </button>

    <button
        onclick="scrollToSection('signals',this)">
        SIGNALS
    </button>

    <button
        onclick="scrollToSection('smc',this)">
        SMC
    </button>

    <button
        onclick="scrollToSection('logs',this)">
        LOGS
    </button>

</nav>


<!-- =========================================================
     MARKET CARDS
     ========================================================= -->

<section id="markets">

<div class="market-grid">


<!-- BTC -->

<div class="market-card">

    <div class="market-head">

        <div class="asset">

            <div class="asset-icon">
                🟠
            </div>

            <div>

                <div class="asset-name">
                    BTC/USD
                </div>

                <div class="spot">
                    Spot:
                    <span id="btc-spot">--</span>
                    • Vol:
                    <span id="btc-vol">--</span>
                </div>

            </div>

        </div>


        <div class="price">

            <div
                class="live-price"
                id="btc-price">
                Loading...
            </div>

            <div
                class="price-change"
                id="btc-change">
                LIVE
            </div>

        </div>

    </div>


    <div class="mini-chart"></div>


    <div class="metrics-grid">

        <div class="metric">
            <div class="metric-label">PDH</div>
            <div
                class="metric-value cyan"
                id="btc-pdh">
                --
            </div>
        </div>

        <div class="metric">
            <div class="metric-label">PDL</div>
            <div
                class="metric-value yellow"
                id="btc-pdl">
                --
            </div>
        </div>

        <div class="metric">
            <div class="metric-label">DIST PDH</div>
            <div
                class="metric-value"
                id="btc-dist-pdh">
                --
            </div>
        </div>

        <div class="metric">
            <div class="metric-label">DIST PDL</div>
            <div
                class="metric-value"
                id="btc-dist-pdl">
                --
            </div>
        </div>

    </div>


    <div
        class="metrics-grid"
        style="margin-top:5px">

        <div class="metric">
            <div class="metric-label">TODAY HIGH</div>
            <div
                class="metric-value cyan"
                id="btc-cdh">
                --
            </div>
        </div>

        <div class="metric">
            <div class="metric-label">TODAY LOW</div>
            <div
                class="metric-value yellow"
                id="btc-cdl">
                --
            </div>
        </div>

        <div class="metric">
            <div class="metric-label">FEED</div>
            <div class="metric-value green">
                WS
            </div>
        </div>

        <div class="metric">
            <div class="metric-label">STATUS</div>
            <div class="metric-value green">
                LIVE
            </div>
        </div>

    </div>

</div>


<!-- ETH -->

<div class="market-card">

    <div class="market-head">

        <div class="asset">

            <div class="asset-icon">
                🔷
            </div>

            <div>

                <div class="asset-name">
                    ETH/USD
                </div>

                <div class="spot">
                    Spot:
                    <span id="eth-spot">--</span>
                    • Vol:
                    <span id="eth-vol">--</span>
                </div>

            </div>

        </div>


        <div class="price">

            <div
                class="live-price"
                id="eth-price">
                Loading...
            </div>

            <div
                class="price-change"
                id="eth-change">
                LIVE
            </div>

        </div>

    </div>


    <div class="mini-chart"></div>


    <div class="metrics-grid">

        <div class="metric">
            <div class="metric-label">PDH</div>
            <div
                class="metric-value cyan"
                id="eth-pdh">
                --
            </div>
        </div>

        <div class="metric">
            <div class="metric-label">PDL</div>
            <div
                class="metric-value yellow"
                id="eth-pdl">
                --
            </div>
        </div>

        <div class="metric">
            <div class="metric-label">DIST PDH</div>
            <div
                class="metric-value"
                id="eth-dist-pdh">
                --
            </div>
        </div>

        <div class="metric">
            <div class="metric-label">DIST PDL</div>
            <div
                class="metric-value"
                id="eth-dist-pdl">
                --
            </div>
        </div>

    </div>


    <div
        class="metrics-grid"
        style="margin-top:5px">

        <div class="metric">
            <div class="metric-label">TODAY HIGH</div>
            <div
                class="metric-value cyan"
                id="eth-cdh">
                --
            </div>
        </div>

        <div class="metric">
            <div class="metric-label">TODAY LOW</div>
            <div
                class="metric-value yellow"
                id="eth-cdl">
                --
            </div>
        </div>

        <div class="metric">
            <div class="metric-label">FEED</div>
            <div class="metric-value green">
                WS
            </div>
        </div>

        <div class="metric">
            <div class="metric-label">STATUS</div>
            <div class="metric-value green">
                LIVE
            </div>
        </div>

    </div>

</div>

</div>

</section>


<!-- =========================================================
     DESKTOP LAYOUT
     ========================================================= -->

<div class="desktop-layout">

<div>


<!-- =========================================================
     SFP + MSS
     ========================================================= -->

<section
    class="section"
    id="signals">

<div class="section-head">

    <div class="section-title">
        ⚡ SFP + MSS SIGNAL ENGINE
    </div>

    <div class="tabs">

        <button
            class="tab active"
            id="sfp-tab-15m"
            onclick="switchSFPTF('15m')">
            15M
        </button>

        <button
            class="tab"
            id="sfp-tab-5m"
            onclick="switchSFPTF('5m')">
            5M
        </button>

    </div>

</div>


<div class="signal-grid">


<!-- BTC SIGNAL -->

<div class="signal-card">

    <div class="signal-top">

        <span class="signal-asset">
            🟠 BTC
            <span class="sfp-tf-label">15M</span>
        </span>

        <span
            class="badge badge-wait"
            id="btc-sfp-badge">
            NO SWEEP
        </span>

    </div>


    <div class="pipeline">

        <div
            class="step active-step"
            id="btc-step-1">
            <span>01</span>
            ZONE
        </div>

        <div
            class="step"
            id="btc-step-2">
            <span>02</span>
            SWEEP
        </div>

        <div
            class="step"
            id="btc-step-3">
            <span>03</span>
            MSS
        </div>

        <div
            class="step"
            id="btc-step-4">
            <span>04</span>
            EXEC
        </div>

    </div>


    <div class="params">

        <div class="param">

            <div class="param-lbl">
                SIGNAL
            </div>

            <div
                class="param-val"
                id="btc-sfp-signal">
                WAIT
            </div>

        </div>


        <div class="param">

            <div class="param-lbl">
                ENTRY
            </div>

            <div
                class="param-val"
                id="btc-sfp-entry">
                --
            </div>

        </div>


        <div class="param">

            <div class="param-lbl">
                SL
            </div>

            <div
                class="param-val red"
                id="btc-sfp-sl">
                --
            </div>

        </div>

    </div>


    <div
        class="params signal-targets">

        <div class="param">

            <div class="param-lbl">
                TP1 / EQ
            </div>

            <div
                class="param-val green"
                id="btc-sfp-tp1">
                --
            </div>

        </div>


        <div class="param">

            <div class="param-lbl">
                TP2 / POOL
            </div>

            <div
                class="param-val cyan"
                id="btc-sfp-tp2">
                --
            </div>

        </div>

    </div>


    <div
        class="explain"
        id="btc-sfp-rationale">
        Waiting for institutional sweep at HTF key levels...
    </div>

</div>


<!-- ETH SIGNAL -->

<div class="signal-card">

    <div class="signal-top">

        <span class="signal-asset">
            🔷 ETH
            <span class="sfp-tf-label">15M</span>
        </span>

        <span
            class="badge badge-wait"
            id="eth-sfp-badge">
            NO SWEEP
        </span>

    </div>


    <div class="pipeline">

        <div
            class="step active-step"
            id="eth-step-1">
            <span>01</span>
            ZONE
        </div>

        <div
            class="step"
            id="eth-step-2">
            <span>02</span>
            SWEEP
        </div>

        <div
            class="step"
            id="eth-step-3">
            <span>03</span>
            MSS
        </div>

        <div
            class="step"
            id="eth-step-4">
            <span>04</span>
            EXEC
        </div>

    </div>


    <div class="params">

        <div class="param">

            <div class="param-lbl">
                SIGNAL
            </div>

            <div
                class="param-val"
                id="eth-sfp-signal">
                WAIT
            </div>

        </div>


        <div class="param">

            <div class="param-lbl">
                ENTRY
            </div>

            <div
                class="param-val"
                id="eth-sfp-entry">
                --
            </div>

        </div>


        <div class="param">

            <div class="param-lbl">
                SL
            </div>

            <div
                class="param-val red"
                id="eth-sfp-sl">
                --
            </div>

        </div>

    </div>


    <div
        class="params signal-targets">

        <div class="param">

            <div class="param-lbl">
                TP1 / EQ
            </div>

            <div
                class="param-val green"
                id="eth-sfp-tp1">
                --
            </div>

        </div>


        <div class="param">

            <div class="param-lbl">
                TP2 / POOL
            </div>

            <div
                class="param-val cyan"
                id="eth-sfp-tp2">
                --
            </div>

        </div>

    </div>


    <div
        class="explain"
        id="eth-sfp-rationale">
        Waiting for institutional sweep at HTF key levels...
    </div>

</div>

</div>

</section>


<!-- =========================================================
     SMC / ORDER BLOCK
     ========================================================= -->

<section
    class="section"
    id="smc">

<div class="section-head">

    <div class="section-title">
        🎯 SMC / ORDER BLOCK SCANNER
    </div>

    <div class="tabs">

        <button
            class="tab active"
            id="tab-15m"
            onclick="switchTF('15m')">
            15M
        </button>

        <button
            class="tab"
            id="tab-5m"
            onclick="switchTF('5m')">
            5M
        </button>

    </div>

</div>


<div class="smc-grid">


<!-- BTC SMC -->

<div class="smc-card">

    <div class="smc-top">

        <span
            style="
            font:900 9px monospace;
            ">

            🟠 BTC
            (<span class="tf-label">15M</span>)
            •
            <span id="btc-smc-state">
                SCANNING
            </span>

        </span>


        <span
            class="badge badge-wait"
            id="btc-badge">
            WAITING
        </span>

    </div>


    <div class="ob-panel">

        <div>

            <div
                class="ob-type"
                id="btc-ob-type">
                Scanning OB...
            </div>

            <div
                class="ob-range"
                id="btc-ob-range">
                Zone: --
            </div>

        </div>


        <div
            class="ob-status badge-wait"
            id="btc-ob-status">
            UNTESTED
        </div>

    </div>


    <div class="trade-param-row">

        <div class="trade-param-box">

            <div class="param-lbl">
                ACTION
            </div>

            <div
                class="param-val"
                id="btc-action">
                MONITOR
            </div>

        </div>


        <div class="trade-param-box">

            <div class="param-lbl">
                ENTRY / OB
            </div>

            <div
                class="param-val"
                id="btc-entry">
                --
            </div>

        </div>


        <div class="trade-param-box">

            <div class="param-lbl">
                STOP LOSS
            </div>

            <div
                class="param-val red"
                id="btc-sl">
                --
            </div>

        </div>

    </div>


    <div
        class="explain"
        id="btc-narrative">
        Scanning OB footprint and structure...
    </div>

</div>


<!-- ETH SMC -->

<div class="smc-card">

    <div class="smc-top">

        <span
            style="
            font:900 9px monospace;
            ">

            🔷 ETH
            (<span class="tf-label">15M</span>)
            •
            <span id="eth-smc-state">
                SCANNING
            </span>

        </span>


        <span
            class="badge badge-wait"
            id="eth-badge">
            WAITING
        </span>

    </div>


    <div class="ob-panel">

        <div>

            <div
                class="ob-type"
                id="eth-ob-type">
                Scanning OB...
            </div>

            <div
                class="ob-range"
                id="eth-ob-range">
                Zone: --
            </div>

        </div>


        <div
            class="ob-status badge-wait"
            id="eth-ob-status">
            UNTESTED
        </div>

    </div>


    <div class="trade-param-row">

        <div class="trade-param-box">

            <div class="param-lbl">
                ACTION
            </div>

            <div
                class="param-val"
                id="eth-action">
                MONITOR
            </div>

        </div>


        <div class="trade-param-box">

            <div class="param-lbl">
                ENTRY / OB
            </div>

            <div
                class="param-val"
                id="eth-entry">
                --
            </div>

        </div>


        <div class="trade-param-box">

            <div class="param-lbl">
                STOP LOSS
            </div>

            <div
                class="param-val red"
                id="eth-sl">
                --
            </div>

        </div>

    </div>


    <div
        class="explain"
        id="eth-narrative">
        Scanning OB footprint and structure...
    </div>

</div>

</div>

</section>


<!-- =========================================================
     AUDIT LOG
     ========================================================= -->

<section
    class="section"
    id="logs">

<div class="console-header">

    <span>
        ▣ AUDIT LOGS •
        <span id="log-active-tf">
            15M
        </span>
    </span>

    <span
        style="
        color:var(--cyan);
        cursor:pointer;
        "
        onclick="clearLogs()">
        CLEAR
    </span>

</div>


<div
    class="console-box"
    id="console-logs">

    <div class="log-line">

        <span class="log-time">
            [INIT]
        </span>

        SFP + MSS Strategy Engine active.
        Listening for Wick Rejections...

    </div>

</div>

</section>

</div>


<!-- =========================================================
     DESKTOP STATUS PANEL
     ========================================================= -->

<aside class="side-panel">

    <div class="side-title">
        ⚡ NEON TERMINAL STATUS
    </div>


    <div class="side-row">
        <span>WEBSOCKET</span>
        <span>READY</span>
    </div>


    <div class="side-row">
        <span>BTC/USD</span>
        <span id="side-btc">--</span>
    </div>


    <div class="side-row">
        <span>ETH/USD</span>
        <span id="side-eth">--</span>
    </div>


    <div class="side-row">
        <span>SMC ENGINE</span>
        <span>ACTIVE</span>
    </div>


    <div class="side-row">
        <span>SFP ENGINE</span>
        <span>ACTIVE</span>
    </div>


    <div class="side-row">
        <span>15M / 5M</span>
        <span>READY</span>
    </div>

</aside>

</div>


<!-- =========================================================
     MOBILE BOTTOM NAV
     ========================================================= -->

<div class="bottom-nav">

    <button
        class="active"
        onclick="scrollToSection('markets',this)">
        <span>⌂</span>
        MARKETS
    </button>

    <button
        onclick="scrollToSection('signals',this)">
        <span>⚡</span>
        SIGNALS
    </button>

    <button
        onclick="scrollToSection('smc',this)">
        <span>◈</span>
        SMC
    </button>

    <button
        onclick="scrollToSection('logs',this)">
        <span>▤</span>
        LOGS
    </button>

    <button
        onclick="toggleTheme()">
        <span>☼</span>
        THEME
    </button>

</div>


<script>

/* ============================================================
   UI HELPERS
   ============================================================ */

function scrollToSection(id,btn){

    const target =
        document.getElementById(id);

    if(target){

        target.scrollIntoView({
            behavior:"smooth",
            block:"start"
        });

    }

    document
        .querySelectorAll(
            ".top-nav button,.bottom-nav button"
        )
        .forEach(
            b => b.classList.remove("active")
        );

    if(btn){
        btn.classList.add("active");
    }
}


/* ============================================================
   THEME
   ============================================================ */

function toggleTheme(){

    /*
       Neon UI intentionally stays dark.
       Button retained for compatibility.
    */

    document.body.style.filter =
        document.body.style.filter ===
        "brightness(1.08)"
        ? ""
        : "brightness(1.08)";
}


/* ============================================================
   TIME
   ============================================================ */

function updateClock(){

    const now =
        new Date();

    const el =
        document.getElementById(
            "utc-clock"
        );

    if(el){

        el.innerText =
            now.toUTCString()
                .split(" ")[4]
            + " UTC";

    }
}

setInterval(
    updateClock,
    1000
);

updateClock();


/* ============================================================
   ORIGINAL STATE
   ============================================================ */

let activeTF = "15m";

let activeSFPTF = "15m";


function switchTF(tf){

    activeTF = tf;

    document
        .getElementById("tab-15m")
        .classList
        .toggle(
            "active",
            tf === "15m"
        );

    document
        .getElementById("tab-5m")
        .classList
        .toggle(
            "active",
            tf === "5m"
        );

    document
        .querySelectorAll(".tf-label")
        .forEach(
            el =>
                el.innerText =
                tf.toUpperCase()
        );

    renderSMCUI("BTCUSD");
    renderSMCUI("ETHUSD");
}


function switchSFPTF(tf){

    activeSFPTF = tf;

    document
        .getElementById("sfp-tab-15m")
        .classList
        .toggle(
            "active",
            tf === "15m"
        );

    document
        .getElementById("sfp-tab-5m")
        .classList
        .toggle(
            "active",
            tf === "5m"
        );

    document
        .querySelectorAll(".sfp-tf-label")
        .forEach(
            el =>
                el.innerText =
                tf.toUpperCase()
        );

    document
        .getElementById("log-active-tf")
        .innerText =
        tf.toUpperCase();

    renderSFPUI("BTCUSD");
    renderSFPUI("ETHUSD");

    filterLogs();
}


/* ============================================================
   ORIGINAL STATE DATA
   ============================================================ */

const state = {

    BTCUSD: {

        price:0,
        spot:0,
        vol:0,
        cdh:0,
        cdl:0,
        pdh:0,
        pdl:0,
        dec:1,

        "15m":{
            action:"MONITOR",
            state:"SCANNING",
            obType:"--",
            obRange:"--",
            obStatus:"UNTESTED",
            entry:"--",
            sl:"--",
            narrative:""
        },

        "5m":{
            action:"MONITOR",
            state:"SCANNING",
            obType:"--",
            obRange:"--",
            obStatus:"UNTESTED",
            entry:"--",
            sl:"--",
            narrative:""
        },

        sfp_15m:{
            signal:"WAIT",
            badge:"NO SWEEP",
            entry:"--",
            sl:"--",
            tp1:"--",
            tp2:"--",
            step:1,
            rationale:"",
            lastSig:""
        },

        sfp_5m:{
            signal:"WAIT",
            badge:"NO SWEEP",
            entry:"--",
            sl:"--",
            tp1:"--",
            tp2:"--",
            step:1,
            rationale:"",
            lastSig:""
        }

    },


    ETHUSD: {

        price:0,
        spot:0,
        vol:0,
        cdh:0,
        cdl:0,
        pdh:0,
        pdl:0,
        dec:2,

        "15m":{
            action:"MONITOR",
            state:"SCANNING",
            obType:"--",
            obRange:"--",
            obStatus:"UNTESTED",
            entry:"--",
            sl:"--",
            narrative:""
        },

        "5m":{
            action:"MONITOR",
            state:"SCANNING",
            obType:"--",
            obRange:"--",
            obStatus:"UNTESTED",
            entry:"--",
            sl:"--",
            narrative:""
        },

        sfp_15m:{
            signal:"WAIT",
            badge:"NO SWEEP",
            entry:"--",
            sl:"--",
            tp1:"--",
            tp2:"--",
            step:1,
            rationale:"",
            lastSig:""
        },

        sfp_5m:{
            signal:"WAIT",
            badge:"NO SWEEP",
            entry:"--",
            sl:"--",
            tp1:"--",
            tp2:"--",
            step:1,
            rationale:"",
            lastSig:""
        }

    }

};


const logsHistory = [];


/* ============================================================
   FORMAT
   ============================================================ */

function fmt(val,dec){

    if(
        !val ||
        isNaN(val)
    ){
        return "--";
    }

    return Number(val)
        .toLocaleString(
            "en-US",
            {
                minimumFractionDigits:dec,
                maximumFractionDigits:dec
            }
        );
}


/* ============================================================
   LOGGING
   ============================================================ */

function addLog(tf,msg){

    const now =
        new Date()
            .toTimeString()
            .split(" ")[0];

    const item = {
        tf,
        text:msg,
        time:now
    };

    logsHistory.push(item);

    if(
        logsHistory.length > 80
    ){
        logsHistory.shift();
    }

    if(
        activeSFPTF === tf ||
        tf === "ALL"
    ){
        appendLogToBox(item);
    }
}


function appendLogToBox(log){

    const box =
        document.getElementById(
            "console-logs"
        );

    const el =
        document.createElement(
            "div"
        );

    el.className =
        "log-line";

    el.innerHTML =
        `<span class="log-time">
            [${log.time}]
        </span>
        <span class="log-tf">
            [${log.tf.toUpperCase()}]
        </span>
        ${log.text}`;

    box.appendChild(el);

    box.scrollTop =
        box.scrollHeight;
}


function filterLogs(){

    const box =
        document.getElementById(
            "console-logs"
        );

    box.innerHTML = "";

    logsHistory
        .filter(
            l =>
                l.tf === activeSFPTF ||
                l.tf === "ALL"
        )
        .forEach(
            appendLogToBox
        );
}


function clearLogs(){

    logsHistory.length = 0;

    document.getElementById(
        "console-logs"
    ).innerHTML =
        `<div class="log-line">
            <span class="log-time">
                [CLEARED]
            </span>
            Logs reset.
        </div>`;
}


/* ============================================================
   ORIGINAL DAILY CANDLE FETCH
   ============================================================ */

async function fetchDailyStats(){

    try{

        const symbols =
            ["BTCUSD","ETHUSD"];

        for(
            const sym of symbols
        ){

            const nowSec =
                Math.floor(
                    Date.now()/1000
                );

            const startSec =
                nowSec -
                (86400 * 3);

            const res =
                await fetch(
                    `https://api.india.delta.exchange/v2/history/candles?resolution=1d&symbol=${sym}&start=${startSec}&end=${nowSec}`
                );

            const data =
                await res.json();

            if(
                data.result &&
                data.result.length >= 2
            ){

                const today =
                    data.result[0];

                const yesterday =
                    data.result[1];

                state[sym].pdh =
                    parseFloat(
                        yesterday.high
                    );

                state[sym].pdl =
                    parseFloat(
                        yesterday.low
                    );

                state[sym].cdh =
                    parseFloat(
                        today.high
                    );

                state[sym].cdl =
                    parseFloat(
                        today.low
                    );

                updateMetricsUI(sym);

                evaluateSMC(
                    sym,
                    "15m"
                );

                evaluateSMC(
                    sym,
                    "5m"
                );

                evaluateSFPStrategy(
                    sym,
                    "15m"
                );

                evaluateSFPStrategy(
                    sym,
                    "5m"
                );

            }

        }

    }
    catch(e){

        console.log(
            "Candles err",
            e
        );

    }
}


/* ============================================================
   ORIGINAL SMC ENGINE
   ============================================================ */

function evaluateSMC(sym,tf){

    const d =
        state[sym];

    if(
        !d.price ||
        !d.pdh ||
        !d.pdl
    ){
        return;
    }

    const tfData =
        d[tf];

    const eq =
        (d.pdh + d.pdl) / 2;

    const distToPDH =
        d.price - d.pdh;

    const distToPDL =
        d.price - d.pdl;

    const factor =
        tf === "5m"
        ? 0.4
        : 1.0;

    const obBuffer =
        d.price *
        (
            tf === "5m"
            ? 0.0015
            : 0.0035
        );

    let action =
        "MONITOR";

    let stateText =
        "CONSOLIDATING";

    let obType = "";

    let obLow = 0;

    let obHigh = 0;

    let obStatus =
        "UNTESTED";

    let entry = "--";

    let sl = "--";

    let narrative = "";


    if(
        distToPDH >=
        -(25 * factor)
    ){

        action =
            "SELL / SHORT";

        stateText =
            tf === "5m"
            ? "5M CHoCH CONFIRMED"
            : "15M PDH LIQUIDITY SWEEP";

        obType =
            "🔴 Bearish Supply OB";

        obHigh =
            Math.max(
                d.cdh,
                d.pdh
            );

        obLow =
            obHigh - obBuffer;

        entry =
            `$${fmt(obLow,d.dec)} - $${fmt(obHigh,d.dec)}`;

        sl =
            `$${fmt(
                obHigh * 1.002,
                d.dec
            )}`;

        obStatus =
            d.price >= obLow &&
            d.price <= obHigh
            ? "MITIGATING"
            : "PENDING TAP";

        narrative =
            `${tf.toUpperCase()} Supply Order Block created above PDH ($${fmt(d.pdh,d.dec)}). Target internal discount liquidity.`;

    }

    else if(
        distToPDL <=
        (25 * factor)
    ){

        action =
            "BUY / LONG";

        stateText =
            tf === "5m"
            ? "5M CHoCH BREAKOUT"
            : "15M PDL LIQUIDITY RAID";

        obType =
            "🟢 Bullish Demand OB";

        obLow =
            Math.min(
                d.cdl,
                d.pdl
            );

        obHigh =
            obLow + obBuffer;

        entry =
            `$${fmt(obLow,d.dec)} - $${fmt(obHigh,d.dec)}`;

        sl =
            `$${fmt(
                obLow * 0.998,
                d.dec
            )}`;

        obStatus =
            d.price >= obLow &&
            d.price <= obHigh
            ? "MITIGATING"
            : "PENDING TAP";

        narrative =
            `${tf.toUpperCase()} Demand Order Block established near PDL ($${fmt(d.pdl,d.dec)}). Target EQ ($${fmt(eq,d.dec)}).`;

    }

    else{

        if(
            d.price > eq
        ){

            stateText =
                "PREMIUM BOS RETEST";

            action =
                tf === "5m"
                ? "WAIT SHORT"
                : "WATCH PREMIUM";

            obType =
                "Bearish Internal OB";

            obHigh =
                d.price +
                obBuffer;

            obLow =
                d.price;

            entry =
                `Retest $${fmt(
                    obHigh,
                    d.dec
                )}`;

            sl =
                `SL > $${fmt(
                    d.pdh,
                    d.dec
                )}`;

            obStatus =
                "INACTIVE";

            narrative =
                `${tf.toUpperCase()} trading above 50% EQ range. High time-frame bears defending supply.`;

        }

        else{

            stateText =
                "DISCOUNT OB MITIGATION";

            action =
                tf === "5m"
                ? "WAIT LONG"
                : "WATCH DISCOUNT";

            obType =
                "Bullish Internal OB";

            obLow =
                d.price -
                obBuffer;

            obHigh =
                d.price;

            entry =
                `Pullback $${fmt(
                    obLow,
                    d.dec
                )}`;

            sl =
                `SL < $${fmt(
                    d.pdl,
                    d.dec
                )}`;

            obStatus =
                "INACTIVE";

            narrative =
                `${tf.toUpperCase()} testing discount array. Look for shift of character on 5m for entry.`;

        }

    }


    tfData.action =
        action;

    tfData.state =
        stateText;

    tfData.obType =
        obType;

    tfData.obRange =
        `$${fmt(obLow,d.dec)} - $${fmt(obHigh,d.dec)}`;

    tfData.obStatus =
        obStatus;

    tfData.entry =
        entry;

    tfData.sl =
        sl;

    tfData.narrative =
        narrative;


    if(
        activeTF === tf
    ){

        renderSMCUI(sym);

    }

}


/* ============================================================
   ORIGINAL SFP + MSS ENGINE
   ============================================================ */

function evaluateSFPStrategy(sym,tf){

    const d =
        state[sym];

    if(
        !d.price ||
        !d.pdh ||
        !d.pdl
    ){
        return;
    }

    const key =
        tf === "15m"
        ? "sfp_15m"
        : "sfp_5m";

    const sfp =
        d[key];

    const eq =
        (d.pdh + d.pdl) / 2;

    const distToPDH =
        d.price - d.pdh;

    const distToPDL =
        d.price - d.pdl;

    const fvgBuffer =
        d.price *
        (
            tf === "5m"
            ? 0.001
            : 0.002
        );

    let signal =
        "WAIT";

    let badge =
        "IN RANGE";

    let entry =
        "--";

    let sl =
        "--";

    let tp1 =
        `$${
