import pandas as pd
import plotly.express as px

# ==========================
# CHOOSE CITY HERE
# ==========================

CITY = "Hyderabad"

# Options:
# "Delhi"
# "Mumbai"
# "Hyderabad"
# "Bengaluru"

# ==========================
# DATASET PATHS
# ==========================

city_files = {
    "Delhi": "datasets/Delhi_Master_Dataset_V3.csv",
    "Mumbai": "datasets/Mumbai_Master_Dataset.csv",
    "Hyderabad": "datasets/Hyderabad_Master_Dataset.csv",
    "Bengaluru": "datasets/Bengaluru_Master_Dataset.csv"
}

# ==========================
# CHECK CITY
# ==========================

if CITY not in city_files:
    raise ValueError("City name is wrong. Use Delhi, Mumbai, Hyderabad, or Bengaluru.")

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv(city_files[CITY])

# ==========================
# CLEAN BASIC DATA
# ==========================

df = df.dropna()

# ==========================
# HEAT RISK CATEGORY
# ==========================

df["Heat Risk"] = pd.cut(
    df["LST"],
    bins=[0, 30, 35, 40, 45, 100],
    labels=["Low", "Moderate", "High", "Very High", "Extreme"]
)

# ==========================
# CREATE MAP
# ==========================

fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    color="LST",
    color_continuous_scale="Hot",
    zoom=9,
    height=800,
    hover_data={
        "LST": ":.2f",
        "Heat Risk": True,
        "NDVI": ":.3f",
        "Humidity": ":.2f",
        "WindSpeed": ":.2f",
        "BuildingDensity": True
    },
    title=f"{CITY} Urban Heat Hotspot Map"
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 50, "l": 0, "b": 0}
)

# ==========================
# SAVE AND SHOW
# ==========================

output_file = f"images/{CITY.lower()}_heatmap.html"

fig.write_html(output_file)
fig.show()

print("Heatmap created successfully!")
print("Saved:", output_file)