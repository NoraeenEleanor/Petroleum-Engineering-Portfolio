import streamlit as st 
import pandas as pd
import datetime

# Title
st.set_page_config(page_title="OFM Data Export for Power BI", layout="centered")
st.title("📊 OFM Data Export App for Power BI")
st.caption("Simulate data pipeline from Streamlit to Powr BI using DUMMY production and well test data")

# Input Data
try:
    prod_df = pd.read_csv("dummy_production.csv")
    test_df = pd.read_csv("dummy_welltest.csv")
except FileNotFoundError:
    st.error("❌ Dummy CSV files not found. Please upload or ensure they are in the same directory ")
    st.stop()
    
# Data Screening
with st.expander("🔍 Preview Production Data"):
    st.dataframe(prod_df)
    
with st.expander("🔍 Preview Well Test Data"):
    st.dataframe(test_df)
    
# Data Merging
merged_df = pd.merge(prod_df, test_df, how="left", on="WELL")

# Data Filtering
st.subheader("🎛 Screening Data Before Exporting")

selected_well = st.multiselect("🛢 Select WELL(s):", options=merged_df['WELL'].unique(), default=merged_df['WELL'].unique())
selected_test = st.multiselect("🧪 Select TEST TYPE(s):", options=merged_df['TEST_TYPE'].dropna().unique(), default=merged_df['TEST_TYPE'].dropna().unique())

filtered_df = merged_df[(merged_df['WELL'].isin(selected_well)) & (merged_df['TEST_TYPE'].isin(selected_test))]

st.markdown(f"✅ Showing **{len(filtered_df)}** rows after filtering")
st.dataframe(filtered_df)

# Data Exporting
st.subheader("📤 Export CSV for Power BI")

filename = f"powerbi_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Your CSV File",
    data=csv_data,
    file_name=filename,
    mime="text/csv"
)

# Footer
st.caption("💼 Dummy OFM Dashboard Export Prototype | Prepared by Wan Norain")