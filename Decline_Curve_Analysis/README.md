# 📉 Project 2: Decline Curve Analysis (Python + Arps)

This project demonstrates oil production forecasting using classical Decline Curve Analysis (DCA). It applies exponential, hyperbolic, and harmonic models to estimate future performance based on historical production data.

---

## 🔗 Live App

You can try the interactive app here:  
👉 [Decline Curve Analysis App](https://petroleum-engineering-portfolio-6b2zswgw2yzbxmub8wrfwe.streamlit.app/)

⚠️ *Note: App may take 30–60 seconds to load if inactive (Streamlit free tier auto-sleep feature). Please wait for it to initialize.*

---

## 📂 Project Structure

- `decline_curve.ipynb` — Python notebook with DCA models and plotting
- `production_data.csv` — Sample historical data
- `forecast_results.csv` — Exported forecast
- `streamlit_app.py` — Interactive web app version

---

## ⚙️ Models Used

- **Exponential Decline**  
- **Harmonic Decline**  
- **Hyperbolic Decline (variable b-factor)**

---

## 🧠 Engineering Reflection

- Decline curve fitting was done using raw production data and classical Arps models.
- Forecasts are sensitive to **initial rate assumptions** and **b-factor selection**.
- No noise filtering or smoothing was applied, so anomalies (shut-ins, slugging) may skew results.
- Despite simplifications, this model reflects a solid foundation for production forecasting and can be extended to material balance or PTA integration.

---

## 📈 Example Output

![Forecast Plot](images/dca_plot.png)

---

## 🔗 Next Steps

For field application:
- Integrate DCA with material balance (MBAL) or RTA
- Use history matching to refine parameter estimates
- Add confidence intervals or P10/P50/P90 cases


