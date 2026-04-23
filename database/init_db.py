import sqlite3

DB_PATH = "database/energy_market.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS energy_market_data (
    date TEXT,
    temperature REAL,
    wind_speed REAL,
    electricity_demand REAL,
    electricity_price REAL,
    day_of_week INTEGER,
    month INTEGER,
    day_of_year INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS latest_prices (
    timestamp TEXT,
    price_dkk REAL
)
""")

conn.commit()
conn.close()

print("Database initialized.")
