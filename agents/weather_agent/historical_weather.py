import requests
import pandas as pd

url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 55.6761,
    "longitude": 12.5683,
    "start_date": "2015-01-01",
    "end_date": "2024-01-01",
    "daily": "temperature_2m_mean,windspeed_10m_mean",
    "timezone": "UTC"
}

r = requests.get(url, params=params)

print("Status:", r.status_code)

data = r.json()

df = pd.DataFrame({
    "date": data["daily"]["time"],
    "temperature": data["daily"]["temperature_2m_mean"],
    "wind_speed": data["daily"]["windspeed_10m_mean"]
})

df.to_csv("data/weather_history.csv", index=False)

print(df.head())