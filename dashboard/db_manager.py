import sqlite3
import pandas as pd

DB_PATH = "database/energy_market.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def load_market_data():
    """
    Load the main dataset used for ML and dashboard
    """
    conn = get_connection()

    query = """
    SELECT *
    FROM energy_market_data
    ORDER BY date
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def load_latest_prices():
    """
    Load most recent electricity prices
    """
    conn = get_connection()

    query = """
    SELECT *
    FROM latest_prices
    ORDER BY timestamp
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df
