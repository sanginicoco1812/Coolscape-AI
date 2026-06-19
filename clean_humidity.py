import pandas as pd

humidity = pd.read_csv("datasets/Delhi_Humidity_2025.csv")

# Keep only useful columns
humidity = humidity[["Latitude", "Longitude", "Humidity"]]

# Remove missing values and duplicates
humidity = humidity.dropna()
humidity = humidity.drop_duplicates()

# Keep realistic humidity values
humidity = humidity[
    (humidity["Humidity"] >= 0) &
    (humidity["Humidity"] <= 100)
]

# Save clean file
humidity.to_csv("datasets/Delhi_Humidity_Clean.csv", index=False)

print("Humidity Shape:", humidity.shape)

print("\nColumns:")
print(humidity.columns)

print("\nFirst 5 Rows:")
print(humidity.head())

print("\nHumidity file cleaned successfully!")
