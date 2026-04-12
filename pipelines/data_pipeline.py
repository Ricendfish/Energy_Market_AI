import pandas as pd

# Load datasets
weather = pd.read_csv("data/weather_history.csv")
demand = pd.read_csv("data/electricity_demand.csv")
prices = pd.read_csv("data/electricity_prices.csv")

# Convert to datetime
weather["date"] = pd.to_datetime(weather["date"])
demand["date"] = pd.to_datetime(demand["date"], utc=True)
prices["date"] = pd.to_datetime(prices["date"], utc=True)

# Convert everything to daily resolution
weather["date"] = weather["date"].dt.date
demand["date"] = demand["date"].dt.date
prices["date"] = prices["date"].dt.date

# Aggregate hourly datasets into daily values
demand = demand.groupby("date").mean(numeric_only=True).reset_index()
prices = prices.groupby("date").mean(numeric_only=True).reset_index()

# Merge datasets
df = weather.merge(demand, on="date", how="inner")
df = df.merge(prices, on="date", how="inner")

# Feature Engineering
df["day_of_week"] = pd.to_datetime(df["date"]).dt.dayofweek
df["month"] = pd.to_datetime(df["date"]).dt.month
df["day_of_year"] = pd.to_datetime(df["date"]).dt.dayofyear

# Save dataset
df.to_csv("data/final_dataset.csv", index=False)

print(df.head())
print("Dataset shape:", df.shape)