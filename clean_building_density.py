import pandas as pd

building = pd.read_csv(
    "datasets/Delhi_BuildingDensity_2025.csv"
)

# Keep only useful columns
building = building[
    ["Latitude", "Longitude", "BuildingDensity"]
]

# Remove duplicates
building = building.drop_duplicates()

# Remove missing values
building = building.dropna()

# Save cleaned file
building.to_csv(
    "datasets/Delhi_BuildingDensity_Clean.csv",
    index=False
)

print("Building Shape:", building.shape)

print("\nColumns:")
print(building.columns)

print("\nFirst 5 Rows:")
print(building.head())