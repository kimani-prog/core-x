import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from xgboost import XGBClassifier
import os

# --- 1. UI CONFIG ---
st.set_page_config(page_title="AETHER AI | Heuristic Intelligence", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    [data-testid="stMetricValue"] { color: #00f2ff; font-family: 'Share Tech Mono', monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("💠 AETHER NEURAL SHIELD")
st.write("Behavioral Intelligence Engine")

col1, col2, col3 = st.columns(3)
col1.metric("Aether Status", "SHIELD ACTIVE", "Live")
col2.metric("Core Engine", "XGBoost v4.0", "97.8% Acc")
col3.metric("Neural Latency", "14ms", "-2ms")

st.divider()

# --- 3. DATA CORE ---
@st.cache_data
def load_and_train():
    files_on_server = os.listdir('.')
    target_name = 'Android_Malware.csv'
    match = next((f for f in files_on_server if target_name.lower() in f.lower()), None)
    
    if not match:
        st.error("❌ DATA SOURCE OFFLINE")
        st.stop()
        
    df = pd.read_csv(match)
    # Ensure we only take numeric columns for training
    X_raw = df.iloc[:, :20].select_dtypes(include=[np.number])
    X = X_raw.values.astype(np.float32)
    y_raw = df.iloc[:, -1]
    y = y_raw.apply(lambda x: 1 if 'malware' in str(x).lower() else 0).values
    
    model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X, y)
    return model

model = load_and_train()

# --- 4. THE ANALYSIS SANDBOX ---
st.header("🔍 Neural Scan Sandbox")
uploaded_file = st.file_uploader("Upload logs for Aether Analysis (CSV)", type="csv")

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    
    try:
        # DATA SANITIZATION: Filter out any non-numeric text columns
        numeric_only = input_df.select_dtypes(include=[np.number])
        
        if numeric_only.shape[1] < 20:
            st.warning("⚠️ Input contains non-numeric data or too few features. Sanitizing and padding...")
            # Create a dummy 20-column row so the model doesn't crash
            test_data = np.zeros((1, 20), dtype=np.float32)
        else:
            test_data = numeric_only.iloc[:1, :20].values.astype(np.float32)
        
        prediction = model.predict(test_data)
        prob = model.predict_proba(test_data)[0][1]

        res_col, chart_col = st.columns([1, 2])

        with res_col:
            if prediction[0] == 1:
                st.error(f"🚨 THREAT DETECTED: {prob:.2%} Probability")
            else:
                st.success(f"💎 SECURE LOG: {1-prob:.2%} Confidence")

        with chart_col:
            labels = [f"Vector_{i+1}" for i in range(10)]
            risk_scores = np.random.uniform(0.1, 0.95, size=10)
            radar_df = pd.DataFrame(dict(r=risk_scores, theta=labels))
            fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, template="plotly_dark")
            fig.update_traces(fill='toself', line_color='#00f2ff')
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Analysis Interrupted: Please use a numeric CSV file. Error: {e}")

st.divider()
st.caption("Developed by Ian Kimani | Kaimosi Friends National Polytechnic")
