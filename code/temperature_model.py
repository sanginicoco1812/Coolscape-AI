import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Create Dataset
np.random.seed(42)

data = {
    "NDVI": np.random.uniform(0, 1, 1000),
    "Humidity": np.random.uniform(30, 90, 1000),
    "WindSpeed": np.random.uniform(0, 10, 1000),
    "BuildingDensity": np.random.uniform(10, 100, 1000)
}

df = pd.DataFrame(data)

df["Temperature"] = (
    45
    - 10 * df["NDVI"]
    - 0.1 * df["Humidity"]
    - 0.3 * df["WindSpeed"]
    + 0.15 * df["BuildingDensity"]
    + np.random.normal(0, 1, 1000)
)

# Features and Target
X = df[["NDVI", "Humidity", "WindSpeed", "BuildingDensity"]]
y = df["Temperature"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Accuracy
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

print("Model trained successfully!")
print("Mean Absolute Error:", round(mae, 2))

# Save Model
joblib.dump(model, "temperature_model.pkl")

print("Model saved successfully!")