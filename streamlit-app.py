import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Wind Turbine SME Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0d0f12 !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background-color: #111318 !important; }
[data-testid="stMainBlockContainer"] { padding: 2rem 3rem !important; max-width: 1100px; }

/* ── TOPBAR ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #1e2330;
    padding-bottom: 20px;
    margin-bottom: 40px;
}
.topbar-left { display: flex; align-items: center; gap: 14px; }
.topbar-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #e2e4e9;
    letter-spacing: -0.2px;
}
.topbar-sub {
    font-size: 0.75rem;
    color: #4a5568;
    margin-top: 2px;
}
.topbar-right { display: flex; align-items: center; gap: 16px; }
.status-pill {
    display: flex; align-items: center; gap: 7px;
    background: #111318;
    border: 1px solid #1e2330;
    border-radius: 20px;
    padding: 5px 12px;
}
.status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 6px rgba(34,197,94,0.5);
    animation: blink 2.5s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.35} }
.status-text {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #6b7280;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.model-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #6b7280;
    background: #111318;
    border: 1px solid #1e2330;
    border-radius: 4px;
    padding: 5px 10px;
    letter-spacing: 0.5px;
}

/* ── CONSOLE PANEL ── */
.console-panel {
    background: #111318;
    border: 1px solid #1e2330;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 20px;
}
.console-header {
    background: #0d0f12;
    border-bottom: 1px solid #1e2330;
    padding: 13px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.console-header-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: #6b7280;
    letter-spacing: 1.2px;
    text-transform: uppercase;
}
.console-body { padding: 20px; }

.input-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: #3d4455;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

/* ── TEXTAREA ── */
.stTextArea textarea {
    background-color: #0d0f12 !important;
    color: #c9d1d9 !important;
    border: 1px solid #1e2330 !important;
    border-radius: 6px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    line-height: 1.65 !important;
    padding: 16px !important;
    resize: vertical !important;
    caret-color: #f5a623;
    box-shadow: none !important;
    outline: none !important;
}
.stTextArea textarea:focus {
    border-color: rgba(245,166,35,0.35) !important;
    box-shadow: 0 0 0 3px rgba(245,166,35,0.05) !important;
}
.stTextArea textarea::placeholder { color: #252836 !important; }
.stTextArea label { display: none !important; }

/* ── BUTTON ── */
.stButton > button {
    background: #f5a623 !important;
    color: #0d0f12 !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    padding: 11px 28px !important;
    transition: all 0.15s !important;
    width: auto !important;
}
.stButton > button:hover {
    background: #e8961a !important;
    box-shadow: 0 4px 14px rgba(245,166,35,0.2) !important;
}

/* ── RESULT ── */
.result-panel {
    background: #111318;
    border: 1px solid #1e2330;
    border-radius: 8px;
    overflow: hidden;
    margin-top: 20px;
}
.result-panel-header {
    background: #0d0f12;
    border-bottom: 1px solid #1e2330;
    padding: 13px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.result-panel-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: #6b7280;
    letter-spacing: 1.2px;
    text-transform: uppercase;
}
.result-ok-chip {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: #4ade80;
    background: rgba(74,222,128,0.07);
    border: 1px solid rgba(74,222,128,0.15);
    border-radius: 4px;
    padding: 3px 9px;
    letter-spacing: 0.8px;
}
.result-body {
    padding: 24px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    color: #c9d1d9;
    line-height: 1.8;
    white-space: pre-wrap;
    word-break: break-word;
    border-left: 2px solid #f5a623;
}

/* ── ALERTS ── */
.stAlert {
    background: #111318 !important;
    border: 1px solid #1e2330 !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.84rem !important;
    color: #9ca3af !important;
}

/* ── FOOTER ── */
.footer {
    margin-top: 40px;
    padding-top: 18px;
    border-top: 1px solid #1c1e26;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.footer-text {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: #2d3344;
    letter-spacing: 0.5px;
}

/* hide Streamlit chrome */
#MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── TOPBAR ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-left">
        <div>
            <div class="topbar-title">Wind Turbine Equipment — SME Assistant</div>
            <div class="topbar-sub">Predictive Maintenance &amp; Diagnostic Analysis</div>
        </div>
    </div>
    <div class="topbar-right">
        <div class="model-tag">amazon.nova-pro-v1</div>
        <div class="status-pill">
            <div class="status-dot"></div>
            <div class="status-text">Online</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── INPUT PANEL ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="console-panel">
    <div class="console-header">
        <div class="console-header-title">Equipment Log Input</div>
    </div>
    <div class="console-body">
""", unsafe_allow_html=True)

st.markdown('<div class="input-label">// Paste raw equipment logs below</div>', unsafe_allow_html=True)

prompt = st.text_area(
    label="log_input",
    height=200,
    placeholder="Paste equipment logs, sensor data, or fault records here...",
    label_visibility="collapsed"
)

col_l, col_btn, col_r = st.columns([4, 2, 4])
with col_btn:
    analyze_btn = st.button("Run Diagnostic")

st.markdown("</div></div>", unsafe_allow_html=True)

# ── RESULT PANEL ─────────────────────────────────────────────────────────────
if analyze_btn:
    if not prompt.strip():
        st.warning("No log data detected. Paste equipment logs to proceed.")
    else:
        with st.spinner("Analyzing equipment data..."):
            try:
                response = requests.post(
                    "https://jmu8tqrqda.execute-api.ap-south-1.amazonaws.com/prod/sme_assistant",
                    json={"prompt": prompt},
                    timeout=30
                )
                if response.status_code == 200:
                    response_data = response.json()
                    if isinstance(response_data, dict) and "body" in response_data:
                        result = json.loads(response_data["body"])
                    else:
                        result = response_data

                    st.markdown(f"""
                    <div class="result-panel">
                        <div class="result-panel-header">
                            <div class="result-panel-title">Expert Analysis Output</div>
                            <div class="result-ok-chip">Analysis Complete</div>
                        </div>
                        <div class="result-body">{result}</div>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    st.error(f"API error — HTTP {response.status_code}")

            except requests.exceptions.Timeout:
                st.error("Request timed out (30s). The endpoint may be warming up — please retry.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-text">Wind Turbine SME Assistant · AWS Lambda · API Gateway · ap-south-1</div>
    <div class="footer-text">Powered by Amazon Bedrock</div>
</div>
""", unsafe_allow_html=True)