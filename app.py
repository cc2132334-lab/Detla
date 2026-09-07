import streamlit as st
import websocket
import json
import threading
import time

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Delta Live Terminal v1.0.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INJECT CSS TO HIDE STREAMLIT TOOLBAR, HEADER & FOOTER ---
hide_streamlit_ui = """
<style>
    /* Hide top header, hamburger menu, deploy button, and decorations */
    header {visibility: hidden; display: none !important;}
    #MainMenu {visibility: hidden; display: none !important;}
    .stDeployButton {display: none !important;}
    #stDecoration {display: none !important;}
    div[data-testid="stToolbar"] {visibility: hidden; display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    
    /* Hide bottom footer and running status */
    footer {visibility: hidden; display: none !important;}
    div[data-testid="stStatusWidget"] {visibility: hidden; display: none !important;}
    
    /* Remove unnecessary default top paddings */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
</style>
"""
st.markdown(hide_streamlit_ui, unsafe_allow_html=True)

# --- GLOBAL TICK DATA STORE ---
if "market_data" not in st.session_state:
    st.session_state.market_data = {
        "BTCUSD": {"mark_price": "0.0", "spot_price": "0.0", "timestamp": "-"},
        "ETHUSD": {"mark_price": "0.0", "spot_price": "0.0", "timestamp": "-"}
    }

# Delta Exchange India WebSocket URL: wss://socket.india.delta.exchange
# Delta Global WebSocket URL: wss://socket.delta.exchange
WS_URL = "wss://socket.india.delta.exchange"
SYMBOLS = ["BTCUSD", "ETHUSD"]

def on_message(ws, message):
    try:
        data = json.loads(message)
        # v2/ticker payload parsing
        if "symbol" in data and data.get("symbol") in st.session_state.market_data:
            sym = data["symbol"]
            st.session_state.market_data[sym]["mark_price"] = data.get("mark_price", "0.0")
            st.session_state.market_data[sym]["spot_price"] = data.get("spot_price", "0.0")
            st.session_state.market_data[sym]["timestamp"] = time.strftime("%H:%M:%S")
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

# Start WebSocket thread once
if "ws_thread_started" not in st.session_state:
    st.session_state.ws_thread_started = True
    t = threading.Thread(target=run_ws, daemon=True)
    t.start()

# --- UI DISPLAY ---
st.subheader("⚡ Delta Live Feed [v1.0.0]")

col1, col2 = st.columns(2)

with col1:
    btc_box = st.empty()
with col2:
    eth_box = st.empty()

# --- FAST REFRESH LOOP ---
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

    # Minimal sleep for responsiveness
    time.sleep(0.1)
