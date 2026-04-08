import requests
import pandas as pd

url = "https://api.energidataservice.dk/datastore_search_sql"

query = """
SELECT "HourUTC","ConsumptionMWh"
FROM "consumptionpergridarea"
LIMIT 500000
"""

params = {"sql": query}

r = requests.get(url, params=params)

print("Status:", r.status_code)

data = r.json()["result"]["records"]

df = pd.DataFrame(data)

df.rename(columns={
    "HourUTC": "date",
    "ConsumptionMWh": "electricity_demand"
}, inplace=True)

df.to_csv("data/electricity_demand.csv", index=False)

print(df.head())