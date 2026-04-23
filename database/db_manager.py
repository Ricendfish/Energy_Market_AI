import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "database", "energy_market.db")


def get_connection():
    """
    Create SQLite connection
    """
    return sqlite3.connect(DB_PATH)


def load_market_data():
    """
    Load historical dataset used by ML model
    """
    conn = get_connection()

    try:

        df = pd.read_sql_query(
            "SELECT * FROM energy_market_data",
            conn
        )

    except Exception:

        # fallback if DB table missing
        csv_path = os.path.join(BASE_DIR, "data", "final_dataset.csv")
        df = pd.read_csv(csv_path)

    conn.close()

    return df


def load_latest_prices():
    """
    Load latest electricity prices
    """
    conn = get_connection()

    try:

        df = pd.read_sql_query(
            "SELECT * FROM latest_prices",
            conn
        )

    except Exception:

        # fallback to CSV
        csv_path = os.path.join(BASE_DIR, "data", "latest_prices.csv")

        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            df = pd.DataFrame()

    conn.close()

    return df
