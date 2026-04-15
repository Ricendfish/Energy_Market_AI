import joblib
import pandas as pd

# load model
model = joblib.load("models/hourly_price_model.pkl")

# the exact features used during training
MODEL_FEATURES = [
    "temperature",
    "wind_speed",
    "electricity_demand",
    "hour",
    "day_of_week",
    "month"
]


def predict_24_hours(weather_features):

    predictions = []

    for hour in range(24):

        features = weather_features.copy()

        # set hour for prediction
        features["hour"] = hour

        # ensure only training features are passed
        features = features[MODEL_FEATURES]

        predicted_mwh = model.predict(features)[0]

        # convert MWh → kWh
        predicted_kwh = predicted_mwh / 1000

        predictions.append({
            "hour": hour,
            "price": predicted_kwh
        })

    return pd.DataFrame(predictions)