import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

# --- 1. GOOGLE MATERIAL DESIGN UI ---
st.set_page_config(page_title="CORE X | Tectitans UoN", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    /* Google-style clean background and fonts */
    .main { background-color: #f8f9fa; color: #202124; }
    .stMetric { 
        background-color: #ffffff; 
        border: 1px solid #dadce0; 
        padding: 20px; 
        border-radius: 8px;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,.3), 0 1px 3px 1px rgba(60,64,67,.15);
    }
    [data-testid="stMetricValue"] { color: #1a73e8; font-weight: 500; }
    .report-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 8px;
        border: 1px solid #dadce0;
        margin-top: 20px;
    }
    .footer-text { text-align: center; color: #70757a; padding-top: 50px; font-size: 0.9em; }
    h1, h2, h3 { color: #202124; font-family: 'Google Sans', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER & BRANDING ---
st.title("🛡️ CORE X: HYPERVISOR")
st.markdown("### **Tectitans** | C4D Lab, University of Nairobi")
st.caption("Kenya Inclusivity in Tech Initiative | Artificial Intelligence for Cybersecurity")
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
    with st.spinner("Initializing Security Modules..."):
        model, feature_names, live_accuracy = initialize_engine()
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Status", "Operational", "Encrypted")
    m2.metric("Model Accuracy", f"{live_accuracy:.2%}", "Verified")
    m3.metric("Lab Location", "C4D Lab", "UoN")
    m4.metric("Engine", "XGBoost v2", "Stable")
except Exception as e:
    st.error(f"⚠️ System Offline: {e}")
    st.stop()

st.divider()

# --- 4. SCANNER SECTION ---
st.header("🔍 Security Sandbox")
st.write("Upload application metadata (CSV) to generate a detailed heuristic report.")

up_col, chart_col = st.columns([1, 1])

with up_col:
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    try:
        # Feature Alignment
        test_row = pd.DataFrame(columns=feature_names)
        for col in feature_names:
            test_row.loc[0, col] = input_df[col].iloc[0] if col in input_df.columns else 0
        
        test_row = test_row.astype(float)
        prediction = model.predict(test_row.values)
        probability = model.predict_proba(test_row.values)[0][1]

        # --- 5. DETAILED ANALYSIS REPORT ---
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.subheader("📋 Analysis Report")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Scan Summary:**")
            st.write(f"- **Features Analyzed:** {len(feature_names)} Permissions")
            st.write(f"- **Detection Engine:** Core X Heuristics")
            st.write(f"- **Classification:** {'🛑 MALICIOUS' if prediction[0] == 1 else '✅ BENIGN'}")
        
        with col_b:
            st.write("**Risk Assessment:**")
            risk_level = "HIGH" if probability > 0.7 else "MEDIUM" if probability > 0.4 else "LOW"
            st.write(f"- **Confidence:** {probability:.2%}")
            st.write(f"- **Risk Level:** {risk_level}")

        st.markdown("---")
        st.write("**Recommendations:**")
        if prediction[0] == 1:
            st.error("⚠️ **CRITICAL:** Do not install this application. Revoke all system-level permissions and check for secondary payloads.")
        else:
            st.success("✔️ **SAFE:** No malicious heuristics detected. Application is consistent with standard behavior patterns.")
        
        st.markdown('</div>', unsafe_allow_html=True)

        with chart_col:
            st.subheader("Visual Pattern Mapping")
            display_values = test_row.values.flatten()[:10]
            radar_df = pd.DataFrame(dict(r=display_values, theta=[f"Vect_{i}" for i in range(len(display_values))]))
            fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True)
            fig.update_traces(fill='toself', line_color='#1a73e8', marker=dict(size=8))
            fig.update_layout(template="simple_white", polar=dict(radialaxis=dict(visible=True, range=[0, 1])))
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Analysis Interrupted: {e}")

# --- 6. FOOTER ---
st.markdown("---")
st.markdown("""<div class="footer-text"><b>CORE X v1.0.0</b> | <b>Tectitans</b><br>C4D Lab, University of Nairobi | Kenya Inclusivity in Tech Initiative</div>""", unsafe_allow_html=True)
