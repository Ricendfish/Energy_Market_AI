import pandas as pd
from datetime import datetime
from nordpool import elspot


def get_live_electricity_price():

    prices_spot = elspot.Prices()

    data = prices_spot.hourly(
        areas=["DK1"]
    )

    records = []

    today_prices = data["areas"]["DK1"]["values"]

    for entry in today_prices:

        records.append({
            "timestamp": entry["start"],
            "price_dkk": entry["value"] / 1000
        })

    df = pd.DataFrame(records)

    return df


if __name__ == "__main__":

    df = get_live_electricity_price()

    if df.empty:
        print("No electricity price data retrieved")
    else:
        print("Latest electricity prices:")
        print(df.tail())