import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/Delhi_Training_Dataset.csv")

correlation = df["NDVI"].corr(df["LST"])

print("Correlation:", correlation)

plt.figure(figsize=(8,6))
plt.scatter(df["NDVI"], df["LST"], alpha=0.3)
plt.xlabel("NDVI")
plt.ylabel("LST (°C)")
plt.title("NDVI vs Land Surface Temperature")
plt.show()