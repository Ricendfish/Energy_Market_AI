import pandas as pd
from datetime import date
from nordpool import elspot


def get_live_electricity_price():

    prices_spot = elspot.Prices()

    try:

        # request latest available prices
        data = prices_spot.hourly(
            areas=["DK1"],
            end_date=date.today()
        )

        if data is None:
            return pd.DataFrame(columns=["timestamp", "price_dkk"])

        records = []

        values = data["areas"]["DK1"]["values"]

        for entry in values:

            records.append({
                "timestamp": entry["start"],
                "price_dkk": entry["value"] / 1000
            })

        df = pd.DataFrame(records)

        return df

    except Exception as e:

        print("Nordpool API error:", e)

        return pd.DataFrame(columns=["timestamp", "price_dkk"])


if __name__ == "__main__":

    df = get_live_electricity_price()

    if df.empty:
        print("No electricity price data retrieved")
    else:
        print(df.tail())