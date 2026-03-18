import streamlit as st
import pandas as pd
import plotly.express as px
import pdfplumber

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Scope 3 Data Engine", page_icon="🌍", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Engine Configuration")
    
    st.markdown("**Taxonomy & Frameworks**")
    st.selectbox("Active Standard", ["GHG Protocol (2024)", "SBTi Corporate Manual", "ISO 14064"])
    st.selectbox("Logic Library", ["Scope3_Library.csv", "Standard Spend Proxy"])
    
    st.markdown("**Processing Parameters**")
    st.slider("AI Confidence Threshold", 50, 100, 85)
    st.checkbox("Auto-Exclude Financial Noise", value=True)
    st.checkbox("Enable Strict Audit Mode", value=True)
    
    st.markdown("---")
    st.caption("User ID: ESG Consultant")
    st.caption("Deployment: Capstone V2.0")

# --- HEADER ---
st.title("🏢 JATA: Scope 3 Data Preparation Engine")
st.markdown("Upload multiple managing agent invoices to extract and structure emissions-relevant data.")

# --- FILE UPLOAD ---
uploaded_files = st.file_uploader(
    "Drop PDF/CSV Invoice Documents Here",
    type=['pdf', 'csv'],
    accept_multiple_files=True
)

# --- TEXT EXTRACTION ---
all_text = []

if uploaded_files:
    with st.spinner(f"Processing {len(uploaded_files)} document(s)..."):
        for file in uploaded_files:
            if file.type == "application/pdf":
                with pdfplumber.open(file) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() or ""
                    all_text.append(text)

            elif file.type == "text/csv":
                df_csv = pd.read_csv(file)
                all_text.append(df_csv.to_string())

# --- PREVIEW ---
if all_text:
    st.subheader("Extracted Raw Text Preview")
    for i, text in enumerate(all_text):
        st.text_area(f"Document {i+1}", text[:1000], height=200)

# --- KEYWORD DETECTION ---
keywords = {
    "electricity": "Cat 3: Energy",
    "water": "Cat 3: Energy",
    "waste": "Cat 5: Waste",
    "cleaning": "Cat 1: Services"
}

detected_items = []

for text in all_text:
    for word in keywords:
        if word in text.lower():
            detected_items.append(word)

detected_items = list(set(detected_items))

if detected_items:
    st.write("Detected Keywords:", detected_items)

# --- ACCOUNTING TYPE LOGIC ---
accounting_type = "Spend-based"

for text in all_text:
    if "kwh" in text.lower():
        accounting_type = "Activity Data"
        break

# --- SIMULATED STRUCTURED DATA ---
data = {
    "Verification Status": [
        "✅ Verified", "🚫 EXCLUDED", "✅ Verified", "⚠️ UNCLEAR",
        "✅ Verified", "✅ Verified", "⚠️ UNCLEAR", "✅ Verified",
        "🚫 EXCLUDED", "✅ Verified"
    ],
    "Line Item Description": [
        "Electricity Usage (Meter Ref: E-9921) - 891 kWh",
        "Carbon Management & Regulatory Admin Fee",
        "Monthly Chiller Maintenance - Block A",
        "Uniform & Equipment Ref: U-112",
        "General Waste Haulage (Weight: 4.25 Tonnes)",
        "Daily Office Cleaning (Level 1-10)",
        "Fogging Services - Ref: PC-55",
        "Consolidated Water Bill (Usage: 450 m3)",
        "Corporate ESG Levy",
        "Repair of Auto-door Motor Job #882"
    ],
    "Extracted Vendor": [
        "METRO ENERGY", "GLOBAL GRID", "DAIKIN", "Missing",
        "WASTERECYCLE PTE", "SPARKLE COMMERCIAL", "Missing",
        "URBAN FACILITIES", "METRO PROPERTY", "DORMA"
    ],
    "Scope 3 Categorisation": [
        "Cat 3: Fuel & Energy", "Non-Emissive", "Cat 1: Services", "Pending",
        "Cat 5: Waste", "Cat 1: Services", "Pending",
        "Cat 3: Fuel & Energy", "Non-Emissive", "Cat 1: Services"
    ],
    "Accounting Type": [
        "Activity (kWh)", "Spend-based", "Spend-based", "Spend-based",
        "Activity (Tonnes)", "Spend-based", "Spend-based",
        "Activity (m3)", "Spend-based", "Spend-based"
    ],
    "Audit Logic Rule": [
        "Metric Extraction", "Financial Noise", "Subcontractor",
        "Uncertainty", "Metric Extraction", "Subcontractor",
        "Uncertainty", "Metric Extraction", "Exclusion", "Subcontractor"
    ]
}

df = pd.DataFrame(data)

# --- CONNECT PIPELINE ---
if detected_items:
    df["Detected Keywords"] = ", ".join(detected_items)

# --- KPIs ---
st.subheader("Batch Processing Summary")
col1, col2, col3, col4 = st.columns(4)

total_items = len(df)
activity_items = df["Accounting Type"].str.contains("Activity").sum()
activity_yield = round((activity_items / total_items) * 100, 1)
excluded_items = (df["Verification Status"] == "🚫 EXCLUDED").sum()
manual_hours_saved = round(total_items * 0.1, 1)

col1.metric("Total Line Items", total_items)
col2.metric("Est. Manual Hours Saved", f"{manual_hours_saved} hrs")
col3.metric("Excluded Items", excluded_items)
col4.metric("Activity Data Yield", f"{activity_yield}%")

st.markdown("---")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Resolution Desk", "📊 Analytics", "⚙️ Logs", "📥 Export"
])

# --- TAB 1 ---
with tab1:
    st.markdown("### Human Validation")

    edited_df = st.data_editor(
        df,
        disabled=["Line Item Description", "Accounting Type"],
        use_container_width=True
    )

# --- TAB 2 ---
with tab2:
    st.markdown("### Analytics")

    fig = px.pie(
        df,
        names="Scope 3 Categorisation"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 3 ---
with tab3:
    st.code("System processing logs simulated...", language="text")

# --- TAB 4 ---
with tab4:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "scope3_output.csv")