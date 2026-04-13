# ⚡ AI Electricity Cost Optimizer

An end-to-end data science application that analyzes electricity market data and predicts optimal times to use electricity based on price trends and weather conditions.

## 🌐 Live Dashboard

Access the live application here:

https://energymarketai-mdlpk9mvffqevtw5prxpum.streamlit.app/

The dashboard allows users to:

* View historical electricity market data
* Explore energy demand and price trends
* Analyze the relationship between weather and electricity demand
* Predict electricity prices for selected dates
* Identify the cheapest hours to run appliances

## 📊 Project Overview

Electricity prices fluctuate depending on market demand, weather conditions, and generation sources. This project builds a machine learning pipeline to analyze these patterns and provide actionable insights for electricity consumption.

The system integrates real-time market data, weather information, and machine learning models to help users optimize their electricity usage.

## ⚙️ System Architecture

```
Electricity Market Data + Weather Data
                 ↓
           Data Pipeline
                 ↓
       Feature Engineering
                 ↓
      Machine Learning Models
                 ↓
        Optimization Engine
                 ↓
        Streamlit Dashboard
```

## 🤖 Machine Learning Pipeline

The automated pipeline performs:

1. Data ingestion from electricity market APIs and weather sources
2. Data cleaning and preprocessing
3. Feature engineering (seasonality, weather indicators, time variables)
4. Model training and evaluation
5. Electricity price prediction

The pipeline is automated using **GitHub Actions**, allowing the model to update regularly.

## 📈 Dashboard Features

* Electricity price trend analysis
* Demand vs electricity price exploration
* Weather impact on electricity demand
* Price prediction for selected dates
* Appliance usage optimization recommendations

## 🐳 Docker Deployment

The project is containerized using Docker.

Build the image:

```
docker build -t energy-ai:1.0 .
```

Run the container:

```
docker run --name energy-ai-demo -p 8501:8501 energy-ai:1.0
```

Then open:

```
http://localhost:8501
```

## 🔄 Automation

A scheduled **GitHub Actions workflow** runs the machine learning pipeline automatically to:

* Fetch updated data
* Retrain the model
* Refresh predictions

## 🧰 Tech Stack

* Python
* Streamlit
* Pandas
* Scikit-learn
* XGBoost
* Plotly
* Meteostat Weather API
* Docker
* GitHub Actions


