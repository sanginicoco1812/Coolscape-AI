import pandas as pd                             

ndvi = pd.read_csv("datasets/Delhi_NDVI_Clean.csv")
lst = pd.read_csv("datasets/Delhi_LST_Clean.csv")

print("NDVI Shape:", ndvi.shape)
print("LST Shape:", lst.shape)

print("\nNDVI Head:")
print(ndvi.head())

print("\nLST Head:")
print(lst.head())
