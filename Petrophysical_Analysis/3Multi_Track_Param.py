import streamlit as st
import pandas as pd
import numpy as np
import lasio
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import io

# Streamlit Page Config
st.set_page_config(page_title="Petrophysical Log Analyzer", layout="wide")
st.title("🛢️ Petrophysical Log Analyzer")

# --- Sidebar: File Upload & Curve Selection ---
st.sidebar.header("📂 Upload LAS File")
uploaded_file = st.sidebar.file_uploader("Choose LAS file", type=[".las"])

if uploaded_file:
    # ✅ Proper read and decode
    file_str = uploaded_file.read().decode('utf-8', errors='ignore')
    las = lasio.read(io.StringIO(file_str))

    # --- DataFrame preparation ---
    df = las.df().reset_index()
    df.columns = df.columns.str.upper()
    df.replace([-999.25, -9999, -999.0], np.nan, inplace=True)
    curves = df.columns.tolist()

    # --- Sidebar: Select curves ---
    st.sidebar.header("🧪 Curve Selection")
    gr_curve = st.sidebar.selectbox("GR (Gamma Ray)", curves, index=curves.index("GR") if "GR" in curves else 0)
    cali_curve = st.sidebar.selectbox("CALI (Caliper)", curves, index=curves.index("CALI") if "CALI" in curves else 0)
    res_curve = st.sidebar.selectbox("RDEP (Resistivity)", curves, index=curves.index("RDEP") if "RDEP" in curves else 0)
    rhob_curve = st.sidebar.selectbox("RHOB (Density)", curves, index=curves.index("RHOB") if "RHOB" in curves else 0)
    nphi_curve = st.sidebar.selectbox("NPHI (Neutron)", curves, index=curves.index("NPHI") if "NPHI" in curves else 0)

    # --- Sidebar: Select interval ---
    st.sidebar.header("📏 Depth Interval")
    depth_col = df.columns[0]  # usually 'DEPT'
    depth_min, depth_max = df[depth_col].min(), df[depth_col].max()
    top = st.sidebar.number_input("Top Depth", float(depth_min), float(depth_max), float(depth_min))
    base = st.sidebar.number_input("Base Depth", float(depth_min), float(depth_max), float(depth_max))

    # --- Filter Interval ---
    interval_df = df[(df[depth_col] >= top) & (df[depth_col] <= base)].copy()

    # Normalize NPHI if needed
    if interval_df[nphi_curve].max() > 1.0:
        st.warning(f"NPHI max value > 1.0 detected (max = {interval_df[nphi_curve].max():.2f}). Converting from % to fraction.")
        interval_df[nphi_curve] /= 100

    # --- Calculate Vshale, φ, Sw ---
    gr_clean = interval_df[gr_curve].clip(20, 150)
    gr_min, gr_max = gr_clean.min(), gr_clean.max()
    interval_df['VSH'] = (interval_df[gr_curve] - gr_min) / (gr_max - gr_min)
    interval_df['PHID'] = (2.65 - interval_df[rhob_curve]) / (2.65 - 1.0)
    interval_df['PHIN'] = interval_df[nphi_curve]
    interval_df['PHIE'] = (interval_df['PHID'] + interval_df['PHIN']) / 2
    interval_df['RT'] = interval_df[res_curve]
    a, m, n = 1, 2, 2
    rw = 0.05
    interval_df['SW'] = ((a * rw) / (interval_df['RT'] * interval_df['PHIE'] ** m)) ** (1/n)
    interval_df['SW'] = interval_df['SW'].clip(0, 1)

    # --- Cutoffs ---
    interval_df['PAY'] = (interval_df['PHIE'] >= 0.1) & (interval_df['SW'] <= 0.6) & (interval_df['VSH'] <= 0.35)

    # --- TAB LAYOUT ---
    tab1, tab2, tab3 = st.tabs(["📊 Log Plot", "📋 Summary", "⬇️ Export"])

    with tab1:
        st.subheader("📊 Log Visualization with Shading")
        fig = plt.figure(figsize=(16, 10))
        gs = gridspec.GridSpec(1, 6, width_ratios=[1, 1, 1, 1, 1, 1])

        depth = interval_df[depth_col]
        tracks = [
            (gr_curve, 'GR', 'lime'),
            (res_curve, 'Resistivity', 'blue'),
            (rhob_curve, 'RHOB', 'red'),
            (nphi_curve, 'NPHI', 'purple'),
            ('VSH', 'Vshale', 'brown'),
            ('SW', 'Water Saturation', 'black')
        ]

        for i, (curve, title, color) in enumerate(tracks):
            ax = fig.add_subplot(gs[0, i])
            ax.plot(interval_df[curve], depth, color=color, label=curve)
            ax.set_ylim(depth.max(), depth.min())
            ax.set_title(title)
            ax.grid(True)
            ax.set_xlabel(curve)

            # Lithology shading (sand vs shale)
            if title == 'GR':
                ax.fill_betweenx(depth, interval_df[curve], 150, where=interval_df[curve]<75, color='khaki', alpha=0.4, label='Sand')
                ax.fill_betweenx(depth, interval_df[curve], 150, where=interval_df[curve]>=75, color='saddlebrown', alpha=0.3, label='Shale')
            # Hydrocarbon Indication
            if title == 'Resistivity':
                ax.fill_betweenx(depth, 0, interval_df[curve], where=(interval_df[curve]>20) & (interval_df[gr_curve]<75), color='green', alpha=0.3, label='HC Indication')
            # PHID overlay
            if title == 'RHOB':
                ax.plot(interval_df['PHID'], depth, linestyle='--', color='orange', label='PHID')
            # PHIN overlay
            if title == 'NPHI':
                ax.plot(interval_df['PHIN'], depth, linestyle='--', color='deeppink', label='PHIN')
            # Net Pay highlight
            ax.fill_betweenx(depth, 0, 1, where=interval_df['PAY'], transform=ax.get_xaxis_transform(), color='gold', alpha=0.3, label='Net Pay')

            ax.legend(fontsize=7)

        st.pyplot(fig)

    with tab2:
        st.subheader("🧾 Pay Zone Summary Table")
        interval_thickness = depth.diff().mean()
        net_thick = interval_df[interval_df['PAY']][depth_col].count() * interval_thickness
        gross_thick = interval_df[depth_col].count() * interval_thickness
        net_gross = net_thick / gross_thick if gross_thick > 0 else 0

        summary_data = {
            "Top (m)": [top],
            "Base (m)": [base],
            "Gross Thickness (m)": [gross_thick],
            "Net Thickness (m)": [net_thick],
            "Net/Gross": [net_gross],
            "Avg φ": [interval_df["PHIE"].mean()],
            "Avg Sw": [interval_df["SW"].mean()],
            "Avg Vsh": [interval_df["VSH"].mean()]
        }
        st.table(pd.DataFrame(summary_data))

    with tab3:
        st.subheader("📤 Export CSV Results")
        csv = interval_df.to_csv(index=False)
        st.download_button("📥 Download Interval CSV", csv, "interval_output.csv", "text/csv")

else:
    st.info("👈 Upload a LAS file to begin.")
