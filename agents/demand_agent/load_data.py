import pandas as pd

url = "https://data.open-power-system-data.org/time_series/latest/time_series_60min_singleindex.csv"

df = pd.read_csv(url)

# select Denmark load
df = df[["utc_timestamp", "DK_load_actual_entsoe_transparency"]]

df.rename(columns={
    "utc_timestamp": "date",
    "DK_load_actual_entsoe_transparency": "electricity_demand"
}, inplace=True)

df.to_csv("data/electricity_demand.csv", index=False)

print(df.head())