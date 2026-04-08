import requests
import pandas as pd

url = "https://api.energidataservice.dk/dataset/Elspotprices"

params = {
    "start": "2020-01-01",
    "end": "2024-01-01",
    "filter": '{"PriceArea":["DK1","DK2"]}',
    "limit": 0
}

r = requests.get(url, params=params)
data = r.json()["records"]

df = pd.DataFrame(data)

df = df[["HourUTC", "PriceArea", "SpotPriceEUR"]]

df.rename(columns={
    "HourUTC": "date",
    "SpotPriceEUR": "electricity_price"
}, inplace=True)

df.to_csv("data/electricity_prices.csv", index=False)

print(df.head())