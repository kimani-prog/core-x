import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.metrics import accuracy_score, roc_auc_score
from xgboost import XGBClassifier

# --- PAGE SETUP ---
st.set_page_config(page_title="SENTINEL AI | Malware Intelligence", layout="wide", page_icon="🛡️")

# --- ADVANCED UI ENGINE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #050505;
        color: #E0E0E0;
    }

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 15, 15, 0.95);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Metric Cards - Modern Floating Style */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #111111, #1a1a1a);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: transform 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
    }

    /* High-End Button */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 12px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        width: 100%;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
        transition: 0.3s all;
    }
    .stButton>button:hover {
        box-shadow: 0 6px 25px rgba(37, 99, 235, 0.5);
        transform: scale(1.02);
    }

    /* Modern Headers */
    h1 { font-weight: 800 !important; color: white !important; background: -webkit-linear-gradient(#fff, #999); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    h2, h3 { font-weight: 600 !important; color: #3b82f6 !important; }

    /* Custom Checkbox Styling */
    .stCheckbox label {
        font-size: 0.9rem !important;
        color: #9ca3af !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col_head1, col_head2 = st.columns([2, 1])
with col_head1:
    st.title("SENTINEL AI")
    st.markdown("#### Cloud-Native Malware Intelligence & Heuristic Analysis")

# --- DATA PROCESSING LOGIC ---
@st.cache_data
def process_intel(file):
    df = pd.read_csv(file)
    X = df.drop('Result', axis=1)
    y = df['Result']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    selector = SelectKBest(chi2, k=20)
    X_train_sel = selector.fit_transform(X_train, y_train)
    X_test_sel = selector.transform(X_test)
    
    model = XGBClassifier(n_estimators=100, eval_metric='logloss', random_state=42)
    model.fit(X_train_sel, y_train)
    
    y_pred = model.predict(X_test_sel)
    y_prob = model.predict_proba(X_test_sel)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    top_features = [X.columns[i] for i in selector.get_support(indices=True)]
    
    return df, model, selector, acc, auc, top_features, X

# --- SIDEBAR ---
st.sidebar.markdown("### 🛰️ CONTROL PANEL")
uploaded_file = st.sidebar.file_uploader("Upload Security Logs (CSV)", type="csv")

if uploaded_file is not None:
    df, model, selector, acc, auc, top_features, X_raw = process_intel(uploaded_file)
    
    # --- METRICS SECTION ---
    st.markdown("### 📊 ENGINE STATUS")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Predictive Accuracy", f"{acc:.2%}")
    m2.metric("Neural Confidence", f"{auc:.3f}")
    m3.metric("Nodes Scanned", f"{len(df)}")
    m4.metric("Engine State", "Optimized")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- VISUALIZATION SECTION ---
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### ☣️ THREAT OVERVIEW")
        counts = df['Result'].value_counts()
        fig1, ax1 = plt.subplots(figsize=(6, 6))
        fig1.patch.set_facecolor('none')
        ax1.set_facecolor('none')
        ax1.pie(counts, labels=['Safe', 'Infected'], autopct='%1.1f%%', startangle=90, 
               colors=['#10b981', '#ef4444'], textprops={'color':"w", 'weight':'bold'},
               wedgeprops={'width': 0.5, 'edgecolor': 'none'}) # Donut chart for modern look
        st.pyplot(fig1)

    with col2:
        st.markdown("#### ⚡ ATTACK VECTORS")
        perm_counts = df.drop('Result', axis=1).sum().sort_values(ascending=False).head(10)
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        fig2.patch.set_facecolor('none')
        ax2.set_facecolor('none')
        sns.barplot(x=perm_counts.values, y=[p.split('.')[-1] for p in perm_counts.index], palette="Blues_r", ax=ax2)
        ax2.tick_params(colors='#9ca3af', labelsize=10)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        st.pyplot(fig2)

    # --- PREDICTION SANDBOX ---
    st.markdown("---")
    st.markdown("### 🧪 HEURISTIC SANDBOX")
    st.info("Simulate permission requests to generate an AI risk score.")
    
    user_inputs = {}
    cols = st.columns(4)
    for i, feature in enumerate(top_features):
        clean_name = feature.split('.')[-1]
        user_inputs[feature] = cols[i % 4].checkbox(f"• {clean_name}", key=f"feat_{i}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("RUN MALWARE ANALYSIS"):
        input_row = pd.DataFrame([{col: 1 if user_inputs.get(col) else 0 for col in X_raw.columns}])
        input_sel = selector.transform(input_row)
        pred = model.predict(input_sel)[0]
        prob = model.predict_proba(input_sel)[0][1]
        
        if pred == 1:
            st.error(f"🚨 **CRITICAL THREAT:** {prob:.2%} Probability. App behavior matches known Malicious patterns.")
        else:
            st.success(f"✅ **SECURE:** {1-prob:.2%} Clean Score. No malicious heuristic signatures found.")

else:
    # Modern Empty State
    st.markdown("<div style='text-align: center; margin-top: 100px; color: #4b5563;'>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/ios/100/3b82f6/data-configuration.png")
    st.markdown("### Awaiting Data Input")
    st.markdown("Please upload your security logs via the sidebar to initialize the Sentinel Engine.")
    st.markdown("</div>", unsafe_allow_html=True)

