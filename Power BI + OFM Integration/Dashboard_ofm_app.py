import streamlit as st 
import pandas as pd
import datetime

# Title
st.set_page_config(page_title="OFM Data Export for Power BI", layout="centered")
st.title("📊 OFM Data Export App for Power BI")
st.caption("Integrate Cleaned OFM Data for Power BI Dashboarding")

# Input Data
try:
    prod_df = pd.read_csv("dummy_ofm_production.csv")
    test_df = pd.read_csv("dummy_ofm_welltest.csv")
except FileNotFoundError:
    st.error("❌ Dummy CSV files not found. Please upload or ensure they are in the same directory ")
    st.stop()
    
# Data Cleaning
prod_clean = prod_df.rename(columns={
    "Well Name": "WELL",
    "Date": "DATE",
    "Oil Rate (bbl/d)": "OIL_BOPD",
    "Gas Rate (Mscf/d)": "GAS_MSCFD",
    "Water Rate (bbl/d)": "WATER_BWPD",
    "WHP (psi)": "WHP_PSIG",
    "Status": "STATUS"
})[["WELL", "DATE", "OIL_BOPD", "GAS_MSCFD", "WATER_BWPD", "WHP_PSIG", "STATUS"]]

test_clean = test_df.rename(columns={
    "Well Name": "WELL",
    "Test Date": "TEST_DATE",
    "Q_liq (bbl/d)": "Q_LIQ",
    "Water Cut (%)": "WCUT",
    "GOR (scf/bbl)": "GOR",
    "THP (psi)": "THP_PSIG",
    "Lift Method": "LIFT_METHOD"
})[["WELL", "TEST_DATE", "Q_LIQ", "WCUT", "GOR", "THP_PSIG", "LIFT_METHOD"]]
    
# Data Merging
merged_df = pd.merge(prod_clean, test_clean, how="left", on="WELL")

# Data Filtering
st.subheader("🎛 Screening Data Before Exporting")

wells = merged_df['WELL'].unique().tolist()
methods = merged_df["LIFT_METHOD"].dropna().unique().tolist()

selected_wells = st.multiselect("🛢 Select WELL(s):", options=wells, default=wells)
selected_lift = st.multiselect("⚙️ Select LIFT METHOD(s):", options=methods, default=methods)

filtered_df = merged_df[(merged_df["WELL"].isin(selected_wells)) & (merged_df["LIFT_METHOD"].isin(selected_lift))]

st.markdown(f"✅ Showing **{len(filtered_df)}** rows after filtering")
st.dataframe(filtered_df)

# Data Exporting
st.subheader("📤 Export CSV for Power BI")

filename = f"powerbi_export_{datetime.datetime.now().strftime('%d-%b-%Y_%H-%M')}.csv"
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Your CSV File",
    data=csv_data,
    file_name=filename,
    mime="text/csv"
)

# Footer
st.caption("💼 Dummy OFM Dashboard Export Prototype | Prepared by Wan Norain")