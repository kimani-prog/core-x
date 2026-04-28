import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

# --- 1. FUTURISTIC DARK-THEME UI ---
st.set_page_config(page_title="CORE X | Tectitans UoN", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    /* Global Background and Fonts */
    .main { background: radial-gradient(circle, #1a1c23 0%, #0e1117 100%); color: #e1e1e1; }
    
    /* Glowing Glassmorphism Cards */
    .stMetric, .report-card {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid #00f2ff; /* Neon Cyan Border */
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Neon Accents for Text */
    [data-testid="stMetricValue"] { 
        color: #00f2ff; 
        font-family: 'Share Tech Mono', monospace; 
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.5); 
    }
    
    /* Buttons and File Uploader */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #00f2ff, #0072ff);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 20px #00f2ff;
        transform: scale(1.02);
    }
    
    /* Custom Headers */
    h1, h2, h3 { 
        color: #00f2ff; 
        text-transform: uppercase; 
        letter-spacing: 2px;
        font-family: 'Share Tech Mono', sans-serif;
    }

    .footer-text { text-align: center; color: #57606a; padding-top: 50px; font-family: 'Share Tech Mono'; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER SECTION ---
st.markdown("# 🛡️ CORE X: HYPERVISOR")
st.markdown("#### **TECTITANS** // STRATEGIC DEFENSE UNIT")
st.markdown("`LOCATION: C4D LAB | UNIVERSITY OF NAIROBI | KENYA`")
st.divider()

# --- 3. INTELLIGENCE ENGINE ---
@st.cache_data
def initialize_engine():
    filename = 'Android_Malware.csv'
    current_dir = os.path.dirname(__file__)
    target_path = os.path.join(current_dir, filename)

    if not os.path.exists(target_path):
        target_path = filename 
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Source Data Offline: {filename}")

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
    with st.spinner("⚡ DEPLOYING NEURAL SHIELDS..."):
        model, feature_names, live_accuracy = initialize_engine()
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("SHIELD", "ARMED", "Operational")
    m2.metric("ACCURACY", f"{live_accuracy:.2%}", "Synced")
    m3.metric("UPLINK", "C4D LAB", "Active")
    m4.metric("REGION", "KE_UON", "Secure")
except Exception as e:
    st.error(f"⚠️ SYSTEM BREACH DETECTED: {e}")
    st.stop()

st.divider()

# --- 4. SCANNER SANDBOX ---
st.header("🔍 THREAT ANALYSIS INTERFACE")
st.write("Intercept and analyze suspected application manifests.")

up_col, chart_col = st.columns([1, 1])

with up_col:
    uploaded_file = st.file_uploader("UPLOAD HEX-LOGS / CSV", type="csv")

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    try:
        # Data Alignment
        test_row = pd.DataFrame(columns=feature_names)
        for col in feature_names:
            test_row.loc[0, col] = input_df[col].iloc[0] if col in input_df.columns else 0
        
        test_row = test_row.astype(float)
        prediction = model.predict(test_row.values)
        probability = model.predict_proba(test_row.values)[0][1]

        # --- 5. FUTURISTIC BRIEFING REPORT ---
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.subheader("📡 DIAGNOSTIC BRIEFING")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**MISSION PARAMETERS:**")
            st.code(f"SCAN_TYPE: Heuristic_AI\nVECTOR_COUNT: {len(feature_names)}\nSTATUS: Completed")
        
        with c2:
            st.markdown("**THREAT PROBABILITY:**")
            risk_color = "#ff4b4b" if prediction[0] == 1 else "#00f2ff"
            st.markdown(f"<h2 style='color:{risk_color}; text-shadow: 0 0 10px {risk_color};'>{probability:.2%}</h2>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("💡 SYSTEM RECOMMENDATIONS")
        if prediction[0] == 1:
            st.error("⚠️ **MALWARE DETECTED.** Initiating Quarantine. File contains permissions inconsistent with benign software. DO NOT EXECUTE.")
        else:
            st.success("✔️ **INTEGRITY VERIFIED.** No malicious signatures found. File is safe for standard system integration.")
        
        st.markdown('</div>', unsafe_allow_html=True)

        with chart_col:
            st.subheader("🧠 NEURAL FINGERPRINT")
            display_values = test_row.values.flatten()[:10]
            radar_df = pd.DataFrame(dict(r=display_values, theta=[f"V_{i}" for i in range(len(display_values))]))
            
            fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True)
            fig.update_traces(fill='toself', line_color='#00f2ff', marker=dict(size=10, color='#ffffff'))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color="#00f2ff",
                polar=dict(
                    bgcolor='rgba(16, 20, 24, 0.5)',
                    radialaxis=dict(visible=True, range=[0, 1], gridcolor="#30363d"),
                    angularaxis=dict(gridcolor="#30363d")
                )
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"ANALYSIS INTERRUPTED: {e}")

# --- 6. FOOTER ---
st.markdown("---")
st.markdown("""<div class="footer-text"><b>HYPERVISOR v1.0.0 // TECTITANS</b><br>C4D LAB | UNIVERSITY OF NAIROBI | KENYA INCLUSIVITY IN TECH</div>""", unsafe_allow_html=True)
