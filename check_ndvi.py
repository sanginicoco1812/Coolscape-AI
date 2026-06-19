import pandas as pd

df = pd.read_csv("datasets/Delhi_NDVI_Samples_2025.csv")

print(df.head())

print("\nColumns:")
print(df.columns)

print("\nShape:")
print(df.shape)
