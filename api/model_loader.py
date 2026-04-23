import pickle
from pathlib import Path

MODEL_PATH = Path("models/price_model.pkl")

def load_model():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model
