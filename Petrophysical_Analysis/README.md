# 🧱 Project 4: Petrophysical Analysis (LAS Log Interpretation)

This project analyzes well log data from LAS files to estimate porosity, water saturation, net pay, and lithology using Python. The app includes visualization, basic interpretation methods, and CSV export for further integration.

---

## 📂 Project Structure

- `las_analyzer.ipynb` — Core notebook for LAS processing and property calculation  
- `las_streamlit.py` — Streamlit app for interactive log visualization  
- `las_files/` — Raw LAS files (e.g., Cendor-5, Irama)  
- `results/` — Exported CSV tables with calculated properties  
- `images/` — Plot snapshots and well zone diagrams

---

## 📊 Properties Calculated

- **Porosity**: Density (ϕD), Neutron (ϕN), Sonic (ϕS)  
- **Water Saturation**: Archie’s equation (Sw)  
- **Vshale**: GR-based method  
- **Net Pay**: Based on Sw & Porosity cutoff  
- **Lithology**: GR & RHOB-NPHI crossover analysis  
- **Optional**: Permeability via Coates/Timur models

---

## 🧠 Engineering Reflection

- Calculations used typical assumptions (e.g., Rw, a, m, n) due to lack of lab core data.  
- Lithology inference and pay zone cutoffs are based on basic log curve relationships and GR thresholds.  
- Petrophysical models were kept simple to focus on interpretative logic, with flexibility to enhance for field calibration.  
- Demonstrates clear understanding of how raw LAS logs translate into reservoir quality indicators.

---

## 🚀 Next Steps

- Integrate machine learning for lithology classification  
- Include crossplots (M-N, Pickett)  
- Link with reservoir simulation models or DST data
