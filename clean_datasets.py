import pandas as pd

# ==========================
# LOAD DATASETS
# ==========================

ndvi = pd.read_csv("datasets/Delhi_NDVI_Samples_2025.csv")
lst = pd.read_csv("datasets/Delhi_LST_Samples_2025.csv")

# ==========================
# KEEP ONLY REQUIRED COLUMNS
# ==========================

ndvi = ndvi[['Latitude', 'Longitude', 'NDVI']]
lst = lst[['Latitude', 'Longitude', 'LST']]

# ==========================
# REMOVE DUPLICATES
# ==========================

ndvi = ndvi.drop_duplicates()
lst = lst.drop_duplicates()

# ==========================
# REMOVE NULL VALUES
# ==========================

ndvi = ndvi.dropna()
lst = lst.dropna()

# ==========================
# SAVE CLEAN FILES
# ==========================

ndvi.to_csv(
    "datasets/Delhi_NDVI_Clean.csv",
    index=False
)

lst.to_csv(
    "datasets/Delhi_LST_Clean.csv",
    index=False
)

# ==========================
# REPORT
# ==========================

print("NDVI Shape:", ndvi.shape)
print("LST Shape:", lst.shape)

print("\nNDVI Columns:")
print(ndvi.columns)

print("\nLST Columns:")
print(lst.columns)

print("\nClean datasets saved successfully!")