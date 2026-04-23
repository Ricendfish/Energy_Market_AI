from fastapi import FastAPI
import numpy as np
import sqlite3

from api.schemas import PredictionRequest
from api.model_loader import load_model

app = FastAPI(
    title="Energy Market AI API",
    description="API for electricity price prediction and market data",
    version="1.0"
)

# Load ML model at startup
model = load_model()


# -------------------------------
# Health Check Endpoint
# -------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Energy Market AI API"
    }


# -------------------------------
# Prediction Endpoint
# -------------------------------

@app.post("/predict")
def predict_price(data: PredictionRequest):

    features = np.array([[
        data.temperature,
        data.wind_speed,
        data.electricity_demand,
        data.day_of_week,
        data.month,
        data.day_of_year
    ]])

    prediction = model.predict(features)[0]

    return {
        "predicted_price": float(prediction)
    }


# -------------------------------
# Latest Market Prices Endpoint
# -------------------------------

@app.get("/prices/latest")
def get_latest_prices():

    conn = sqlite3.connect("energy_market.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, price_dkk
        FROM latest_prices
        ORDER BY timestamp DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    results = []

    for r in rows:
        results.append({
            "timestamp": r[0],
            "price_dkk": r[1]
        })

    conn.close()

    return {
        "latest_prices": results
    }
