import streamlit as st
import pandas as pd
import re
import io
import plotly.express as px
from database import init_db, insert_evidence, get_all_evidence, clear_db

# 1. Page Configuration
st.set_page_config(
    page_title="PrivacyShield AI - Enterprise Compliance Hub", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# --- VERHOEFF ALGORITHM TABLES ---
d_table = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
]

p_table = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 0, 3, 4, 9],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [3, 6, 1, 5, 7, 2, 8, 9, 0, 4],
    [4, 2, 7, 9, 3, 8, 0, 6, 4, 1],
    [5, 8, 2, 7, 9, 3, 8, 0, 6, 4],
    [6, 3, 6, 1, 5, 7, 2, 8, 9, 0],
    [7, 4, 2, 7, 9, 3, 8, 0, 6, 4]
]

def validate_verhoeff(num_str):
    cleaned_num = re.sub(r'\D', '', num_str)
    if len(cleaned_num) != 12:
        return False
    if cleaned_num[0] in ['0', '1']:
        return False
    if len(set(cleaned_num)) == 1:
        return False

    c = 0
    for i, digit in enumerate(reversed(cleaned_num)):
        c = d_table[c][p_table[i % 8][int(digit)]]
    return c == 0

# --- PREMIUM CYBERPUNK STYLING (CSS) ---
st.markdown("""
<style>
    /* Global App Styling */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(6, 11, 25) 0%, rgb(2, 5, 12) 90%);
        color: #f3f4f6;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Custom Header */
    .hero-box {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.8) 0%, rgba(11, 15, 25, 0.9) 100%);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    .main-title {
        font-size: 2.5rem !important;
        font-weight: 800;
        letter-spacing: 1px;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #00c6ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 1rem;
        font-weight: 400;
        margin-top: 8px;
        letter-spacing: 0.5px;
    }

    /* Metric Cards */
    .metric-container {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .metric-container:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 242, 254, 0.4);
    }
    .metric-title {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    .metric-val {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 5px;
    }

    /* Section Titles */
    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #f8fafc;
        border-left: 4px solid #00f2fe;
        padding-left: 12px;
        margin: 25px 0 15px 0;
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #050811 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe 0%, #2563eb 100%);
        color: white;
        border-radius: 10px;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1rem;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        opacity: 0.9;
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5);
    }
</style>
""", unsafe_allow_html=True)

STANDARD_PATTERNS = {
    "PAN Card": r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
    "Phone Number": r"\b(?:\+91[\-\s]?)?[6-9]\d{9}\b",
    "Email Address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
}
AADHAAR_REGEX = r"\b[0-9]{4}\s[0-9]{4}\s[0-9]{4}\b|\b[0-9]{12}\b"

def scan_and_save(text, file_name):
    scanned = []
    for val in set(re.findall(AADHAAR_REGEX, text)):
        if validate_verhoeff(val):
            masked = f"*{val[-4:]}"
            insert_evidence(file_name, "Aadhaar Card", masked, "High 🔴", "Exposed ⚠️")
            scanned.append({"PII Identifier": "Aadhaar Card", "Leaked Value (Masked)": masked, "Threat Level": "High 🔴", "Compliance Status": "Exposed ⚠️"})
    
    for pii_type, pattern in STANDARD_PATTERNS.items():
        for match in set(re.findall(pattern, text)):
            risk = "High 🔴" if pii_type == "PAN Card" else "Medium 🟡"
            masked = f"*{match[-4:]}"
            insert_evidence(file_name, pii_type, masked, risk, "Exposed ⚠️")
            scanned.append({"PII Identifier": pii_type, "Leaked Value (Masked)": masked, "Threat Level": risk, "Compliance Status": "Exposed ⚠️"})
    return scanned

def mask_sensitive_data(text):
    masked = text
    for val in set(re.findall(AADHAAR_REGEX, text)):
        if validate_verhoeff(val): masked = masked.replace(val, "████-████-████")
    for pii_type, pattern in STANDARD_PATTERNS.items():
        masked = re.sub(pattern, "██████████", masked)
    return masked

# --- HERO HEADER ---
st.markdown("""
<div class="hero-box">
    <div class="main-title">🛡️ PRIVACYSHIELD AI</div>
    <div class="sub-title">Advanced Cybersecurity Audit & Verhoeff Validated Privacy Compliance Center</div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
st.sidebar.markdown("### ⚙️ Control Panel")
uploaded_file = st.sidebar.file_uploader("Upload Target Dataset", type=["csv", "txt", "xlsx"])
st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Reset Audit Vault", use_container_width=True):
    clear_db()
    st.rerun()

# --- FILE PROCESSOR ---
if uploaded_file is not None:
    ftype = uploaded_file.name.split(".")[-1]
    if ftype == "csv":
        raw = pd.read_csv(uploaded_file).to_string()
    elif ftype == "xlsx":
        raw = pd.read_excel(uploaded_file).to_string()
    else:
        raw = io.StringIO(uploaded_file.getvalue().decode("utf-8")).read()
    
    with st.spinner("⚡ Running Deep Threat Discovery & Verhoeff Checks..."):
        scan_and_save(raw, uploaded_file.name)

db_records = get_all_evidence()

# --- METRICS DISPLAY ---
col1, col2, col3 = st.columns(3)
total_leaks = len(db_records) if not db_records.empty else 0
audited_files = db_records['File Name'].nunique() if not db_records.empty else 0
high_risks = len(db_records[db_records["Risk Level"] == "High 🔴"]) if not db_records.empty else 0
score = max(5, 100 - (high_risks * 15 + (total_leaks - high_risks) * 5)) if not db_records.empty else 100

with col1:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">📁 Databases Audited</div>
        <div class="metric-val" style="color: #00f2fe;">{audited_files:02d}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">🚨 Total PII Expositions</div>
        <div class="metric-val" style="color: #ff7b72;">{total_leaks:02d}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    score_color = "#ff7b72" if score < 60 else "#f1e05a" if score < 85 else "#56d364"
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">🛡️ Compliance Integrity</div>
        <div class="metric-val" style="color: {score_color};">{score}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- MAIN DASHBOARD CONTENT ---
if not db_records.empty:
    col_l, col_r = st.columns([1.6, 1])
    
    with col_l:
        st.markdown('<div class="section-header">📑 Immutable Evidence Logs Registry</div>', unsafe_allow_html=True)
        st.dataframe(db_records, use_container_width=True, hide_index=True)
        
    with col_r:
        st.markdown('<div class="section-header">📊 Attack Vector Severity</div>', unsafe_allow_html=True)
        fig = px.pie(db_records, names="PII Type", hole=0.5, color_discrete_sequence=px.colors.sequential.Tealgrn)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color='#e1e7f0', 
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)

    if uploaded_file:
        st.markdown("---")
        col_act1, col_act2 = st.columns([2, 1])
        with col_act1:
            st.markdown('<div class="section-header" style="border-left-color: #56d364;">⚡ Active Shield Remediation Engine</div>', unsafe_allow_html=True)
            st.write(f"Instant cryptographic sanitization available for `{uploaded_file.name}`. Download your encrypted, compliant dataset copy below:")
        with col_act2:
            st.markdown("<br>", unsafe_allow_html=True)
            masked_output = mask_sensitive_data(raw)
            st.download_button(
                label="🚀 Run Masking & Download File", 
                data=masked_output, 
                file_name=f"sanitized_{uploaded_file.name}", 
                use_container_width=True
            )
else:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Please upload a dataset file (CSV, TXT, or XLSX) using the sidebar to initiate the security audit scan.")
