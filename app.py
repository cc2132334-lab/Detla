import streamlit as st
import websocket
import json
import threading
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Delta Live Terminal v1.0.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. AGGRESSIVE CSS: HIDE ALL STREAMLIT TOOLBARS & MANAGE APP BUTTON ---
hide_streamlit_ui = """
<style>
    /* Top Header, Toolbar, Menu, Deploy Button */
    header, header[data-testid="stHeader"] {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    #MainMenu {display: none !important;}
    .stDeployButton {display: none !important;}

    /* Bottom Footer, Running Status */
    footer {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}

    /* Streamlit Cloud Specific: Manage App Button, Viewer Badges, Floating Actions */
    [data-testid="manage-app-button"] {display: none !important;}
    button[title="Manage app"] {display: none !important;}
    .viewerBadge_container__r5tak {display: none !important;}
    .viewerBadge_link__qRIco {display: none !important;}
    div[class*="viewerBadge"] {display: none !important;}
    div[class*="manage-app"] {display: none !important;}
    div[class*="StreamlitFloatingActions"] {display: none !important;}
    div[data-testid="stFloatingActions"] {display: none !important;}

    /* Mobile & Desktop Clean Full-Screen Layout */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
</style>
"""
st.markdown(hide_streamlit_ui, unsafe_allow_html=True)

# --- 3. GLOBAL TICK DATA STORE ---
if "market_data" not in st.session_state:
    st.session_state.market_data = {
        "BTCUSD": {"mark_price": "0.0", "spot_price": "0.0"},
        "ETHUSD": {"mark_price": "0.0", "spot_price": "0.0"}
    }

# Delta Exchange India WebSocket (Change to wss://socket.delta.exchange for Global)
WS_URL = "wss://socket.india.delta.exchange"
SYMBOLS = ["BTCUSD", "ETHUSD"]

def on_message(ws, message):
    try:
        data = json.loads(message)
        if "symbol" in data and data.get("symbol") in st.session_state.market_data:
            sym = data["symbol"]
            st.session_state.market_data[sym]["mark_price"] = data.get("mark_price", "0.0")
            st.session_state.market_data[sym]["spot_price"] = data.get("spot_price", "0.0")
    except Exception:
        pass

def on_open(ws):
    payload = {
        "type": "subscribe",
        "payload": {
            "channels": [
                {
                    "name": "v2/ticker",
                    "symbols": SYMBOLS
                }
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
            ws.run_forever()
        except Exception:
            time.sleep(2)

# Run WebSocket in Background Thread
if "ws_thread_started" not in st.session_state:
    st.session_state.ws_thread_started = True
    t = threading.Thread(target=run_ws, daemon=True)
    t.start()

# --- 4. DASHBOARD UI ---
st.subheader("⚡ Delta Live Feed [v1.0.0]")

col1, col2 = st.columns(2)

with col1:
    btc_box = st.empty()
with col2:
    eth_box = st.empty()

# --- 5. REAL-TIME FAST REFRESH LOOP ---
while True:
    btc_info = st.session_state.market_data.get("BTCUSD", {})
    eth_info = st.session_state.market_data.get("ETHUSD", {})

    btc_box.metric(
        label="BTC/USD",
        value=f"${float(btc_info.get('mark_price', 0)):,.2f}",
        delta=f"Spot: ${float(btc_info.get('spot_price', 0)):,.2f}"
    )

    eth_box.metric(
        label="ETH/USD",
        value=f"${float(eth_info.get('mark_price', 0)):,.2f}",
        delta=f"Spot: ${float(eth_info.get('spot_price', 0)):,.2f}"
    )

    time.sleep(0.2)
