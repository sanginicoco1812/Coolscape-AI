import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

CITY = "Bengaluru"   # Change to: Delhi, Mumbai, Hyderabad, Bengaluru

datasets = {
    "Delhi": "datasets/Delhi_Master_Dataset_V3.csv",
    "Mumbai": "datasets/Mumbai_Master_Dataset.csv",
    "Hyderabad": "datasets/Hyderabad_Master_Dataset.csv",
    "Bengaluru": "datasets/Bengaluru_Master_Dataset.csv"
}

models = {
    "Delhi": "models/real_temperature_model_v3.pkl",
    "Mumbai": "models/mumbai_temperature_model.pkl",
    "Hyderabad": "models/hyderabad_temperature_model.pkl",
    "Bengaluru": "models/bengaluru_temperature_model.pkl"
}

df = pd.read_csv(datasets[CITY])

features = ["NDVI", "Humidity", "WindSpeed", "BuildingDensity"]
X = df[features]

model = joblib.load(models[CITY])

# sample for speed
X_sample = X.sample(300, random_state=42)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_sample)

print(f"{CITY} SHAP values calculated successfully!")

shap.summary_plot(shap_values, X_sample, show=False)

output_path = f"images/{CITY.lower()}_shap_summary.png"
plt.savefig(output_path, bbox_inches="tight", dpi=300)
plt.close()

print("Saved:", output_path)