import pandas as pd
import joblib

# Load trained model
model = joblib.load("models/real_temperature_model_v3.pkl")

# Load final dataset
df = pd.read_csv("datasets/Delhi_Master_Dataset_V3.csv")

# Select a hotspot that is hot AND has building density
hotspot = df[df["BuildingDensity"] > 1000].sort_values(
    "LST",
    ascending=False
).iloc[0]

print("\nHOTSPOT FOUND:")
print(hotspot)

# Current condition
current = pd.DataFrame([{
    "NDVI": hotspot["NDVI"],
    "Humidity": hotspot["Humidity"],
    "WindSpeed": hotspot["WindSpeed"],
    "BuildingDensity": hotspot["BuildingDensity"]
}])

current_temp = model.predict(current)[0]

# Scenario 1: Increase vegetation by 20%
green = current.copy()
green["NDVI"] = green["NDVI"] * 1.2

green_temp = model.predict(green)[0]

# Scenario 2: Reduce building density by 20%
buildings = current.copy()
buildings["BuildingDensity"] = buildings["BuildingDensity"] * 0.8

building_temp = model.predict(buildings)[0]

# Results
print("\nCURRENT TEMP:")
print(round(current_temp, 2), "°C")

print("\nIF NDVI INCREASES BY 20%:")
print(round(green_temp, 2), "°C")

print("\nIF BUILDING DENSITY DECREASES BY 20%:")
print(round(building_temp, 2), "°C")

print("\nCOOLING FROM MORE VEGETATION:")
print(round(current_temp - green_temp, 2), "°C")

print("\nCOOLING FROM LOWER BUILDING DENSITY:")
print(round(current_temp - building_temp, 2), "°C")

# Recommendation
veg_cooling = current_temp - green_temp
building_cooling = current_temp - building_temp

print("\nRECOMMENDATION:")

if veg_cooling > building_cooling:
    print("Increase vegetation cover / tree plantation is more effective.")
    print("Expected cooling:", round(veg_cooling, 2), "°C")
else:
    print("Reducing built-up density / adding cool roofs is more effective.")
    print("Expected cooling:", round(building_cooling, 2), "°C")