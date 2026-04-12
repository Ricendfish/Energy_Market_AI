# ⚡ Energy Market Intelligence System

This project is a **Data Engineering and Machine Learning Operations (MLOps)** pipeline that predicts:

• Electricity demand from weather conditions  
• Electricity prices from predicted demand  
• Market insights for major energy companies  

The system integrates **data pipelines, machine learning models, and an interactive dashboard** to analyze how weather impacts the energy market.

---

# 🌐 Live Dashboard

Access the deployed dashboard here:

👉 https://energymarketai-mdlpk9mvffqevtw5prxpum.streamlit.app/

The dashboard provides:

• Weather simulation inputs  
• Electricity demand prediction  
• Electricity price forecasting  
• Market indicators  
• Energy company stock comparisons  
• Data analysis visualizations  

---

# 📊 Dashboard Features

### Weather Simulation
Users can adjust:

- Temperature
- Wind Speed
- Month

These inputs simulate weather conditions that influence electricity demand.

---

### Energy Demand Forecast

A **Random Forest model** predicts electricity demand using:

- Temperature
- Wind speed
- Day of week
- Month
- Day of year

---

### Electricity Price Prediction

Electricity prices are predicted using:

- Weather conditions
- Predicted electricity demand

This demonstrates the **economic relationship between weather, demand, and energy pricing**.

---

### Market Indicators

The dashboard includes **Bloomberg-style indicators**:

- Predicted electricity demand
- Predicted electricity price
- Market signal (Bullish / Weak energy market)

These indicators help interpret potential market trends.

---

### Energy Company Market Comparison

The dashboard visualizes stock performance of major energy companies:

Renewable Energy Companies

- Ørsted
- Vestas Wind Systems
- Siemens Energy
- Iberdrola

Integrated Energy Companies

- Equinor
- TotalEnergies
- Shell
- BP

Stock data is retrieved using the **Yahoo Finance API**.

---



