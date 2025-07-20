import streamlit as st 
import pandas as pd
import lasio
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import io

# Configuration
st.set_page_config(page_title="LAS Viewer", layout='wide')

# Sidebar (for Uploading LAS File)
st.sidebar.header("📂 Upload LAS File")
uploaded_file = st.sidebar.file_uploader("Choose a LAS file", type=["las"])

# App Deployment
st.title("🛢️ LAS File Multi-Track Log Viewer")
if uploaded_file:
    las = lasio.read(io.StringIO(uploaded_file.read().decode("utf-8", errors="ignore")))
    df = las.df().reset_index()
    
    # Handle 'DEPTH' or 'DEPT'
    depth_col = 'DEPTH' if 'DEPTH' in df.columns else 'DEPT'
    df.rename(columns={depth_col: 'DEPTH'}, inplace=True)
    
    # Well Info
    st.subheader("📋 Well Header Info")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text(f"Well: {las.well.get('WELL', 'N/A')}")
    with col2:
        st.text(f"Field: {las.well.get('FLD', 'N/A')}")
    with col3:
        st.text(f"Company: {las.well.get('COMP', 'N/A')}")
    
    # Depth Selection
    st.subheader("📏 Select Depth Interval")
    min_depth = float(df['DEPTH'].min())
    max_depth = float(df['DEPTH'].max())
    top = st.number_input("Top Depth", value=min_depth, min_value=min_depth, max_value=max_depth)
    base = st.number_input("Base Depth", value=max_depth, min_value=min_depth, max_value=max_depth)
    
    # Curve Info
    st.subheader("📈 Available Curves")
    curve_list = list(df.columns)       # Display all columns including DEPTH
    st.write(curve_list)
    
    st.subheader("🎛️ Select Curve for Multi-Track")
    available_curves = [col for col in df.columns if col != 'DEPTH']
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gr_curve = st.selectbox("Gamma Ray (GR)", options=available_curves, index=available_curves.index("GR") if "GR" in available_curves else 0)
    
    with col2:
        rhob_curve = st.selectbox("RHOB", options=[col for col in available_curves if 'RHOB' in col.upper()] or available_curves)
        nphi_curve = st.selectbox("NPHI", options=[col for col in available_curves if 'NPHI' in col.upper()] or available_curves)
    
    with col3:
        resistivity_options = ["RT", "RES", "ILD", "LLD"]
        resistivity_curve = next((r for r in resistivity_options if r in available_curves), available_curves[0] )
        resistivity_curve = st.selectbox("Resistivity", options=available_curves, index=available_curves.index("RT") if "RT" in available_curves else 0) 
    
    # 🔃 Refresh interval_df after curve selection
    interval_df = df[(df["DEPTH"] >= top) & (df["DEPTH"] <= base)].copy()

    # 🧠 Normalize NPHI if needed
    if interval_df[nphi_curve].max() > 1.0:
        st.warning(f"NPHI max value > 1.0 detected (max = {interval_df[nphi_curve].max():.2f}). Converting from % to fraction.")
        interval_df[nphi_curve] = interval_df[nphi_curve] / 100

    # 🔍 Clean missing values for selected curves
    interval_df.replace([-999.25, -9999, -999.0], pd.NA, inplace=True)
    interval_df = interval_df.dropna(subset=[rhob_curve, nphi_curve])
    
    # Track Width Adjustment
    st.subheader("📐 Customize Track Widths")
    col_width1, col_width2, col_width3 = st.columns(3)
    with col_width1:
        width1 = st.slider("Track 1 Width (GR)", min_value=1, max_value=5, value=2)
    with col_width2:
        width2 = st.slider("Track 2 Width (RHOB/NPHI)", min_value=1, max_value=5, value=2)
    with col_width3:
        width3 = st.slider("Track 3 Width (Resistivity)", min_value=1, max_value=5, value=2)
    
    # Log Plot
    st.subheader("🧪 Log Visualization")
    fig = plt.figure(figsize=(width1 + width2 + width3 + 2, 10 ))
    gs = gridspec.GridSpec(1, 4, width_ratios=[width1, width2, width3, width2])
    
    # Track 1: GR
    ax0 = plt.subplot(gs[0])
    ax0.plot(interval_df[gr_curve], interval_df["DEPTH"], color="green")
    ax0.set_xlabel(gr_curve)
    ax0.set_xlim(0, 150)
    ax0.invert_yaxis()
    ax0.grid(True)
    ax0.set_ylabel("DEPTH (ft)")
    ax0.set_title("Gamma Ray")

    # Track 2: Resistivity
    ax1 = plt.subplot(gs[1])
    ax1.semilogx(interval_df[resistivity_curve], interval_df["DEPTH"], color="black")
    ax1.set_xlabel(resistivity_curve)
    ax1.set_xlim(0.2, 2000)
    ax1.invert_yaxis()
    ax1.grid(True, which="both")
    ax1.set_title("Resistivity")

    # Track 3: RHOB / NPHI
    ax2 = plt.subplot(gs[2])
    ax2.plot(interval_df[rhob_curve], interval_df["DEPTH"], color="red", label="RHOB")
    ax2.plot(interval_df[nphi_curve], interval_df["DEPTH"], color="blue", label="NPHI")
    ax2.fill_betweenx(interval_df["DEPTH"], interval_df[rhob_curve], interval_df[nphi_curve],
                  where=(interval_df[rhob_curve] >= interval_df[nphi_curve]),
                  facecolor="violet", alpha=0.3, label="RHOB > NPHI")
    ax2.set_xlabel("RHOB / NPHI")
    ax2.set_xlim(1.95, 2.95)
    ax2.invert_yaxis()
    ax2.grid(True)
    ax2.legend()
    ax2.set_title("RHOB / NPHI")

    # Track 4: CALI (if exists)
    if "CALI" in interval_df.columns:
        ax3 = plt.subplot(gs[3])
        ax3.plot(interval_df["CALI"], interval_df["DEPTH"], color="brown")
        ax3.set_xlabel("CALI")
        ax3.set_xlim(6, 18)
        ax3.invert_yaxis()
        ax3.grid(True)
        ax3.set_title("CALI")

    # Show Plot
    st.pyplot(fig)
        
    # Export Files
    st.subheader("📤 Export Interval to CSV")
    csv_data = interval_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Your CSV Files",
        data=csv_data,
        file_name="las.interval.csv",
        mime="text/csv"
    )
else:
    st.warning("Please upload a LAS file from the sidebar")
    