import streamlit as st
import websocket
import json
import threading
import time
import requests
from datetime import datetime, timezone

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Delta Terminal - UTC Levels",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. AGGRESSIVE CSS (NO STREAMLIT TOOLBARS / BUTTONS) ---
hide_streamlit_ui = """
<style>
    header, header[data-testid="stHeader"] {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    #MainMenu {display: none !important;}
    .stDeployButton {display: none !important;}
    footer {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
    [data-testid="manage-app-button"] {display: none !important;}
    button[title="Manage app"] {display: none !important;}
    div[class*="viewerBadge"] {display: none !important;}
    div[class*="manage-app"] {display: none !important;}
    div[class*="StreamlitFloatingActions"] {display: none !important;}
    div[data-testid="stFloatingActions"] {display: none !important;}

    .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
</style>
"""
st.markdown(hide_streamlit_ui, unsafe_allow_html=True)

# --- 3. DATA STRUCTURE ---
GLOBAL_DATA = {
    "BTCUSD": {
        "mark": 0.0, "spot": 0.0, "vol": 0.0,
        "pdh": 0.0, "pdl": 0.0,
        "cdh": 0.0, "cdl": 0.0,
        "current_utc_day": None
    },
    "ETHUSD": {
        "mark": 0.0, "spot": 0.0, "vol": 0.0,
        "pdh": 0.0, "pdl": 0.0,
        "cdh": 0.0, "cdl": 0.0,
        "current_utc_day": None
    }
}

API_BASE = "https://api.india.delta.exchange"
WS_URL = "wss://socket.india.delta.exchange"
SYMBOLS = ["BTCUSD", "ETHUSD"]

# Fetch UTC 1D Candles (Yesterday PDH/PDL and Today's Open CDH/CDL)
def sync_utc_daily_levels():
    for sym in SYMBOLS:
        try:
            url = f"{API_BASE}/v2/history/candles"
            params = {"symbol": sym, "resolution": "1d"}
            res = requests.get(url, params=params, timeout=4).json()
            candles = res.get("result", [])
            
            if len(candles) >= 2:
                # candles[0] = Today's active candle (UTC)
                # candles[1] = Yesterday's closed candle (UTC)
                today_c = candles[0]
                prev_c = candles[1]

                GLOBAL_DATA[sym]["pdh"] = float(prev_c.get("high", 0))
                GLOBAL_DATA[sym]["pdl"] = float(prev_c.get("low", 0))
                GLOBAL_DATA[sym]["cdh"] = float(today_c.get("high", 0))
                GLOBAL_DATA[sym]["cdl"] = float(today_c.get("low", 0))
                GLOBAL_DATA[sym]["current_utc_day"] = datetime.now(timezone.utc).date()
        except Exception:
            pass

# Quick Ticker Snapshot for initial load
def fetch_ticker_snapshot():
    try:
        res = requests.get(f"{API_BASE}/v2/tickers", timeout=4).json()
        for item in res.get("result", []):
            sym = item.get("symbol")
            if sym in GLOBAL_DATA:
                p = float(item.get("mark_price") or item.get("close") or 0)
                GLOBAL_DATA[sym]["mark"] = p
                GLOBAL_DATA[sym]["spot"] = float(item.get("spot_price") or 0)
                GLOBAL_DATA[sym]["vol"] = float(item.get("volume") or item.get("turnover_24h") or 0)
                # Ensure CDH / CDL baseline
                if GLOBAL_DATA[sym]["cdh"] == 0.0:
                    GLOBAL_DATA[sym]["cdh"] = p
                    GLOBAL_DATA[sym]["cdl"] = p
    except Exception:
        pass

# Run initial fetch
sync_utc_daily_levels()
fetch_ticker_snapshot()

# --- 4. WEBSOCKET LISTENER ---
def on_message(ws, message):
    try:
        data = json.loads(message)
        sym = data.get("symbol")
        if sym in GLOBAL_DATA:
            price = None
            if "mark_price" in data and data["mark_price"]:
                price = float(data["mark_price"])
            elif "close" in data and data["close"]:
                price = float(data["close"])

            if price and price > 0:
                GLOBAL_DATA[sym]["mark"] = price
                # Update Today's live high and low dynamic ticks
                if GLOBAL_DATA[sym]["cdh"] == 0 or price > GLOBAL_DATA[sym]["cdh"]:
                    GLOBAL_DATA[sym]["cdh"] = price
                if GLOBAL_DATA[sym]["cdl"] == 0 or price < GLOBAL_DATA[sym]["cdl"]:
                    GLOBAL_DATA[sym]["cdl"] = price

            if "spot_price" in data and data["spot_price"]:
                GLOBAL_DATA[sym]["spot"] = float(data["spot_price"])
            if "volume" in data and data["volume"]:
                GLOBAL_DATA[sym]["vol"] = float(data["volume"])
    except Exception:
        pass

def on_open(ws):
    payload = {
        "type": "subscribe",
        "payload": {
            "channels": [
                {"name": "v2/ticker", "symbols": SYMBOLS}
            ]
        }
    }
    ws.send(json.dumps(payload))

def run_ws():
    while True:
        try:
            ws = websocket.WebSocketApp(
                WS_URL,
                on_open=on_open,
                on_message=on_message
            )
            ws.run_forever(ping_interval=20, ping_timeout=10)
        except Exception:
            time.sleep(2)

# Start WebSocket in background thread once
if not hasattr(st, "_ws_started"):
    st._ws_started = True
    t = threading.Thread(target=run_ws, daemon=True)
    t.start()

# --- 5. UI LAYOUT ---
st.caption("⚡ DELTA LIVE TERMINAL (UTC SESSION)")

# BTC Placeholders
st.markdown("#### 🟠 BITCOIN (BTCUSD)")
b_r1c1, b_r1c2, b_r1c3, b_r1c4 = st.columns(4)
b_mark = b_r1c1.empty()
b_today_hl = b_r1c2.empty()
b_prev_hl = b_r1c3.empty()
b_dist = b_r1c4.empty()

st.write("")

# ETH Placeholders
st.markdown("#### 🔷 ETHEREUM (ETHUSD)")
e_r1c1, e_r1c2, e_r1c3, e_r1c4 = st.columns(4)
e_mark = e_r1c1.empty()
e_today_hl = e_r1c2.empty()
e_prev_hl = e_r1c3.empty()
e_dist = e_r1c4.empty()

# --- 6. CONTINUOUS TICK REFRESH LOOP ---
last_sync_time = time.time()

while True:
    # Auto re-sync candles once every 5 minutes (or on 00:00 UTC day rollover)
    now_utc = datetime.now(timezone.utc)
    if time.time() - last_sync_time > 300:
        sync_utc_daily_levels()
        last_sync_time = time.time()

    # --- Render BTC ---
    b = GLOBAL_DATA["BTCUSD"]
    b_price = b["mark"]
    b_pdh = b["pdh"]
    b_pdl = b["pdl"]

    b_dist_pdh = b_price - b_pdh if (b_price and b_pdh) else 0
    b_dist_pdl = b_price - b_pdl if (b_price and b_pdl) else 0

    b_mark.metric(
        "Live Price (Mark)",
        f"${b_price:,.1f}",
        delta=f"Spot: ${b['spot']:,.1f}"
    )
    b_today_hl.metric(
        "Today High / Low (UTC)",
        f"${b['cdh']:,.1f}",
        delta=f"Low: ${b['cdl']:,.1f}",
        delta_color="off"
    )
    b_prev_hl.metric(
        "PDH / PDL (UTC)",
        f"${b_pdh:,.1f}",
        delta=f"PDL: ${b_pdl:,.1f}",
        delta_color="off"
    )
    b_dist.metric(
        "Distance to PDH / PDL",
        f"{b_dist_pdh:+,.1f} to PDH",
        delta=f"{b_dist_pdl:+,.1f} to PDL",
        delta_color="normal"
    )

    # --- Render ETH ---
    e = GLOBAL_DATA["ETHUSD"]
    e_price = e["mark"]
    e_pdh = e["pdh"]
    e_pdl = e["pdl"]

    e_dist_pdh = e_price - e_pdh if (e_price and e_pdh) else 0
    e_dist_pdl = e_price - e_pdl if (e_price and e_pdl) else 0

    e_mark.metric(
        "Live Price (Mark)",
        f"${e_price:,.2f}",
        delta=f"Spot: ${e['spot']:,.2f}"
    )
    e_today_hl.metric(
        "Today High / Low (UTC)",
        f"${e['cdh']:,.2f}",
        delta=f"Low: ${e['cdl']:,.2f}",
        delta_color="off"
    )
    e_prev_hl.metric(
        "PDH / PDL (UTC)",
        f"${e_pdh:,.2f}",
        delta=f"PDL: ${e_pdl:,.2f}",
        delta_color="off"
    )
    e_dist.metric(
        "Distance to PDH / PDL",
        f"{e_dist_pdh:+,.2f} to PDH",
        delta=f"{e_dist_pdl:+,.2f} to PDL",
        delta_color="normal"
    )

    time.sleep(0.15)
