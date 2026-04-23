import os
import sys
import sqlite3
import numpy as np
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

# ------------------------------------------------
# PATH SETUP
# ------------------------------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

MODEL_PATH = os.path.join(BASE_DIR, "models", "electricity_price_model.pkl")

# ------------------------------------------------
# LOAD MODEL
# ------------------------------------------------

model = joblib.load(MODEL_PATH)

# ------------------------------------------------
# FASTAPI APP
# ------------------------------------------------

app = FastAPI(
    title="Energy Market AI API",
    description="Electricity price prediction API",
    version="1.0"
)

# ------------------------------------------------
# REQUEST SCHEMA
# ------------------------------------------------

class PredictionRequest(BaseModel):

    temperature: float
    wind_speed: float
    electricity_demand: float
    day_of_week: int
    month: int
    day_of_year: int


# ------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------

@app.get("/health")

def health():

    return {
        "status": "ok",
        "service": "Energy Market AI API"
    }


# ------------------------------------------------
# PRICE PREDICTION
# ------------------------------------------------

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
        "predicted_price_mwh": float(prediction),
        "predicted_price_kwh": float(prediction / 1000)
    }


# ------------------------------------------------
# LATEST MARKET PRICES
# ------------------------------------------------

@app.get("/prices/latest")

def latest_prices():

    db_path = os.path.join(BASE_DIR, "energy_market.db")

    if not os.path.exists(db_path):

        return {"error": "database not found"}

    conn = sqlite3.connect(db_path)

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
            "price_dkk": r[1],
            "price_kwh": r[1] / 1000
        })

    conn.close()

    return {
        "latest_prices": results
    }
