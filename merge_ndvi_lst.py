import pandas as pd

# Load datasets
ndvi = pd.read_csv("datasets/Delhi_NDVI_Samples_2025.csv")
lst = pd.read_csv("datasets/Delhi_LST_Samples_2025.csv")

print("NDVI Shape:", ndvi.shape)
print("LST Shape:", lst.shape)

print("\nNDVI Columns:")
print(ndvi.columns)

print("\nLST Columns:")
print(lst.columns)