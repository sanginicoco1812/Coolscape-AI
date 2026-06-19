import pandas as pd

# Load CSV
df = pd.read_csv("datasets/Mumbai_Heat_Dataset.csv")

print("Original Shape:", df.shape)
print("\nOriginal Columns:")
print(df.columns)

# Keep only useful columns
df = df[
    [
        "Latitude",
        "Longitude",
        "NDVI",
        "LST",
        "Humidity",
        "WindSpeed",
        "BuildingDensity"
    ]
]

# Remove missing values
df = df.dropna()

# Reset index
df = df.reset_index(drop=True)

# Save cleaned file
df.to_csv(
    "datasets/Mumbai_Master_Dataset.csv",
    index=False
)

print("\nCleaned Shape:", df.shape)

print("\nColumns:")
print(df.columns)

print("\nFirst 5 Rows:")
print(df.head())

print("\nSaved:")
print("datasets/Mumbai_Master_Dataset.csv")