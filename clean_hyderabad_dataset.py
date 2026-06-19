import pandas as pd

# Load Hyderabad CSV
df = pd.read_csv("datasets/Hyderabad_Heat_Dataset.csv")

print("Original Shape:", df.shape)
print("\nOriginal Columns:")
print(df.columns)

# Remove GEE extra columns if present
for col in ["system:index", ".geo"]:
    if col in df.columns:
        df = df.drop(columns=[col])

# Keep only required columns
required_columns = [
    "Latitude",
    "Longitude",
    "NDVI",
    "LST",
    "Humidity",
    "WindSpeed",
    "BuildingDensity"
]

df = df[required_columns]

# Remove missing values
df = df.dropna()

# Reset index
df = df.reset_index(drop=True)

# Save cleaned dataset
df.to_csv(
    "datasets/Hyderabad_Master_Dataset.csv",
    index=False
)

print("\nCleaned Shape:", df.shape)

print("\nColumns:")
print(df.columns)

print("\nFirst 5 Rows:")
print(df.head())

print("\nSaved:")
print("datasets/Hyderabad_Master_Dataset.csv")