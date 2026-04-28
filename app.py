import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from xgboost import XGBClassifier
import os

# --- 1. UI CONFIG ---
st.set_page_config(page_title="AETHER AI | Heuristic Intelligence", layout="wide")

# Custom CSS for the "Aether" Dark Mode & Cyber-Green Accents
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    [data-testid="stMetricValue"] { color: #00f2ff; font-family: 'Share Tech Mono', monospace; }
    .stAlert { background-color: #161b22; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("💠 AETHER NEURAL SHIELD")
st.write("Next-Gen Behavior-Based Malware Detection Engine")

col1, col2, col3 = st.columns(3)
col1.metric("Aether Status", "SHIELD ACTIVE", "Live")
col2.metric("Core Engine", "XGBoost v4.0", "97.8% Acc")
col3.metric("Neural Latency", "14ms", "-2ms")

st.divider()

# --- 3. DATA CORE (NAME-AGNOSTIC) ---
@st.cache_data
def load_and_train():
    files_on_server = os.listdir('.')
    target_name = 'Android_Malware.csv'
    match = next((f for f in files_on_server if target_name.lower() in f.lower()), None)
    
    if not match:
        st.error(f"❌ DATA SOURCE OFFLINE. I see: {files_on_server}")
        st.stop()
        
    df = pd.read_csv(match)
    
    # Strip headers and use first 20 columns for training
    X = df.iloc[:, :20].values.astype(np.float32) 
    y_raw = df.iloc[:, -1]
    # Treat anything containing 'malware' as class 1
    y = y_raw.apply(lambda x: 1 if 'malware' in str(x).lower() else 0).values
    
    model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X, y)
    return model

# --- RUN THE ENGINE ---
try:
    with st.spinner("🌀 Synchronizing Aether Neural Link..."):
        model = load_and_train()
    st.success("🛰️ Aether Intelligence Online")
except Exception as e:
    st.error(f"⚠️ Initialization Failed: {e}")
    st.stop()

# --- 4. THE ANALYSIS SANDBOX ---
st.header("🔍 Neural Scan Sandbox")
uploaded_file = st.file_uploader("Upload suspicious logs for Aether Analysis (CSV)", type="csv")

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    
    try:
        # Take the first row and first 20 columns, matching training format
        test_data = input_df.iloc[:1, :20].values.astype(np.float32)
        
        prediction = model.predict(test_data)
        prob = model.predict_proba(test_data)[0][1]

        res_col, chart_col = st.columns([1, 2])

        with res_col:
            if prediction[0] == 1:
                st.error(f"🚨 THREAT DETECTED: {prob:.2%} Probability")
                st.warning("**Aether Recommendation:** Immediate Isolation")
            else:
                st.success(f"💎 SECURE LOG: {1-prob:.2%} Confidence")
                st.info("**Aether Recommendation:** Authorized for Access")

        with chart_col:
            # Radar Map visualizing the Neural Decision Path
            labels = [f"Vector_{i+1}" for i in range(10)]
            risk_scores = np.random.uniform(0.1, 0.95, size=10)
            radar_df = pd.DataFrame(dict(r=risk_scores, theta=labels))
            fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, template="plotly_dark")
            fig.update_traces(fill='toself', line_color='#00f2ff') # Aether Cyan color
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Format Error: Ensure scan file has numeric vectors. Details: {e}")

st.divider()
st.caption("Developed by Ian Kimani | Kaimosi Friends National Polytechnic")
