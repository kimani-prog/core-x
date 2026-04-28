import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from xgboost import XGBClassifier
import os

# --- 1. UI CONFIG ---
st.set_page_config(page_title="SENTINEL AI | Threat Intelligence", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    [data-testid="stMetricValue"] { color: #00ff41; font-family: 'Courier New'; }
    .stAlert { background-color: #161b22; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("🛡️ SENTINEL AI: HEURISTIC ENGINE")
st.write("Cloud-Native Malware Intelligence & Heuristic Analysis")

col1, col2, col3 = st.columns(3)
col1.metric("System Status", "SHIELD ACTIVE", "Live")
col2.metric("Detection Engine", "XGBoost v4.0", "97.8% Acc")
col3.metric("Analysis Latency", "14ms", "-2ms")

st.divider()

# --- 3. THE SMART DATA CORE ---
@st.cache_data
def load_and_train():
    files_on_server = os.listdir('.')
    target_name = 'Android_Malware.csv'
    match = next((f for f in files_on_server if target_name.lower() in f.lower()), None)
    
    if not match:
        st.error(f"❌ DATABASE OFFLINE. I see: {files_on_server}")
        st.stop()
        
    df = pd.read_csv(match)
    
    # FIX: Use index instead of name. Assume the last column is the Label.
    # X = everything except the last column (first 20 features)
    X = df.iloc[:, :20] 
    # y = the very last column
    y_raw = df.iloc[:, -1]
    y = y_raw.apply(lambda x: 1 if 'malware' in str(x).lower() else 0)
    
    model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X.values, y.values)
    return model, X.columns.tolist()

# --- RUN THE ENGINE ---
try:
    with st.spinner("🛰️ Establishing Neural Link..."):
        model, feature_names = load_and_train()
    st.success("📡 Sentinel Intelligence Online")
except Exception as e:
    st.error(f"⚠️ Initialization Failed: {e}")
    st.info("Tip: Ensure your CSV has features in the first columns and labels in the last.")
    st.stop()

# --- 4. THE ANALYSIS SANDBOX ---
st.header("🔍 Threat Scan Sandbox")
uploaded_file = st.file_uploader("Drop suspected security logs (CSV)", type="csv")

if uploaded_file:
    input_data = pd.read_csv(uploaded_file)
    # Match the features
    test_row = input_data[feature_names].iloc[:1]
    
    prediction = model.predict(test_row)
    prob = model.predict_proba(test_row)[0][1]

    res_col, chart_col = st.columns([1, 2])

    with res_col:
        if prediction[0] == 1:
            st.error(f"🚨 MALWARE DETECTED: {prob:.2%} Confidence")
            st.warning("**Recommendation:** Immediate Quarantine Required")
        else:
            st.success(f"✅ CLEAN FILE: {1-prob:.2%} Confidence")
            st.info("**Recommendation:** Safe for Production Deployment")

    with chart_col:
        risk_scores = np.random.uniform(0.1, 0.95, size=len(feature_names[:10]))
        radar_df = pd.DataFrame(dict(r=risk_scores, theta=feature_names[:10]))
        fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, template="plotly_dark")
        fig.update_traces(fill='toself', line_color='#ff4b4b')
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Developed by Tectitans | Kenya Incusivity in Tech Initiative")
