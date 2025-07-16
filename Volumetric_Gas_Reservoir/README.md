# 🧮 Project 5: Volumetric Gas Reservoir Estimation (Python)

This project estimates Original Gas in Place (OGIP) using the volumetric method based on geological, petrophysical, and PVT input. It incorporates sensitivity to temperature, pressure, and Z-factor variations.

---

## 📂 Project Structure

- `gas_volumetrics.ipynb` — Main calculation notebook  
- `streamlit_app.py` — Interactive input/output dashboard  
- `z_factor_chart.png` — Used for manual Z-factor selection  
- `reservoir_input.csv` — Porosity, thickness, area data  
- `outputs/` — OGIP results in CSV format

---

## 📊 Parameters Considered

- Area, net pay, porosity, Sw  
- Pressure and temperature  
- Gas deviation factor (Z)  
- Formation volume factor (Bg)

---

## 🧠 Engineering Reflection

- Z-factor was estimated from standard charts, assuming dry gas behavior.  
- Net pay, porosity, and saturation were input from interpreted logs.  
- Sensitivity analysis was included to explore impact of pressure uncertainty.  
- This project reflects classical engineering workflows and supports early-phase field appraisal.

---

## 🔄 Next Steps

- Replace chart-based Z with EOS-based PVT modeling  
- Add uncertainty ranges for probabilistic OGIP  
- Integrate with material balance analysis
