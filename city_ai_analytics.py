import pandas as pd
import joblib
import matplotlib.pyplot as plt

CITY = "Bengaluru"   # Change city here

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
model = joblib.load(models[CITY])

features = ["NDVI", "Humidity", "WindSpeed", "BuildingDensity"]

importance = model.feature_importances_

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": importance
}).sort_values("Importance", ascending=False)

print(f"\n{CITY} Feature Importance")
print(importance_df)

plt.figure(figsize=(8, 5))
plt.bar(importance_df["Feature"], importance_df["Importance"])
plt.title(f"{CITY} Feature Importance")
plt.xlabel("Feature")
plt.ylabel("Importance")
plt.savefig(f"images/{CITY.lower()}_feature_importance.png", dpi=300, bbox_inches="tight")
plt.close()

corr = df[features + ["LST"]].corr()

plt.figure(figsize=(8, 6))
plt.imshow(corr, cmap="coolwarm")
plt.colorbar()

plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
plt.yticks(range(len(corr.columns)), corr.columns)

for i in range(len(corr)):
    for j in range(len(corr)):
        plt.text(j, i, f"{corr.iloc[i,j]:.2f}", ha="center", va="center")

plt.title(f"{CITY} Correlation Matrix")
plt.tight_layout()
plt.savefig(f"images/{CITY.lower()}_correlation_matrix.png", dpi=300)
plt.close()

print("\nSaved:")
print(f"images/{CITY.lower()}_feature_importance.png")
print(f"images/{CITY.lower()}_correlation_matrix.png")