import requests
import pandas as pd
from datetime import datetime


def get_live_electricity_price():

    url = "https://api.energy-charts.info/price?bzn=DK1"

    response = requests.get(url)

    print("Status code:", response.status_code)

    data = response.json()

    timestamps = data["unix_seconds"]
    prices = data["price"]

    rows = []

    for t, p in zip(timestamps, prices):

        rows.append({
            "timestamp": datetime.utcfromtimestamp(t),
            "price_dkk": p / 1000
        })

    df = pd.DataFrame(rows)

    return df


if __name__ == "__main__":

    df = get_live_electricity_price()

    print("\nLatest electricity prices:\n")
    print(df.tail(10))