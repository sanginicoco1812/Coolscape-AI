import pandas as pd
import joblib
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/Delhi_Master_Dataset.csv")

X = df[["NDVI", "Humidity", "WindSpeed"]]

model = joblib.load("models/real_temperature_model.pkl")

importance = model.feature_importances_

importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
}).sort_values(by="Importance", ascending=False)

print(importance_df)

plt.figure(figsize=(8, 5))
plt.bar(importance_df["Feature"], importance_df["Importance"])
plt.xlabel("Features")
plt.ylabel("Importance Score")
plt.title("Feature Importance for LST Prediction")
plt.savefig("images/feature_importance_real.png", bbox_inches="tight", dpi=300)
plt.close()

print("Saved: images/feature_importance_real.png")