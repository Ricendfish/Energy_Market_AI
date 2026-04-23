import pandas as pd
import joblib
import wandb

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# -----------------------------------
# Initialize Weights & Biases
# -----------------------------------

wandb.init(
    project="energy-market-ai",
    config={
        "model": "RandomForest",
        "test_size": 0.2,
        "random_state": 42
    }
)

config = wandb.config

# -----------------------------------
# Load dataset
# -----------------------------------

df = pd.read_csv("data/final_dataset.csv")

X = df.drop(columns=["electricity_price", "date"])
y = df["electricity_price"]

# -----------------------------------
# Train test split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=config.test_size,
    random_state=config.random_state
)

# -----------------------------------
# Model
# -----------------------------------

model = RandomForestRegressor(
    n_estimators=200,
    random_state=config.random_state
)

model.fit(X_train, y_train)

# -----------------------------------
# Prediction
# -----------------------------------

preds = model.predict(X_test)

mae = mean_absolute_error(y_test, preds)

print("Model MAE:", mae)

# -----------------------------------
# Log metrics to W&B
# -----------------------------------

wandb.log({
    "MAE": mae
})

# -----------------------------------
# Save model
# -----------------------------------

joblib.dump(model, "models/electricity_price_model.pkl")

# -----------------------------------
# Save artifact
# -----------------------------------

artifact = wandb.Artifact(
    "electricity-price-model",
    type="model"
)

artifact.add_file("models/electricity_price_model.pkl")

wandb.log_artifact(artifact)

wandb.finish()

print("Model saved and logged to Weights & Biases.")
