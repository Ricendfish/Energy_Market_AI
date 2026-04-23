import pandas as pd
from nordpool import elspot
from datetime import datetime
import os
import sqlite3

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SAVE_PATH = os.path.join(BASE_DIR, "data", "latest_prices.csv")
DB_PATH = os.path.join(BASE_DIR, "database", "energy_market.db")


def get_live_electricity_price():

    try:
        prices_spot = elspot.Prices()

        data = prices_spot.hourly(areas=["DK1"])

        timestamps = []
        prices = []

        for row in data["areas"]["DK1"]["values"]:
            timestamps.append(row["start"])
            prices.append(row["value"])

        df = pd.DataFrame({
            "timestamp": timestamps,
            "price_dkk": prices
        })

        return df

    except Exception as e:
        print("Nordpool API error:", e)
        return None


def save_prices_to_csv(df):

    df.to_csv(SAVE_PATH, index=False)
    print("latest_prices.csv written successfully")


def save_prices_to_db(df):

    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        "latest_prices",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Latest prices saved to database")


def save_prices():

    df = get_live_electricity_price()

    if df is not None and not df.empty:

        # Save CSV (backup / compatibility)
        save_prices_to_csv(df)

        # Save to database
        save_prices_to_db(df)

    else:

        if os.path.exists(SAVE_PATH):
            print("Using existing CSV data")

        else:
            print("No electricity price data available")


if __name__ == "__main__":
    save_prices()
