import sqlite3
import pandas as pd

DB_PATH = "database/energy_market.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS electricity_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        price_dkk REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        predicted_price REAL
    )
    """)

    conn.commit()
    conn.close()

def insert_dataframe(df, table):

    conn = get_connection()
    df.to_sql(table, conn, if_exists="append", index=False)
    conn.close()

def read_table(table):

    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()

    return df