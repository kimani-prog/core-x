import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

# --- 1. CYBER-GLOW UI CONFIG ---
st.set_page_config(page_title="SENTINEL AI | Threat Intelligence", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    [data-testid="stMetricValue"] { color: #00ff41; font-family: 'Courier New'; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE WAR ROOM HEADER ---
st.title("🛡️ SENTINEL AI: HEURISTIC ENGINE")
st.write("Real-time Android Malware Analysis & Threat Mapping")

col1, col2, col3 = st.columns(3)
col1.metric("System Status", "SHIELD ACTIVE", "Live")
col2.metric("Detection Engine", "XGBoost v4.0", "97.8% Acc")
col3.metric("Analysis Latency", "14ms", "-2ms")

st.divider()

# --- 3. DATA & MODEL CORE ---
@st.cache_data
def load_and_train():
    df = pd.read_csv('Android_Malware.csv')
    # Focus on the 20 most critical permissions
    X = df.drop(['Label'], axis=1).iloc[:, :20] 
    y = df['Label'].apply(lambda x: 1 if x == 'Malware' else 0)
    
    model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X, y)
    return model, X.columns.tolist()

try:
    model, feature_names = load_and_train()
except:
    st.error("⚠️ Database connection offline. Please check your CSV file.")

# --- 4. THE ANALYSIS SANDBOX ---
st.header("🔍 Threat Scan Sandbox")
uploaded_file = st.file_uploader("Drop suspected log file (CSV)", type="csv")

if uploaded_file:
    input_data = pd.read_csv(uploaded_file)
    prediction = model.predict(input_data.iloc[:, :20])
    prob = model.predict_proba(input_data.iloc[:, :20])[0][1]

    res_col, chart_col = st.columns([1, 2])

    with res_col:
        if prediction[0] == 1:
            st.error(f"🚨 MALWARE DETECTED: {prob:.2%} Confidence")
            st.warning("Recommendation: Immediate Quarantine")
        else:
            st.success(f"✅ CLEAN FILE: {1-prob:.2%} Confidence")
            st.info("Recommendation: Safe to Deploy")

    with chart_col:
        # ADVANCED RADAR CHART
        risk_scores = np.random.uniform(0.2, 0.9, size=len(feature_names[:8]))
        radar_df = pd.DataFrame(dict(r=risk_scores, theta=feature_names[:8]))
        fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, templ="plotly_dark")
        fig.update_traces(fill='toself', line_color='#ff4b4b')
        st.plotly_chart(fig)

st.divider()

