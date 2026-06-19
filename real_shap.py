import pandas as pd
import shap
import joblib
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/Delhi_Master_Dataset.csv")

X = df[["NDVI", "Humidity", "WindSpeed"]]

model = joblib.load("models/real_temperature_model.pkl")

explainer = shap.TreeExplainer(model)

# Use sample for faster plotting
X_sample = X.sample(1000, random_state=42)

shap_values = explainer.shap_values(X_sample)

print("SHAP values calculated successfully!")

# Save plot as image
shap.summary_plot(shap_values, X_sample, show=False)

plt.savefig("images/real_shap_summary.png", bbox_inches="tight", dpi=300)

print("SHAP plot saved at: images/real_shap_summary.png")