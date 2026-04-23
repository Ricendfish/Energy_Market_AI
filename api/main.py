from fastapi import FastAPI
import numpy as np

from api.schemas import PredictionRequest
from api.model_loader import load_model

app = FastAPI(title="Energy Market AI API")

model = load_model()

@app.get("/health")
def health():
    return {"status": "ok"}
@app.post("/predict")
def predict(data: PredictionRequest):

    features = np.array([[
        data.temperature,
        data.wind_speed,
        data.electricity_demand,
        data.day_of_week,
        data.month,
        data.day_of_year
    ]])

    prediction = model.predict(features)[0]

    return {"predicted_price": float(prediction)}
