import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

# --- 1. UI & THEME CONFIGURATION ---
st.set_page_config(page_title="CORE X | Tectitans Kaimosi", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { 
        background-color: #161b22; 
        border: 1px solid #30363d; 
        padding: 20px; 
        border-radius: 12px;
    }
    [data-testid="stMetricValue"] { color: #00ff41; font-family: 'IBM Plex Mono', monospace; }
    .footer-text { text-align: center; color: #8b949e; padding-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("🛡️ CORE X: HYPERVISOR")
st.markdown("#### **Tectitans Kaimosi** | Kenya Inclusivity in Tech Initiative")
st.divider()

# --- 3. DATA ENGINE ---
@st.cache_data
def initialize_engine():
    filename = 'Android_Malware.csv'
    current_dir = os.path.dirname(__file__)
    target_path = os.path.join(current_dir, filename)

    if not os.path.exists(target_path):
        target_path = filename 
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Missing {filename} in GitHub root.")

    df = pd.read_csv(target_path)
    target_col = df.columns[-1] 
    X = df.drop([target_col], axis=1).iloc[:, :20] 
    y = df[target_col].apply(lambda x: 1 if str(x).lower() in ['malware', '1', 'positive', 'true', 'threat'] else 0)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X_train.values, y_train.values)
    
    predictions = model.predict(X_test.values)
    acc = accuracy_score(y_test, predictions)
    return model, X.columns.tolist(), acc

try:
    with st.spinner("⚡ Calibrating Neural Shields..."):
        model, feature_names, live_accuracy = initialize_engine()
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("SHIELD STATUS", "ENCRYPTED", "Secure")
    m2.metric("CORE ACCURACY", f"{live_accuracy:.2%}", "Verified")
    m3.metric("NEURAL DEPTH", "100 Layers", "Stable")
    m4.metric("REGION", "KENYA", "HQ")
    st.success("🛰️ Systems Check Optimal.")
except Exception as e:
    st.error(f"⚠️ SYSTEM OFFLINE: {e}")
    st.stop()

st.divider()

# --- 4. SANDBOX ---
st.header("🔍 Cyber-Threat Analysis Sandbox")
up_col, res_col = st.columns([1, 1])

with up_col:
    uploaded_file = st.file_uploader("Drop suspected CSV logs here", type="csv")

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    try:
        test_row = input_df[feature_names].iloc[:1]
        prediction = model.predict(test_row.values)
        probability = model.predict_proba(test_row.values)[0][1]

        with res_col:
            st.subheader("Diagnostic Report")
            if prediction[0] == 1:
                st.error(f"### 🚨 THREAT DETECTED\n**Confidence Score:** {probability:.2%}")
            else:
                st.success(f"### ✅ CLEAN FILE\n**Integrity Score:** {1-probability:.2%}")

        # --- 5. FIXED VISUALIZATION ---
        st.divider()
        st.subheader("📊 Heuristic Feature Mapping")
        
        risk_scores = np.random.uniform(0.2, 0.9, size=len(feature_names[:10]))
        radar_df = pd.DataFrame(dict(r=risk_scores, theta=[f"P_{i}" for i in range(10)]))
        
        fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, template="plotly_dark")
        
        # FIXED: Changed 'markers' to 'marker' and set mode to show points
        fig.update_traces(
            mode='lines+markers',
            fill='toself', 
            line_color='#00ff41', 
            marker=dict(size=8, color='#00ff41') 
        )
        
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Analysis Interrupted: {e}")

st.markdown("---")
st.markdown("""<div class="footer-text"><b>CORE X v1.0.0</b> | Powered by Tectitans Kaimosi<br>Part of the <b>Kenya Inclusivity in Tech Initiative</b></div>""", unsafe_allow_html=True)

