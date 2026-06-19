import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

df = pd.read_csv("datasets/Mumbai_Master_Dataset.csv")

X = df[
    [
        "NDVI",
        "Humidity",
        "WindSpeed",
        "BuildingDensity"
    ]
]

y = df["LST"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Mumbai Model Results")
print("MAE:", round(mae, 2))
print("R²:", round(r2, 3))

joblib.dump(
    model,
    "models/mumbai_temperature_model.pkl"
)

print("Saved model.")