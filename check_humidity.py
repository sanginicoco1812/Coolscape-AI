import pandas as pd

df = pd.read_csv("datasets/Delhi_Humidity_2025.csv")

print(df.head())
print("\nShape:", df.shape)
print("\nColumns:")
print(df.columns)