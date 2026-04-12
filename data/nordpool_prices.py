<<<<<<< HEAD

=======
import requests
import pandas as pd

def fetch_nordpool_prices():

    url = "https://www.nordpoolgroup.com/api/marketdata/page/10?currency=DKK"

    response = requests.get(url)
    data = response.json()

    prices = []

    for row in data["data"]["Rows"]:
        hour = row["Name"]
        price = row["Columns"][0]["Value"]

        prices.append({
            "hour": hour,
            "price_dkk": price
        })

    df = pd.DataFrame(prices)

    return df


if __name__ == "__main__":
    df = fetch_nordpool_prices()
    print(df.head())
>>>>>>> 02c548b (Added Nordpool electricity price ingestion script)
