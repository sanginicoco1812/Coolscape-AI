import pandas as pd

df = pd.read_csv("datasets/Bengaluru_Heat_Dataset.csv")

for col in ["system:index", ".geo"]:
    if col in df.columns:
        df = df.drop(columns=[col])

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
df = df.dropna().reset_index(drop=True)

df.to_csv("datasets/Bengaluru_Master_Dataset.csv", index=False)

print("Cleaned Shape:", df.shape)
print(df.head())