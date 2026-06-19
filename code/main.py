import pandas as pd

# Creating a sample dataset
data = {
    "NDVI": [0.2, 0.5, 0.7, 0.1, 0.4],
    "Humidity": [45, 60, 70, 40, 55],
    "WindSpeed": [2, 5, 3, 1, 4],
    "BuildingDensity": [80, 50, 30, 90, 60],
    "Temperature": [38, 32, 28, 40, 34]
}

df = pd.DataFrame(data)

print(df)