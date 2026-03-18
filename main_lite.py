import streamlit as st
import pandas as pd
import time
import plotly.express as px

# 1. Page Configuration (Sets wide mode and professional browser title)
st.set_page_config(page_title="Scope 3 Data Engine", page_icon="🌍", layout="wide")

# 2. Sidebar Settings (Creates the illusion of a robust enterprise tool)
with st.sidebar:
    st.title("⚙️ Engine Settings")
    st.selectbox("Active Framework", ["GHG Protocol (2024)", "SBTi Corporate Manual"])
    st.selectbox("Taxonomy Logic", ["Enhanced_FM_Scope3_Library.csv", "Standard Spend Proxy"])
    st.slider("Uncertainty Confidence Threshold", min_value=0.5, max_value=1.0, value=0.85, help="Items below this confidence will be flagged for human review.")
    st.markdown("---")
    st.caption("User: Senior ESG Auditor | Network: SECURE")

# 3. Main Header & Value Proposition
st.title("🏢 Data Preparation: Scope 3 Disaggregation")
st.markdown("Automate entity resolution, filter financial noise, and extract hybrid activity data for audit-ready reporting.")

# 4. The Interactive Upload Zone
uploaded_file = st.file_uploader("Upload Consolidated Managing Agent Invoice (PDF)", type=['pdf'])

if uploaded_file is not None:
    # Simulates the AI processing time to build anticipation during your demo
    with st.spinner("Executing Logic framework and semantic extraction..."):
        time.sleep(2.5) 
        
        # 5. KPI Dashboard (Directly addresses your Pains & Gains)
        st.subheader("Audit Processing Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Line Items Processed", value="46", delta="100% Extracted")
        col2.metric(label="Manual Hours Saved", value="4.5 hrs", delta="-82% Processing Time", delta_color="inverse")
        col3.metric(label="Financial Noise Excluded", value="$1,895", delta="Prevents Emissions Inflation", delta_color="normal")
        col4.metric(label="Data Quality Score", value="Hybrid", delta="Activity Data Isolated", delta_color="normal")
        
        st.markdown("---")

        # 6. The "Ground Truth" Dataset from your Trial Results
        data = {
            "Audit Status": ["✅ Auto-Verified", "⚠️ UNCLEAR", "✅ Auto-Verified", "🚫 EXCLUDED"],
            "Source Line Item": [
                "Consolidated Water Bill (Usage: 450 m3)", 
                "Chiller Maintenance Ref: 9910", 
                "Monthly Cleaning Contract - Sub-con: SparklePure",
                "Management Fee for Jan Operations"
            ],
            "Resolved Vendor": ["URBAN FACILITIES", "Missing (Ref 9910)", "SparklePure", "URBAN FACILITIES"],
            "Scope 3 Mapping": ["Cat 3: Fuel & Energy", "Pending Human Input", "Cat 1: Services", "Non-Emissive"],
            "Accounting Basis": ["Activity-based (450 m3)", "Spend-based", "Spend-based", "Spend-based"],
            "Logic Applied": ["Metric Extraction", "Entity Resolution: Uncertainty", "Subcontractor Resolution", "Financial Noise Filter"]
        }
        df = pd.DataFrame(data)

        # 7. Interactive Consultant Tabs
        tab1, tab2, tab3 = st.tabs(["📝 Human-in-the-Loop Validation", "📊 Quality Analytics", "📥 Audit Export"])
        
        with tab1:
            st.markdown("### Resolve Ambiguous Entities")
            st.info("The system flagged **1 item** that requires professional judgment. Please resolve the 'UNCLEAR' status below to complete the audit trail.")
            
            # Interactive Data Editor (The "Relief" feature)
            edited_df = st.data_editor(
                df,
                column_config={
                    "Audit Status": st.column_config.SelectboxColumn(
                        "Status", options=["✅ Auto-Verified", "⚠️ UNCLEAR", "✅ Resolved", "🚫 EXCLUDED"], required=True
                    ),
                    "Resolved Vendor": st.column_config.TextColumn("Vendor (Editable)"),
                },
                disabled=["Source Line Item", "Accounting Basis", "Logic Applied"], # Locks the raw data from being tampered with
                hide_index=True,
                use_container_width=True
            )
            
            # Fake commit button for the demo
            if st.button("Commit Resolutions to Database"):
                st.success("Human-in-the-Loop resolutions committed successfully. Data is now 100% Audit-Ready.")

        with tab2:
            st.markdown("### Data Quality: The Hybrid Transition")
            st.markdown("By moving away from spend-based proxies, the carbon footprint accuracy is significantly increased.")
            
            # Professional Donut Chart using Plotly
            chart_data = pd.DataFrame({
                "Accounting Method": ["Spend-Based (Proxy)", "Activity-Based (Physical)"],
                "Count": [75, 25] # Mock percentages for visual impact
            })
            fig = px.pie(chart_data, values='Count', names='Accounting Method', hole=0.5, 
                         color_discrete_sequence=['#AEC6CF', '#77DD77'])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.markdown("### Compliance & System Export")
            st.markdown("Download the fully resolved, mapped, and filtered dataset for immediate ingestion into standard carbon calculators (e.g., Asuene, Persefoni).")
            
            # Creates a downloadable CSV from the edited data
            csv = edited_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Audit-Ready CSV",
                data=csv,
                file_name='scope3_resolved_audit.csv',
                mime='text/csv',
                type="primary"
            )