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

        if data and "areas" in data and "DK1" in data["areas"]:
            values = data["areas"]["DK1"]["values"]

            records = []

            for entry in values:
                records.append({
                    "timestamp": entry["start"],
                    "price_dkk": entry["value"] / 1000
                })

            return pd.DataFrame(records)

        return pd.DataFrame()

    except Exception as e:
        print("Nordpool API error:", e)
        return pd.DataFrame()


if __name__ == "__main__":

    print("Fetching latest electricity prices...")

    df = get_live_electricity_price()

    # ALWAYS create the file
    if df is None or df.empty:
        print("No electricity price data retrieved.")
        df = pd.DataFrame(columns=["timestamp", "price_dkk"])

    df.to_csv("data/latest_prices.csv", index=False)

    print("latest_prices.csv written successfully")