import streamlit as st 
import pandas as pd
import lasio
import matplotlib.pyplot as plt
import io

# Title
st.set_page_config(page_title="LAS File Explorer", layout='wide')

# Sidebar (for Uploading LAS File)
st.sidebar.header("📂 Upload LAS File")
uploaded_file = st.sidebar.file_uploader("Choose a LAS file", type=["las"])

# App Deployment
st.title("🛢️ LAS File Data Explorer")
if uploaded_file:
    las = lasio.read(io.StringIO(uploaded_file.read().decode("utf-8", errors="ignore")))
    df = las.df()
    df.reset_index(inplace=True)
    
    # Well Info
    st.subheader("📋 Well Header Info")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text(f"Well: {las.well.WELL.value}")
    with col2:
        st.text(f"Field: {las.well.get('FLD', 'N/A')}")
    with col3:
        st.text(f"Company: {las.well.get('COMP', 'N/A')}")
    
    # Curve Info
    st.subheader("📈 Available Curves")
    curve_list = list(df.columns)
    st.write(curve_list)
    
    # Depth Selection
    st.subheader("📏 Select Depth Interval")
    min_depth = float(df['DEPT'].min())
    max_depth = float(df['DEPT'].max())
    top = st.number_input("Top Depth", value=min_depth, min_value=min_depth, max_value=max_depth)
    base = st.number_input("Base Depth", value=max_depth, min_value=min_depth, max_value=max_depth)
    
    interval_df = df[(df['DEPT'] >= top) & (df['DEPT'] <= base)]
    
    # Logs Plot
    st.subheader("🧪 Log Visualization")
    selected_curves = st.multiselect("Select curves to plot", options=curve_list, default=['GR'])
    
    if selected_curves:
        for curve in selected_curves:
            fig, ax = plt.subplots(figsize=(4, 8))
            ax.plot(interval_df[curve], interval_df['DEPT'], label=curve)
            ax.invert_yaxis()
            ax.set_xlabel(curve), ax.set_ylabel("Depth (ft)")
            ax.grid(True)
            st.pyplot(fig)
    else:
        st.info("Please select one cuver to plot")
        
    # Export Files
    st.subheader("📤 Export Interval to CSV")
    csv_data = interval_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Your CSV Files",
        data=csv_data,
        file_name="internal_logs.csv",
        mime="text/csv"
    )
else:
    st.warning("Please upload a LAS file from the sidebar")
    