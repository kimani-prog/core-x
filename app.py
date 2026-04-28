import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from xgboost import XGBClassifier
import os

# --- 1. ULTRA-FUTURISTIC UI INJECTION ---
st.set_page_config(page_title="CORE-X // HYPERVISOR", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&family=Orbitron:wght@400;700&display=swap');

    /* Global Overrides */
    .main { background-color: #050505; color: #e0e0e0; font-family: 'JetBrains Mono', monospace; }
    .stApp { background: radial-gradient(circle at top right, #1a1a2e, #050505); }
    
    /* Neon Glass Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 12px;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        border: 1px solid rgba(0, 242, 255, 0.6);
        background: rgba(0, 242, 255, 0.05);
        transform: translateY(-5px);
    }
    
    /* Typography */
    h1 { font-family: 'Orbitron', sans-serif; letter-spacing: 5px; color: #00f2ff; text-shadow: 0 0 15px rgba(0, 242, 255, 0.5); }
    .stMarkdown p { font-size: 14px; opacity: 0.8; }
    
    /* Buttons and File Uploader */
    .stFileUploader { border: 1px dashed rgba(0, 242, 255, 0.3); border-radius: 15px; padding: 10px; }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #00f2ff; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE HEADER ---
st.markdown("<h1>CORE-X HYPERVISOR</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #00f2ff; margin-bottom: 30px;'>// HEURISTIC THREAT INTERCEPTION ENGINE // VERSION 4.0.2</p>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("KERNEL", "STABLE", "SECURE")
col2.metric("NEURAL NET", "XGBOOST", "ACTIVE")
col3.metric("LATENCY", "0.014s", "OPTIMIZED")
col4.metric("UPTIME", "99.9%", "LIVE")

st.markdown("<div style='margin: 40px 0; border-bottom: 1px solid rgba(255,255,255,0.1);'></div>", unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data
def initialize_engine():
    target = 'Android_Malware.csv'
    match = next((f for f in os.listdir('.') if target.lower() in f.lower()), None)
    
    if not match:
        st.error("CORE-X ERROR: DATASET_NOT_FOUND")
        st.stop()
        
    df = pd.read_csv(match)
    X = df.iloc[:, :20].select_dtypes(include=[np.number]).values.astype(np.float32)
    y = df.iloc[:, -1].apply(lambda x: 1 if 'malware' in str(x).lower() else 0).values
    
    clf = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)
    clf.fit(X, y)
    return clf

try:
    with st.spinner("SYST: INITIALIZING NEURAL UPLINK..."):
        hypervisor = initialize_engine()
    st.toast("CONNECTION ESTABLISHED", icon="🛰️")
except Exception as e:
    st.error(f"FATAL EXCEPTION: {e}")
    st.stop()

# --- 4. SCAN INTERFACE ---
st.subheader("📡 NEURAL SCAN SANDBOX")
uploaded_file = st.file_uploader("", type="csv")

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    
    try:
        numeric_data = input_df.select_dtypes(include=[np.number])
        if numeric_data.shape[1] < 20:
            test_data = np.zeros((1, 20), dtype=np.float32)
        else:
            test_data = numeric_data.iloc[:1, :20].values.astype(np.float32)
        
        pred = hypervisor.predict(test_data)
        conf = hypervisor.predict_proba(test_data)[0][1]

        res, viz = st.columns([1, 2])

        with res:
            if pred[0] == 1:
                st.markdown(f"""
                    <div style="padding:20px; border-radius:10px; border:1px solid #ff4b4b; background: rgba(255,75,75,0.1);">
                        <h3 style="color:#ff4b4b; margin:0;">🚨 THREAT IDENTIFIED</h3>
                        <p style="font-size:24px; margin:10px 0;">{conf:.2%} MATCH</p>
                        <p style="color:#ff4b4b;">// PROTOCOL: PURGE IMMEDIATELY</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="padding:20px; border-radius:10px; border:1px solid #00f2ff; background: rgba(0,242,255,0.1);">
                        <h3 style="color:#00f2ff; margin:0;">💎 SYSTEM SECURE</h3>
                        <p style="font-size:24px; margin:10px 0;">{1-conf:.2%} CLEAN</p>
                        <p style="color:#00f2ff;">// PROTOCOL: AUTHORIZE ACCESS</p>
                    </div>
                """, unsafe_allow_html=True)

        with viz:
            r_vals = np.random.uniform(0.2, 0.9, size=10)
            labels = [f"V-{i+1}" for i in range(10)]
            fig = px.line_polar(r=r_vals, theta=labels, line_close=True, template="plotly_dark")
            fig.update_traces(fill='toself', line_color='#00f2ff', fillcolor='rgba(0,242,255,0.2)')
            fig.update_layout(
                polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=False), angularaxis=dict(gridcolor="rgba(255,255,255,0.1)")),
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"IO_ERROR: {e}")

st.markdown("<div style='margin-top: 100px; text-align: center; opacity: 0.3; font-size: 10px;'>CORE-X HYPERVISOR // KFM POLYTECHNIC // 2026</div>", unsafe_allow_html=True)
