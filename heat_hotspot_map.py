import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/Delhi_Master_Dataset_V3.csv")

plt.figure(figsize=(8, 7))

plt.scatter(
    df["Longitude"],
    df["Latitude"],
    c=df["LST"],
    s=8,
    cmap="hot"
)

plt.colorbar(label="Land Surface Temperature (°C)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Delhi NCR Urban Heat Hotspot Map")

plt.savefig("images/delhi_heat_hotspot_map.png", dpi=300, bbox_inches="tight")
plt.show()

print("Saved: images/delhi_heat_hotspot_map.png")