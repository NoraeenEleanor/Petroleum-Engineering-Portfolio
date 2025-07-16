import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title
st.title(" Nodal Analysis: IPR vs. VLP")
st.markdown("Comparing IPR Models (Vogel & Fetkovich) with Simple VLP Gradient")

# (Sidebar) Input Parameters 
st.sidebar.title("Input Parameters")

model = st.sidebar.selectbox("Select IPR Model", ["Vogel", "Fetkovich"])
q_range = np.linspace(0, 2000, 100)

# Input Parameters for VLP
whp = st.sidebar.number_input("Wellhead Pressure (psi)", value=500)
gradient = st.sidebar.number_input("Tubing Gradient (psi/ft)", value=0.65)
length = st.sidebar.number_input("Tubing Length (ft)", value=6000.0)

# Define IPR & VLP (Vogel & Fetkovich Model)

if model == "Vogel":
    pr = st.sidebar.number_input("Reservoir Pressure (psi)", value=3500)
    qo = st.sidebar.number_input("Qo (STB/day at Pwf=0)", value=1500)
    
    def vlp_model(q): return whp + gradient * length + 0.0001 * q ** 1.1
    ipr_pwf = pr + (1 - 0.2 * (q_range / qo) - 0.8 * (q_range / qo) ** 2)

elif model == "Fetkovich":
    pr = st.sidebar.number_input("Reservoir Pressure (psi)", value=3500)
    pi = st.sidebar.number_input("PI (STB/day/psi)", value=2.5)   
    
    def vlp_model(q): return whp + gradient * length + 0.002 * q ** 1.5
    ipr_pwf = pr - q_range / pi
    
# Plot VLP Curve
vlp_pwf = [vlp_model(q) for q in q_range]

# Plot (Oilfield & Academic View)
style = st.radio("Plot Style", ["Oilfield (IPR ↑, VLP ↓)", "Academic (IPR ↓, VLP ↑)"])

fig, ax = plt.subplots()

if style == "Oilfield (IPR ↑, VLP ↓)":
    ax.plot(q_range, ipr_pwf, label=f"IPR - {model}", color='green')
    ax.plot(q_range, vlp_pwf, label="VLP", color='blue')
    ax.set_xlabel("Bottomhole Pressure (psig)"), ax.set_ylabel("Flowrate (STB/day)")
    ax.invert_yaxis()
else:
    ax.plot(ipr_pwf, q_range, label=f"IPR - {model}", color='green')
    ax.plot(vlp_pwf, q_range, label="VLP", color='blue')
    ax.set_xlabel("Bottomhole Pressure (psig)"), ax.set_ylabel("Flowrate (STB/day)")

ax.set_title("Nodal Analysis Plot")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# Intersection (Operating Point)
q_diff = np.abs(np.array(ipr_pwf) - np.array(vlp_pwf))
q_index = np.argmin(q_diff)
q_intersect = q_range[q_index]
p_intersect = ipr_pwf[q_index]

st.markdown(f"""
### Estimated Operating Point
**Flowrate:** {q_intersect:.2f} STB/day
**Bottomhole Pressure:** {p_intersect:.2f} psi)
""")
