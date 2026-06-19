import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Load Dataset
df = pd.read_csv("datasets/Bengaluru_Master_Dataset.csv")

print("Dataset Shape:", df.shape)

# Features
X = df[
    [
        "NDVI",
        "Humidity",
        "WindSpeed",
        "BuildingDensity"
    ]
]

# Target
y = df["LST"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Metrics
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\nBengaluru Model Results")
print("MAE:", round(mae, 2))
print("R²:", round(r2, 3))

# Save Model
joblib.dump(
    model,
    "models/bengaluru_temperature_model.pkl"
)

print("\nSaved:")
print("models/bengaluru_temperature_model.pkl")