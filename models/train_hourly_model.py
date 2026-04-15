import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("data/final_dataset.csv")

df["date"] = pd.to_datetime(df["date"])

# Add hour feature
df["hour"] = df["date"].dt.hour

features = [
    "temperature",
    "wind_speed",
    "electricity_demand",
    "hour",
    "day_of_week",
    "month"
]

X = df[features]
y = df["electricity_price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)

mae = mean_absolute_error(y_test, preds)

print("Hourly model MAE:", mae)

joblib.dump(model, "models/hourly_price_model.pkl")

print("Hourly model saved")