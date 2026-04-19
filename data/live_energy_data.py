import pandas as pd
from datetime import date

def get_live_electricity_price():
    try:
        from nordpool import elspot

        prices_spot = elspot.Prices()

        data = prices_spot.hourly(
            areas=["DK1"],
            end_date=date.today()
        )

        if data is None:
            print("Nordpool returned no data.")
            return pd.DataFrame()

        if "areas" not in data:
            print("Unexpected Nordpool format.")
            return pd.DataFrame()

        values = data["areas"]["DK1"]["values"]

        if values is None or len(values) == 0:
            print("No electricity price values returned.")
            return pd.DataFrame()

        records = []

        for entry in values:
            try:
                records.append({
                    "timestamp": entry["start"],
                    "price_dkk": entry["value"] / 1000
                })
            except Exception:
                continue

        df = pd.DataFrame(records)

        return df

    except Exception as e:
        print("Nordpool API error:", e)
        return pd.DataFrame()


if __name__ == "__main__":

    print("Fetching latest electricity prices...")

    df = get_live_electricity_price()

    if df is not None and not df.empty:
        df.to_csv("data/latest_prices.csv", index=False)
        print("Saved latest electricity prices.")
    else:
        print("No electricity price data retrieved.")