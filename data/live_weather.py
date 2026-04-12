import requests
import pandas as pd
from datetime import datetime


def get_weather_features(date):

    latitude = 55.6761
    longitude = 12.5683

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        "&daily=temperature_2m_mean,windspeed_10m_max"
        "&timezone=auto"
    )

    response = requests.get(url)
    data = response.json()

    dates = data["daily"]["time"]
    temps = data["daily"]["temperature_2m_mean"]
    winds = data["daily"]["windspeed_10m_max"]

    target = date.strftime("%Y-%m-%d")

    if target not in dates:
        return None

    idx = dates.index(target)

    temperature = temps[idx]
    wind_speed = winds[idx]

    features = {
        "temperature": temperature,
        "wind_speed": wind_speed,
        "electricity_demand": 4000,
        "day_of_week": date.weekday(),
        "month": date.month,
        "day_of_year": date.timetuple().tm_yday
    }

    return pd.DataFrame([features])