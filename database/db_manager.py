import sqlite3
import pandas as pd
import os

# Base project directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Database path
DB_PATH = os.path.join(BASE_DIR, "database", "energy_market.db")

# CSV fallback paths
FINAL_DATASET_PATH = os.path.join(BASE_DIR, "data", "final_dataset.csv")
LATEST_PRICES_PATH = os.path.join(BASE_DIR, "data", "latest_prices.csv")


def get_connection():
    """
    Create a connection to the SQLite database
    """
    return sqlite3.connect(DB_PATH)


def load_market_data():
    """
    Load historical dataset used by the ML model
    """

    try:
        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM energy_market_data",
            conn
        )

        conn.close()

        if df.empty:
            raise Exception("Empty table")

        return df

    except Exception:

        # fallback to CSV
        if os.path.exists(FINAL_DATASET_PATH):

            df = pd.read_csv(FINAL_DATASET_PATH)

            return df

        else:

            return pd.DataFrame()


def load_latest_prices():
    """
    Load latest electricity prices for dashboard
    """

    try:
        conn = get_connection()

        df = pd.read_sql_query(
            "SELECT * FROM latest_prices",
            conn
        )

        conn.close()

        if df.empty:
            raise Exception("Empty table")

        return df

    except Exception:

        # fallback to CSV
        if os.path.exists(LATEST_PRICES_PATH):

            df = pd.read_csv(LATEST_PRICES_PATH)

            return df

        else:

            return pd.DataFrame()
