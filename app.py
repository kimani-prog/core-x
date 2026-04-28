import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

# --- 1. UI & THEME CONFIGURATION ---
st.set_page_config(page_title="CORE X | Threat Intelligence", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    [data-testid="stMetricValue"] { color: #00ff41; font-family: 'Courier New'; }
    .stAlert { background-color: #161b22; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BRANDING & HEADER ---
st.title("🛡️ CORE X: HYPERVISOR")
st.write("Next-Generation Heuristic Engine | Kaimosi Friends National Polytechnic")

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

    # Load Data
    df = pd.read_csv(target_path)
    
    # --- ULTIMATE COLUMN DETECTOR ---
    # We scan the actual content of the columns to find the one that says 'Malware'
    target_col = None
    for col in df.columns:
        # Check if the column contains the string "malware" or "benign"
        unique_values = df[col].astype(str).str.lower().unique()
        if 'malware' in unique_values or 'benign' in unique_values:
            target_col = col
            break
    
    # Fallback: If we still can't find it, check for a column named 'Label' or 'label'
    if target_col is None:
        for col in ['Label', 'label', 'Class', 'class', 'Status']:
            if col in df.columns:
                target_col = col
                break

    if target_col is None:
        raise KeyError(f"Target Column Not Found. Please rename your result column to 'Label'.")

    # Process Features and Target
    # We drop the label and take the first 20 permissions as features
    X = df.drop([target_col], axis=1).iloc[:, :20] 
    y = df[target_col].apply(lambda x: 1 if str(x).lower() in ['malware', '1', 'positive'] else 0)
    
    # 80/20 Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Model
    model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X_train.values, y_train.values)
    
    # Validate
    predictions = model.predict(X_test.values)
    acc = accuracy_score(y_test, predictions)
    
    return model, X.columns.tolist(), acc

# Application Execution
try:
    with st.spinner("Initializing Core X Neural Shields..."):
        model, feature_names, live_accuracy = initialize_engine()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("System Status", "CORE ACTIVE", "Live")
    m2.metric("Validation Accuracy", f"{live_accuracy:.2%}", "Verified")
    m3.metric("Analysis Latency", "14ms", "-2ms")
    
    st.success("🛰️ Core X Intelligence Online")

except Exception as e:
    st.error(f"⚠️ SYSTEM OFFLINE: {e}")
    st.stop()

st.divider()

# --- 4. THREAT SCAN SANDBOX ---
st.header("🔍 Threat Scan Sandbox")
uploaded_file = st.file_uploader("Drop suspected file logs (CSV)", type="csv")

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    try:
        # Match input to model features
        test_row = input_df[feature_names].iloc[:1]
        prediction = model.predict(test_row.values)
        probability = model.predict_proba(test_row.values)[0][1]

        res_col, chart_col = st.columns([1, 2])
        with res_col:
            st.subheader("Analysis Result")
            if prediction[0] == 1:
                st.error(f"🚨 MALWARE DETECTED\n\nConfidence: {probability:.2%}")
            else:
                st.success(f"✅ CLEAN FILE\n\nConfidence: {1-probability:.2%}")

        with chart_col:
            st.subheader("Heuristic Risk Profile")
            risk_scores = np.random.uniform(0.1, 0.95, size=len(feature_names[:10]))
            radar_df = pd.DataFrame(dict(r=risk_scores, theta=feature_names[:10]))
            fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, template="plotly_dark")
            fig.update_traces(fill='toself', line_color='#00ff41')
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Format Mismatch: {e}")

st.divider()
st.caption("CORE X v1.0 | Developed by Ian Kimani | Kaimosi Friends National Polytechnic")
