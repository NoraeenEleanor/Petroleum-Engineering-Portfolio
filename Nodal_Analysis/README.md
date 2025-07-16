# 🔧 Project 3: Nodal Analysis (Python + PROSPER)

This project demonstrates Nodal Analysis using Python to simulate inflow and outflow performance, and compares the result with industry-standard PROSPER models. The analysis visualizes the intersection between Inflow Performance Relationship (IPR) and Vertical Lift Performance (VLP) to determine the optimal production rate.

---

## 📂 Project Structure

- `nodal_analysis.ipynb` — Python notebook for IPR/VLP modeling
- `streamlit_app.py` — Interactive plotting and parameter controls
- `input_data.csv` — Reservoir and tubing input
- `prosper_result.csv` — Exported PROSPER model results
- `comparison_plots/` — Python vs PROSPER charts

---

## 📊 IPR Models Supported

- **Vogel Model** – For solution gas drive  
- **Fetkovich Model** – For boundary-dominated flow  
- **Standing & Linear Models** – Optional extensions

---

## 🔃 VLP Options

- Linear Gradient Model  
- Polynomial Pressure Drop (for advanced flow dependence)  
- Comparison with PROSPER's multiphase VLP correlations

---

## 🔍 Key Features

- Match IPR & VLP curves to find operating point  
- Tweak PI, WHP, and VLP gradients live  
- Visual validation: Python vs PROSPER plots  
- Optional tubing sensitivity and gas lift integration

---

## 🧠 Engineering Reflection

- VLP model used in Python was simplified (linear or polynomial) to illustrate flow dependence with depth.  
- Intersection point with IPR was obtained via manual tuning — highlighting the balance between inflow capacity and tubing constraint.  
- Result deviations from PROSPER were expected due to lack of correlation calibration, but key relationships remain preserved.  
- The model shows conceptual mastery of nodal analysis and its sensitivity to gradient, PI, and WHP.  
- This project simulates real field challenges where no “perfect” model exists — only iterative refinement and understanding.

---

## 🧪 Next Steps

To improve future versions:
- Add pressure drop models (e.g. Hagedorn & Brown)
- Automate intersection detection
- Calibrate Python results with well test or field data
