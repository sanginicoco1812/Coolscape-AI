import pandas as pd
import joblib

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
model = joblib.load(models[CITY])

hotspot = df[df["BuildingDensity"] > 1000].sort_values("LST", ascending=False).iloc[0]

current = pd.DataFrame([{
    "NDVI": hotspot["NDVI"],
    "Humidity": hotspot["Humidity"],
    "WindSpeed": hotspot["WindSpeed"],
    "BuildingDensity": hotspot["BuildingDensity"]
}])

current_temp = model.predict(current)[0]

green = current.copy()
green["NDVI"] *= 1.2

building = current.copy()
building["BuildingDensity"] *= 0.8

green_temp = model.predict(green)[0]
building_temp = model.predict(building)[0]

veg_cooling = current_temp - green_temp
building_cooling = current_temp - building_temp

print(f"\n{CITY} Cooling Recommendation")
print("\nHOTSPOT:")
print(hotspot)

print("\nCurrent Temp:", round(current_temp, 2), "°C")
print("After NDVI +20%:", round(green_temp, 2), "°C")
print("Vegetation Cooling:", round(veg_cooling, 2), "°C")

print("\nAfter Building Density -20%:", round(building_temp, 2), "°C")
print("Building Cooling:", round(building_cooling, 2), "°C")

print("\nRECOMMENDATION:")
if veg_cooling >= building_cooling:
    print("Increase vegetation cover.")
    print("Expected Cooling:", round(veg_cooling, 2), "°C")
else:
    print("Reduce built-up density / cool roof intervention.")
    print("Expected Cooling:", round(building_cooling, 2), "°C")