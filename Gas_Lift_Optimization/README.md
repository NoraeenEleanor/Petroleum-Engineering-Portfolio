# 🎯 Project 1: Dual String Gas Lift Optimization (Python + PROSPER + OLGA)

This project investigates the performance of dual string gas lift wells using a hybrid workflow with Python simulation, PROSPER modeling, and OLGA validation. The goal is to optimize gas injection rate, dome pressure, and valve configuration across both tubing strings.

---

## 🔗 Live App

You can try the interactive app here:  
👉 [Dual String GL App](https://petroleum-engineering-portfolio-hq3u8fq8zjk2xtdjvvonev.streamlit.app/)

⚠️ *Note: App may take 30–60 seconds to load if inactive (Streamlit free tier auto-sleep feature). Please wait for it to initialize.*

---

## 📂 Project Structure

- `gas_lift_dual.ipynb` — Main Python simulation notebook
- `streamlit_app.py` — Interactive Streamlit dashboard
- `input_data/` — PVT, well test, and injection gas files
- `results/` — Plots and CSV outputs for sensitivity studies
- `OLGA/` — Sample OLGA case input and output (if available)
- `PROSPER/` — Snapshot of matching PROSPER models

---

## 🧪 Parameters Explored

- Gas Injection Rate (MMscf/d)
- Dome Pressure (psig)
- Productivity Index (PI)
- Pressure Drop Between Valves (∆P)
- Flow Distribution Between Tubing Strings

---

## 📈 Sensitivity Results

The study uses parametric sweep to visualize the impact of each variable on well deliverability. Outputs include:

- IPR/VLP intersection points
- Injection gas utilization efficiency
- Comparative curves: Python vs PROSPER vs OLGA

---

## 🧠 Engineering Reflection

- The simulation uses a simplified gas lift model with assumed injection profiles and fixed dome pressures.  
- Dynamic behavior such as valve hysteresis, surging, and dual string interaction is complex and was approximated manually.  
- While not fully field-calibrated, this approach demonstrates understanding of injection-response relationships and the impact of pressure drop assumptions.  
- For field application, OLGA or lift performance tests would be used to tune valve opening pressures and injection strategy.

---

## 🔗 Next Steps

To improve the workflow:
- Integrate live data into Python for real-time optimization
- Replace static gradient with pressure drop correlation (e.g. Duns & Ros)
- Add instability simulation (casing heading, density wave surging)

