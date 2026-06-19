import pandas as pd

wind = pd.read_csv("datasets/Delhi_WindSpeed_2025.csv")

wind = wind[["Latitude", "Longitude", "WindSpeed"]]

wind = wind.dropna()
wind = wind.drop_duplicates()

wind = wind[
    (wind["WindSpeed"] >= 0) &
    (wind["WindSpeed"] <= 50)
]

wind.to_csv("datasets/Delhi_WindSpeed_Clean.csv", index=False)

print("Wind Shape:", wind.shape)
print("\nColumns:")
print(wind.columns)
print("\nFirst 5 Rows:")
print(wind.head())
print("\nWind file cleaned successfully!")