import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/final_dataset.csv")

print(df.describe())

# Demand distribution
plt.figure()
sns.histplot(df["electricity_demand"], kde=True)
plt.title("Electricity Demand Distribution")
plt.show()

# Weather vs demand
plt.figure()
sns.scatterplot(x="temperature", y="electricity_demand", data=df)
plt.title("Temperature vs Electricity Demand")
plt.show()

# Wind vs demand
plt.figure()
sns.scatterplot(x="wind_speed", y="electricity_demand", data=df)
plt.title("Wind Speed vs Electricity Demand")
plt.show()

# Price vs demand
plt.figure()
sns.scatterplot(x="electricity_demand", y="electricity_price", data=df)
plt.title("Demand vs Electricity Price")
plt.show()