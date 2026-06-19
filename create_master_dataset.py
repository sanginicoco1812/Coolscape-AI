import pandas as pd

# ==========================
# LOAD DATASETS
# ==========================

ndvi = pd.read_csv("datasets/Delhi_NDVI_Clean.csv")
lst = pd.read_csv("datasets/Delhi_LST_Clean.csv")
humidity = pd.read_csv("datasets/Delhi_Humidity_Clean.csv")
wind = pd.read_csv("datasets/Delhi_WindSpeed_Clean.csv")

# ==========================
# ROUND COORDINATES
# ==========================

for df in [ndvi, lst, humidity, wind]:
    df["Latitude"] = df["Latitude"].round(4)
    df["Longitude"] = df["Longitude"].round(4)

# ==========================
# MERGE DATASETS
# ==========================

master = ndvi.merge(
    lst,
    on=["Latitude", "Longitude"],
    how="inner"
)

master = master.merge(
    humidity,
    on=["Latitude", "Longitude"],
    how="inner"
)

master = master.merge(
    wind,
    on=["Latitude", "Longitude"],
    how="inner"
)

# ==========================
# SAVE
# ==========================

master.to_csv(
    "datasets/Delhi_Master_Dataset.csv",
    index=False
)

print("Master Dataset Shape:")
print(master.shape)

print("\nColumns:")
print(master.columns)

print("\nFirst 5 Rows:")
print(master.head())