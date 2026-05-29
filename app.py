import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# =========================
# PAGE CONFIG — must be FIRST
# =========================
st.set_page_config(
    page_title="NexaTel · Customer Intelligence",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root tokens ── */
:root {
    --bg:        #0A0D14;
    --surface:   #111520;
    --surface2:  #161B2A;
    --border:    #1E2738;
    --accent:    #00E5C3;
    --accent2:   #3D7EFF;
    --danger:    #FF4D6D;
    --warn:      #FFB547;
    --text:      #E8EDF5;
    --muted:     #6B7A99;
    --font-h:    'Syne', sans-serif;
    --font-b:    'DM Sans', sans-serif;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-b) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1300px !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 2rem; }

/* ── Sidebar logo band ── */
.sidebar-logo {
    display: flex; align-items: center; gap: 10px;
    padding: 0 1rem 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.sidebar-logo .dot {
    width: 36px; height: 36px; border-radius: 10px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.sidebar-logo span {
    font-family: var(--font-h); font-weight: 800;
    font-size: 1.2rem; letter-spacing: -0.5px;
}
.sidebar-logo span em { color: var(--accent); font-style: normal; }

/* ── Sidebar radio nav ── */
div[data-testid="stRadio"] > label { display: none; }
div[data-testid="stRadio"] > div {
    display: flex; flex-direction: column; gap: 4px;
}
div[data-testid="stRadio"] > div > label {
    display: flex; align-items: center;
    padding: 10px 14px; border-radius: 10px;
    cursor: pointer; transition: all .2s;
    font-family: var(--font-b); font-size: 0.9rem; font-weight: 500;
    color: var(--muted) !important;
    border: 1px solid transparent;
}
div[data-testid="stRadio"] > div > label:hover {
    background: var(--surface2); color: var(--text) !important;
}
div[data-testid="stRadio"] > div > label[data-checked="true"],
div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: linear-gradient(135deg, rgba(0,229,195,.12), rgba(61,126,255,.12));
    border-color: rgba(0,229,195,.3);
    color: var(--accent) !important;
}

/* ── Section label ── */
.section-label {
    font-family: var(--font-b); font-size: 0.68rem; font-weight: 500;
    letter-spacing: .12em; text-transform: uppercase;
    color: var(--muted); margin: 1.5rem 0 .6rem;
    padding: 0 1rem;
}

/* ── Sidebar widget labels ── */
[data-testid="stSidebar"] label {
    font-family: var(--font-b) !important;
    font-size: 0.78rem !important; font-weight: 500 !important;
    color: var(--muted) !important; letter-spacing: .04em;
    text-transform: uppercase;
}

/* ── Selectbox & slider ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stSlider"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important; color: var(--text) !important;
}
[data-testid="stSlider"] [data-testid="stThumbValue"] { color: var(--accent) !important; }
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
}

/* ── Page header banner ── */
.page-header {
    display: flex; align-items: flex-start;
    gap: 20px; margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}
.page-header .icon-box {
    width: 52px; height: 52px; flex-shrink: 0;
    border-radius: 14px; display: flex; align-items: center;
    justify-content: center; font-size: 24px;
}
.page-header h1 {
    font-family: var(--font-h) !important; font-weight: 800 !important;
    font-size: 1.6rem !important; line-height: 1.2 !important;
    margin: 0 0 4px !important;
}
.page-header p { margin: 0; color: var(--muted); font-size: .88rem; }

/* ── Metric cards ── */
.metric-row { display: grid; gap: 16px; margin: 1.5rem 0; }
.metric-row-3 { grid-template-columns: repeat(3,1fr); }
.metric-row-2 { grid-template-columns: repeat(2,1fr); }
.metric-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 14px; padding: 20px 22px;
    transition: border-color .2s;
}
.metric-card:hover { border-color: rgba(0,229,195,.3); }
.metric-card .mc-label {
    font-size: .7rem; font-weight: 600; letter-spacing: .1em;
    text-transform: uppercase; color: var(--muted); margin-bottom: 8px;
}
.metric-card .mc-value {
    font-family: var(--font-h); font-size: 2rem; font-weight: 700; line-height: 1;
}
.metric-card .mc-sub {
    font-size: .78rem; color: var(--muted); margin-top: 4px;
}

/* ── Stat pill ── */
.stat-pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 12px; border-radius: 100px; font-size: .8rem; font-weight: 500;
}
.pill-green  { background: rgba(0,229,195,.12); color: var(--accent); }
.pill-red    { background: rgba(255,77,109,.12); color: var(--danger); }
.pill-yellow { background: rgba(255,181,71,.12); color: var(--warn);   }
.pill-blue   { background: rgba(61,126,255,.12); color: var(--accent2);}

/* ── Alert banners ── */
.alert-banner {
    display: flex; align-items: flex-start; gap: 14px;
    padding: 18px 20px; border-radius: 12px; margin: 1rem 0;
    border-left: 3px solid;
}
.alert-danger  { background: rgba(255,77,109,.08);  border-color: var(--danger); }
.alert-warn    { background: rgba(255,181,71,.08);   border-color: var(--warn);  }
.alert-success { background: rgba(0,229,195,.08);    border-color: var(--accent);}
.alert-banner .al-icon { font-size: 1.3rem; margin-top: 2px; }
.alert-banner .al-title { font-family: var(--font-h); font-weight: 700; font-size: .95rem; margin-bottom: 2px; }
.alert-banner .al-body  { font-size: .84rem; color: var(--muted); }

/* ── Gauge bar ── */
.gauge-wrap { margin: 1.5rem 0; }
.gauge-label { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: .82rem; }
.gauge-track {
    width: 100%; height: 8px; border-radius: 99px;
    background: var(--border); overflow: hidden;
}
.gauge-fill {
    height: 100%; border-radius: 99px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    transition: width .8s cubic-bezier(.22,1,.36,1);
}

/* ── Profile table ── */
.profile-grid {
    display: grid; grid-template-columns: repeat(3,1fr); gap: 12px;
    margin-bottom: 1.5rem;
}
.profile-cell {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; padding: 14px 16px;
}
.profile-cell .pc-k {
    font-size: .68rem; font-weight: 600; letter-spacing: .1em;
    text-transform: uppercase; color: var(--muted); margin-bottom: 4px;
}
.profile-cell .pc-v { font-family: var(--font-h); font-weight: 600; font-size: 1rem; }

/* ── Cluster badge ── */
.cluster-badge {
    display: inline-flex; align-items: center; gap: 10px;
    padding: 14px 20px; border-radius: 14px;
    font-family: var(--font-h); font-weight: 700; font-size: 1.1rem;
    margin: 1rem 0;
}

/* ── Insight list ── */
.insight-list { list-style: none; padding: 0; margin: 1rem 0; }
.insight-list li {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 10px 0; border-bottom: 1px solid var(--border);
    font-size: .88rem;
}
.insight-list li:last-child { border-bottom: none; }
.insight-list li .il-dot {
    width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0;
    margin-top: 6px; background: var(--accent);
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Streamlit button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #000 !important; font-family: var(--font-h) !important;
    font-weight: 700 !important; font-size: .9rem !important;
    border: none !important; border-radius: 10px !important;
    padding: 12px 28px !important; cursor: pointer;
    letter-spacing: .02em;
    transition: opacity .2s, transform .1s !important;
    box-shadow: 0 4px 20px rgba(0,229,195,.25) !important;
}
[data-testid="stButton"] > button:hover {
    opacity: .88 !important; transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: 10px !important; overflow: hidden; }

/* ── Expander ── */
details { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; margin-top: 1rem !important; }
details summary { padding: 12px 16px !important; font-family: var(--font-h) !important; font-weight: 600 !important; font-size: .9rem !important; cursor: pointer; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# =========================
# MOCK MODEL LAYER
# (Remove this block & un-comment the pickle loads when real models exist)
# =========================
class MockChurn:
    def predict_proba(self, X):
        np.random.seed(int(X.sum().sum()) % 100)
        p = np.random.uniform(0.1, 0.9)
        return np.array([[1 - p, p]])
    def predict(self, X):
        return (self.predict_proba(X)[0][1] > 0.5).astype(int).reshape(1)

class MockRevenue:
    def predict(self, X):
        np.random.seed(42)
        return np.array([np.random.uniform(30, 130)])

class MockKMeans:
    def predict(self, X):
        v = X.sum()
        return np.array([int(v * 3) % 4])

class MockScaler:
    def transform(self, X):
        return X / 100.0

DEMO_FEATURES = [
    "gender","tenure","PhoneService","PaperlessBilling","MonthlyCharges",
    "Partner_Yes","Dependents_Yes",
    "SeniorCitizen_Yes","SeniorCitizen_No",
    "InternetService_DSL","InternetService_Fiber optic","InternetService_No",
    "Contract_Month-to-month","Contract_One year","Contract_Two year",
    "PaymentMethod_Electronic check","PaymentMethod_Mailed check",
    "PaymentMethod_Bank transfer","PaymentMethod_Credit card",
]

try:
    churn_model = pickle.load(open("churn_model.pkl","rb"))
    revenue_model = pickle.load(open("revenue_model.pkl","rb"))
    kmeans        = pickle.load(open("kmeans.pkl","rb"))
    scaler        = pickle.load(open("scaler.pkl","rb"))
    features      = pickle.load(open("features.pkl","rb"))
    DEMO_MODE = False
except Exception:
    churn_model   = MockChurn()
    revenue_model = MockRevenue()
    kmeans        = MockKMeans()
    scaler        = MockScaler()
    features      = DEMO_FEATURES
    DEMO_MODE = True

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="dot">📡</div>
        <span>Nexa<em>Tel</em></span>
    </div>
    """, unsafe_allow_html=True)

    if DEMO_MODE:
        st.markdown("""
        <div style="background:rgba(255,181,71,.1);border:1px solid rgba(255,181,71,.3);
                    border-radius:8px;padding:10px 12px;margin-bottom:12px;font-size:.78rem;color:#FFB547;">
            ⚡ Demo mode — using mock predictions
        </div>
        """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigation",
        ["🔮  Churn Prediction", "💰  Revenue Risk", "📊  Segmentation"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="section-label">Demographics</div>', unsafe_allow_html=True)
    gender   = st.selectbox("Gender", ["Male","Female"])
    senior   = st.selectbox("Senior Citizen", ["No","Yes"])
    partner  = st.selectbox("Partner", ["Yes","No"])
    deps     = st.selectbox("Dependents", ["Yes","No"])

    st.markdown('<div class="section-label">Service</div>', unsafe_allow_html=True)
    tenure   = st.slider("Tenure (months)", 0, 72, 12)
    monthly  = st.slider("Monthly Charges ($)", 0, 150, 70)
    phone    = st.selectbox("Phone Service", ["Yes","No"])
    internet = st.selectbox("Internet Service", ["DSL","Fiber optic","No"])

    st.markdown('<div class="section-label">Contract & Billing</div>', unsafe_allow_html=True)
    paperless = st.selectbox("Paperless Billing", ["Yes","No"])
    contract  = st.selectbox("Contract", ["Month-to-month","One year","Two year"])
    payment   = st.selectbox("Payment Method",
                    ["Electronic check","Mailed check","Bank transfer","Credit card"])

# =========================
# PREPROCESSING
# =========================
def build_dataframe():
    return pd.DataFrame([[
        gender, senior, partner, deps,
        tenure, phone, paperless,
        internet, contract, payment, monthly
    ]], columns=[
        "gender","SeniorCitizen","Partner","Dependents",
        "tenure","PhoneService","PaperlessBilling",
        "InternetService","Contract","PaymentMethod","MonthlyCharges"
    ])

def preprocess(df):
    df = df.copy()
    yn = {"Yes":1,"No":0}
    for col in ["Partner","Dependents","PhoneService","PaperlessBilling"]:
        df[col] = df[col].map(yn)
    df["gender"] = df["gender"].map({"Male":1,"Female":0})
    df = pd.get_dummies(df)
    df = df.reindex(columns=features, fill_value=0)
    return df

input_df  = build_dataframe()
processed = preprocess(input_df)

# =========================
# SHARED PROFILE CARD HTML
# =========================
def profile_html(df_row):
    r = df_row.iloc[0]
    items = [
        ("Gender",   r["gender"]),
        ("Senior",   r["SeniorCitizen"]),
        ("Partner",  r["Partner"]),
        ("Dependents", r["Dependents"]),
        ("Tenure",   f"{tenure} mo"),
        ("Monthly",  f"${monthly}"),
        ("Internet", r["InternetService"]),
        ("Contract", r["Contract"]),
        ("Payment",  r["PaymentMethod"]),
    ]
    cells = "".join(f"""
        <div class="profile-cell">
            <div class="pc-k">{k}</div>
            <div class="pc-v">{v}</div>
        </div>""" for k,v in items)
    return f'<div class="profile-grid">{cells}</div>'

def gauge_html(prob, label="Churn Probability"):
    color = "var(--danger)" if prob > .7 else "var(--warn)" if prob > .4 else "var(--accent)"
    pct   = int(prob * 100)
    fill  = f"background: {color};"
    return f"""
    <div class="gauge-wrap">
        <div class="gauge-label">
            <span style="color:var(--muted);font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;">{label}</span>
            <span style="font-family:var(--font-h);font-weight:700;font-size:1.1rem;color:{color};">{pct}%</span>
        </div>
        <div class="gauge-track">
            <div class="gauge-fill" style="width:{pct}%;{fill}"></div>
        </div>
    </div>"""

# =========================
# PAGE 1 — CHURN PREDICTION
# =========================
if "Churn" in menu:
    st.markdown("""
    <div class="page-header">
        <div class="icon-box" style="background:linear-gradient(135deg,rgba(0,229,195,.2),rgba(61,126,255,.2));">🔮</div>
        <div>
            <h1>Churn Prediction</h1>
            <p>Evaluate churn probability and retention signals for the selected customer profile.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Customer Profile")
    st.markdown(profile_html(input_df), unsafe_allow_html=True)

    if st.button("Run Churn Analysis →"):
        prob = churn_model.predict_proba(processed)[0][1]
        pred = churn_model.predict(processed)[0]

        st.markdown(gauge_html(prob), unsafe_allow_html=True)

        # Risk status banner
        if prob > 0.7:
            st.markdown(f"""
            <div class="alert-banner alert-danger">
                <div class="al-icon">🚨</div>
                <div>
                    <div class="al-title">High Churn Risk</div>
                    <div class="al-body">This customer has a {prob:.0%} probability of churning. Immediate intervention is recommended — consider priority outreach, loyalty incentives, or contract upgrade offers.</div>
                </div>
            </div>""", unsafe_allow_html=True)
        elif prob > 0.4:
            st.markdown(f"""
            <div class="alert-banner alert-warn">
                <div class="al-icon">⚠️</div>
                <div>
                    <div class="al-title">Medium Churn Risk</div>
                    <div class="al-body">Churn probability is {prob:.0%}. Monitor engagement and consider a proactive check-in or a promotional offer to strengthen retention.</div>
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-banner alert-success">
                <div class="al-icon">✅</div>
                <div>
                    <div class="al-title">Low Churn Risk</div>
                    <div class="al-body">Customer appears stable with only a {prob:.0%} churn probability. Maintain current engagement cadence and watch for behavioural shifts at contract renewal.</div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Insight bullets
        insights = []
        if contract == "Month-to-month":
            insights.append("Month-to-month contract — highest churn correlation. Offer annual upgrade.")
        if payment == "Electronic check":
            insights.append("Electronic check payers churn ~45% more than auto-pay customers.")
        if internet == "Fiber optic" and monthly > 90:
            insights.append("High-spend Fiber customer — ensure service quality expectations are met.")
        if tenure < 12:
            insights.append("Early-tenure customer (< 12 months) — highest vulnerability window.")
        if not insights:
            insights.append("No major risk signals detected. Customer profile is stable.")

        bullets = "".join(f'<li><div class="il-dot"></div><span>{i}</span></li>' for i in insights)
        st.markdown(f"""
        <div style="margin-top:1.5rem;">
            <div style="font-family:var(--font-h);font-weight:700;font-size:.95rem;margin-bottom:.5rem;">Key Risk Signals</div>
            <ul class="insight-list">{bullets}</ul>
        </div>""", unsafe_allow_html=True)

        with st.expander("📋 View raw feature vector"):
            st.dataframe(processed.T.rename(columns={0:"Value"}), height=300)

# =========================
# PAGE 2 — REVENUE RISK
# =========================
elif "Revenue" in menu:
    st.markdown("""
    <div class="page-header">
        <div class="icon-box" style="background:linear-gradient(135deg,rgba(255,181,71,.2),rgba(255,77,109,.2));">💰</div>
        <div>
            <h1>Revenue Risk Analysis</h1>
            <p>Estimate expected monthly revenue loss if this customer churns.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Customer Profile")
    st.markdown(profile_html(input_df), unsafe_allow_html=True)

    if st.button("Estimate Revenue Risk →"):
        churn_prob   = churn_model.predict_proba(processed)[0][1]
        revenue_loss = revenue_model.predict(processed)[0]
        expected     = churn_prob * revenue_loss

        st.markdown(gauge_html(churn_prob, "Churn Probability"), unsafe_allow_html=True)

        # Metric cards
        st.markdown(f"""
        <div class="metric-row metric-row-3">
            <div class="metric-card">
                <div class="mc-label">Churn Probability</div>
                <div class="mc-value" style="color:{'var(--danger)' if churn_prob>.6 else 'var(--warn)' if churn_prob>.35 else 'var(--accent)'};">{churn_prob:.0%}</div>
                <div class="mc-sub">Model confidence</div>
            </div>
            <div class="metric-card">
                <div class="mc-label">Predicted Monthly Loss</div>
                <div class="mc-value" style="color:var(--accent2);">${revenue_loss:.0f}</div>
                <div class="mc-sub">If customer churns</div>
            </div>
            <div class="metric-card">
                <div class="mc-label">Expected Loss</div>
                <div class="mc-value" style="color:{'var(--danger)' if expected>60 else 'var(--warn)'}">${expected:.0f}</div>
                <div class="mc-sub">Prob-weighted exposure</div>
            </div>
        </div>""", unsafe_allow_html=True)

        annual = expected * 12
        if revenue_loss > 80:
            st.markdown(f"""
            <div class="alert-banner alert-danger">
                <div class="al-icon">🔥</div>
                <div>
                    <div class="al-title">High Financial Exposure</div>
                    <div class="al-body">Annualised expected loss: <strong>${annual:,.0f}</strong>. Prioritise retention spend — even a 10% improvement in churn probability saves ~${annual*0.1:,.0f}/yr.</div>
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-banner alert-success">
                <div class="al-icon">🟢</div>
                <div>
                    <div class="al-title">Controlled Revenue Risk</div>
                    <div class="al-body">Annualised expected exposure is ${annual:,.0f}. Standard retention measures are sufficient.</div>
                </div>
            </div>""", unsafe_allow_html=True)

# =========================
# PAGE 3 — SEGMENTATION
# =========================
elif "Segment" in menu:
    st.markdown("""
    <div class="page-header">
        <div class="icon-box" style="background:linear-gradient(135deg,rgba(61,126,255,.2),rgba(0,229,195,.2));">📊</div>
        <div>
            <h1>Customer Segmentation</h1>
            <p>Cluster-based behavioural segment derived from tenure and spend patterns.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cluster_input = np.array([[tenure, monthly]])
    scaled        = scaler.transform(cluster_input)
    cluster       = kmeans.predict(scaled)[0]

    SEGMENTS = {
        0: {
            "name": "Loyal Core",
            "icon": "🟢",
            "color": "var(--accent)",
            "bg":    "rgba(0,229,195,.1)",
            "border":"rgba(0,229,195,.3)",
            "desc":  "Long-tenured, steady spenders. High LTV, low churn risk. Reward loyalty and upsell premium tiers.",
            "actions": [
                "Offer loyalty rewards or anniversary discounts.",
                "Promote premium add-ons (e.g. roaming, cloud storage).",
                "Solicit NPS feedback — they are your best advocates.",
            ],
        },
        1: {
            "name": "At-Risk Segment",
            "icon": "⚠️",
            "color": "var(--warn)",
            "bg":    "rgba(255,181,71,.1)",
            "border":"rgba(255,181,71,.3)",
            "desc":  "Moderate tenure but declining engagement signals. Intervention window is now.",
            "actions": [
                "Trigger personalised win-back campaign.",
                "Offer contract upgrade with price lock.",
                "Assign dedicated account manager for high-value profiles.",
            ],
        },
        2: {
            "name": "Premium Tier",
            "icon": "💎",
            "color": "var(--accent2)",
            "bg":    "rgba(61,126,255,.1)",
            "border":"rgba(61,126,255,.3)",
            "desc":  "High monthly spend, strong engagement. Focus on service quality and exclusive perks.",
            "actions": [
                "Enrol in VIP support programme.",
                "Early access to new service bundles.",
                "Dedicated SLA guarantees.",
            ],
        },
        3: {
            "name": "Early Stage",
            "icon": "🆕",
            "color": "var(--danger)",
            "bg":    "rgba(255,77,109,.1)",
            "border":"rgba(255,77,109,.3)",
            "desc":  "New or recently joined customers. Critical onboarding period — first 90 days define retention.",
            "actions": [
                "Send a structured onboarding sequence (days 1/7/30).",
                "Proactive check-in call at day 14.",
                "Offer introductory loyalty incentive at 3-month mark.",
            ],
        },
    }

    seg = SEGMENTS.get(cluster, SEGMENTS[3])

    st.markdown(f"""
    <div class="cluster-badge" style="background:{seg['bg']};border:1px solid {seg['border']};color:{seg['color']};">
        {seg['icon']}&nbsp; Cluster {cluster} — {seg['name']}
    </div>
    <p style="color:var(--muted);font-size:.9rem;margin-bottom:1.5rem;">{seg['desc']}</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"""
        <div class="metric-row metric-row-2" style="margin-top:0;">
            <div class="metric-card">
                <div class="mc-label">Tenure</div>
                <div class="mc-value" style="color:{seg['color']};">{tenure}</div>
                <div class="mc-sub">months</div>
            </div>
            <div class="metric-card">
                <div class="mc-label">Monthly Spend</div>
                <div class="mc-value" style="color:{seg['color']};">${monthly}</div>
                <div class="mc-sub">per month</div>
            </div>
        </div>""", unsafe_allow_html=True)

    with col2:
        ltv = tenure * monthly
        st.markdown(f"""
        <div class="metric-card" style="height:100%;box-sizing:border-box;">
            <div class="mc-label">Estimated LTV</div>
            <div class="mc-value" style="color:{seg['color']};">${ltv:,}</div>
            <div class="mc-sub">tenure × monthly charges</div>
        </div>""", unsafe_allow_html=True)

    # Recommended actions
    actions_html = "".join(f'<li><div class="il-dot" style="background:{seg["color"]};"></div><span>{a}</span></li>' for a in seg["actions"])
    st.markdown(f"""
    <div style="margin-top:1.5rem;">
        <div style="font-family:var(--font-h);font-weight:700;font-size:.95rem;margin-bottom:.5rem;">Recommended Actions</div>
        <ul class="insight-list">{actions_html}</ul>
    </div>""", unsafe_allow_html=True)

    # All segments overview
    with st.expander("View all segment definitions"):
        for k, s in SEGMENTS.items():
            marker = " ← current" if k == cluster else ""
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--border);">
                <div style="width:32px;height:32px;border-radius:8px;background:{s['bg']};
                            border:1px solid {s['border']};display:flex;align-items:center;
                            justify-content:center;font-size:16px;">{s['icon']}</div>
                <div>
                    <div style="font-family:var(--font-h);font-weight:600;font-size:.9rem;color:{s['color']};">
                        Cluster {k} — {s['name']}{marker}
                    </div>
                    <div style="font-size:.78rem;color:var(--muted);">{s['desc']}</div>
                </div>
            </div>""", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<hr style="margin-top:3rem;">
<div style="display:flex;justify-content:space-between;align-items:center;
            font-size:.75rem;color:var(--muted);padding-bottom:1rem;">
    <span>⚡ NexaTel Customer Intelligence Platform</span>
    <span>Powered by Streamlit · Machine Learning</span>
</div>
""", unsafe_allow_html=True)    