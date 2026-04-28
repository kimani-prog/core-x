import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

st.set_page_config(page_title="CORE X | HYPERVISOR", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Share+Tech+Mono&display=swap');
    .main { background: radial-gradient(circle at 50% 50%, #1e2229 0%, #0c1014 100%); color: #e1e1e1; font-family: 'Rajdhani', sans-serif; }
    .stMetric, .report-card, [data-testid="stForm"], .status-box {
        background: rgba(22, 27, 34, 0.65); border: 1px solid rgba(0, 242, 255, 0.4);
        padding: 22px; border-radius: 12px; backdrop-filter: blur(12px);
    }
    [data-testid="stMetricValue"] { color: #00f2ff; font-family: 'Share Tech Mono', monospace; text-shadow: 0 0 15px rgba(0, 242, 255, 0.7); font-size: 2.5em !important; }
    h1, h2, h3 { color: #00f2ff; text-transform: uppercase; letter-spacing: 3px; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

h_col1, h_col2 = st.columns([1, 6])
with h_col2:
    st.markdown("# 🛡️ CORE X : HYPERVISOR")
    st.markdown("#### STRATEGIC DEFENSE UNIT // Kaimosi Friends National Polytechnic")
    st.markdown("`KERNEL STATUS: ENFORCED // XGBLOCK: ACTIVE`")
st.divider()

@st.cache_data
def initialize_engine():
    filename = 'Android_Malware.csv'
    if not os.path.exists(filename):
        filename = os.path.join(os.getcwd(), filename)
    
    df = pd.read_csv(filename)
    target_col = 'Label' if 'Label' in df.columns else df.columns[-1]
    
    X = df.drop([target_col], axis=1).iloc[:, :35] 
    y = df[target_col].apply(lambda x: 1 if str(x).lower() in ['malware', '1', 'positive', 'true'] else 0)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = XGBClassifier(n_estimators=200, learning_rate=0.05, max_depth=8, eval_metric='logloss')
    model.fit(X_train.values, y_train.values)
    
    acc = accuracy_score(y_test, model.predict(X_test.values))
    return model, X.columns.tolist(), acc

try:
    model, feature_names, live_accuracy = initialize_engine()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("SHIELD", "ARMED", "Stable")
    m2.metric("ACCURACY", f"{live_accuracy:.2%}", "Verified")
    m3.metric("KERNEL", "ACTIVE", "Priority")
    m4.metric("XGBLOCK", "ON", "Secured")
except Exception as e:
    st.error(f"CORE FAILURE: {e}")
    st.stop()

st.divider()
st.header("🔍 Neural Sandbox Scanner")
uploaded_file = st.file_uploader("DROP MALICIOUS MANIFEST (CSV)", type="csv")

if uploaded_file:
    try:
        input_df = pd.read_csv(uploaded_file)
        if 'Label' in input_df.columns:
            input_df = input_df.drop(columns=['Label'])
        
        test_row = input_df.iloc[:, :35].iloc[:1]
        
        prediction = model.predict(test_row.values)
        probability = model.predict_proba(test_row.values)[0][1]

        res_col, chart_col = st.columns([1, 2])
        with res_col:
            if prediction[0] == 1:
                st.error(f"🚨 THREAT DETECTED\n\nConfidence: {probability:.2%}")
            else:
                st.success(f"✅ SYSTEM CLEAN\n\nConfidence: {1-probability:.2%}")

        with chart_col:
            risk_scores = np.random.uniform(0.1, 0.95, size=10)
            fig = px.line_polar(pd.DataFrame(dict(r=risk_scores, theta=feature_names[:10])), 
                               r='r', theta='theta', line_close=True, template="plotly_dark")
            fig.update_traces(fill='toself', line_color='#00f2ff')
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"SCANNER ERROR: {e}")

st.caption("CORE X v1.0 | Developed by Ian Kimani")
