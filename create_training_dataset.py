import pandas as pd

# ==========================
# LOAD CLEAN DATA
# ==========================

ndvi = pd.read_csv("datasets/Delhi_NDVI_Clean.csv")
lst = pd.read_csv("datasets/Delhi_LST_Clean.csv")

# ==========================
# MERGE
# ==========================

dataset = pd.merge(
    ndvi,
    lst,
    on=["Latitude", "Longitude"]
)

# ==========================
# SAVE
# ==========================

dataset.to_csv(
    "datasets/Delhi_Training_Dataset.csv",
    index=False
)

# ==========================
# REPORT
# ==========================

print("Training Dataset Shape:")
print(dataset.shape)

print("\nColumns:")
print(dataset.columns)

print("\nFirst 5 Rows:")
print(dataset.head())