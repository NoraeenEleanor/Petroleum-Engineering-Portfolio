import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import trapezoid


#📘 Define DC Functions (Fundamental)
def exponential_decline (qi, D, t):
    return qi * np.exp(-D * t)

def harmonic_decline (qi, D, t):
    return qi / (1 + D * t)

def hyperbolic_decline (qi, D, b, t):
    return qi / np.power (1 + b * D * t, 1 /b)

def calculate_EUR (model, qi, D, b = None, t_end = 120):
    t = np.arange (0, t_end + 1)
    if model == "Exponential":
        q = exponential_decline (qi, D, t)
    elif model == "Harmonic":
        q = harmonic_decline (qi, D, t)
    elif model == "Hyperbolic":
        q = hyperbolic_decline (qi, D ,b, t)
    EUR = trapezoid (q, t)
    return t, q, EUR


#🧪 Implement the App
st.set_page_config(page_title="📉 Decline Curve Analysis", layout="centered")
st.title(" Decline Curve Analysis (Arps)")

st.sidebar.header("Input Parameters")
qi = st.sidebar.number_input("Initial Rate, qi (stb/day)", min_value=0.0, value=1000.0)
D = st.sidebar.number_input("Nominal Decline Rate, D (fraction)", min_value=0.0, max_value=1.0, value=0.15)
b = st.sidebar.number_input("Hyperbolic Exponent, b", min_value=0.0, max_value=2.0, value=0.7)
t_end = st.sidebar.slider("Forecast Period (months)", min_value=12, max_value=360, value=120)
model = st.sidebar.selectbox("Select Decline Model", ["Exponential", "Harmonic", "Hyperbolic"])


#🔧 Calculation
t, q, EUR = calculate_EUR(model, qi, D, b, t_end)


#📊 Plot the Results
fig, ax = plt.subplots()
ax.plot(t, q, label = f"{model} Decline")
ax.set_xlabel ("Time (months)"), ax.set_ylabel ("Production Rate (stb/day)")
ax.set_title ("Production Decline Curve")
ax.grid(True)
ax.legend()
st.pyplot(fig)


#🔧 Display EUR
st.markdown(f"### Estimated Ultimate Recovery (EUR): `{EUR:.2f} stb`")


# Export Data in CSV
df = pd.DataFrame({
    "Time (months)": t,
    "Rate (stb/day)": q
})
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Forecast CSV", data = csv, file_name="DCS_Prediction.csv", mime='text/csv')

st.caption("Happy Coding!❤️")
