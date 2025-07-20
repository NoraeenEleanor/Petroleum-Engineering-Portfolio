# 📊 Project 6: Power BI Integration Dashboard

This project connects a Python-based data backend (Streamlit app) to a front-end Power BI dashboard. It demonstrates how field production or simulation data can be exported, shared, and visualized using a modern data pipeline.

---

## 🔗 Live App

You can try the interactive app here:  
👉 [Power BI + OFM Integration App](https://petroleum-engineering-portfolio-jxckuaasbpyypahscvscmu.streamlit.app/)

⚠️ *Note: App may take 30–60 seconds to load if inactive (Streamlit free tier auto-sleep feature). Please wait for it to initialize.*

---

## 📂 Project Structure

- `data_streamlit_app.py` — Streamlit backend for data input & export  
- `powerbi_dashboard.pbix` — Power BI file with linked visualizations  
- `csv_exports/` — Generated CSVs from Streamlit  
- `images/` — Power BI dashboard snapshots

---

## 🔁 Workflow Summary

1. Streamlit app generates & exports simulation/engineering data  
2. Power BI reads CSVs and builds live-linked dashboard  
3. Users interact with plots, slicers, and KPIs in Power BI

---

## 📈 Dashboard Features

- Production summary by well and reservoir  
- Trend charts (rate, pressure, gas injection)  
- Custom filters: by well, zone, lift method  
- Optional: Forecast, decline overlay, or NPV estimation

---

## 🧠 Engineering Reflection

- Data transfer relies on CSV which may limit real-time sync.  
- Dashboard depends on clean input formatting for stability.  
- This project showcases end-to-end thinking: from engineering data generation to business visualization.  
- A scalable solution for production engineers, planners, or asset teams.

---

## 🔗 Future Additions

- Replace CSV with database or live API  
- Add engineering calculations inside Power BI (DAX)  
- Link to corporate reporting systems
