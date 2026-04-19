import pandas as pd
from datetime import date
from nordpool import elspot


def get_live_electricity_price():

    try:

        prices_spot = elspot.Prices()

        data = prices_spot.hourly(
            areas=["DK1"],
            end_date=date.today()
        )

        if not data or "areas" not in data:
            return pd.DataFrame(columns=["timestamp", "price_dkk"])

        values = data["areas"]["DK1"]["values"]

        records = []

        for entry in values:

            records.append({
                "timestamp": entry["start"],
                "price_dkk": entry["value"] / 1000
            })

        df = pd.DataFrame(records)

        return df

    except Exception as e:

        print("Nordpool API failure:", e)

        return pd.DataFrame(columns=["timestamp", "price_dkk"])