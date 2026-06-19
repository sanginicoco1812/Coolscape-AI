import pandas as pd
import shap
import joblib

# Load trained model
model = joblib.load("temperature_model.pkl")

# Example area
sample = pd.DataFrame({
    "NDVI": [0.8],
    "Humidity": [70],
    "WindSpeed": [5],
    "BuildingDensity": [30]
})

# SHAP Explainer
explainer = shap.TreeExplainer(model)

shap_values = explainer.shap_values(sample)

features = sample.columns

print("\nFeature Contributions:\n")

for feature, value in zip(features, shap_values[0]):
    print(f"{feature}: {round(value, 2)}")