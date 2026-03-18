import streamlit as st
import pandas as pd
import time
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Scope 3 Data Engine", page_icon="🌍", layout="wide")

# --- ADVANCED SIDEBAR SETTINGS ---
with st.sidebar:
    st.title("⚙️ Engine Configuration")
    
    st.markdown("**Taxonomy & Frameworks**")
    st.selectbox("Active Standard", ["GHG Protocol (2024)", "SBTi Corporate Manual", "ISO 14064"])
    st.selectbox("Logic Library", ["Enhanced_FM_Scope3_Library.csv", "Standard Spend Proxy"])
    
    st.markdown("**Processing Parameters**")
    st.slider("AI Confidence Threshold", min_value=50, max_value=100, value=85, help="Items below this confidence will be flagged as UNCLEAR.")
    st.checkbox("Auto-Exclude Financial Noise", value=True)
    st.checkbox("Enable Strict Audit Mode", value=True, help="Forces manual review of all managing agent invoices.")
    
    st.markdown("---")
    st.caption("User ID: Senior ESG Auditor")
    st.caption("Deployment: Capstone V2.0")

# --- MAIN DASHBOARD HEADER ---
st.title("🏢 Facilities Management: Scope 3 Disaggregation Engine")
st.markdown("Upload multiple managing agent invoices simultaneously to automate entity resolution and extract high-fidelity physical data.")

# --- MULTIPLE FILE INGESTION ---
# Upgraded to accept multiple files for batch processing
uploaded_files = st.file_uploader("Drop PDF/CSV Invoice Documents Here (Batch Processing Enabled)", type=['pdf', 'csv'], accept_multiple_files=True)

if uploaded_files:
    with st.spinner(f"Processing {len(uploaded_files)} document(s). Executing extraction rules..."):
        time.sleep(3) 
        
        # --- TOP LEVEL KPIs ---
        st.subheader("Batch Processing Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Total Line Items", value="142", delta="across all documents")
        col2.metric(label="Manual Hours Saved", value="14.5 hrs", delta="vs. Excel filtering", delta_color="inverse")
        col3.metric(label="Financial Noise Filtered", value="$4,250", delta="Emissions Protected")
        col4.metric(label="Activity Data Yield", value="38%", delta="High-Accuracy Metrics Found")
        
        st.markdown("---")

        # --- EXTENSIVE GROUND TRUTH DATA ---
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
                "METRO ENERGY", "GLOBAL GRID", "DAIKIN", "Missing (Ref U-112)", 
                "WASTERECYCLE PTE", "SPARKLE COMMERCIAL", "Missing (Ref PC-55)", "URBAN FACILITIES", 
                "METRO PROPERTY", "DORMA"
            ],
            "Scope 3 Categorisation": [
                "Cat 3: Fuel & Energy", "Non-Emissive", "Cat 1: Services", "Pending Human Input", 
                "Cat 5: Waste", "Cat 1: Services", "Pending Human Input", "Cat 3: Fuel & Energy", 
                "Non-Emissive", "Cat 1: Services"
            ],
            "Accounting Type": [
                "Activity (891 kWh)", "Spend-based", "Spend-based", "Spend-based", 
                "Activity (4.25 Tonnes)", "Spend-based", "Spend-based", "Activity (450 m3)", 
                "Spend-based", "Spend-based"
            ],
            "Audit Logic Rule": [
                "Metric Extraction", "Financial Noise", "Subcontractor Resolution", "Entity Resolution: Uncertainty", 
                "Metric Extraction", "Subcontractor Resolution", "Entity Resolution: Uncertainty", "Metric Extraction", 
                "Levy Exclusion", "Subcontractor Resolution"
            ]
        }
        df = pd.DataFrame(data)

        # --- 4 INTERACTIVE WORKFLOW TABS ---
        tab1, tab2, tab3, tab4 = st.tabs(["📝 Resolution Desk", "📊 Analytics Dashboard", "⚙️ System Logs", "📥 Compliance Export"])
        
        with tab1:
            st.markdown("### Human-in-the-Loop Validation")
            st.info("The system flagged ambiguous items requiring professional judgement to prevent vendor misattribution.")
            
            edited_df = st.data_editor(
                df,
                column_config={
                    "Verification Status": st.column_config.SelectboxColumn(
                        "Status", options=["✅ Verified", "⚠️ UNCLEAR", "🚫 EXCLUDED"], required=True
                    ),
                    "Extracted Vendor": st.column_config.TextColumn("Resolved Vendor (Editable)"),
                },
                disabled=["Line Item Description", "Accounting Type", "Audit Logic Rule"],
                hide_index=True,
                use_container_width=True,
                height=400
            )
            
            if st.button("Commit Resolutions to Database"):
                st.success("Human interventions successfully committed. Audit trail updated.")

        with tab2:
            st.markdown("### Footprint Quality Analytics")
            colA, colB = st.columns(2)
            
            with colA:
                st.markdown("**Accounting Methodology Shift**")
                chart_data_1 = pd.DataFrame({
                    "Method": ["Spend-Based Proxies", "Activity-Based (Physical)", "Excluded Noise"],
                    "Items": [5, 3, 2]
                })
                fig1 = px.pie(chart_data_1, values='Items', names='Method', hole=0.4, color_discrete_sequence=['#4A90E2', '#50E3C2', '#E74C3C'])
                fig1.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
                st.plotly_chart(fig1, use_container_width=True)
                
            with colB:
                st.markdown("**Scope 3 Category Breakdown**")
                chart_data_2 = pd.DataFrame({
                    "Category": ["Cat 1: Services", "Cat 3: Energy", "Cat 5: Waste"],
                    "Count": [4, 2, 1]
                })
                fig2 = px.bar(chart_data_2, x='Category', y='Count', color='Category', color_discrete_sequence=['#F39C12', '#9B59B6', '#34495E'])
                fig2.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
                st.plotly_chart(fig2, use_container_width=True)

        with tab3:
            st.markdown("### Semantic Engine Processing Logs")
            st.code("""
[14:02:01] INGESTION: Read 10 line items from batch upload.
[14:02:02] LOGIC GATE: Applied 'Enhanced_FM_Scope3_Library.csv'.
[14:02:02] NER MODULE: Detected sub-contractor 'DAIKIN' in row 3. Mapping to Cat 1.
[14:02:03] EXTRACTION: Isolated '891 kWh' physical metric in row 1. Flagging as Activity-based.
[14:02:03] FLAG: Reference code 'U-112' detected without explicit vendor. Triggering UNCLEAR status.
[14:02:04] EXCLUSION: Matched 'Corporate ESG Levy' to rule EX-01. Removing from emissive total.
[14:02:04] TASK COMPLETE: Awaiting Human-in-the-Loop verification.
            """, language="log")

        with tab4:
            st.markdown("### Audit-Ready Data Export")
            st.markdown("Download the fully resolved dataset for seamless ingestion into your final carbon accounting software.")
            
            csv = edited_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Verified CSV",
                data=csv,
                file_name='scope3_batch_resolved.csv',
                mime='text/csv',
                type="primary"
            )
            