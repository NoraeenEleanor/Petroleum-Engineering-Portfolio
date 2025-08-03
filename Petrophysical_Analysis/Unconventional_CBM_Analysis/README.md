# 🧱 Project 4b: Unconventional CBM Analysis (Coal Facies & Gas Content Mapping)

This project focuses on the petrophysical interpretation of a coalbed methane (CBM) reservoir using well log data and core gas content samples. The analysis includes coal zone identification based on log cutoffs, facies classification, gas content visualization, and coal interval export — all built using Python and Streamlit.

---

## 🔗 Live App  
You can try the interactive app here:  
👉 CBM Coal Zone & Gas Content Analyzer (Streamlit App) *(link placeholder)*

⚠️ Note: App may take 30–60 seconds to load if inactive (Streamlit free tier auto-sleep feature). Please wait for it to initialize.

---

## 📂 Project Structure  
`cbm_log_analyzer.ipynb` — Main notebook for CBM-focused log interpretation  
`cbm_streamlit.py` — Streamlit app for interactive coal zone & gas content visualization  
`ALTHORPE_1_MAIN_HR_Althorpe.las` — Raw LAS file from CBM well  
`export_coal_intervals.csv` — Extracted coal seam intervals based on cutoff rules  
`images/` — Snapshot plots (GR, RHOB, facies, gas content overlays)

---

## 📊 Features & Interpretation Logic

- **Coal Zone Identification**:  
  GR < 50, RHOB < 1.8 g/cc, PEF < 1.5, Porosity > 4–6%
  
- **Facies Classification**:  
  Coal, shale, sandstone, siltstone, limestone via rule-based logic

- **Gas Content Visualization**:  
  Plotted gas samples vs depth (midpoint), shaded seams using `axhspan()`

- **Depth Alignment**:  
  Adjusted +16.0 ft from GL to RT to match core depths

- **Output**:  
  Highlighted coal intervals, facies shading, optional CSV export

---

## 🧠 Engineering Reflection

This project showcases unconventional reservoir handling where coal seams act both as source and reservoir. Cutoffs were tuned to avoid missing thin coal beds. Facies classification was done via basic deterministic logic using GR, RHOB, PEF, and porosity. Gas content overlays help identify productive seams and evaluate gas-bearing potential.

It demonstrates my understanding of:
- Log-based coal identification
- Depth interval matching to core gas data
- Visual synthesis of petrophysical and sample-based data

---

## 🚀 Next Steps

- Include gas content gradient trends
- Estimate gas-in-place (GIP) using Langmuir assumptions
- Add borehole image or lithofacies classification
- Compare to conventional well log for benchmarking
