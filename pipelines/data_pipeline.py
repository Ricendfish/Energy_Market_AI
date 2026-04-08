import pandas as pd

weather = pd.read_csv("data/weather_history.csv")
demand = pd.read_csv("data/electricity_demand.csv")
prices = pd.read_csv("data/electricity_prices.csv")

# Convert to datetime
weather["date"] = pd.to_datetime(weather["date"])
demand["date"] = pd.to_datetime(demand["date"], utc=True).dt.tz_localize(None)
prices["date"] = pd.to_datetime(prices["date"], utc=True).dt.tz_localize(None)

# Merge datasets
df = weather.merge(demand, on="date", how="inner")
df = df.merge(prices, on="date", how="inner")

df = df.dropna()
# Feature Engineering
df["day_of_week"] = pd.to_datetime(df["date"]).dt.dayofweek
df["month"] = pd.to_datetime(df["date"]).dt.month
df["day_of_year"] = pd.to_datetime(df["date"]).dt.dayofyear


df.to_csv("data/final_dataset.csv", index=False)

print(df.head())
print("Dataset shape:", df.shape)