import subprocess
import datetime

print("Starting daily energy pipeline...")

print("Step 1: Fetching live electricity data")
subprocess.run(["python", "data/live_energy_data.py"])

print("Step 2: Updating dataset")
subprocess.run(["python", "pipelines/data_pipeline.py"])

print("Step 3: Retraining model")
subprocess.run(["python", "models/train_price_model.py"])

print("Pipeline completed successfully")

print("Timestamp:", datetime.datetime.now())