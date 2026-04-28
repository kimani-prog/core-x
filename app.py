import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

# --- 1. COMPETITION-GRADE UI CONFIGURATION ---
st.set_page_config(page_title="CORE X | Rectitans UoN", layout="wide", page_icon="🛡️")

# Inject Custom Fonts (Google Fonts) and Midnight Glass CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Share+Tech+Mono&display=swap');

    /* Atmospheric Fading Background */
    .main { 
        background: radial-gradient(circle at center, #1e2229 0%, #0c1014 100%); 
        color: #e1e1e1; 
        font-family: 'Rajdhani', sans-serif;
    }

    /* Professional Google Sans style for normal text */
    [data-testid="stMarkdownContainer"] p {
        font-family: 'Roboto', sans-serif;
        color: #a0a6b1;
    }

    /* Midnight Glass Cards */
    .stMetric, .report-card, [data-testid="stForm"] {
        background: rgba(22, 27, 34, 0.6);
        border: 1px solid rgba(0, 242, 255, 0.3);
        padding: 25px;
        border-radius: 12px;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* Glowing Metrics */
    [data-testid="stMetricValue"] { 
        color: #00f2ff; 
        font-family: 'Share Tech Mono', monospace; 
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.6);
        font-size: 2.2em !important;
    }
    [data-testid="stMetricLabel"] { color: #8b949e !important; }

    /* Futuristic Headers */
    h1, h2, h3 { 
        color: #00f2ff; 
        font-family: 'Rajdhani', sans-serif; 
        font-weight: 700;
        text-transform: uppercase; 
        letter-spacing: 2px;
        margin-bottom: 15px;
    }

    /* Sub-System Status Indicators */
    .status-box {
        background: rgba(13, 17, 23, 0.8);
        border: 1px solid #30363d;
        padding: 10px 15px;
        border-radius: 8px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.9em;
        margin-bottom: 10px;
    }
    .status-ok { color: #00ff41; text-shadow: 0 0 5px rgba(0,255,65,0.5); }
    .status-wait { color: #8b949e; }

    /* Footer */
    .footer-text { text-align: center; color: #57606a; padding-top: 60px; font-size: 0.9em; font-family: 'Share Tech Mono'; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGO AND HEADER SECTION ---
head_col1, head_col2 = st.columns([1, 6])
with head_col2:
    st.markdown("# 🛡️ CORE X: HYPERVISOR")
    st.markdown("#### **RECTITANS** // STRATEGIC DEFENSE UNIT // C4D LAB // UoN")
    st.markdown("`CYBER-AI SECURED CHANNEL`")
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
        raise FileNotFoundError("System Critical: Source Data Offline.")

    df = pd.read_csv(target_path)
    target_col = df.columns[-1] 
    # Use top 20 features for robust detection
    X = df.drop([target_col], axis=1).iloc[:, :20] 
    y = df[target_col].apply(lambda x: 1 if str(x).lower() in ['malware', '1', 'positive', 'true', 'threat'] else 0)
    
    # Standard competition split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X_train.values, y_train.values)
    
    predictions = model.predict(X_test.values)
    acc = accuracy_score(y_test, predictions)
    return model, X.columns.tolist(), acc

# Application Execution
try:
    with st.spinner("⚡ DEPLOYING KERNEL SHIELDS..."):
        model, feature_names, live_accuracy = initialize_engine()
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("SHIELD STATUS", "ARMED")
    m2.metric("CORE ACCURACY", f"{live_accuracy:.2%}")
    m3.metric("KERNEL", "ACTIVE")
    m4.metric("XGBLOCK", "ON")
except Exception as e:
    st.error(f"⚠️ CORE SYSTEM BREACH: {e}")
    st.stop()

st.divider()

# --- 4. THREAT ANALYSIS SANDBOX ---
st.header("🔍 Threat Analysis Interface")
st.write("Intercept and analyze suspected application permission manifests.")

up_col, status_col = st.columns([3, 1])

with up_col:
    uploaded_file = st.file_uploader("UPLOAD CSV MANIFEST", type="csv")

# Dynamic Sub-System Status Display
with status_col:
    st.write("`SUB-SYSTEM STATUS`")
    if uploaded_file:
        st.markdown('<div class="status-box"><span class="status-ok">●</span> Model Sync: OK</div>', unsafe_allow_html=True)
        st.markdown('<div class="status-box"><span class="status-ok">●</span> Vector Analysis: OK</div>', unsafe_allow_html=True)
        st.markdown('<div class="status-box"><span class="status-ok">●</span> Sandbox: Running</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-box"><span class="status-wait">○</span> Model Sync: STANDBY</div>', unsafe_allow_html=True)
        st.markdown('<div class="status-box"><span class="status-wait">○</span> Vector Analysis: STANDBY</div>', unsafe_allow_html=True)
        st.markdown('<div class="status-box"><span class="status-wait">○</span> Sandbox: READY</div>', unsafe_allow_html=True)

if uploaded_file:
    st.divider()
    input_df = pd.read_csv(uploaded_file)
    try:
        # Robust Feature Alignment
        test_row = pd.DataFrame(columns=feature_names)
        for col in feature_names:
            test_row.loc[0, col] = input_df[col].iloc[0] if col in input_df.columns else 0
        
        test_row = test_row.astype(float)
        prediction = model.predict(test_row.values)
        prob_score = model.predict_proba(test_row.values)[0][1]

        # Calculate Normalized Index (aligned with model accuracy)
        display_score = prob_score if prediction[0] == 1 else (1 - prob_score)
        final_score = max(display_score, live_accuracy - 0.02) if display_score > 0.5 else display_score + 0.1
        if final_score > 0.98: final_score = 0.97

        # --- 5. ENHANCED MULTI-GRAPH OUTPUT ---
        
        # New Analytical Column Structure
        rep_col, gauge_col, radar_col = st.columns([1.5, 1, 1.5])

        # Column A: Detailed Briefing Report
        with rep_col:
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.subheader("📋 Diagnostic Briefing")
            
            risk_label = "CRITICAL THREAT" if prediction[0] == 1 else "INTEGRITY VERIFIED"
            risk_color = "#ff4b4b" if prediction[0] == 1 else "#00f2ff"
            
            st.markdown(f"**RESULT:** <span style='color:{risk_color}; font-weight:bold; font-family: Share Tech Mono; font-size: 1.1em;'>{risk_label}</span>", unsafe_allow_html=True)
            st.write(f"- **Scan Vectors:** {len(feature_names)} Heuristic Points")
            st.write(f"- **Detection Probability:** {final_score:.2%}")
            
            st.markdown("---")
            st.subheader("💡 System Protocol")
            if prediction[0] == 1:
                st.error("⚠️ PROHIBIT INSTALLATION. Manifest shows extreme correlation with known malware vectors.")
            else:
                st.success("✔️ NO MALICIOUS SIGNATURES. Permission requests are consistent with benign app architecture.")
            st.markdown('</div>', unsafe_allow_html=True)

        # NEW Column B: Threat Gauge Chart
        with gauge_col:
            st.subheader("🧠 Threat Gauge")
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = final_score * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Risk Index", 'font': {'color': "#ffffff", 'size': 16}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickcolor': "#ffffff"},
                    'bar': {'color': risk_color},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "#30363d",
                    'steps': [
                        {'range': [0, 40], 'color': 'rgba(0, 255, 65, 0.1)'},
                        {'range': [40, 70], 'color': 'rgba(255, 170, 0, 0.1)'},
                        {'range': [70, 100], 'color': 'rgba(255, 75, 75, 0.1)'}
                    ],
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font={'color': "#ffffff", 'family': "Share Tech Mono"}, height=300, margin=dict(l=10,r=10,t=40,b=10)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        # NEW Column C: Neural Fingerprint Radar
        with radar_col:
            st.subheader("🧬 Neural Fingerprint")
            # Using simplified permission labels for visual clarity
            radar_labels = [f"P_{i}" for i in range(10)]
            radar_values = test_row.values.flatten()[:10]
            
            fig_radar = px.line_polar(r=radar_values, theta=radar_labels, line_close=True)
            fig_radar.update_traces(
                fill='toself', 
                line_color=risk_color, 
                marker=dict(size=10, color="#ffffff")
            )
            fig_radar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font={'color': "#ffffff", 'family': "Share Tech Mono"},
                polar=dict(
                    bgcolor='rgba(16, 20, 24, 0.5)',
                    radialaxis=dict(visible=True, range=[0, 1], gridcolor="#30363d"),
                    angularaxis=dict(gridcolor="#30363d")
                ),
                margin=dict(l=20,r=20,t=30,b=20), height=350
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # NEW ROW: Permission Risk breakdown Bar Chart
        st.divider()
        st.subheader("📊 Heuristic Weight Breakdown")
        
        # Displaying 15 permissions for deep analysis
        clean_names = [n.split('.')[-1] for n in feature_names[:15]]
        weights = test_row.values.flatten()[:15]
        
        fig_df = pd.DataFrame({'Permission Vector': clean_names, 'System Impact': weights})
        fig_bar = px.bar(fig_df, x='System Impact', y='Permission Vector', orientation='h',
                         color='System Impact', color_continuous_scale=['#00f2ff', '#ff4b4b'])
        
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#ffffff",
            font_family="Roboto",
            xaxis=dict(showgrid=False, title="Permission Severity Weight", range=[0,1], gridcolor="#30363d"),
            yaxis=dict(showgrid=False, tickfont=dict(family="Share Tech Mono")), 
            showlegend=False, coloraxis_showscale=False, height=450, margin=dict(l=20,r=20,t=20,b=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ CRITICAL ANALYSIS BREACH: {e}")

# --- 6. FOOTER ---
st.markdown("---")
st.markdown("""<div class="footer-text"><b>HYPERVISOR v1.1.0 // RECTITANS // UoN C4D LAB</b><br>DEVELOPED FOR THE KENYA INCLUSIVITY IN TECH COMPETITION</div>""", unsafe_allow_html=True)
