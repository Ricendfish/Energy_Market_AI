import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# load dataset
df = pd.read_csv("data/final_dataset.csv")

# features and target
X = df[
    [
        "temperature",
        "wind_speed",
        "day_of_week",
        "month",
        "day_of_year"
    ]
]
y = df["electricity_demand"]

# train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# model
model = RandomForestRegressor(n_estimators=100)

# train
model.fit(X_train, y_train)

# predictions
preds = model.predict(X_test)

import matplotlib.pyplot as plt

plt.scatter(y_test, preds)
plt.xlabel("Actual Demand")
plt.ylabel("Predicted Demand")
plt.title("Actual vs Predicted Electricity Demand")
plt.show()

# evaluation
mae = mean_absolute_error(y_test, preds)

print("Mean Absolute Error:", mae)

# save model
joblib.dump(model, "models/demand_model/demand_model.pkl")

print("Model saved!")