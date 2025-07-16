" Dual String Gas Lift Sensitivity Analysis"

import streamlit as st 
import pandas as pd
import altair as alt

# Set page config
st.set_page_config(page_title="Dual String Gas Lift Sensitivity Analysis", page_icon = '💡', layout = "wide")

# Title & Description
st.title("Dual String Gas Lift Sensitivity Analysis")
st.markdown("""
This app compares **Python model results** with **OLGA** and **PROSPER** for various sensitivity analysis:
- Gas Injection Rate
- Productivity Index (PI)
- Dome Pressure
- Pressure Drop between Valves

""")

# Sidebar inputs
st.sidebar.header("Project Inputs")
pvt_data = st.sidebar.file_uploader("Uploaded PVT Data (CSV)", type="csv")
well_data = st.sidebar.file_uploader("Upload Well Test Data (CSV)", type="csv")
st.sidebar.markdown("Or use example datasets below ⬇️")

# Example data
if pvt_data is not None:
    pvt_df = pd.read_csv(pvt_data)
else:
    pvt_df = pd.read_csv("sample_pvt_data.csv")
    
if well_data is not None:
    well_df = pd.read_csv(well_data)
else:
    well_df = pd.read_csv("sample_well_data.csv")
    
# Show example data  
st.subheader("Example PVT Data")
st.dataframe(pvt_df.head())

st.subheader("Example Well Test Data")
st.dataframe(well_df.head())

# Sensitivity Analysis Results
st.header("Sensitivity Analysis Results")
selected_param = st.selectbox("Select Parameter for Sensitivity", ["Gas Injection Rate", "Productivity Index", "Dome Pressure", "Pressure Drop between Valves" ])

# Load Sensitivity Results
sensitivity_df = pd.read_csv(f"sensitivity_{selected_param.replace(' ', '_').lower()}.csv")

# Plot   
st.subheader(f"{selected_param} Sensitivity Plot")
chart = alt.Chart(sensitivity_df).mark_line(point=True).encode(
    x = alt.X(selected_param, title = selected_param),
    y = alt.Y("Oil Rate", title = "Oil Production Rate (STB/d)"),
    color = "Method:N"
).properties(width = 700, height = 400)
st.altair_chart(chart, use_container_width=True)

# Comparison Table
st.header("Comparison Table: Python vs OLGA vs PROSPER")
st.dataframe(sensitivity_df)

# Download option
st.download_button("Download Sensitivity Data as CSV", data = sensitivity_df.to_csv(index=False).encode('utf-8'), file_name = "sensitivity_analysis.csv")

# Footer
st.markdown("---")
st.markdown("**Project by Noraeen Eleanor 💖**")           
