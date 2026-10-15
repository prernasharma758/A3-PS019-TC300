import streamlit as st
import pandas as pd
import re
import io
import plotly.express as px
from database import init_db, insert_evidence, get_all_evidence, clear_db

# 1. Premium Theme Configuration
st.set_page_config(
    page_title="PrivacyShield AI - Compliance Command Center", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize local DB
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

# 2. CSS Styling
st.markdown("""
<style>
    .stApp { background-color: #080c14; color: #e1e7f0; font-family: 'Segoe UI', Roboto, sans-serif; }
    .header-container { padding: 20px 0px; border-bottom: 2px solid #1f2937; margin-bottom: 30px; }
    .main-title { font-size: 3rem !important; font-weight: 900; background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .sub-title { color: #00f2fe; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 5px; }
    .status-card { background: rgba(17, 24, 39, 0.7); border: 1px solid #1f2937; border-radius: 16px; padding: 24px; flex: 1; box-shadow: 0 8px 32px 0 rgba(0,0,0,0.37); }
    .status-label { font-size: 0.85rem; color: #9ca3af; text-transform: uppercase; font-weight: 600; }
    .status-value { font-size: 2.5rem; font-weight: 800; margin-top: 10px; color: #ffffff; }
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

# --- UI HEADER ---
st.markdown("""<div class="header-container"><div class="main-title">PRIVACYSHIELD AI</div><div class="sub-title">🛡️ Cybersecurity Audit & Verhoeff Validated Privacy Evidence Center</div></div>""", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("Upload a file to start audit", type=["csv", "txt", "xlsx"])
if st.sidebar.button("🗑️ Reset Command Database", use_container_width=True):
    clear_db()
    st.rerun()

if uploaded_file is not None:
    ftype = uploaded_file.name.split(".")[-1]
    raw = pd.read_csv(uploaded_file).to_string() if ftype == "csv" else (pd.read_excel(uploaded_file).to_string() if ftype == "xlsx" else io.StringIO(uploaded_file.getvalue().decode("utf-8")).read())
    scan_and_save(raw, uploaded_file.name)

db_records = get_all_evidence()

if not db_records.empty:
    total_leaks = len(db_records)
    high_risks = len(db_records[db_records["Risk Level"] == "High 🔴"])
    score = max(5, 100 - (high_risks * 15 + (total_leaks - high_risks) * 5))
    
    col_l, col_r = st.columns([1.5, 1])
    with col_l:
        st.markdown("<h3 style='color:#00f2fe;'>📑 Evidence Logs Registry</h3>", unsafe_allow_html=True)
        st.dataframe(db_records, use_container_width=True, hide_index=True)
    with col_r:
        st.markdown("<h3 style='color:#00f2fe;'>📊 Attack Vector Severity</h3>", unsafe_allow_html=True)
        fig = px.pie(db_records, names="PII Type", hole=0.4, color_discrete_sequence=px.colors.sequential.Electric)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#e1e7f0', margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    
    if uploaded_file:
        masked_output = mask_sensitive_data(raw)
        st.download_button("🚀 Run Cryptographic Masking & Download", data=masked_output, file_name=f"masked_{uploaded_file.name}", use_container_width=True)
else:
    st.info("👈 Upload a dataset via the sidebar to initiate the security audit scan.")
