import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
import joblib

# Load dataset
df = pd.read_csv("data/final_dataset.csv")

# Features and target
df["target_price"] = df["electricity_price"].shift(-1)

df = df.dropna()

X = df.drop(columns=["electricity_price", "target_price", "date"])
y = df["target_price"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# Model
model = XGBRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=5
)

model.fit(X_train, y_train)

# Predictions
preds = model.predict(X_test)

# Evaluate
mae = mean_absolute_error(y_test, preds)

print("Model MAE:", mae)

# Save model
joblib.dump(model, "models/electricity_price_model.pkl")

print("Model saved.")