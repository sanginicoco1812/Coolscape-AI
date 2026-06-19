import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

# Load trained model
model = joblib.load("temperature_model.pkl")

# Create city grid
grid_size = 50

temperatures = np.zeros((grid_size, grid_size))

for i in range(grid_size):
    for j in range(grid_size):

        ndvi = np.random.uniform(0, 1)
        humidity = np.random.uniform(30, 90)
        windspeed = np.random.uniform(0, 10)
        buildingdensity = np.random.uniform(10, 100)

        area = pd.DataFrame({
            "NDVI": [ndvi],
            "Humidity": [humidity],
            "WindSpeed": [windspeed],
            "BuildingDensity": [buildingdensity]
        })

        temp = model.predict(area)[0]

        temperatures[i, j] = temp

# Plot heatmap
plt.figure(figsize=(8, 6))

plt.imshow(temperatures)

plt.colorbar(label="Temperature (°C)")

plt.title("Urban Heat Map")

plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")

plt.show()