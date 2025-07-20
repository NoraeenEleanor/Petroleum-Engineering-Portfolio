import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import io

# Streamlit config
st.set_page_config(page_title="Nodal Analysis App", layout="wide")
st.title("🛢️ Nodal Analysis - IPR vs VLP Curves")

st.markdown("""
This app performs **IPR vs VLP analysis** using **Fetkovich IPR model** and a simple **VLP model**.
- You can adjust **Wellhead Pressure (WHP)** values.
- Results are plotted in both Oilfield View (inverted y-axis) and Academic View.
""")

# --- INPUT SECTION ---
# User Inputs
p_res = st.number_input("Reservoir Pressure (psia)", value=1400)
depth = st.number_input("Depth (ft)", value=8000)
gradient = st.number_input("Gradient (psi/ft)", value=0.12)

whp = st.slider("Select Wellhead Pressure (WHP, psig)", min_value=100, max_value=700, value=500, step=50)
st.caption("ℹ️ WHP as low as 100 psig can represent low surface backpressure wells such as gas-lifted or strong PI systems.")

whp_list = [whp]

# Static Data
q_list = [100, 250, 400, 550, 700, 850]
pwf_list = [1300, 1200, 1100, 1000, 850, 700]

# --- IPR CALCULATION ---
df = pd.DataFrame({
    'q_stb': q_list,
    'pwf_psig': pwf_list
})
df['delta^2'] = p_res**2 - df['pwf_psig']**2
df['log_q'] = np.log10(df['q_stb'])
df['log_delta2'] = np.log10(df['delta^2'])

fit = np.polyfit(df['log_q'], df['log_delta2'], 1)
n = 1 / fit[0]
c = q_list[0] / (p_res**2 - pwf_list[0]**2)**n

pwf_range = np.arange(100, p_res, 10)
q_ipr = [c * (p_res**2 - pwf**2)**n for pwf in pwf_range]

# VLP Function
def vlp_model(q, whp):
    return whp + gradient * depth + 0.002 * q**1.5

# --- PLOTTING SECTION ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharex=True)
colors = ['blue', 'orange', 'purple']

for idx, ax in enumerate(axes):
    ax.plot(q_ipr, pwf_range, label='Fetkovich IPR', color='red', linewidth=2)

    for i, whp in enumerate(whp_list):
        q_vlp = np.linspace(0, max(q_ipr) * 1.1, 100)
        p_vlp = vlp_model(q_vlp, whp)

        # Check for intersection when WHP = 500
        if whp == 500:
            ipr_func = interp1d(q_ipr, pwf_range, fill_value='extrapolate')
            vlp_func = interp1d(q_vlp, p_vlp, fill_value='extrapolate')
            q_common = np.linspace(0, min(max(q_ipr), max(q_vlp)), 200)
            delta_P = np.abs(ipr_func(q_common) - vlp_func(q_common))
            idx_min = np.argmin(delta_P)
            q_intersect = q_common[idx_min]
            p_intersect = ipr_func(q_common)[idx_min]
            ax.scatter(q_intersect, p_intersect, color='black', marker='X', s=100,
                       label=f'Operating Point\nQ={q_intersect:.1f}, Pwf={p_intersect:.1f}')

        ax.plot(q_vlp, p_vlp, linestyle='--', label=f'VLP WHP={whp} psig', color=colors[i % len(colors)])

    ax.scatter(q_list, pwf_list, label='Well Test Data', color='green')
    ax.set_xlabel('Flowrate (STB/day)')
    ax.set_ylabel('Bottomhole Pressure (psig)')
    ax.grid(True)
    ax.legend()

axes[0].invert_yaxis()
axes[0].set_title('Oilfield Standard View (Y-axis Inverted)')
axes[1].set_title('Academic View (General Y-axis)')

plt.suptitle('Nodal Analysis: IPR vs. Multi-VLP', fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Show Plot
st.pyplot(fig)

# --- Optional Output ---
if 500 in whp_list:
    st.subheader("📌 Estimated Operating Point (for WHP = 500 psig)")
    st.write(f"**Flowrate** = `{q_intersect:.1f}` STB/day")
    st.write(f"**Bottomhole Pressure** = `{p_intersect:.1f}` psig")


# Save as PDF
pdf_buffer = io.BytesIO()
fig.savefig(pdf_buffer, format='pdf')
st.download_button(
    label="📥 Download Plot as PDF",
    data=pdf_buffer,
    file_name="nodal_analysis_plot.pdf",
    mime='application/pdf'
)

# Export IPR & VLP to CSV
ipr_df = pd.DataFrame({'Pwf (psig)': pwf_range, 'IPR Q (STB/d)': q_ipr})
vlp_df = pd.DataFrame({'Q (STB/d)': q_vlp, 'VLP Pwf (psig)': vlp_model(q_vlp, whp)})

csv_export = io.StringIO()
combined_df = pd.concat([ipr_df, vlp_df], axis=1)
combined_df.to_csv(csv_export, index=False)

st.download_button(
    label="📥 Download IPR + VLP Data as CSV",
    data=csv_export.getvalue(),
    file_name='ipr_vlp_data.csv',
    mime='text/csv'
)

