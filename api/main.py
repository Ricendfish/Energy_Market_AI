from fastapi import FastAPI
import numpy as np

from api.schemas import PredictionRequest
from api.model_loader import load_model

app = FastAPI(title="Energy Market AI API")

model = load_model()

@app.get("/health")
def health():
    return {"status": "ok"}
