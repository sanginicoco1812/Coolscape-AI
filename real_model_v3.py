import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.read_csv("datasets/Delhi_Master_Dataset_V3.csv")

X = df[["NDVI", "Humidity", "WindSpeed", "BuildingDensity"]]
y = df["LST"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

joblib.dump(model, "models/real_temperature_model_v3.pkl")

print("Model V3 trained successfully!")
print("MAE:", round(mae, 2))
print("R2 Score:", round(r2, 3))