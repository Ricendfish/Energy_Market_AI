import pandas as pd
import joblib

def run_pipeline():

    print("Loading models...")

    demand_model = joblib.load("models/demand_model/demand_model.pkl")
    price_model = joblib.load("models/price_model/price_model.pkl")

    print("Loading latest weather data...")

    weather = pd.read_csv("data/weather_history.csv")

    latest = weather.iloc[-1]

    temperature = latest["temperature"]
    wind_speed = latest["wind_speed"]

    day_of_week = pd.to_datetime(latest["date"]).dayofweek
    month = pd.to_datetime(latest["date"]).month
    day_of_year = pd.to_datetime(latest["date"]).dayofyear

    # Demand prediction
    demand_features = [[
        temperature,
        wind_speed,
        day_of_week,
        month,
        day_of_year
    ]]

    predicted_demand = demand_model.predict(demand_features)[0]

    # Price prediction
    price_features = [[
        temperature,
        wind_speed,
        day_of_week,
        month,
        day_of_year,
        predicted_demand
    ]]

    predicted_price = price_model.predict(price_features)[0]

    print("\nForecast Results")
    print("------------------")
    print("Temperature:", temperature)
    print("Wind Speed:", wind_speed)
    print("Predicted Demand:", round(predicted_demand, 2))
    print("Predicted Electricity Price:", round(predicted_price, 2))


if __name__ == "__main__":
    run_pipeline()